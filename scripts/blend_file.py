"""Save and reopen a Blender scene at the caller's requested output path."""
import math
from pathlib import Path
import shutil
import tempfile

import bpy


def _check_motion(sample):
    name, index, first, second = sample
    if type(index) is not int or index < 0:
        raise ValueError("motion_sample requires a nonnegative vertex index")
    if type(first) is not int or type(second) is not int or first == second:
        raise ValueError("motion_sample requires two distinct integer frames")
    scene = bpy.context.scene
    frame, subframe = scene.frame_current, scene.frame_subframe
    positions = []
    try:
        for at in (first, second):
            scene.frame_set(at)
            mesh = scene.objects.get(name)
            if mesh is None or mesh.type != 'MESH':
                raise ValueError(f"Expected a mesh named {name!r} in the current scene")
            evaluated = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
            vertices = evaluated.data.vertices
            if index >= len(vertices):
                raise ValueError(f"Mesh {name!r} has no evaluated vertex {index} at frame {at}")
            positions.append(evaluated.matrix_world @ vertices[index].co)
    finally:
        scene.frame_set(frame, subframe=subframe)
    distance = (positions[1] - positions[0]).length
    if not math.isfinite(distance) or distance <= 1e-5:
        raise ValueError(f"Motion check failed: {name!r} vertex {index} moved {distance:.6g} "
                         f"world units between frames {first} and {second} (need > 1e-5)")


def _save_and_open(target):
    saved = bpy.ops.wm.save_as_mainfile(filepath=str(target))
    if "FINISHED" not in saved:
        raise RuntimeError(f"Save failed for {target}: {saved}")
    opened = bpy.ops.wm.open_mainfile(filepath=str(target))
    if "FINISHED" not in opened:
        raise RuntimeError(f"Open failed for {target}: {opened}")

    actual = bpy.data.filepath
    if not actual or Path(actual).resolve() != target.resolve():
        raise RuntimeError(f"Opened {actual!r}, expected {str(target)!r}")
    return actual


def save_and_reopen(output_path, *, motion_sample=None):
    """Return the reopened file path. Optional (mesh name, evaluated vertex index,
    frame A, frame B) must move over 1e-5 world units before and after saving.
    Choose a mesh with stable vertex indices between the sampled frames.
    """
    target = Path(output_path)
    if not target.is_absolute() or target.suffix.lower() != ".blend":
        raise ValueError(f"Expected an absolute .blend output path, got {output_path!r}")
    if motion_sample is None:
        target.parent.mkdir(parents=True, exist_ok=True)
        return _save_and_open(target)

    _check_motion(motion_sample)
    target.parent.mkdir(parents=True, exist_ok=True)
    # A dependency that moves in memory may be unavailable after loading from disk.
    with tempfile.TemporaryDirectory(dir=target.parent) as directory:
        backup = Path(directory) / "previous.blend"
        if target.exists():
            shutil.copy2(target, backup)
        try:
            actual = _save_and_open(target)
            _check_motion(motion_sample)
        except Exception as exc:
            if backup.exists():
                backup.replace(target)
                outcome = "Restored the previous file on disk."
            else:
                target.unlink(missing_ok=True)
                outcome = "Discarded the failed output file."
            raise RuntimeError(f"{exc}. {outcome} The active scene may differ from disk.") from exc
    return actual
