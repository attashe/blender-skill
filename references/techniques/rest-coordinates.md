# Rest coordinates for procedural pigment

**Use:** markings should follow a deforming mesh with stable point correspondence. Inputs:
owned undeformed mesh, attribute name and the exact shader Vector input for pigment mapping.
Shared mesh/material users share the change. Capture before deformation, not at an arbitrary pose.

**Small implementation:** [rest_coordinates.py](../../scripts/techniques/rest_coordinates.py).
`capture_rest_positions(mesh_object)` writes POINT/FLOAT_VECTOR source-local coordinates;
`connect_rest_coordinates(material, coordinate_input)` routes an Attribute output to only that
input. Existing attributes are not overwritten: verify/reuse them on a prepared asset.

**First proof:** deform enough to distinguish following from stationary mapping. Compare the
evaluated attribute to its source and inspect the pigment boundary before/after under identical
viewing conditions. Attribute presence alone does not prove the material uses it. Do not replace
every mapping input: other effects may intentionally use world or different coordinates.

**Verify:** modifiers preserve required data/interpolation; pigment follows in the saved scene
and chosen renderer. UV painting, remeshing and export need a representation their consumer
supports; this is not a universal solution for changing topology or a substitute for UVs.

[Shader guide](../shader-nodes-workflow.md) · [Recipe](../recipes/character-gesture.md) · [Evidence](provenance.md)
