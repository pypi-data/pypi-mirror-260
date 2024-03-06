from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping, Sequence, Union

from backstage_catalog_client.raw_entity import RawEntity

EntityFilterItem = Mapping[str, Union[str, Sequence[str]]]

EntityFilterQuery = Sequence[EntityFilterItem]
"""
A key-value based filter expression for entities.

Each key of a record is a dot-separated path into the entity structure, e.g.
`metadata.name`.
The values are literal values to match against. As a value you can also pass
in the symbol `CATALOG_FILTER_EXISTS` (exported from this package), which
means that you assert on the existence of that key, no matter what its value
is.
All matching of keys and values is case insensitive.
If multiple filter sets are given as an array, then there is effectively an
OR between each filter set.
Within one filter set, there is effectively an AND between the various keys.
Within one key, if there are more than one value, then there is effectively
an OR between them.
Example: For an input of
```
[
  { kind: ['API', 'Component'] },
  { 'metadata.name': 'a', 'metadata.namespace': 'b' }
]
```

This effectively means
```
(kind = EITHER 'API' OR 'Component')
OR
(metadata.name = 'a' AND metadata.namespace = 'b' )
```
"""


@dataclass
class SerializedError:
    pass


@dataclass
class EntityOrderQuery:
    field: str
    order: Literal["asc", "desc"]


@dataclass
class GetEntitiesRequest:
    """A request items for fetching backstage entities"""

    entity_filter: EntityFilterQuery | None = None
    """If given, only entities matching this filter will be returned."""
    fields: list[str] | None = None
    """If given, return only the parts of each entity that match the field declarations."""
    order: EntityOrderQuery | Sequence[EntityOrderQuery] | None = None
    """If given, order the result set by those directives."""
    offset: int | None = None
    """If given, skips over the first N items in the result set."""
    limit: int | None = None
    """If given, returns at most N items from the result set."""
    after: str | None = None
    """If given, skips over all items before that cursor as returned by a previous request."""


@dataclass
class GetEntitiesResponse:
    """the repsonse type for getEntities"""

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
    """Options you can pass into a catalog request for additional information."""

    token: str | None = None
    """an Authentication token for authenticated requests"""


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
