"""
Settings are split over two locations:

A local file called `local-settings.json` contains information which is
needed right at startup, such as database connection strings.

The remainder of the settings are stored in the database, allowing for
dynamic configuration.
"""

from __future__ import annotations

import asyncio
import enum
import threading
import time
import weakref
from datetime import datetime, timedelta
from pathlib import Path
from typing import *  # type: ignore

import json5
import uniserde
from uniserde import ObjectId, Serde

try:
    import motor.motor_asyncio  # type: ignore
except ImportError:
    if TYPE_CHECKING:
        import motor.motor_asyncio  # type: ignore
    else:
        motor = None

__all__ = [
    "load_local_settings",
    "SettingsError",
    "SettingsManager",
]


LS = TypeVar("LS")
DS = TypeVar("DS")
S = TypeVar("S")


_DEFAULTS_BY_TYPE: dict[Type, Any] = {
    Any: None,
    bool: False,
    bytes: b"",
    datetime: datetime.now(),
    dict: {},
    enum.Enum: "",
    enum.Flag: [],
    float: 0.0,
    int: 0,
    list: [],
    Literal: "",
    set: set(),
    str: "",
    timedelta: timedelta(),
    tuple: tuple(),
    Union: None,
    ObjectId: "",
}  # type: ignore


class SettingsError(Exception):
    """
    Raised when settings couldn't be loaded, for whichever reason.
    """

    pass


def _create_template(_local_settings_class: Type) -> str:
    # Create a new instance of the local settings class
    as_instance = object.__new__(_local_settings_class)  # type: ignore

    # Fill it up with empty values
    for fname, ftype in get_type_hints(_local_settings_class).items():
        origin = get_origin(ftype)

        if origin is None:
            origin = ftype

        as_instance.__dict__[fname] = _DEFAULTS_BY_TYPE.get(origin, None)

    # Serialize the instance into formatted JSON
    serialized: str = json5.dumps(
        uniserde.as_json(as_instance),
        indent=4,
        quote_keys=True,
        trailing_commas=True,
    )

    # Add comments describing the fields
    serialized = serialized.strip()
    lines = serialized.splitlines()

    for ii, line in enumerate(lines[1:-1]):
        lines[ii] = "  // " + line.strip()

    # Done
    return "\n".join(lines) + "\n"


def load_local_settings(
    local_settings_path: Path,
    local_settings_class: Type[LS],
) -> LS:
    """
    Loads the local settings from disk. If the file does not exist, it is
    created with template values and an exception is raised.
    """

    # If the file doesn't exist create a template and raise
    if not local_settings_path.exists():
        local_settings_path.parent.mkdir(parents=True, exist_ok=True)
        local_settings_path.write_text(_create_template(local_settings_class))

        raise SettingsError(
            f"""
The local settings file does not exist. A template will be created for you.
Please fill in the missing values and restart the program.

You can find the file at {local_settings_path}.
""".strip()
        )

    # The file exists, so load it
    try:
        with open(local_settings_path, "r") as f:
            raw_local_settings = json5.load(f)
    except Exception as err:
        raise SettingsError(
            "The local settings file exists, but could not be read!"
        ) from err

    # Parse them into a python class
    try:
        local_settings = uniserde.from_json(raw_local_settings, local_settings_class)
    except uniserde.SerdeError as err:
        raise SettingsError(
            f"""
The local settings file is invalid. Please check the file at
{local_settings_path} and try again.

The error was: {err}
""".strip()
        )

    return local_settings


async def load_dynamic_settings(
    db: motor.motor_asyncio.AsyncIOMotorCollection,
    dynamic_settings_class: Type[DS],
) -> DS:
    """
    Loads the dynamic settings from the database, parses and returns them.
    """

    # The collection should have exactly one document
    matches = []
    async for bson_doc in db.find():
        matches.append(bson_doc)

    if len(matches) != 1:
        raise SettingsError(
            f"Expected exactly one document in the settings collection, but found {len(matches)}!"
        )

    # Deserialize the document
    try:
        dynamic_settings = uniserde.from_bson(matches[0], dynamic_settings_class)
    except uniserde.SerdeError as err:
        raise SettingsError(
            f"The database settings couldn't be deserialized: {err}"
        ) from err

    # TODO: Would be nice not to crash just because the database contains
    # *additional* fields, as those may be added at runtime.

    return dynamic_settings


