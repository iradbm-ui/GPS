"""A deterministic simulated GPS sensor with noisy boundary measurements."""

from dataclasses import dataclass
import math
import random

from .config import Circle, Rectangle
from .geometry import signed_distance


@dataclass(frozen=True)
class Position:
    x: float
    y: float


class SimulatedGpsSensor:
    """Move along a smooth variable-speed path and expose distance-only readings."""

    def __init__(
        self,
        region_a: Circle,
        region_b: Rectangle,
        noise_stddev: float,
        random_seed: int,
    ) -> None:
        self._region_a = region_a
        self._region_b = region_b
        self._noise_stddev = noise_stddev
        self._random = random.Random(random_seed)
        self._position = Position(0.0, 0.0)

    @property
    def position(self) -> Position:
        return self._position

    def advance(self, elapsed_seconds: float) -> Position:
        """Advance to a curving path with sinusoidally varying speed."""
        # The phase terms make both speed and heading change continuously.
        phase = elapsed_seconds * 0.17
        speed_scale = 1.0 + 0.28 * math.sin(elapsed_seconds * 0.63)
        self._position = Position(
            x=-34.0 + elapsed_seconds * 1.55 * speed_scale,
            y=3.0 * math.sin(phase) + 1.4 * math.sin(elapsed_seconds * 0.41),
        )
        return self._position

    def get_dist_a(self) -> float:
        """Return noisy signed shortest distance to region A."""
        return self._measure(self._region_a)

    def get_dist_b(self) -> float:
        """Return noisy signed shortest distance to region B."""
        return self._measure(self._region_b)

    def _measure(self, region: Circle | Rectangle) -> float:
        true_distance = signed_distance(self._position.x, self._position.y, region)
        return true_distance + self._random.gauss(0.0, self._noise_stddev)
