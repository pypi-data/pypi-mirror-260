from pathlib import Path
from typing import Dict, Tuple

import tensorflow as tf
from tensorboard.plugins.hparams import api as hp

from sukta.metrics.tracker import TrackerHandler


class TensorboardTrackerHandler(TrackerHandler):
    def __init__(
        self,
        log_dir: Path,
    ):
        self.writer = tf.summary.create_file_writer(logdir=str(log_dir / "tb"))

    def hparams(self, hparams: Dict, key_metrics: Tuple[str] = ()):
        with self.writer.as_default():
            hp.hparams_config(
                [hp.HParam(k) for k in hparams.keys()],
                metrics=[hp.Metric(k) for k in key_metrics],
            )
            hp.hparams(hparams)

    def log(
        self,
        metrics: Dict,
        step: int | None = None,
        epoch: int | None = None,
        context: Dict[str, str] | None = None,
    ):
        super().log(metrics, step, epoch, context)
        if step is not None and epoch is not None:
            self.scalar("epoch", epoch, step=step, context=dict(mode="chart"))

    def scalar(
        self,
        name: str,
        value: float,
        step: int | None = None,
        epoch: int | None = None,
        context: Dict[str, str] | None = None,
    ):
        with self.writer.as_default(step=self.step_or_epoch(step, epoch)):
            mode_key = self.get_mode_key(context, name)
            tf.summary.scalar(mode_key, value)

    def update(
        self,
        total_updates: int,
        incr: int = 1,
        step: int | None = None,
        epoch: int | None = None,
        SPU: float | None = None,
    ):
        pass

    def close(self, completed: bool = True):
        self.writer.flush()
        self.writer.close()
