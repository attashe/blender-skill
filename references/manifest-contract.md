# File-based manifest and publication checks

## Scope of this implementation profile

Read this when the project uses the bundled `asset-manifest.json` and Python checker. This
profile deliberately requires one source file per asset node, meters/Z-up, typed dependency
levels and hash-bound evidence. Those are checker constraints, not universal requirements
for Blender projects. Use an existing project contract when it already serves the work;
do not force a multi-collection single-file project into an incompatible schema.

Once adopted, retain these checks throughout the work. Do not omit a failed check or switch
tracking methods to call an unverified asset complete. The checker scripts and schema are
unchanged by the broader production workflow. References, artistic decisions and stage notes
live in the project brief/review record; the checker does not validate them automatically.

### Working sequence within this profile

1. Map every required object/system to nodes and observable acceptance checks. Review the
   original request for omissions; the checker cannot discover missing semantic requirements.
   Include visual checks tied to inspected references when appearance matters. Record actual
   observed differences and justified design choices, not merely "matches reference."
2. Validate the plan before detailed production. Use `next` to identify ready source work;
   mark work `building`. Model in an isolated source/session or a controlled extraction copy.
3. For generators, declare bounded controls and run `preflight` before evaluation. Clamp the
   actual implementation and measure/test it as described in [procedural geometry](procedural-geometry.md).
4. Save/reopen, audit, inspect images and execute acceptance checks before marking a source
   `verified`. Use a fresh/background Blender where available; state any reopening limitation.
5. Run `gate` before building a consumer-ready parent from its children. Resolve missing files,
   stale hashes or failed checks at their owning source. Keep a parent mainly to references,
   transforms, constraints and assembly controls. Declare intentional owned parent geometry
   through `inline_geometry`; otherwise give it its own source. Inspect fit, clearances,
   requested motion, material consistency and expanded cost, then verify the parent similarly.
6. Test source-update propagation in a controlled checkpoint and re-audit affected consumers.
   For delivery/export of the complete declared graph, run `validate --require-ready` and
   inspect the final target views. Preserve editable sources and make derived exports separately.

Exploratory blockouts and in-progress integration copies may combine unfinished proxies. They
do not carry a `verified` claim and are not consumer-ready parent builds. Keep disposable
experiments outside the deliverable graph, since `--require-ready` checks every declared node.
Stage checks are technical/artistic decisions, not routine requests for user approval.

If the requested deliverable is a study/blockout within a larger planned project, validate
its own saved output and acceptance criteria. Keep future graph nodes planned; do not use
`--require-ready` as a demand to build unrequested final assets or claim it passed for the
whole graph. A study delivered outside the final graph must be clearly identified as such.
For delivery of the complete declared graph, all existing readiness checks still apply.

## Contents

