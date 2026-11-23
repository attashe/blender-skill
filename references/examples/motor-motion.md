# Motor motion: adapt controls before building a clip

This is an asset-specific integration interface. For a reusable operation start with the
[technique index](../technique-index.md); for composition use the [recipe](../recipes/mechanical-motion.md).

Use for constant shaft speed or pitch-coupled fastener motion on the existing detailed motor.
This is an external mechanism study, not internal motor physics or manufacturing CAD.
The example scenes were exercised in Blender 5.2.1 LTS, build 9e2066aef7ef; verify your runtime.

## Asset interface

| Part | Static model already contains | The historical clip builder adds |
| --- | --- | --- |
| `CTRL_Shaft` | Pivot, `angle_deg` property and dependent shaft/key/cutter hierarchy | Driver from degrees to Y rotation, then a speed Action |
| `Mount_nut_0` … `Mount_nut_3` | Modeled fasteners; 1 mm pitch, nut local +Z along world +Y in this asset | `CTRL_Nut_*` pivots and coupled rotation/travel drivers |
| `CTRL_Asset` | Asset root | Shared `nut_turns` and `explode` controls for its demonstration clips |

A property present in the base model does not imply that motion is wired. In the example,
`angle_deg` drives shaft Y rotation with a minus sign; a positive nut turn rotates around +Y
and moves +0.001 m along Y. Confirm these relationships in your actual input/version.
The historical `nut_turns` moves **all four nuts**. A one-nut task needs a separate control or
equivalent isolated relation; preserve the seated offset and the other fasteners.

## Relevant implementation, then one changed sample

Open the [shaft clip](../../assets/motor-example/shaft.blend) for the 30 rpm loop. Open the [fastener study](../../assets/motor-example/fasteners.blend) for a one-turn pitch change. Inspect the Action on the owning control and the drivers on the carried parts. The [constant rotation](../techniques/constant-rotation.md) and [pitch coupling](../techniques/pitch-coupling.md) examples expose the corresponding operations.

Choose speed, timing, turns and affected parts from the current brief. Independently expect
`angle_degrees = initial + rpm * 6 * seconds` and `travel = turns * pitch` with the chosen
axis/handedness. Test one changed angle or fractional turn on an evaluated copy and inspect
the shaft/keyway or fastener view before expanding the timeline. Fix only that relation if it
fails; a full inventory of unrelated properties does not help establish it.

## Verify the saved result

Reopen your delivered scene; verify stationary parts, carried cutter/key, axial pitch,
intermediate times and visible clearance. For a loop, distinguish the N delivered frames
from the matching endpoint at start+N; check continuity near the seam, including subframes
when using time-driven controls. A saved source edit is not an updated .blend.
