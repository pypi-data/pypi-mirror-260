import json
from pathlib import Path
from typing import Dict, Tuple

from aim import Run

from sukta.metrics.tracker import TrackerHandler


class AimTrackerHandler(TrackerHandler):
    def __init__(
        self,
        log_dir: Path,
        experiment: str | None = None,
    ):
        metadata_fn = log_dir / "aim.json"
        metadata = {}
        if metadata_fn.exists():
            with open(metadata_fn, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        run_hash = metadata.get("run_hash", None)
        self.run = Run(
            run_hash=run_hash,
            experiment=experiment,
            log_system_params=True,
            capture_terminal_logs=True,
        )
        metadata["run_hash"] = self.run.hash
        with open(metadata_fn, "w", encoding="utf-8") as f:
            json.dump(metadata, f)

    def hparams(self, hparams: Dict, key_metrics: Tuple[str] = ()):
        self.run["hparams"] = hparams

    def scalar(
        self,
        name: str,
        value: float,
        step: int | None = None,
        epoch: int | None = None,
        context: Dict[str, str] | None = None,
    ):
        self.run.track(value, name=name, step=step, epoch=epoch, context=context)

    def update(
        self,
        total_updates: int,
        incr: int = 1,
        step: int | None = None,
        epoch: int | None = None,
        SPU: float | None = None,
    ):
        self.run.report_progress(expect_next_in=SPU * 2)

    def close(self, completed: bool = True):
        self.run.report_successful_finish()
