# A dimensioned tile field and its junction

Use for a backsplash, planar tiled wall or floor where module size, seams and edge cuts
matter. Work inside the accepted interior composition; this is not a room generator or
construction-code validation. Find the product's actual dimensions, thickness, finish and
joint guidance; nominal size can differ. Choose the representation for the closest view:
geometry for visible thickness/edge silhouettes, a material for distant fields, or both.

## Plan the pattern before multiplying it

Identify the wall's two local axes, field boundary, reference line and actual tile size.
Pitch is **tile size + clear joint**, not tile size alone. Choose the pattern phase from
the composition: centerline, countertop, visible corner or established adjoining field.
Compare edge cuts before building detail. Changing wall width should change counts/cuts,
not stretch every tile. Retain awkward slivers in the diagnostic layout until the phase,
boundary or tile choice is deliberately revised; silently deleting them leaves holes.

For a regular rectangular field, [tile_layout.py](../../scripts/techniques/tile_layout.py)
returns bounded clipped footprints and cut-side flags in caller-defined plane coordinates:

```python
from tile_layout import rect_tiles
pieces = rect_tiles((-0.402, 0.402, 0, 0.5127), (0.1, 0.1), 0.003175,
                    phase=(-0.05, 0), max_tiles=500)
# each piece: cell=(column,row), bounds=(umin,umax,vmin,vmax), cut=(left,right,bottom,top)
```

The function is pure math. It does not create geometry, choose materials, handle openings,
reserve perimeter sealant or infer units. All lengths share one unit. Boundary clipping
may end inside a joint, leaving a partial joint at the boundary. Choose a different phase
or explicit trim where the design requires a tile edge. Check the returned extents.
For staggered/irregular patterns or openings, use an appropriate layout/construction route.

Build one tile with useful thickness and restrained edge radius. Reuse its mesh or instances
for whole tiles; clipped edge pieces have their own size. Keep bevel width in physical units
after scale changes. For a very large field use [GN placement](gn-patterns.md) and preserve
instances; material variation on unrealized instances needs the
[attribute bridge](instance-shader-attribute.md). Array/modifier offset semantics depend on
the chosen tool: verify actual pitch on the evaluated result.

## Separate the surfaces and the adjoining construction

Glaze is a dielectric surface; a low roughness can already express it. A second coat is not
automatically necessary. Place a broad source where its reflection can be seen; compare one
roughness change with camera/light fixed. Grout has its own rougher response and sits slightly
behind tile faces. A darker base color alone does not create a recessed seam. Keep thickness,
edge radius, broad waviness and pore detail at distinct scales; strong generic noise should
not replace a viewed ceramic finish. Use restrained per-tile variation where supported by
the reference; brick seams baked into a scan must not be overlaid on contradictory geometry.

Treat a counter/wall change of plane and visible field edge as separate junctions. Reserve
their intended gap/trim/seal geometry instead of pushing tiles through the countertop or
stretching the last row. The exact dimensions and construction come from the brief/product;
the example values above are not a universal installation specification.

## Prove the slice

- Measure a full tile, horizontal and vertical seams, thickness and cut-piece extents.
- Change the host width or phase: retain full tile dimensions and inspect new edge pieces.
- Check the lower junction and target-view silhouette; inspect glaze and grout in fixed light.
- Reopen the saved view and resources; change a shared source/finish in a copy and verify it persists.

Extracted from an authored Blender 5.2.1 LTS kitchen junction: 45 tiles with two shared mesh
sizes, 100 mm modules, 3.175 mm gaps, 9.525 mm thickness, explicit cut edges and seal strip.
Math tests cover another width, shifted/negative phase, exact boundaries and invalid budgets;
the scene was checked after reopen. This validates a smooth ceramic study, not a replica of
handmade Zellige undulations, a waterproof installation or an independent Pi pass.
The module retains a simplified sink/counter and is not a completed kitchen.

[Viewed product reference and dimension table](https://digitalassets.daltile.com/content/dam/Marazzi/website/documents/product-detail-page/zellige/MZ_Zellige_SS.pdf)
· [Surface families](../surface-families.md) · [Assembly fit](assembly-fit.md)
