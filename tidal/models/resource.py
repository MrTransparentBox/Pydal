from .base import BaseType
from .metadata import Metadata


class Resource(BaseType):
    id: str


class ExpandedResource[T](Resource):
    resource: T
    status: int
    message: str


class ResourceItem(BaseType):
    resource: Resource


class DataItems(BaseType):
    data: list[ResourceItem]
    metadata: Metadata


class ExpandedDataItems[T](BaseType):
    data: list[ExpandedResource[T]]
    metadata: Metadata
