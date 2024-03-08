"""
aim init
python -m examples.tracker
aim up --port 8000
"""

import shutil
import time
from pathlib import Path

from sukta.logging import getLogger
from sukta.metrics import TrackerConfig

log = getLogger("test")

tracker_cfg = TrackerConfig(handlers=["cli", "aim"])

log_dir = Path("logs")
shutil.rmtree(log_dir, ignore_errors=True)

tracker_cfg.replace(
    logger=log,
    log_dir=log_dir,
)

N_UPDATES = 10
with tracker_cfg.get_tracker() as tracker:
    tracker.hparams(
        {
            "a": 1,
            "b": 2,
        },
        key_metrics=["chart/SPU"],
    )

    for i in range(N_UPDATES):
        time.sleep(0.5)
        log.info(i)
        tracker.update(N_UPDATES, step=i)
