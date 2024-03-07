"""
Utilities for setting up Python's weirdo logging system. Including logging to
MongoDB if you feel crazy.
"""

from __future__ import annotations

import asyncio
import logging
import logging.handlers
import socket
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import *  # type: ignore

import uniserde
from bson import ObjectId

try:
    import motor  # type: ignore
    import motor.motor_asyncio  # type: ignore
except ImportError:
    if TYPE_CHECKING:
        import motor  # type: ignore
        import motor.motor_asyncio  # type: ignore


__all__ = [
    "LogLevel",
    "MongoDbLogger",
    "setup_logging",
]


LogLevel: TypeAlias = Literal["debug", "info", "warning", "error", "fatal"]
LOG_LEVEL_NAMES = get_args(LogLevel)


def _log_level_to_python(level: LogLevel) -> int:
    return getattr(logging, level.upper())


def _log_level_from_python(level: int) -> LogLevel:
    return logging.getLevelName(level).lower()


@dataclass
class LogEntry(uniserde.Serde):
    id: ObjectId
    timestamp: datetime
    host: str
    level: LogLevel
    message: str
    tag: str | None
    payload: dict[str, Any]


class MongoDbLogger(logging.StreamHandler):
    """
    Logger, which stores its entries in a MongoDB database.

    Database access is asynchronous, and likely on another server. `await`ing
    every log operation would be incredibly slow. Instead, this logger only
    synchronously queues log entries, and then later asynchronously copies them
    to the database.
    """

    def __init__(
        self,
        db_collection: motor.motor_asyncio.AsyncIOMotorCollection,
    ):
        super().__init__()

        self.db_collection = db_collection

        self._log_worker_running = False
        self._last_log_writeback_time = time.time()
        self._pending_log_entries = []

        # Cached for performance. Not sure if fetching the hostname would cause
        # a context switch otherwise.
        self._hostname = socket.gethostname()

    async def create_log_entries(self, entries: Iterable[LogEntry]) -> None:
        """
        Batch creates new log entries in the database.

        The entries need to have unique ids among all entries in the database.
        This is not checked for performance reasons.
        """
        entry_data = [entry.as_bson() for entry in entries]
        await self.db_collection.insert_many(entry_data)

    async def flush_async(self) -> None:
        """
        Copies any not yet stored log entries into the database.
        """

        # Move the log entries into a local variable, to ensure any second call
        # to this function doesn't create duplicate entries
        in_flight_entries = self._pending_log_entries
        self._pending_log_entries = []

        # Push the entries into the database
        await self.create_log_entries(in_flight_entries)

    async def _database_log_worker(self) -> None:
        CYCLE_TIME = 5.0

        # Needs to be set by the caller to avoid races
        assert self._log_worker_running

        # Keep copying entries
        try:
            while self._pending_log_entries:
                # Wait at least CYCLE_TIME seconds before writing back
                now = time.time()
                sleep_time = CYCLE_TIME - (now - self._last_log_writeback_time)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

                self._last_log_writeback_time = time.time()

                # Copy the pending log entries into the database
                await self.flush_async()

        # More bookkeeping
        finally:
            self._log_worker_running = False

    def queue_log(
        self,
        level: LogLevel,
        message: str,
        tag: str | None = None,
        *,
        payload: dict[str, Any] | None = None,
        timestamp: datetime | None = None,
    ) -> None:
        """
        Creates a log entry and queues it for storage to the database.
        """

        if payload is None:
            payload = {}

        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        assert timestamp.tzinfo is not None, timestamp

        # Queue the log entry
        self._pending_log_entries.append(
            LogEntry(
                id=ObjectId(),
                timestamp=timestamp,
                host=self._hostname,
                level=level,
                message=message,
                tag=tag,
                payload=payload,
            )
        )

        # Make sure a worker is running to copy these entries back into the
        # database
        if not self._log_worker_running:
            self._log_worker_running = True
            asyncio.create_task(self._database_log_worker())

    def emit(self, record: logging.LogRecord) -> None:
        """
        For compatibility with python's logging module.
        """

        self.queue_log(
            level=_log_level_from_python(record.levelno),
            message=record.message,
        )


@overload
def setup_logging(
    *,
    info_log_path: Path,
    debug_log_path: Path,
    database_collection: None,
    database_log_level: LogLevel = "debug",
) -> MongoDbLogger:
    ...


@overload
def setup_logging(
    *,
    info_log_path: Path,
    debug_log_path: Path,
    database_collection: None,
    database_log_level: LogLevel = "debug",
) -> None:
    ...


def setup_logging(
    *,
    info_log_path: Path,
    debug_log_path: Path,
    database_collection: motor.motor_asyncio.AsyncIOMotorCollection | None,
    database_log_level: LogLevel = "debug",
) -> MongoDbLogger | None:
    """
    Creates a nice logging setup.

    - INFO logs to `info_log_path`, keeping logs indefinitely
    - DEBUG logs to `stdout`
    - DEBUG logs to `debug_log_path`, keeping a limited number of days
    - DEBUG logs into the database

    Persistence loggers can lose some log entries if they are not flushed before
    closing the application. If every single entry is important to you, make
    sure to flush the returned persistence logger before ending the script.

    :param info_log_path: Path to the info log file
    :param debug_log_path: Path to the debug log file
    :param db: The persistence to store logs in
    :return: The created PersistenceLogger
    """

    root_logger = logging.getLogger("")
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s")

    # Make sure the log directories exist
    info_log_path.parent.mkdir(parents=True, exist_ok=True)
    debug_log_path.parent.mkdir(parents=True, exist_ok=True)

    # Info -> file
    handler = logging.handlers.TimedRotatingFileHandler(
        info_log_path,
        encoding="utf-8",
        when="midnight",
        utc=True,
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Debug -> stdout
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Debug -> file
    handler = logging.handlers.TimedRotatingFileHandler(
        debug_log_path,
        encoding="utf-8",
        when="midnight",
        utc=True,
        backupCount=7,
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Debug -> database
    if database_collection is None:
        pers_logger = None
    else:
        pers_logger = MongoDbLogger(database_collection)

        pers_logger.setLevel(_log_level_to_python(database_log_level))
        root_logger.addHandler(pers_logger)

    return pers_logger
