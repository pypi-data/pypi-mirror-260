import abc
import time
from typing import Dict, List, Optional, Tuple

import sukta.tree_util as stu


class TrackerHandler(abc.ABC):
    @abc.abstractmethod
    def hparams(self, hparams: Dict, key_metrics: Tuple[str] = ()):
        """Log run hparams
        Args:
            hparams: Dict -- dictionary of hparams
            key_metrics: Tuple -- key metrics that are tracked
        """
        ...

    def log(
        self,
        metrics: Dict,
        step: Optional[int] = None,
        epoch: Optional[int] = None,
        context: Optional[Dict[str, str]] = None,
    ):
        for k, v in stu.iter_path(metrics, delim="/"):
            self.scalar(k, v, step, epoch, context)

    @abc.abstractmethod
    def scalar(
        self,
        name: str,
        value: float,
        step: Optional[int] = None,
        epoch: Optional[int] = None,
        context: Optional[Dict[str, str]] = None,
    ): ...

    @abc.abstractmethod
    def update(
        self,
        total_updates: int,
        incr: int = 1,
        step: Optional[int] = None,
        epoch: Optional[int] = None,
        SPU: Optional[float] = None,
    ):
        """Loop update"""
        ...

    @abc.abstractmethod
    def close(self, completed: bool = True): ...

    @staticmethod
    def get_mode_key(context: Optional[Dict[str, str]], key: Optional[str] = None):
        if context:
            mode = context.get("mode", None)
            if mode:
                if key:
                    return mode + "/" + key
                else:
                    return mode
            else:
                return key
        else:
            return key

    @staticmethod
    def step_or_epoch(step: Optional[int] = None, epoch: Optional[int] = None):
        if step is None:
            return epoch
        else:
            return step


class Tracker(TrackerHandler):
    def __init__(self, handlers: List[TrackerHandler] = []) -> None:
        self.handlers = handlers
        self.num_updates = 0
        self.start_time = time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.end_time = time.time()
        self.scalar(
            "total_time_s", self.end_time - self.start_time, context=dict(mode="chart")
        )
        self.close(exc_type is None)

    def hparams(self, hparams: Dict, key_metrics: Tuple[str] = ()):
        for h in self.handlers:
            h.hparams(hparams, key_metrics)

    def scalar(
        self,
        name,
        value: float,
        step: int | None = None,
        epoch: int | None = None,
        context: Dict[str, str] | None = None,
    ):
        for h in self.handlers:
            h.scalar(name, value, step, epoch, context)

    def log(
        self,
        metrics: Dict,
        step: int | None = None,
        epoch: int | None = None,
        context: Dict[str, str] | None = None,
    ):
        for h in self.handlers:
            h.log(metrics, step, epoch, context)

    def close(self, completed: bool = True):
        for h in self.handlers:
            h.close(completed)

    def update(
        self,
        total_updates: int,
        incr: int = 1,
        step: int | None = None,
        epoch: int | None = None,
        SPU: float | None = None,
    ):
        self.num_updates += 1
        SPU = (time.time() - self.start_time) / self.num_updates
        self.scalar("SPU", SPU, step, epoch, context=dict(mode="chart"))
        for h in self.handlers:
            h.update(total_updates, incr, step, epoch, SPU)
