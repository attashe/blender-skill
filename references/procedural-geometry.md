# Bounded Geometry Nodes, curves and NURBS

## Contents

- Choose the representation
- Use basic GN operations deliberately
- Bound topology before evaluating it
- Control curve and surface tessellation
- Verify the parameter family and production graph
- Official sources

## Choose the representation

Make this choice before adding detailed topology. Combine representations where useful.

| Shape or operation | Starting representation | Reason and acceptance check |
| --- | --- | --- |
| Unique plate, bracket or opening | Explicit mesh + appropriate modifiers | Direct topology control; inspect edges, silhouette and modifier output |
| Repeated vents, fasteners or configurable layout | GN/collection instances of a source part | Shared editable source; bounded count, correct spacing/orientation |
| Straight segments or intentional corners | Poly curve | Exact path samples; do not smooth corners by increasing subdivision |
| Art-directed cable, rail or contour | Bézier curve + profile | Handles control bends; inspect curvature, tilt, end caps and profile orientation |
| Rational arc or weighted smooth profile | NURBS curve | Order and weights control shape; verify the intended rational construction |
| Smooth patch with a U/V control net | NURBS surface | Separate control and tessellation in two axes; inspect continuity, seams and export |

Choose NURBS for a concrete shape benefit. Blender NURBS curves and surfaces have different
editing and evaluation rules; a GN curve node does not imply support for a NURBS surface net.
Keep editable authoring geometry and create a separate mesh export variant when required.
For a zero-thickness profile/trajectory source, record the intended nonzero axes and keep
plane/orientation checks in acceptance. In the manifest profile use `contract.bounds_axes`
(for example X/Y for an XY profile). Do not add fake thickness to pass a volume audit.

## Use basic GN operations deliberately

Read the installed node modes, sockets and domains before wiring. Start with a small working
graph and inspect its evaluated result; use reusable groups for repeated functions.

| Need | Candidate operations | Cost/control rule |
| --- | --- | --- |
| Repeat one source part | Instance on Points, Translate/Rotate/Scale Instances | Bound point count before generating points; keep instances until an operation needs mesh data |
| Deform a surface | Set Position + fields | Choose the consumer domain; avoid a Python loop that duplicates the surface per point |
| Sample a path | Resample Curve, Sample Curve, Spline Parameter | Bound evaluated path samples; inspect orientation and cyclic seams |
| Make a swept section | Curve to Mesh + profile; Curve to Tube modifier where suitable | Bound path samples and profile sides independently; account for caps and joins |
| Carry data across operations | Capture Attribute or Store Named Attribute when needed | Choose the correct domain and consumer; do not store unused attributes |
| Select variants or iterations | Switch/selection, Repeat Zone | Bound every topology-producing branch and iteration count; include nested multipliers |

Instancing reduces duplicated geometry storage. Expanded geometry, shading and export costs
still grow with occurrence count. Compare [exported and target costs](performance-workflow.md),
including UV/normal vertex splits and the consumer's actual batching. Delay Realize Instances until a required mesh operation or
export; an early realization can erase the storage benefit without changing the silhouette.

Use Count mode when an exact curve sample cap is required. Length mode needs both a minimum
step and a maximum path length, followed by a verified sample bound. Density alone is not a
hard point-count limit. For scatter, bound source area, density and the generated point count;
prefer a bounded source when an exact cap matters. Deleting points or selecting `Index < cap`
after an expensive distribution does not bound the cost of creating that distribution.

## Bound topology before evaluating it

For topology-generating GN, curve/surface tessellation, Array, subdivision and repeat systems,
record topology controls with minimum, nominal and maximum values and a conservative cost
bound. In the manifest profile declare `procedural: true` and integer `min`, `value`, `max`
controls. Outside that profile use the project's own contract; the actual bounds and tests
still apply. For float density/step, derive and enforce an integer count cap; keep the
physical float range in the asset's contract and test it as well.

Clamp inputs in the builder and in the graph wherever external fields or drivers can supply
them. Node-interface UI limits describe an interface; they do not prove evaluation limits.
Cap iterations and nested counts. Do not append topology-changing modifiers after a checked
model without revising its conservative envelope.

Use explicit growth formulas to plan limits:

| Simple topology | Growth |
| --- | --- |
| Open path with C samples and closed P-sided profile, no caps | Vertices = C × P; side triangles = 2 × (C − 1) × P |
| Flat caps on that simple sweep | Add 2 × (P − 2) triangles; curved/round caps need their own envelope |
| Open U × V sampled grid | Vertices = U × V; triangles = 2 × (U − 1) × (V − 1) |
| L subdivisions of all-quad input with Q faces | Faces = Q × 4^L; triangles = 2 × Q × 4^L |
| N occurrences of a generated part | Expanded cost = N × part cost; multiply again for nested repetition |

