import logging
from abc import abstractmethod, ABC
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import sukta.tree_util as stu
from sukta.logging import getLogger
from sukta.metrics import TrackerConfig


@dataclass
class WorkspaceConfig:
    experiment: str = "default"

    tracker: TrackerConfig = field(default_factory=TrackerConfig)
    log: logging.Logger = field(init=False)

    seed: int
    run_dir: Optional[Path] = None

    def __post_init__(self):
        if self.run_dir is None:
            self.run_dir = Path("runs") / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir.mkdir(exist_ok=True, parents=True)
        self.log = getLogger(self.experiment, self.run_dir / "logs")
        self.tracker.replace(
            experiment=self.experiment,
            logger=self.log,
            log_dir=self.run_dir / "logs",
        )

    def hparam_dict(self):
        return stu.apply_vfunc(str, asdict(self))


class Workspace(ABC):
    def __init__(self, cfg: WorkspaceConfig):
        self.cfg = cfg
        self.log = cfg.log
        self.get_tracker = cfg.tracker.get_tracker
        self.set_seed(cfg.seed)

    def run(self):
        with self.get_tracker() as self.tracker:
            self.main()
        self.finish()

    @abstractmethod
    def main(self):
        """
        TIPS:
        - self exposes `log` and `tracker` for IO logging and metrics
        - add hparam logging at the beginning of main

            ```python
            tracker.hparams(self.cfg.hparam_dict, key_metrics=['loss'])
            ```
        """
        ...

    @abstractmethod
    def set_seed(self, seed: int): ...

    @abstractmethod
    def save_snapshot(self, tag: str): ...

    @abstractmethod
    def load_snapshot(self, tag: str): ...

    @abstractmethod
    def finish(self): ...
