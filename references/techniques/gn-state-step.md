# Advance survivors, then add births

Use for compact particles with constant acceleration and no contacts during the step.
Inputs share the stationary simulation host's local space: point position p, velocity v
in units/second, acceleration a, age/lifetime in seconds and Simulation Input Delta Time.
A separately animated emitter can be sampled through Object Info in Relative space.

## Node/data order

| Stage | Operation | State boundary |
| --- | --- | --- |
| Advance old points | Set Position Offset = v·dt + a·dt²/2 | Read previous velocity |
| Update attributes | Store velocity = v+a·dt, then age = age+dt | Point domain on carried geometry |
| Expire | Delete Geometry where updated age ≥ lifetime | Before counting survivors |
| Birth | New points at current emitter location, age=0, initial velocity and birth time | Sample once, assign persistent ID |
| Retain | Join survivors and births → Simulation Output | Render instances afterward |

For a numeric sample of that same update:

```python
def constant_acceleration_step(p, v, a, age, dt):
    assert dt >= 0
    return (tuple(x+u*dt+g*dt*dt/2 for x,u,g in zip(p,v,a)),
            tuple(u+g*dt for u,g in zip(v,a)), age+dt)
```

This convention adds births at the end of the interval: they first move on the next
step. Never advance newborns by a full dt or overwrite survivors with the current emitter
position. Initial dt=0 does not advance state. Read the updated stored age for expiry;
an unconnected field is not persistent state. Changing host transforms after birth moves
the whole local simulation; use a stable host when world-space trails are required.

## Check and boundary

Track one ID: stored birth position stays fixed while its emitter moves away; position
matches the constant-acceleration solution at its age. Compare equal elapsed seconds at
two effective FPS values (fps/fps_base), allowing quantized births. Check age zero at birth
and empty tail after stopping emission. Wrong dt units and current-emitter overwrite should
fail these checks. This does not implement drag, contacts, inherited emitter velocity or
subframe birth sampling. Those require their own integration/space contract.

[Emission budget](gn-emission-budget.md), [durable replay](gn-bake-replay.md),
[broader state guide](../particle-simulation-nodes.md).
[Extraction evidence](provenance.md#state-and-motion-extraction-batch).