These formulas apply to the stated topology. Boolean cuts, joins, displacement subdivision,
round caps and adaptive tessellation need additional bounds. NURBS control-point counts are
not evaluated U/V sample counts. Use a conservative envelope for anything outside a simple
model, then measure it in Blender.

For example, an uncapped tube at C=32, P=8 has 496 side triangles; C=128, P=64 has 16,256.
A small editable curve can therefore produce a large mesh. Increasing both resolutions costs
much more than increasing one.

When using the manifest profile, run the bundled preflight before changing topology settings:

```bash
python3 <skill>/scripts/geometry_cost.py <skill>/assets/cable-node.json
python3 <skill>/scripts/pipeline.py preflight <project>/asset-manifest.json --node cables
```

The first example is an unbuilt node fragment; embed/adapt it within a project's full manifest.
Outside the profile, use an equivalent pre-evaluation bound calculation and retain its result.
The estimator supports mesh envelopes, simple sweeps/grids, all-quad subdivisions, repetition
and sums. It does not inspect a GN graph or prove arbitrary procedural code safe. Its models
are monotone in the declared count controls; other systems need conservative upper envelopes
and additional mixed-parameter tests. Set limits for the camera, style and target device.

## Control curve and surface tessellation

- Keep path/control structure separate from the evaluated mesh. Use the fewest control points
  that describe the intended shape; inspect whether extra points improve the shape at all.
- Set Spline Resolution affects evaluated points of supported smooth splines. Resample Curve
  can establish a predictable Count after shaping. Poly splines already specify their points.
- Treat profile resolution/bevel resolution as an independent multiplier. Increase it only
  until the intended camera's silhouette/shading passes. Check joins, cyclic seams and caps.
- For NURBS, inspect valid order relative to control points, weights, endpoint/cyclic settings
  and the resulting shape. Weight changes are shape edits, not a substitute for sample bounds.
- For NURBS surfaces, bound evaluated U and V independently. A dense control net and high
  evaluation resolution can both add cost. Preserve the control net for later editing.
- Inspect Preview U/V and Render U/V. A nonzero render override can produce a different mesh;
  zero render resolution uses preview settings where the installed curve/surface API specifies it.
- If supported by the installed version, consider Set NURBS Order and Set NURBS Weight for
  curve construction/adjustment. Check live sockets and spline types; do not assume surface-net support.
- Where available, use Curve to Tube's profile, caps and UV options when they solve the asset
  problem. Round caps/resampling can exceed a simple flat-capped sweep; bound them separately.
- Convert only the derived export copy. Compare source and export silhouette, dimensions,
  normals/materials/UVs and actual exported mesh counts; keep the original editable source.

## Verify the parameter family and production graph

1. Preflight the declared maximum. Build the nominal variant with a bounded small count first.
2. After each topology-expanding operation, measure evaluated vertices, triangles and occurrences.
   Inspect the audit's largest contributors to identify which source causes the cost.
3. In isolated copies, test minimum, nominal and maximum controls. Read actual values back from
   Blender after writes; inspect valid geometry, spacing, orientation, caps and intended behavior.
   Add mixed extrema/threshold tests for coupled or nonmonotone controls.
4. Use a runner timeout for risky background evaluations and available platform resource limits
   when appropriate. Stop on failed preflight, timeout or budget failure; reduce the settings or
   revise the method. A post-evaluation audit cannot prevent an already-running runaway graph.
5. Reopen the nominal saved source after tests. Do not silently leave a maximum-cost test variant
   in the authoring file. Identify the tested source and dependencies in the report; in the
   manifest profile bind it to their hashes as required by that contract. Report actual
   measurements, not estimator output.
6. If viewport/render settings differ, get a real render dependency graph from the host's render
   execution and audit it. `Depsgraph.mode` is readonly; relabeling a viewport report proves nothing.
   Also test maximum controls in that production graph. Treat detected divergence flags as useful
   signals, not an exhaustive discovery of every custom driver or renderer's geometry behavior.

No Blender execution channel means a plan with predicted bounds and unbuilt status. Never fill
the measurement/evidence fields from the estimator and call the asset verified.

## Official sources

- [Geometry Nodes performance](https://docs.staging.blender.org/manual/en/latest/modeling/geometry_nodes/performance.html)
- [Spline Resolution, 5.2](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/curve/read/spline_resolution.html)
- [Resample Curve, 5.2](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/curve/operations/resample_curve.html)
- [Curve to Tube, 5.2](https://docs.blender.org/manual/en/5.2/modeling/modifiers/generate/curve_to_tube.html)
- [NURBS surface active spline, 5.2](https://docs.blender.org/manual/en/5.2/modeling/surfaces/properties/active_spline.html)
- [Blender 5.0 modeling changes](https://developer.blender.org/docs/release_notes/5.0/modeling/)
- [Blender 5.2 release](https://www.blender.org/download/releases/5-2/)
- [Dependency graph API](https://docs.blender.org/api/5.0/bpy.types.Depsgraph.html)
