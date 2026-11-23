# Add thickness while retaining a contact face

**Use:** a flat panel/roof source whose original surface must remain on a support while
thickness changes. Inputs: coherent source normals pointing away from the support, intended
contact plane, thickness in the object's units, suitable scale, independent edge radius.
This is not a general solution for folded shells or self-intersecting corners.

**Mechanism:** preserve the contact surface as the source; Solidify grows to the other side
(`offset = 1` with normals pointing away). Put Bevel after thickness creation when the newly
created rim should receive the manufactured radius. Keep radius and thickness separate;
overlap clamping can reduce the achievable radius on a thin region.

Example on an owned, unthickened Object `panel` with the stated normals/scale:

```python
solid = panel.modifiers.new('Wall thickness', 'SOLIDIFY')
solid.thickness = thickness
solid.offset = 1.0
bevel = panel.modifiers.new('Edge radius', 'BEVEL')
bevel.width = radius
bevel.segments = 3
bevel.use_clamp_overlap = True
```

**First proof:** vary thickness without changing radius or moving the contact source. Measure
evaluated thickness along the intended normal, and the gap between shell and support in one
coordinate space. Check closed geometry/winding where a solid is required. An object bounding
box or nonzero modifier field alone is insufficient. Inspect a grazing view when judging finish.

**Evidence:** extracted from the thin-roof case's fixed support plane and Solidify → Bevel
stack. [Verification and limits](provenance.md#anchored-shell-extension) distinguish the
original supported roof from the separate extraction fixture. No arbitrary curved-sheet
thickness or final surface quality is implied.

[Modifier order](../modifiers-workflow.md#order-follows-the-intended-construction)
