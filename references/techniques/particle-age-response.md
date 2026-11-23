# Drive a visible response with normalized particle age

Use for a designed fade/cooling response. Inputs: stored birth time or age in seconds,
strictly positive per-particle lifetime, and stable IDs. The example is art direction, not
a thermodynamic temperature model. Geometry survival and shader response are separate.

```python
def age_response(age, lifetime):
    assert lifetime > 0
    live = 0 <= age < lifetime
    heat = max(0.0, min(1.0, 1.0-age/lifetime)) if live else 0.0
    return live, heat
```

GN: delete unborn/expired points; on survivors store heat = 1−Clamp(age/lifetime,0,1)
on the point domain before instancing. Shader: read that attribute through the proven
[instance → shader route](instance-shader-attribute.md), map heat to color and multiply
it by a separately exposed peak emission strength. Lifetime changes timing; peak intensity
changes brightness. Connect both to the actual surface output. If instances are realized,
verify attribute propagation and the appropriate shader attribute context again.

## Check

Follow the **same ID** at birth, middle and just before expiry: attribute, emitted pixel
response and survival must agree. Hold camera/exposure/light fixed for the response test;
first disable glow so it cannot conceal a disconnected control. Check zero population and
empty tail. A constant-brightness shader with correctly changing stored heat must fail.
Physical blackbody, transparency, trails and motion blur need separate treatment; a long
mesh dash is not automatically a shutter streak. Use [particle workflow](../particles-workflow.md)
when choosing the representation, then [GN replay](gn-bake-replay.md) if caching is needed.

[Extraction evidence](provenance.md#state-and-motion-extraction-batch).