def _fetch_once(
    weak_manager: weakref.ReferenceType["SettingsManager[LS, DS, S]"],
) -> bool:
    # Get the manager
    manager = weak_manager()

    # If the manager has been garbage collected, stop
    if manager is None:
        return False

    # Otherwise, fetch the settings
    asyncio.run(manager._rebuild_settings())

    # Keep going
    return True


def _fetcher_worker(
    weak_manager: weakref.ReferenceType["SettingsManager[LS, DS, S]"],
    interval: timedelta,
) -> None:
    should_continue = True

    while should_continue:
        # Wait for the interval
        time.sleep(interval.total_seconds())

        # Fetch once
        should_continue = _fetch_once(weak_manager)


class SettingsManager(Generic[LS, DS, S]):
    """
    Manages the settings for a deployment, with the ability to periodically
    reload them from the database. Handles local as well as dynamic settings.

    `LS` is the type of the local settings class. It is loaded from a local
    JSON.

    `DS` is the type of the dynamic settings class. It is loaded from the
    database.

    `S` is the type of the combined settings class. It must be a subclass of
    both `LS` and `DS` and contain no further fields.
    """

    def __init__(
        self,
        local_settings: LS,
        db_collection: motor.motor_asyncio.AsyncIOMotorCollection,
        dynamic_settings_class: Type[DS],
        combined_settings_class: Type[S],
    ):
        assert issubclass(combined_settings_class, type(local_settings))
        assert issubclass(combined_settings_class, dynamic_settings_class)

        self._local_settings = local_settings
        self._db_collection = db_collection
        self._dynamic_settings_class = dynamic_settings_class
        self._combined_settings_class = combined_settings_class

        # Stored to ensure only one fetcher thread is running at a time
        self._fetcher_thread: Optional[threading.Thread] = None

        # Used to ensure the settings aren't loaded twice simultaneously
        self._fetcher_lock = asyncio.Lock()

        # The rest is loaded later
        self._dynamic_settings: Optional[DS] = None
        self._combined_settings: Optional[S] = None

    async def _rebuild_settings(self) -> None:
        """
        Re-fetches the dynamic settings from the database and rebuilds the
        combined settings object.
        """

        # Fetch the dynamic settings from the database
        dynamic_settings = await load_dynamic_settings(
            self._db_collection, self._dynamic_settings_class
        )

        # Combine the settings
        new_settings = self._combined_settings_class(
            **self._local_settings.__dict__,
            **dynamic_settings.__dict__,
        )

        # Atomically replace the settings - this method may run in a thread
        self._combined_settings = new_settings  # type: ignore

    async def get_settings(self) -> S:
        """
        If the settings have already been loaded, returns the cached version.
        Otherwise fetches them from the database, caches and returns them.
        """

        # If the settings are already loaded, return them
        if self._combined_settings is not None:
            return self._combined_settings

        # Otherwise fetch the dynamic settings from the database
        async with self._fetcher_lock:
            # The settings may have been loaded during the wait period. If not,
            # fetch them
            if self._combined_settings is None:
                await self._rebuild_settings()
                assert self._combined_settings is not None

        return self._combined_settings

    def start_fetcher_thread(self, period: timedelta) -> None:
        """
        Starts a thread which periodically fetches the dynamic settings from the
        database. The thread is a daemon, meaning you don't need to explicitly
        stop it. (This is why this method is using a full blown thread rather
        than a task.)

        The thread holds a weak reference to this object and will automatically
        stop if this object is garbage collected.

        Only one fetcher thread may be running at a time.
        """

        # Already running?
        if self._fetcher_thread is not None:
            raise SettingsError("A fetcher thread is already running!")

        # Start a new thread
        self._fetcher_thread = threading.Thread(
            target=_fetcher_worker,
            args=(weakref.ref(self), period),
            daemon=True,
        )

        self._fetcher_thread.start()

    @property
    def has_fetcher(self) -> bool:
        """
        Returns `True` if the fetcher thread is running, `False` otherwise.
        """
        return self._fetcher_thread is not None
