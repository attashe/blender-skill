# Fractional births, capacity and persistent IDs

Use for continuous low-rate emission in a GN Simulation Zone. Inputs: rate ≥ 0 in
particles/second, Delta Time in seconds, carry in [0,1), survivor count, integer capacity,
and a monotonic next ID. Start with zero carry/ID and empty geometry. This variant drops
excess births; it does not queue them. Capacity is fixed during the solve.

## Small mechanism

Carry, Next ID and compact Geometry are Simulation Output state items; pair Simulation
Input after defining them. Translate this reference calculation into Math/Integer Math
nodes and a point-component Domain Size query after expiry:

```python
import math
def emission_step(carry, rate, dt, survivors, capacity, next_id):
    assert 0 <= carry < 1 and rate >= 0 and dt >= 0
    assert 0 <= survivors <= capacity and next_id >= 0
    budget = carry + rate * dt
    requested = math.floor(budget)
    accepted = min(requested, capacity - survivors)
    return budget-requested, accepted, next_id+accepted
```

Generate **accepted** points only, then Set ID = previous Next ID + birth Index. Connect
that expression explicitly: Set ID's unconnected ID uses its implicit Index field;
writing a hidden default_value is not proof of assigning that constant. For a constant
diagnostic ID, link an Integer node and read the evaluated id attribute. Store
birth attributes once; join survivors and births; write all three state outputs.
Keep the fractional part of **requested**, not accepted: full rejected births must not
accumulate into a later burst. Counter advances by accepted births, never live count.
Use integer arithmetic for IDs/capacity; float Math loses integer precision at large counts.
Bound requested rate/time interval and source work as well as output count.

## Check

With rate below FPS, rounding each interval independently should fail a negative control.
Inspect IDs through deaths/rebirths, the first and last emission, zero rate and full capacity.
Compare requested rate separately from accepted rate under saturation. Finite frame grids
quantize birth times; floating-point sums near an integer require a declared tolerance,
not an unexplained epsilon on every frame. This is neither a burst-event detector nor
a variable-capacity eviction policy. Continue with [state step](gn-state-step.md).

[Zone semantics](https://docs.blender.org/manual/en/5.1/modeling/geometry_nodes/simulation/simulation_zone.html).
[Extraction evidence](provenance.md#state-and-motion-extraction-batch).
