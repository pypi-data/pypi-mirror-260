import logging
import typing as tp
from pathlib import Path

from rich.logging import RichHandler


def getLogger(
    log_name: str,
    log_path: tp.Optional[tp.Union[str, Path]] = None,
    level: str = "DEBUG",
) -> logging.Logger:
    logger = logging.getLogger(log_name)

    # term logger
    term_handler = RichHandler(rich_tracebacks=True)
    term_handler.setLevel(level)
    term_handler.setFormatter(logging.Formatter(fmt="%(message)s", datefmt="[%c]"))
    logger.addHandler(term_handler)

    # file logger
    if log_path is not None:
        if isinstance(log_path, str):
            log_path = Path(log_path)
        if log_path.is_dir():
            log_path = log_path / f"{log_name}.log"
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)s:%(name)s: %(message)s", datefmt="[%c]"
            ),
        )
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    logger.setLevel(level)
    return logger


def n2str(x: int | float, fmt=".3f"):
    suffix = ""
    if x < 0:
        prefix = "-"
        x = -x
    else:
        prefix = ""
    # convert with suffix
    if x > 1e9:
        x /= 1e9
        suffix = "G"
    elif x > 1e6:
        x /= 1e6
        suffix = "M"
    elif x > 1e3:
        x /= 1e3
        suffix = "k"
    elif x < 1e-9:
        x *= 1e9
        suffix = "n"
    elif x < 1e-6:
        x *= 1e6
        suffix = "u"
    elif x < 1e-3:
        x *= 1e3
        suffix = "m"
    return f"{prefix}{x:{fmt}}{suffix}"
