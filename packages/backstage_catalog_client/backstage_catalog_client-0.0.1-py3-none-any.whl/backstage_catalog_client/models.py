from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping, Sequence, Union

from backstage_catalog_client.raw_entity import RawEntity

EntityFilterItem = Mapping[str, Union[str, Sequence[str]]]
EntityFilterQuery = Sequence[EntityFilterItem]


@dataclass
class SerializedError:
    pass


@dataclass
class EntityOrderQuery:
    field: str
    order: Literal["asc", "desc"]


@dataclass
class GetEntitiesRequest:
    entity_filter: EntityFilterQuery | None = None
    fields: list[str] | None = None
    order: EntityOrderQuery | Sequence[EntityOrderQuery] | None = None
    offset: int | None = None
    limit: int | None = None
    after: str | None = None


@dataclass
class GetEntitiesResponse:
    items: list[RawEntity]


@dataclass
class GetEntitiesByRefsRequest:
    pass


@dataclass
class GetEntitiesByRefsResponse:
    pass


@dataclass
class GetEntityAncestorsRequest:
    pass


@dataclass
class GetEntityAncestorsResponse:
    pass


@dataclass
class CompoundEntityRef:
    pass


@dataclass
class GetEntityFacetsRequest:
    pass


@dataclass
class GetEntityFacetsResponse:
    pass


@dataclass
class CatalogRequestOptions:
    token: str | None = None


@dataclass
class Location:
    location_id: str
    location_type: str
    target: str


@dataclass
class AddLocationRequest:
    location_type: str | None
    target: str
    dryRun: bool | None


@dataclass
class AddLocationResponse:
    location: Location
    entities: list[RawEntity]
    exists: bool | None


@dataclass
class ValidateEntityResponse:
    valid: bool
    errors: list[SerializedError]


@dataclass
class QueryEntitiesInitialRequest:
    fields: list[str] | None
    limit: int | None
    entity_filter: EntityFilterQuery | None
    orderFields: EntityOrderQuery | None
    fullTextFilter: dict[str, str | list[str]] | None


@dataclass
class QueryEntitiesCursorRequest:
    fields: list[str] | None
    limit: int | None
    cursor: str


@dataclass
class QueryEntitiesRequest:
    query_entity: QueryEntitiesInitialRequest | QueryEntitiesCursorRequest | None


@dataclass
class QueryEntitiesResponse:
    items: list[RawEntity]
    totalItems: int
    pageInfo: dict[str, str] | None
