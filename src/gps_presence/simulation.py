"""Command-line real-time simulation."""

from collections import deque
import argparse
import time

from .classifier import Presence, PresenceClassifier
from .config import SimulationConfig
from .sensor import SimulatedGpsSensor


_STATUS_COLORS = {
    Presence.IN_A: "\033[92m",
    Presence.IN_B: "\033[96m",
    Presence.OUTSIDE: "\033[93m",
}
_RESET = "\033[0m"


def run(config: SimulationConfig, *, sleep: bool = True) -> None:
    """Run classification online and render each result as soon as it is measured."""
    sensor = SimulatedGpsSensor(
        config.region_a,
        config.region_b,
        config.sensor_noise_stddev,
        config.random_seed,
    )
    classifier = PresenceClassifier(config.boundary_margin)
    trail: deque[Presence] = deque(maxlen=config.trail_length)
    elapsed = 0.0
    sample_count = int(config.duration_seconds / config.sample_period_seconds)
    print("GPS presence simulation | Ctrl+C to stop")

    try:
        for _ in range(sample_count + 1):
            position = sensor.advance(elapsed)
            distance_a = sensor.get_dist_a()
            distance_b = sensor.get_dist_b()
            presence = classifier.classify(distance_a, distance_b)
            trail.append(presence)
            color = _STATUS_COLORS[presence]
            trail_text = " > ".join(state.value for state in list(trail)[-6:])
            print(
                f"\r{color}{presence.value:<8}{_RESET} "
                f"t={elapsed:05.1f}s  pos=({position.x:6.1f}, {position.y:5.1f})  "
                f"dist_a={distance_a:6.2f}  dist_b={distance_b:6.2f}  "
                f"recent={trail_text:<58}",
                end="",
                flush=True,
            )
            if sleep:
                time.sleep(config.sample_period_seconds)
            elapsed += config.sample_period_seconds
    except KeyboardInterrupt:
        pass
    finally:
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fast", action="store_true", help="Run without real-time delays")
    args = parser.parse_args()
    run(SimulationConfig(), sleep=not args.fast)


if __name__ == "__main__":
    main()
