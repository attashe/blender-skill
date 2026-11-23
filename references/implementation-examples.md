# Editable examples

Open a scene from this skill and save a working copy in the project before editing. These examples were prepared in Blender 5.2.1 LTS. Each card identifies the control to edit and an observation to repeat after reopening your result.

See the [earlier scene catalog](early-examples.md) for apartment layout, texturing, procedural nodes, cel shading, short films, FX and compositing.

## Geometry and surfaces

| Scene | Edit and check |
| --- | --- |
| [Bézier horn](../assets/sweep-example/horn.blend) | Move one path knot. Compare the tip and the base ring with the [example views](techniques/editable-sweep.md). |
| [Rock with a lattice](../assets/lattice-example/rock.blend) | Adjust the existing cage. Measure the rise on the shoulder and the height of the contact vertices using the [lattice example](techniques/lattice-region.md). |
| [Motor shaft](../assets/motor-example/shaft.blend) | Inspect the mounting holes and modifier stack. The [cut and bevel example](techniques/cut-bevel.md) shows how to check a changed dimension. |

## Motion and simulation

| Scene | Edit and check |
| --- | --- |
| [Rigify walk and greeting](../assets/walk-example/greeting.blend) | Scrub four steps and the change of attention. Track the body relative to the floor and the wrist relative to the shoulder. [Walk example and playback](character-walk.md) |
| [Momo FK gesture](../assets/momo-example/gesture.blend) | Retime the gesture and blink independently. Check feet, hand and eye shapes on the same frames. [Rig interface](examples/character-gesture.md) |
| [Spinning shaft](../assets/motor-example/shaft.blend) and [threaded fasteners](../assets/motor-example/fasteners.blend) | Change the shaft speed or a nut turn. Measure the evaluated angle or axial travel. [Motor interface](examples/motor-motion.md) |

For simulations, the [rigid body cache example](techniques/rigid-cache-replay.md) illustrates a replay check in a fresh process.

## Image and delivery

Compare the edited walk with the [original clip](../assets/walk-example/greeting.mp4) or its [pose sheet](../assets/walk-example/greeting-poses.png). For a handoff check, use the [native relocation example](techniques/clean-project-relocation.md) or [GLB round-trip](techniques/glb-surface-roundtrip.md) on a copy saved in the destination project.
