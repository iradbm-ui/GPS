# GPS Presence Simulation

A small, dependency-free Python simulation of real-time GPS presence classification.
It generates a moving sensor with variable speed, measures signed shortest distance
from the sensor to two configurable regions, and prints the current classification
as each sample arrives.

## Run

```powershell
python -m pip install -e .
.venv\Scripts\python.exe -m gps_presence
```

The terminal updates one live status line. Press `Ctrl+C` to stop. To install the
console command in an active environment:

```powershell
python -m pip install -e .
gps-presence
```

## Algorithm

`get_dist_a()` and `get_dist_b()` expose simulated sensor measurements. They return
signed shortest distance to each boundary: positive means inside that region,
negative means outside, and zero is the boundary. Gaussian noise models measurement
error. The classifier applies a configurable boundary margin and declares `Outside`
unless exactly one region is confidently positive. A positive distance for both
regions is rejected because the assignment requires disjoint regions.

The path uses smooth, changing speed rather than constant velocity and deliberately
passes through region A, the outside area, and region B during one run. Classification
is performed immediately for each generated sample; there is no post-processing.

## Configuration

Edit the `SimulationConfig` defaults in `src/gps_presence/config.py` to change region
shape and size, motion timing, sensor noise, boundary margin, and repeatability. The
geometry layer currently supports circles and axis-aligned rectangles through signed
distance functions.

## Development

```powershell
.venv\Scripts\python.exe -m pytest
```

The project uses only the Python standard library at runtime. It is structured as a
package so the simulation logic, classifier, geometry, and tests can be reused by a
real sensor adapter later.
