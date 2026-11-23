# Separate textile transmission, openings and sheen

**Use:** sheer curtains, thin woven cloth, or another thin scattering sheet. Determine which
cue is missing: backlighting, visibility through the weave, grazing reflection, or folds.
They have different controls. A reduced alpha cannot supply all four.

**Contract:** a non-self-intersecting sheet with intentional front/back behavior; a backlit
view plus a reflected-light view. A zero-thickness sheet is deliberate here, unlike a solid
frame or glass pane. Keep it clear of the pane and sill. Static draped geometry is sufficient
for a still study; use [cloth](../cloth-workflow.md) when motion/contact is part of the task.

## A bounded Thin Wall branch

Blender 5.2 introduced the Principled **Thin Wall** boolean. Inspect the actual node inputs
with the [scoped probe](../api-diagnostics.md#inspect-one-node-or-upstream-branch), then prove
the effect in the selected renderer. Thin Wall and Thin Film are unrelated controls.

For a fresh/caller-owned Principled `surface`, its node tree `tree`, and Material Output
`output`, with unlinked inputs and no competing surface path:

```python
if surface.inputs.get('Thin Wall') is None:
    raise ValueError('Choose a supported thin-sheet scattering model for this runtime')
surface.inputs['Thin Wall'].default_value = True
surface.inputs['Base Color'].default_value = cloth_color
surface.inputs['Metallic'].default_value = 0
surface.inputs['Alpha'].default_value = 1
surface.inputs['Roughness'].default_value = roughness
surface.inputs['Transmission Weight'].default_value = 0
surface.inputs['Subsurface Weight'].default_value = 1
surface.inputs['Subsurface Anisotropy'].default_value = scattering_bias
surface.inputs['Sheen Weight'].default_value = sheen_weight
surface.inputs['Sheen Roughness'].default_value = sheen_roughness
openings = tree.nodes.new('ShaderNodeBsdfTransparent')
coverage = tree.nodes.new('ShaderNodeMixShader')
coverage.inputs[0].default_value = open_fraction  # 0..1; fraction of unresolved holes
tree.links.new(surface.outputs['BSDF'], coverage.inputs[1])
tree.links.new(openings.outputs[0], coverage.inputs[2])
tree.links.new(coverage.outputs[0], output.inputs['Surface'])
```

Thin Wall subsurface supplies diffuse backward/forward scattering, without treating the
sheet as a solid glass boundary. `scattering_bias` controls that balance. Subsurface Radius,
Scale and Method do not set thickness in this mode. In older runtimes, a weighted
Diffuse/Translucent combination is a possible alternative; validate that branch rather
than silently discarding the missing Thin Wall input. The authored check used Cycles,
not a test of this fallback or EEVEE's separate thickness settings.

The Transparent mix models **unresolved open area**, not translucent yarn. Keep the two
controls separate; if there are no visible/averaged holes, set `open_fraction=0` and omit
that branch. Do not use Add Shader to sum two full-strength surfaces. For an existing graph,
edit its controlling sockets instead of appending a second coverage branch.

## Proof and useful limits

With fixed exposure, camera and geometry, compare opaque cloth, diffuse transmission only,
then transmission plus openings under backlight. A contrasting object behind it distinguishes
light passing through the fibers from direct visibility through gaps. Compare one/two layers
and a front-lit view; hems and overlapping folds should change coverage. Keep
[sheen](sheen-response.md) a reflection response rather than a glowing outline.

At architectural distance the mean open fraction can replace individually unresolved yarn
holes. It is an approximation: it does not reproduce angle-dependent yarn occlusion or weave
parallax. For close views, use metric weave/coverage detail with appropriate filtering and
inspect it at delivery resolution; adding stronger noise cannot repair missing construction.
Choose the representation from the view, not an automatic high-frequency texture step.

The author sample used roughness 0.8, scattering bias 0.35, sheen 0.12/0.6 and mean openness
0.16. These illustrate the mechanism, not a universal textile preset. The viewed Air 4
reference is a plain-woven **Trevira CS** fabric; its appearance does not establish linen
composition or measured optical parameters. Fold rhythm, hem, color and lighting remain
art direction. Save/reopen the actual view with the chosen sheet and shader configuration.

[Evidence](provenance.md#window-transmission-extraction) ·
[Blender 5.2 thin-sheet model](https://www.blender.org/download/releases/5-2/) ·
[Principled parameter behavior](https://docs.blender.org/manual/id/5.3/render/shader_nodes/shader/principled.html) ·
[Kvadrat Air 4 visual reference](https://www.kvadrat.dk/en/products/curtains/5801-air-4)
