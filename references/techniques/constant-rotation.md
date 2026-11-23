# Time → unwrapped rotation

**Use:** constant signed rpm on an existing component. Inputs: actual pivot, local Euler axis,
fps, start/endpoint frames, initial angle in radians. Carry attached keys/cutters in its hierarchy.
The implementation creates no geometry or parenting.
For uncertain control/channel state or an API error, use the [scoped probe](../api-diagnostics.md).

**Small implementation:** [motion.py](../../scripts/techniques/motion.py), `constant_spin()`:

```python
motion.constant_spin(pivot, axis=2, rpm=-37.5, fps=30, start=1, endpoint=61)
```

Choose values for your task. The invariant is `angle = initial + 2*pi*(rpm/60)*seconds`.
The helper uses unwrapped linear keys and Repeat Offset; it rejects an occupied channel while
retaining unrelated channels. Decide how to isolate/replace existing animation yourself.

**First proof:** compare evaluated signed angle at an intermediate time and subframe. Check
unchanged pivot and dependent-part transforms relative to the shaft. Then reopen the saved clip.
Use an asymmetric marker to judge rotation visually. For a loop, exclude a duplicate boundary
frame and verify every visible channel closes; constant speed alone is not sufficient.

[Animation](../animation-workflow.md) · [Recipe](../recipes/mechanical-motion.md) · [Evidence](provenance.md)
