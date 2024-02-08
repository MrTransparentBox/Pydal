"""Provides models for unfiltered API responses"""

from .base import BaseType
from .metadata import Metadata


class Properties(BaseType):
    """Resource properties"""

    content: list[str]


class Resource(BaseType):
    """ID tagged resource dict"""

    id: str


class ExpandedResource[T](Resource):
    """Generic resource model"""

    resource: T


class ExpandedResourceStatus[T](ExpandedResource):
    """Generic resource model with status"""

    status: int
    message: str


class ResourceItem(BaseType):
    """Dict with single resource"""

    resource: Resource


class DataItems(BaseType):
    """Multiple resource ids with metadata"""

    data: list[ResourceItem]
    metadata: Metadata


class ExpandedDataItems[T](BaseType):
    """Multiple generic data items with metadata"""

    data: list[ExpandedResourceStatus[T]]
    metadata: Metadata