1. [Project structure](#project-structure)
2. [Manifest](#manifest)
3. [Procedural topology contract](#procedural-topology-contract)
4. [Evidence](#evidence)
5. [Parameter and production evidence](#parameter-and-production-evidence)
6. [Commands](#commands)
7. [Audit scope and limits](#audit-scope-and-limits)

## Project structure

Place `asset-manifest.json` at the project root. Reuse existing conventions when present.
Keep editable sources under `assets/parts/`, `assets/assemblies/`, `assets/modules/`, and
`scenes/`. Keep material/texture libraries under `assets/materials/` and `assets/textures/`.
Keep build code under `scripts/parts/`, `scripts/assemblies/`, `scripts/modules/`, and
`scripts/scenes/`. Keep audits/images under `reports/` and derived delivery formats under
`exports/`. These directories are roles, not a requirement to create empty folders.

One owned node has one public collection, for example `AST_reader`, and one source file.
An asset can contain several objects and private subcollections. Repeated occurrences share
the same source. Use `SOCKET_<purpose>` Empties for attachment points; their transforms are
part of the asset contract. Do not include a QA camera/light rig inside an exported asset root.

## Manifest

See `assets/terminal-manifest.json` for a complete small plan. It is intentionally all `planned`.

| Field | Meaning |
| --- | --- |
| `schema_version` | `1` |
| `project.units`, `project.up_axis` | `meters`, `Z` authoring contract; export conversion is separate |
| `project.deliverables` | IDs of requested final nodes; a single prop can be its own deliverable |
| `project.relative_libraries` | Defaults to `true`; checker rejects absolute linked library paths |
| `requirements` | Original requirements mapped to nodes and named, observable acceptance checks |
| `nodes[].id` | Stable lowercase ID |
| `kind` | `part`, `assembly`, `module`, or `scene` |
| `file` | Unique project-relative `.blend` file; no absolute paths, backslashes, or `..` |
| `root_collection` | Unique public collection name |
| `deps` | IDs of required children; acyclic, no dependency on higher levels or a scene |
| `status` | `planned`, `building`, `verified`; the script never updates it automatically |
| `method` | `selected`, `why`, `alternative` strings |
| `contract` | Required descriptive `pivot`; optional `dimensions_m` + `tolerance_m`, `bounds_axes`, and `sockets` names |
| `budget` | Positive integer limits: `max_expanded_triangles`, `max_expanded_vertices`, `max_instances`, `max_evaluated_objects`; at least one for a fixed asset |
| `procedural` | Optional boolean, defaults to `false`; declare `true` for topology-generating parameter families |
| `complexity` | Required with `procedural: true`: bounded topology controls and a conservative model |
| `inline_geometry` | Optional exact object `name` + `reason` entries for intentional owned parent geometry |
| `library_only_reason` | Optional reason for a reusable library asset not reachable from deliverables |
| `evidence` | Current audit, inspected images, and checks; can be `{}` while planned/building |

Each requirement has `id`, `description`, `nodes`, and `acceptance`. An acceptance entry has
`id`, `node`, `description`; its node belongs to that requirement's node list. To preserve an
authorized exclusion, record `excluded_reason` and empty `nodes`/`acceptance`. Do not use this
field as permission to drop requirements. The checker checks declared mappings, not completeness
against an unseen prompt.

Bounds default to positive X/Y/Z extents for a volume. For an intentionally flat profile use
`contract.bounds_axes: ["X", "Y"]`; a line along X can use `["X"]`. Only listed axes must be
positive, all extents must be finite/nonnegative, and at least one axis is required. A profile's
`dimensions_m` can then include zero thickness. An empty zero-extent result still fails. Keep
planarity/orientation checks in its acceptance contract.

`max_evaluated_objects` counts dependency-graph occurrences, including each instance and
non-mesh helpers. It is not a count of distinct source files, objects or mesh datablocks. Plan
enough room for all repeated occurrences plus generator/support objects, or omit this optional
limit until a meaningful one is available. `max_instances` also counts graph occurrences;
instancing saves shared data but does not make occurrences disappear from these counters.

Example requirement:

```json
{
  "id": "display",
  "description": "A replaceable screen with a surrounding frame",
  "nodes": ["panel", "bezel", "display"],
  "acceptance": [
    {"id": "panel_size", "node": "panel", "description": "Panel meets declared dimensions"},
    {"id": "bezel_fit", "node": "display", "description": "Frame encloses screen without covering the visible area"}
  ]
}
```

## Procedural topology contract

For topology generators, require triangle and vertex budgets, plus an instance budget when
the model repeats geometry. Use the unbuilt `assets/cable-node.json` fragment as an example.
`complexity.controls` maps names to integer `{min, value, max}` with `0 <= min <= value <= max`.
These are topology counts; physical shape parameters such as radius or float density belong
in the asset contract, with a derived and enforced count bound where needed.

`complexity.model` describes the actual simple topology or a conservative envelope. Count
fields can be integer literals or the name of a declared control:

| `type` | Fields and assumptions |
| --- | --- |
| `mesh` | `vertices`, `triangles`: constant or control-driven upper envelope for all included operations |
| `sweep` | `path_points`, `profile_points`; optional `path_cyclic`, `profile_cyclic` (default true), `caps` (default false). Simple rings and flat caps; no round caps, junctions or extra modifiers |
| `grid` | `u_points`, `v_points`: evaluated samples of an open quad grid, not NURBS control points |
| `subdivide_quads` | `base_quads`, `levels`: all-quad subdivision only. Vertices use the conservative bound 4 × resulting faces; levels above 16 are rejected before evaluation |
| `repeat` | `count`, nested `geometry` model. Multiplies expanded geometry and conservatively counts nested instance occurrences |
| `join` | Nonempty `geometry` list of models; sums their cost |

Run preflight before evaluation. It checks the maximum against declared budgets without
opening Blender or allocating meshes. It cannot discover undeclared operations or enforce
the graph's inputs. Clamp the real builder and graph; verify counts after evaluation. Add
conservative envelopes and mixed-parameter checks for nonmonotone or coupled generators.

Fixed-asset manifests remain compatible without procedural fields. Do not use that compatibility
to omit a topology generator's declaration. A parent placing a fixed number of verified linked
children can use measured expanded budgets without becoming a parameterized GN family.

## Evidence

After saving and reopening the source, generate an audit JSON. Open the actual image(s) and
write a concrete review of appearance/fit. Run each acceptance check assigned to this node and
record the observed result; include a separate report or measurement when the check warrants it.
Use real SHA-256 hashes, not these placeholders:

```json
{
  "audit": "reports/panel/audit.json",
  "visuals": [
    {
      "file": "reports/panel/front.png",
      "sha256": "SHA256_OF_IMAGE",
      "source_sha256": "SHA256_OF_SAVED_BLEND",
      "audit_sha256": "SHA256_OF_CURRENT_AUDIT_JSON",
      "review": "Opened front and oblique views; bezel shading is smooth, visible screen is unobstructed."
    }
  ],
  "checks": [
    {
      "id": "panel_size",
      "passed": true,
      "source_sha256": "SHA256_OF_SAVED_BLEND",
      "audit_sha256": "SHA256_OF_CURRENT_AUDIT_JSON",
      "observed": "Evaluated dimensions 0.600 × 0.018 × 0.380 m; within 0.001 m tolerance."
    }
  ]
}
```

Do not set `passed` without executing the check. A checker cannot distinguish a truthful
description from an invented one. Use the audit dimensions/budgets for automatic numerical
checks, and actual inspection/behavior scripts for appearance and behavior.

The audit stores the source hash, hashes of loaded library files, and common external resource
hashes. The checker re-hashes them. Editing a child makes the parent audit stale even when the parent `.blend` did not
change. A parent's readiness also requires each child to be verified with its own current
evidence. Reopening/reloading the parent and repeating its affected checks is necessary.
Bind every visual/check entry to the current audit JSON hash (`audit_sha256`); this prevents
accepting old reviews after a new dependency audit. Common external images/fonts/sounds/clips
are hashed. Simulation caches, sequences, UDIM sets and indirect renderer resources need a
specialized audit that enumerates them; do not assume they are covered.

## Parameter and production evidence

Procedural assets also require `evidence.complexity_tests` with project-relative `file` and
`sha256`. The report describes measurements from isolated variants derived from the nominal
source, with its unchanged dependency/resource state. Bind it to that nominal source and audit:

```json
{
  "schema_version": 1,
  "node_id": "cables",
  "source_sha256": "SHA256_OF_NOMINAL_SAVED_BLEND",
  "audit_sha256": "SHA256_OF_CURRENT_NOMINAL_AUDIT",
  "cases": [
    {
      "name": "maximum",
      "actual_controls": {"path_samples": 64, "profile_sides": 8, "cable_count": 12},
      "evaluation_mode": "VIEWPORT",
      "metrics": {"expanded_triangles": 12240, "expanded_vertices": 6144, "instances": 12},
      "errors": [],
      "behavior_passed": true,
      "observed": "EXAMPLE ONLY: replace with actual measured geometry and inspected behavior."
    }
  ]
}
```

This snippet shows the shape, not valid evidence: it omits the required `minimum` and `nominal`
cases, uses placeholder hashes, and contains predicted numbers. Generate all three cases in
Blender. Each must read back the exact control set returned by `control_cases`, record the
actual `VIEWPORT` mode, all budgeted metrics, an empty error list, and inspected behavior.
Use unique case names. Add further cases for domain-specific risks. Reopen the nominal source
after tests; never mark predictions as measured or change the source without regenerating evidence.

The audit reports known viewport/render differences in `render_divergence`. When nonempty,
require `evidence.production_audit`, a project-relative audit generated from an actual `RENDER`
dependency graph. It must identify the same saved source/root, Blender runtime and meter units,
match current library/resource hashes, contain no errors/missing files, and meet every budget.
Its evaluated bounds must be nonempty and satisfy any declared dimension contract.
Procedural parameter reports then also require `render_maximum`, with the maximum readback
control set, actual `RENDER` mode and the same behavior/metric checks.

Obtain a render graph through the host's real render execution (for example a supported render
engine hook). `AUDIT_DEPSGRAPH` can pass it to `audit_blend.py` through `runpy` alongside
`AUDIT_PARAMS`. The script does not create a render graph. `Depsgraph.mode` is readonly; a
viewport audit or a renamed field cannot substitute for a render measurement. Detecting common
differences is not exhaustive; inspect custom drivers and production renderer behavior too.

## Commands

All `pipeline.py` commands are read-only, output JSON, and return exit `0` for success or `1`
for a rejected check. Run with Python 3.10+; no package installation is required.

```bash
python3 <skill>/scripts/pipeline.py validate <project>/asset-manifest.json
python3 <skill>/scripts/pipeline.py next <project>/asset-manifest.json
python3 <skill>/scripts/pipeline.py gate <project>/asset-manifest.json --node display
python3 <skill>/scripts/pipeline.py preflight <project>/asset-manifest.json --node cables
python3 <skill>/scripts/pipeline.py validate <project>/asset-manifest.json --require-ready
```

`validate` accepts a consistent unbuilt plan but rejects any falsely claimed verified node.
`gate` checks the selected parent's children; it does not require the parent to already exist.
`next` lists buildable work including stale nodes. It does not authorize parallel mutation of
one live Blender session. `--require-ready` requires every declared node to be ready.
`preflight` checks declared topology maxima, with optional `--node`; it accepts unbuilt plans
and does not produce Blender measurements or change status.

For enforced execution, the task runner must run `gate` before invoking a consumer-ready
parent builder and stop on a nonzero exit. Run `validate --require-ready` before declaring completion/export.
The script does not intercept MCP calls or make an agent obey these instructions by itself.

Audit a saved source in background Blender:

```bash
blender --background <project>/assets/parts/panel.blend \
  --python <skill>/scripts/audit_blend.py -- \
  --node-id panel --root-collection AST_panel \
  --output <absolute-project-path>/reports/panel/audit.json
```

Add Blender's `--python-exit-code 1` before `--python` when the task runner must detect an
uncaught Python error. After any audit failure, inspect the returned error, fix the cause and
rerun. Do not construct an alternative “success” report by hand.

If using a Blender MCP with a shared filesystem:

```python
import runpy

report = runpy.run_path(
    audit_script_absolute,
    init_globals={"AUDIT_PARAMS": {
        "node_id": "panel",
        "root_collection": "AST_panel",
        "output": report_file_absolute
    }}
)["result"]
print(report)
```

With separate agent and Blender filesystems, send the script's source through the working
execution channel and retrieve the JSON. Do not assume an agent-side path exists on Blender's
machine. Background Blender is preferable for proving save/reopen persistence.

## Audit scope and limits

The script reads the saved source hash, runtime version/units, public root, referenced collection
roots, local geometry ownership, socket positions, library paths/hashes, common external file
existence, and evaluated geometry. It also records expanded vertices/instance occurrences,
the twenty largest geometry contributors, legacy curve/surface settings, and known render
divergence. It does not change modeled data or auto-save.

Keep the asset root in the active scene and the intended geometry enabled in the active View
Layer for audit. The default dependency graph is the active viewport graph. The script records
its actual `evaluation_mode`; an optional host-supplied `AUDIT_DEPSGRAPH` can audit a real render
graph. Render representative production settings separately when their geometry differs.

Bounds are measured from evaluated mesh vertices transformed by each occurrence's matrix,
not by rotating an object's coarse bounding box. This offline audit can cost time and memory
on a dense scene; it is not part of the realtime render loop.

Expanded triangles include evaluated mesh occurrences from collection/GN instances. Unique
evaluated triangles count each evaluated object once; they are not a mesh-datablock memory or
GPU draw-call measurement. Legacy curves/surfaces/fonts and modern curve objects are measured
through evaluated mesh conversion where supported. Unconvertible curve/hair output, volumes,
point clouds/Grease Pencil and sequences/UDIMs require dedicated checks: the general audit fails
explicitly rather than treating them as free. Instance counts include graph instance occurrences;
they are not GPU draw-call counts.

Dependency reference discovery covers linked collection children and collection-instance Empties
inside the public root, recursively. For procedural graphs that reference external collections
solely through sockets/node inputs, add an appropriate graph-aware audit before claiming those
dependencies passed; do not silently drop them from the manifest.

Preserve generated evidence when a call fails. Fix failures at the actual owning source node,
then rebuild/review affected parents. A passing audit is only one part of acceptance.
