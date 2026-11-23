# One turns control → rotation and axial travel

**Use:** a nut/screw following a known thread. Inputs: owned pivot, numeric Object property in
turns, local axis, pitch in scene units, assembled offset and handedness. The example assumes
an aligned, unscaled parent frame. Determine geometry/clearance; the source motor's pitch is
not a default for other fasteners.

**Small implementation:** [motion.py](../../scripts/techniques/motion.py), `drive_from_property()`:

```python
motion.drive_from_property(pivot, 'rotation_euler', control, 'turns',
                           index=axis, factor=2*math.pi, offset=initial_angle)
motion.drive_from_property(pivot, 'location', control, 'turns',
                           index=axis, factor=pitch, offset=seated_position)
```

Choose signs for actual handedness/axis. The code changes only named channels, without geometry
or parenting edits. Key one source property with `property_keys()`. A shared source drives all
connected parts; a one-nut task needs an isolated relation.

**First proof:** change a fractional turn; independently compare evaluated orientation and
axial travel (`turns*pitch`), including a transformed parent if used. Inspect seating/clearance
and stationary parts, then reopen. Correct ratios do not establish collision-free manufacturing fit.

[Recipe](../recipes/mechanical-motion.md) · [Evidence](provenance.md)
