# Separate glass thickness from surface frosting

**Use:** acid-etched/satin glass, privacy panes or cabinet glazing whose background should
remain luminous but lose detail. Start with a viewed reference and the intended object-to-pane
distance. Frosted glass is not simply gray glass or reduced alpha.

**Contract:** a pane with known scale, no backing proxy blocking the opening, and a camera
that sees both a background edge and a reflection. Choose a closed solid when edge thickness,
refraction or depth tint matters. Check [shell orientation](mesh-orientation.md); coincident
faces and intersecting frame parts can produce defects unrelated to the shader.

For a fresh/caller-owned Principled `surface` with unlinked controls:

```python
surface.inputs['Base Color'].default_value = (1, 1, 1, 1)
surface.inputs['Metallic'].default_value = 0
surface.inputs['Alpha'].default_value = 1
surface.inputs['IOR'].default_value = glass_ior
surface.inputs['Transmission Weight'].default_value = 1
surface.inputs['Roughness'].default_value = surface_roughness
if surface.inputs.get('Thin Wall') is not None:
    surface.inputs['Thin Wall'].default_value = False  # this branch is a closed pane
```

Connect its BSDF to the active Material Output Surface and assign it to the intended faces.
These parameters are not measured manufacturer values. A 6 mm author sample used IOR 1.46
and roughness 0.018/0.38 to expose clear/frosted endpoints; tune against the actual reference.

- **Etched boundary:** roughness broadens reflection and transmission. For one etched side,
  assign the rough material only to that face, keeping the back and edges clear. An all-face
  material represents a different treatment. Keep front/back normals and assignment explicit.
- **Interior tint:** use [absorption](volume-absorption.md) only for a justified depth effect.
  A scattering volume is not needed to reproduce surface etching. Do not compensate for a
  hidden opaque wall by brightening the glass or adding emission.
- **Thin-sheet alternative:** supported Thin Wall transmission is useful when thickness and
  refraction displacement are irrelevant. Do not combine that approximation with the two
  boundaries of a solid pane without checking the resulting double response.

**First proof:** keep camera, exposure and illumination fixed. Compare clear/frosted with a
contrasting form close behind the pane, then farther away. An orthographic test keeps the
background's apparent size constant. Inspect the edge spread and retained color/light, not
only mean brightness. Keep a broad reflected highlight in the view. If it reads opaque,
check the first occluder, face/material assignment, active output and engine transmission
before adding noise or raising sample counts. Integration needs the real frame/reveal and
background: a material test alone cannot prove the window assembly.

**Boundary:** tested in Cycles 5.2.1 with a single etched face, closed 6 mm pane and near/far
background. No measured haze/transmittance, insulated glazing, caustics or EEVEE parity is
certified. Photograph blur is a qualitative cue, not an inferred roughness measurement.

[Evidence](provenance.md#window-transmission-extraction) ·
[Guardian SatinDeco reference](https://www.guardianglass.com/eu/en/our-glass/guardian-satindeco/satindeco) ·
[Principled Thin Wall release notes](https://developer.blender.org/docs/release_notes/5.2/rendering/)
