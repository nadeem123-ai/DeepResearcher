# ============================================================
# utils/logger.py
# Centralized logger — every run saved to logs/run.log
#
# Usage in any file:
#   from utils.logger import get_logger
#   log = get_logger(__name__)
#   log.info("Node started")
#   log.error("Something failed")
# ============================================================

import logging
import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent
LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "run.log"

_FMT = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)-28s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger that writes to both terminal and logs/run.log.
    Pass __name__ so each log line shows which file it came from.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # File handler — every run appended to logs/run.log
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(_FMT)

    # Console handler — INFO and above shown in terminal
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(_FMT)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def log_run_start(topic: str) -> None:
    log = get_logger("run")
    log.info("=" * 60)
    log.info(f"NEW RUN  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"TOPIC    |  {topic}")
    log.info("=" * 60)


def log_run_end(topic: str, pdf_path: str, error: str | None = None) -> None:
    log = get_logger("run")
    if error:
        log.error(f"FAILED   |  {topic}  |  {error}")
    else:
        log.info(f"COMPLETE |  {topic}  |  {pdf_path}")
    log.info("=" * 60)