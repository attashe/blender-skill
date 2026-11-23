# Architectural layout studies

Use for an apartment or house plan, occupied levels and circulation. Stop at the requested
finish; a layout study need not furnish every room. For a camera/light decision outside
architecture, use [blockout, camera and light](blockout-camera-light.md).

## Small first proof

Build and save a small shell with one real opening and one useful view. If a new helper
constructs solids, first check one wall/step with [mesh orientation](techniques/mesh-orientation.md)
and its bundled probe. A primitive is often sufficient; a new face list needs evidence.
Inspect the first image before multiplying rooms or writing a circulation checker.
The first saved view must survive a failure in later validation. For saved shell checks,
reuse the same named-object mesh probe; a bespoke whole-scene validator can spend the
remaining time debugging Mesh/BMesh API differences instead of checking the asset.

For multiple storeys, use explicit occupied floor levels for each storey's walls, openings
and furniture. Check one upper-floor wall's actual lower bound; a shared zero can silently
extend it through the floor below. Keep floor-specific visibility addressable, including
proxies, so selecting a ground-floor plan cannot display upstairs furniture.

## Plan, route and review views

Start with the plan's scale, external envelope, wall thicknesses and occupied levels.
Distinguish gross footprint from clear room area. A furniture photograph can guide a
composition but does not establish room dimensions. Name the intended connections between
entrance, circulation and rooms; build their physical openings as part of the shell.

Keep the first saved plan/volume view small enough to review before furnishing the whole
layout. At the actual output aspect ratio, fit the complete required footprint with a margin.
A top view through lintels can make open doorways look solid. Camera clipping only removes
visible surfaces; it does not cap the cut and can make walls disappear when seen edge-on.
For a section plan, use a capped review copy or an explicit filled 2D section at the chosen
height, while preserving the complete editable walls. Distinguish walls intersecting that
plane from lower sills/furniture seen below it. Check that every room boundary and required
opening remains unambiguous in both wall directions; tilting the camera is not by itself a fix.
Choose a perspective that reveals the layout question rather than hiding it behind the facade.
Save its visibility state with the view (for example, a suitable View Layer or review Scene)
so reopening and selecting the view reproduces the image. Keep temporary hiding from becoming
an undocumented prerequisite. The [saved review views](techniques/saved-review-views.md)
card gives a small static scene setup, ownership boundaries and a fresh-render check.
Derived plan geometry is a snapshot: identify its source and
refresh it after layout changes rather than allowing it to drift from the main scene.
Inspect these images before refining room compositions or adding a broad validation suite.

Validate **opening → continuous route → occupied clearance** separately. A ray through a
door proves a gap at that sample, not a usable route for a person. Follow the route from
outside the entrance, across the threshold and furniture immediately behind it, into each
room. Use a stated body/clearance envelope or measured bottleneck widths; a centreline or
an abstract room graph alone does not establish passage. State assumed sizes as project
criteria, not certified building-code compliance. Door leaves may be excluded for an open-door
check, but their swing/use state and furniture remain relevant to the layout.

Choose check geometry for the question: structural opening tests can isolate walls, while
circulation tests include furniture over the needed body height. Do not move a probe above
a low obstruction and call its floor passage clear. If ignoring an object in a ray query,
continue to the next hit or restrict the query set first; a discarded first hit is not proof
that the remaining segment is empty. Recheck the changed connection after a local correction.

## Stairs connect supported routes

Develop the stair and its landing/slab opening as one spatial assembly. Derive rise count
from the floor-to-floor height; distinguish risers from tread surfaces, including the
upper floor as the final support. Measure actual first/last step elevations, tread depth,
clear width and landing connections. Keep the requested clearance envelope and open-edge
protection visible in a section; a plausible profile alone does not prove the connection.

Probe headroom above the actual walking surfaces along the rise, especially at slab edges
and the top transition. Measuring above the bottom floor or printing the generator's
opening height does not establish this. A free space needs both support below and clearance
above; erasing the stair shaft from a 2D obstacle mask cannot prove a walkable 3D route.
Confirm that the probe's current View Layer includes the stair, slab, guards and lintels;
test a known supported point before interpreting misses. A floor-plan layer can exclude
the upper landing even though the render layer shows it. Missing evaluated mesh data is
a query-scope failure: choose the intended structural evaluation set and repeat the same
samples. Silently skipping those objects leaves support and clearance unverified.
Treat a parameter-based plan/BFS as a preliminary check and compare its critical points
with saved evaluated geometry. Include the doorway threshold in the support samples:
a landing can meet the wall outline yet leave a drop at the actual opening.
The [spatial probe](techniques/assembly-fit.md) supplies directional extents and first-hit
rays without another geometry framework; choose objects/visibility and interpret the result
for this route. State sampled limits rather than certifying every position.

## Handoff at the chosen finish

Open the saved plan and section at delivery size: readable openings, correct storey,
dimension endpoints on their measured features, labels inside the frame. Save a useful
active scene/camera as well as alternate review views. A missing cap, an obscured doorway
or an upstairs proxy on the ground plan is unresolved evidence, not a passing layout.

Once layout is supported, develop only the requested [interior composition](interior-compositions.md)
and surface families. Test a representative finish under its review light before spreading
it through the house; distinguish a material sample from an in-context interior check.
