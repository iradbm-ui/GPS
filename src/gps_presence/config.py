"""Configuration for the simulation and its configurable regions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Circle:
    """A circular region described in simulation coordinate units."""

    center_x: float
    center_y: float
    radius: float

    def __post_init__(self) -> None:
        if self.radius <= 0:
            raise ValueError("Circle radius must be positive")


@dataclass(frozen=True)
class Rectangle:
    """An axis-aligned rectangular region."""

    min_x: float
    min_y: float
    max_x: float
    max_y: float

    def __post_init__(self) -> None:
        if self.min_x >= self.max_x or self.min_y >= self.max_y:
            raise ValueError("Rectangle bounds must have positive width and height")


@dataclass(frozen=True)
class SimulationConfig:
    """All user-tunable values for one simulation run."""

    region_a: Circle = Circle(center_x=-18.0, center_y=0.0, radius=8.0)
    region_b: Rectangle = Rectangle(min_x=10.0, min_y=-7.0, max_x=25.0, max_y=7.0)
    duration_seconds: float = 48.0
    sample_period_seconds: float = 0.20
    sensor_noise_stddev: float = 0.18
    boundary_margin: float = 0.35
    random_seed: int = 7
    trail_length: int = 24

    def __post_init__(self) -> None:
        if self.duration_seconds <= 0 or self.sample_period_seconds <= 0:
            raise ValueError("Duration and sample period must be positive")
        if self.sensor_noise_stddev < 0 or self.boundary_margin < 0:
            raise ValueError("Noise and boundary margin cannot be negative")
        if self.trail_length < 1:
            raise ValueError("Trail length must be at least one sample")
