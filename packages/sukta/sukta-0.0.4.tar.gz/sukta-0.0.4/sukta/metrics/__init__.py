import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Tuple

from .aim import AimTrackerHandler
from .cli import CLITrackerHandler
from .tensorboard import TensorboardTrackerHandler
from .tracker import Tracker


@dataclass
class TrackerConfig:
    experiment: str | None = field(init=False, default=None)
    logger: logging.Logger | None = field(init=False, default=None)
    log_dir: Path = field(init=False, default=None)

    handlers: Tuple[Literal["cli", "aim", "tb"]] = "cli"

    def get_tracker(self) -> Tracker:
        self.log_dir.mkdir(exist_ok=True)
        _handler = dict(
            cli=lambda: CLITrackerHandler(self.log_dir, self.logger),
            aim=lambda: AimTrackerHandler(self.log_dir, self.experiment),
            tb=lambda: TensorboardTrackerHandler(self.log_dir),
        )
        return Tracker(handlers=[_handler[h]() for h in self.handlers])

    def replace(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self
