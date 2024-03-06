from typing import Any, Dict, List

from typing_extensions import NotRequired, TypedDict


class RawEntityTargetRef(TypedDict):
    kind: str
    namespace: str
    name: str


class RawEntityRelation(TypedDict):
    type: str
    targetRef: str
    target: RawEntityTargetRef


class RawEntityLink(TypedDict):
    url: str
    title: NotRequired[str]
    icon: NotRequired[str]
    type: NotRequired[str]


class RawEntityMeta(TypedDict):
    uid: NotRequired[str]
    etag: NotRequired[str]
    name: str
    namespace: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    labels: NotRequired[Dict[str, str]]
    annotations: NotRequired[Dict[str, str]]
    tags: NotRequired[List[str]]
    links: NotRequired[List[RawEntityLink]]


class RawEntity(TypedDict):
    apiVersion: str
    kind: str
    metadata: RawEntityMeta
    spec: NotRequired[Dict[str, Any]]
    relations: NotRequired[List[RawEntityRelation]]
