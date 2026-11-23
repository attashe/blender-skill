# A real opening followed by a bounded bevel

**Use:** a drilled plate/flange/keyway with real geometry and readable edges. Inputs: owned
mesh host/cutter, suitable intersection, local radius and segments. Check units, scale, thickness
and clearance. Choose stack position; do not accumulate this operation on repeated stage runs.

**Small implementation:** [cut_bevel.py](../../scripts/techniques/cut_bevel.py), `cut_and_bevel()`.
It appends Exact Difference then angle-limited Bevel with overlap clamping, returning both.
It does not construct geometry, apply transforms, assign normals, choose ownership or save files.

**First proof:** inspect a section/useful view: the opening passes through, solid areas remain
and thickness is independent of radius. Change radius and compare evaluated geometry. Clamping
can greatly reduce effective bevel; a stored width or more segments does not prove the desired
edge shape. Resolve short edges/clearance or representation when the radius cannot fit.

**Verify:** hole/solid ray or section tests, winding/manifoldness as needed, thickness, edge
response and saved modifier stack. The isolated fixture confirms a through hole and two radii,
not arbitrary Boolean topology or manufacturing tolerances. Normals/shading remain a separate
decision in [modifiers](../modifiers-workflow.md).

[Modeling](../modeling-workflow.md) · [Evidence](provenance.md)
