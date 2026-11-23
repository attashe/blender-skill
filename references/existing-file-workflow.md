# Make a bounded change to an existing file

Use when editing a supplied scene/asset, including a known example. Its familiar filename,
preview or checksum does not establish what the current Blender process has loaded.

## Establish the working scene before diagnosing it

For a file-based job, load the intended file, then verify `bpy.data.filepath` and the required
object/control names. The [scoped API probe](api-diagnostics.md) can perform this check and
inspect a named Object/PoseBone without writing an inventory script. It rejects a startup
scene when a different file is expected. In CLI use, the input and `--python-exit-code` must
precede the executed script; see [execution order](blender-methods.md#scripted-execution-and-inspection).
A checksum establishes file bytes, not that a preceding script inspected those bytes.

For an already open or unsaved session, identify the intended scene/session and relevant
objects through the connector before editing. Preserve the user's work; do not load a file
over unsaved work merely to satisfy a file-based probe.

If the expected rig/mesh seems absent, first check loaded-file/scene identity. Once identity
is confirmed, inspect the relevant names, collection visibility or linked ownership. Report
an absent asset only with evidence from that verified scene. A screenshot of the startup
cube is evidence about the startup scene, not the supplied file.

## Inspect the dependency that will change

Start from the relevant object, PoseBone, node group or modifier and its actual owner.
For animation, check its local space, parent/constraints, assigned channels and drivers;
for a surface edit, its source geometry and affected stack. Expand inspection when a concrete
dependency explains an unexpected result. Materials, every bone and every data-block are
not prerequisites for changing one known control.

Once target names are known, compose the bundled [API](api-diagnostics.md),
[mesh](techniques/mesh-orientation.md) or [spatial](techniques/assembly-fit.md) measurements
when they answer the question. Write the task-specific expected relation around the returned
values; a repair script need not grow its own topology/clearance library. A short name lookup
or a genuinely different check can still be custom.

Choose an operation through the [technique modules](technique-index.md). An interface card
can identify a source asset's controls; a full historical builder is only needed when
investigating a specific integration dependency. Keep the current asset's shape and style
unless the task calls for changes to them.

For imported library components, the [snapshot route](techniques/native-snapshot-ownership.md#measure-the-imported-transform-after-scene-evaluation)
explains scene linking/evaluation before world-space measurements and the load context's
returned datablocks. Reusing an asset does not require executing its historical builder.

## Change, evaluate, save

Work in a copy or the authorized current scene. Change one meaningful sample and check its
evaluated effect: a head angle must produce the intended gesture; a modifier value must
change the intended surface. Save that editable checkpoint before broad reporting or extra
render variants. Preserve unrelated channels and dependencies.

Reopen the actual output and compare the changed sample with the starting state. A successful
save, a zero exit code or a structurally valid JSON report does not establish preservation or
the requested behavior. Distinguish inability to inspect, confirmed missing content, and an
edit that failed. Keep a diagnostic failure from being reported as a defect in the user's file.

## Relative image paths on save

`//` resolves against the currently loaded blend, not the intended future destination.
When adding an image for a relocated copy, keep its path absolute through the first Save As;
then set `image.filepath = bpy.path.relpath(absolute_path)` against the new blend and save again
if relative delivery is wanted. Blender's default path remapping can otherwise preserve a
premature relative path against the old file's directory. Do not disable remapping globally
without accounting for the existing dependencies.

If a saved comp produces an empty image/matte or no expected file outputs, first check
`bpy.path.abspath(image.filepath)`, file existence, loaded image size and selected layer.
Reload/reopen the actual dependency before diagnosing the graph. This does not imply that
every absent output is a path error; it gives one cheap discriminating check for a moved file.
