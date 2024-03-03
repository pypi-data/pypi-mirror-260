"""Classes related to database endpoints
"""

from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import Field, PrivateAttr

from metabase_tools.models.generic_model import Item, MissingParam
from metabase_tools.utils.logging_utils import log_call

if TYPE_CHECKING:
    from metabase_tools.metabase import MetabaseApi

logger = getLogger(__name__)


class DatabaseItem(Item):
    """Database object class with related methods"""

    _BASE_EP: ClassVar[str] = "/database/{id}"

    _adapter: MetabaseApi | None = PrivateAttr(None)

    description: str | None
    features: list[str]
    cache_field_values_schedule: str
    timezone: str | None
    auto_run_queries: bool
    metadata_sync_schedule: str
    caveats: str | None
    is_full_sync: bool
    updated_at: datetime
    native_permissions: str | None
    details: dict[str, Any]
    is_sample: bool
    is_on_demand: bool
    options: str | None
    engine: str
    refingerprint: str | None
    created_at: datetime
    points_of_interest: str | None
    schedules: dict[str, Any] | None
    cache_ttl: int | None
    creator_id: int | None
    initial_sync_status: str | None
    settings: Any | None
    can_manage: bool | None = Field(alias="can-manage")

    @log_call
    def refresh(self: DatabaseItem) -> DatabaseItem:
        """Returns refreshed copy of the database

        Returns:
            DatabaseItem: self
        """
        return super().refresh()

    @log_call
    def delete(self: DatabaseItem) -> None:
        """Deletes the database"""
        return super().delete()

    def _make_update(self: DatabaseItem, **kwargs: Any) -> DatabaseItem:
        """Makes update request

        Args:
            self (DatabaseItem)

        Returns:
            DatabaseItem: self
        """
        return super()._make_update(**kwargs)

    @log_call
    def update(
        self: DatabaseItem,
        engine: str | MissingParam | None = MissingParam(),
        schedules: dict[str, Any] | MissingParam | None = MissingParam(),
        refingerprint: bool | MissingParam | None = MissingParam(),
        points_of_interest: str | MissingParam | None = MissingParam(),
        description: str | MissingParam | None = MissingParam(),
        name: str | MissingParam | None = MissingParam(),
        caveats: str | MissingParam | None = MissingParam(),
        cache_ttl: int | MissingParam | None = MissingParam(),
        details: dict[str, Any] | MissingParam | None = MissingParam(),
        **kwargs: Any,
    ) -> DatabaseItem:
        """Updates a database using the provided parameters

        Args:
            self (DatabaseItem)
            engine (str, optional)
            schedules (dict[str, Any], optional)
            refingerprint (bool, optional)
            points_of_interest (str, optional)
            description (str, optional)
            name (str, optional)
            caveats (str, optional)
            cache_ttl (int, optional)
            details (dict[str, Any], optional)

        Returns:
            DatabaseItem
        """
        return self._make_update(
            engine=engine,
            schedules=schedules,
            refingerprint=refingerprint,
            points_of_interest=points_of_interest,
            description=description,
            name=name,
            caveats=caveats,
            cache_ttl=cache_ttl,
            details=details,
            **kwargs,
        )
