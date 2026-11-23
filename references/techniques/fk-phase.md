# One FK pose → a phased gesture

**Use:** a ready rig within its supported joint range. Inputs: actual PoseBone, local Euler
axis, frame/radian pairs and interpolation. Existing NLA or keyed/driven channels need deliberate
isolation. This technique does not create a skeleton or repair skin weights.
For uncertain PoseBone/Action ownership or an API error, use the [scoped probe](../api-diagnostics.md).

**Small implementation:** [motion.py](../../scripts/techniques/motion.py), `rotation_keys()`.
It keys the PoseBone and resolves the owning rig's Action/slot channelbag:

```python
motion.rotation_keys(bone, axis=0,
                     frame_radians=[(1, 0), (13, math.radians(17)), (61, 0)], cycle='REPEAT')
```

**First proof:** inspect one changed pose in the shot. An axis/angle alone does not mean “nod
down” or “look left”. Confirm direction before filling the timeline. Add a smaller body response
and phase successive tail controls only where the action calls for it; timing/amplitude are
art direction, not fixed constants. Keep required contact/root motion independent.

**Verify:** evaluated pose, contact, silhouette, extremes/in-betweens and timing. Separate the
hand's local gesture from inherited world travel. Inspect the chain's shape, not just peak-frame
order. Reopen after late code changes; a loop requires motion continuity near the boundary too.

[Rigging](../rigging-workflow.md) · [Recipe](../recipes/character-gesture.md) · [Evidence](provenance.md)
