"""Signed shortest-distance calculations for supported region shapes."""

import math
from typing import Protocol

from .config import Circle, Rectangle


class Region(Protocol):
    """Shape accepted by the distance service."""


def signed_distance(point_x: float, point_y: float, region: Circle | Rectangle) -> float:
    """Return positive distance inside a region and negative distance outside."""
    if isinstance(region, Circle):
        distance_to_center = math.hypot(point_x - region.center_x, point_y - region.center_y)
        return region.radius - distance_to_center

    if isinstance(region, Rectangle):
        nearest_x = min(max(point_x, region.min_x), region.max_x)
        nearest_y = min(max(point_y, region.min_y), region.max_y)
        distance_to_edge = math.hypot(point_x - nearest_x, point_y - nearest_y)
        if distance_to_edge > 0:
            return -distance_to_edge
        return min(
            point_x - region.min_x,
            region.max_x - point_x,
            point_y - region.min_y,
            region.max_y - point_y,
        )

    raise TypeError(f"Unsupported region type: {type(region).__name__}")
