from __future__ import annotations

from typing import Protocol

from backstage_catalog_client.models import (
    AddLocationRequest,
    AddLocationResponse,
    CatalogRequestOptions,
    CompoundEntityRef,
    GetEntitiesByRefsRequest,
    GetEntitiesByRefsResponse,
    GetEntitiesRequest,
    GetEntitiesResponse,
    GetEntityAncestorsRequest,
    GetEntityAncestorsResponse,
    GetEntityFacetsRequest,
    GetEntityFacetsResponse,
    Location,
    QueryEntitiesRequest,
    QueryEntitiesResponse,
    ValidateEntityResponse,
)
from backstage_catalog_client.raw_entity import RawEntity


class AsyncCatalogApi(Protocol):
    async def getEntities(
        self,
        request: GetEntitiesRequest | None = None,
        options: CatalogRequestOptions | None = None,
    ) -> GetEntitiesResponse:
        """
        Get a list of entities from the catalog.
        """
        ...


class TODOCatalogApi(Protocol):
    async def getEntitiesByRefs(
        self,
        request: GetEntitiesByRefsRequest,
        options: CatalogRequestOptions | None,
    ) -> GetEntitiesByRefsResponse: ...

    async def queryEntities(
        self,
        request: QueryEntitiesRequest | None,
        options: CatalogRequestOptions | None,
    ) -> QueryEntitiesResponse: ...

    async def getEntityAncestors(
        self,
        request: GetEntityAncestorsRequest,
        options: CatalogRequestOptions | None,
    ) -> GetEntityAncestorsResponse: ...

    async def getEntityByRef(
        self,
        entityRef: str | CompoundEntityRef,
        options: CatalogRequestOptions | None,
    ) -> RawEntity | None: ...

    async def removeEntityByUid(self, uid: str, options: CatalogRequestOptions | None) -> None: ...

    async def refreshEntity(self, entityRef: str, options: CatalogRequestOptions | None) -> None: ...

    async def getEntityFacets(
        self, request: GetEntityFacetsRequest, options: CatalogRequestOptions | None
    ) -> GetEntityFacetsResponse: ...

    async def getLocationById(self, location_id: str, options: CatalogRequestOptions | None) -> Location | None: ...

    async def getLocationByRef(self, locationRef: str, options: CatalogRequestOptions | None) -> Location | None: ...

    async def addLocation(
        self, location: AddLocationRequest, options: CatalogRequestOptions | None
    ) -> AddLocationResponse: ...

    async def removeLocationById(self, location_id: str, options: CatalogRequestOptions | None) -> None: ...

    async def getLocationByEntity(
        self,
        entityRef: str | CompoundEntityRef,
        options: CatalogRequestOptions | None,
    ) -> Location | None: ...

    async def validateEntity(
        self, entity: RawEntity, locationRef: str, options: CatalogRequestOptions | None
    ) -> ValidateEntityResponse: ...
