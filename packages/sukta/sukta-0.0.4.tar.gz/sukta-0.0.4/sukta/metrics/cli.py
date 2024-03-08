import logging
from collections import deque
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.text import Text

import sukta.tree_util as stu
from sukta.logging import n2str
from sukta.metrics.tracker import TrackerHandler


class CLIMeter:
    def __init__(self, window_size: int = 10):
        self.metric = deque([], maxlen=window_size)

    def update(self, value: int | float):
        self.metric.append(value)

    def compute(self):
        x = np.asarray(self.metric).astype(np.float32)
        if x.size:
            v, m, std = x[-1], x.mean(), x.std()
        else:
            v, m, std = np.nan, np.nan, np.nan
        return n2str(v), "{0} ± {1}".format(n2str(m), n2str(std))


class CLITrackerHandler(TrackerHandler):
    def __init__(
        self,
        log_dir: Path,
        logger: logging.Logger | None = None,
        window_size: int = 10,
    ):
        self.log_dir = log_dir
        self.logger = logger
        self.window_size = window_size
        self.console = None
        if self.logger is not None:
            for handler in self.logger.handlers:
                if isinstance(handler, RichHandler):
                    self.console = handler.console
        self.console = self.console or Console()

        self.live = Live(
            self._generate_status_table(), console=self.console
        ).__enter__()

    def hparams(self, hparams: Dict, key_metrics: Tuple[str] = ()):
        table = Table(title="HParams")
        table.add_column("key", justify="left", style="cyan")
        table.add_column("value", justify="right", style="green")
        for k, v in stu.iter_path(hparams, delim="/"):
            table.add_row(k, str(v))
        if self.logger is None:
            self.console.print(table)
        else:
            console = Console()
            with console.capture() as capture:
                console.print(table)
            table = Text.from_ansi(capture.get())
            self.logger.info(table, extra={"markup": True})

        self.key_metrics = {
            k: CLIMeter(window_size=self.window_size) for k in key_metrics
        }

    def scalar(
        self,
        name: str,
        value: float,
        step: int | None = None,
        epoch: int | None = None,
        context: Dict[str, str] | None = None,
    ):
        mode = self.get_mode_key(context)
        if hasattr(self, "key_metrics") or mode == "chart":
            mode_key = self.get_mode_key(context, key=name)
            if mode_key in self.key_metrics:
                self.key_metrics[mode_key].update(value)
            if self.logger:
                self.logger.info(
                    "{0}: {1} [step={2}, epoch={3}] {4}".format(
                        name, n2str(value, ".4f"), step, epoch, context
                    )
                )
            else:
                self.console.log(
                    "{0}: {1} [step={2}, epoch={3}] {4}".format(
                        name, n2str(value, ".4f"), step, epoch, context
                    )
                )

    def update(
        self,
        total_updates: int,
        incr: int = 1,
        step: int | None = None,
        epoch: int | None = None,
        SPU: float | None = None,
    ):
        if not hasattr(self, "job_progress"):
            self.job_progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                MofNCompleteColumn(),
                TextColumn("[bold]| [cyan]ETA ="),
                TimeRemainingColumn(),
                TextColumn("[bold]| [yellow]Elapsed ="),
                TimeElapsedColumn(),
            )
            self.job_task = self.job_progress.add_task(
                "[green]Updates", total=total_updates
            )
        self.job_progress.advance(self.job_task, incr)
        self.live.update(self._generate_status_table())

    def close(self, completed=True):
        self.live.__exit__(None, None, None)

    def generate_metric_table(self):
        self.metric_table = Table(title="Metric Summary")
        self.metric_table.add_column("metric", justify="left")
        self.metric_table.add_column("value", justify="right")
        self.metric_table.add_column("stats", justify="left")
        for k, m in self.key_metrics.items():
            self.metric_table.add_row(k, *m.compute())
        return self.metric_table

    def _generate_status_table(self):
        progress_table = Table.grid()
        if hasattr(self, "key_metrics") and len(self.key_metrics):
            progress_table.add_row(self.generate_metric_table())
        if hasattr(self, "job_progress"):
            progress_table.add_row(
                Panel.fit(
                    self.job_progress,
                    title="[b]Progress",
                    border_style="green",
                )
            )
        return progress_table
