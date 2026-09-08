"""Online region-presence classification from boundary distances."""

from enum import StrEnum


class Presence(StrEnum):
    IN_A = "In A"
    IN_B = "In B"
    OUTSIDE = "Outside"


class PresenceClassifier:
    """Classify one pair of signed boundary distances without retaining history."""

    def __init__(self, boundary_margin: float = 0.0) -> None:
        if boundary_margin < 0:
            raise ValueError("Boundary margin cannot be negative")
        self.boundary_margin = boundary_margin

    def classify(self, distance_a: float, distance_b: float) -> Presence:
        """Return the live state for the two distance measurements."""
        in_a = distance_a > self.boundary_margin
        in_b = distance_b > self.boundary_margin
        if in_a and in_b:
            raise ValueError("Positive distances for both regions violate the disjoint-region assumption")
        if in_a:
            return Presence.IN_A
        if in_b:
            return Presence.IN_B
        return Presence.OUTSIDE
