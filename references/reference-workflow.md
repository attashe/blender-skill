# Find, inspect, and work from references

Read before creating new forms or establishing a new look. References are working evidence:
they should change modeling decisions and be revisited during review. A folder of unseen
images or a list of search links is not reference analysis.

## Start with the questions the images must answer

Inspect user-provided images, existing boards, concept sheets, and project assets first. Treat
the user's direction as the target; use additional sources to resolve gaps rather than drift
into a different design. A narrow edit can reuse already inspected project references.

For a video-derived storyboard or gray prototype, use the
[bounded video-reference workflow](blockout-camera-light.md#video-reference-to-a-bounded-storyboard).
Keep selected panels, inspected source samples and output animation frames as separate budgets.

Distinguish the roles; one image rarely answers all of them:

| Role | Look for / extract |
| --- | --- |
| Design / identity | Defining silhouette, proportions, shape hierarchy, recognizable features and permitted stylization |
| Construction / scale | Multiple views, joints, section thickness, mechanisms, dimensions or credible scale anchors |
| Surface / material | Material boundaries, finish, roughness variation, grain/pattern scale, plausible wear and manufacturing logic |
| Composition / lighting | Focal hierarchy, framing, value/color relationships, depth, light direction and mood |
| Modular system | Repeated units, rhythm, transitions, corners, terminations and ways repetition is varied |
| Motion / deformation | Joint centers and axes, contact, range, timing, bend/twist shapes and material response; compare multiple poses or actual motion, not a single neutral image |

For an invented subject, combine a design reference with real construction/material analogues
and state the design choices. A generated concept may establish a look, but it is not evidence
of real construction, hidden surfaces, dimensions, or multi-view consistency.

## Search to close a visual gap

When an important construction, surface or lighting decision is unsupported, do a bounded
web/reference search before substituting a generic approximation. A supplied wide screenshot
can establish composition while leaving surface structure unresolved. Keep that image as the
design target; seek a real material/detail analogue to answer the missing question. Already
adequate project references need no redundant search.

Use the tools that are actually available: image search for visual candidates; text search
for original artist breakdowns, manufacturers, collections or asset sources; a connected asset
search for reusable materials/HDRIs. Open useful source pages, then actually view the relevant
image or preview. Page text alone cannot show wear distribution, a highlight or surface scale.
If one viewing route fails, try an accessible original/alternate image or browser view rather
than treating the search snippet as visual evidence. Do not let reference gathering stall
independent work; label any important unresolved feature.

Make the query describe the missing evidence, not just the scene genre:

| Missing evidence | Example query direction | Extract for the scene |
| --- | --- | --- |
| Surface construction and age | painted concrete peeling close-up; powder-coated cabinet worn handle | Layer boundaries, exposed material, wear location and scale |
| Directional reflection | brushed steel grazing light; worn rubber side lighting | Highlight width/direction, roughness changes, relief |
| Light on a receiver | fluorescent corridor light falloff; neon sign reflection dry pavement | Source shape, lit area, shadow transitions and reflection footprint |

Use native-language/local terms, synonyms or a source-domain filter when results are repetitive
or irrelevant. Judge applicability: similar substrate/finish, exposure conditions, useful view
and enough resolution. A dramatic grade or another CG render may support mood but be weak
evidence for physical surface detail. Broader discoveries must not silently replace the brief.

For each retained image, connect one observed feature to a proposed scene change and the view
that will test it. Reopen it during that change. Stop searching when the next decision has
enough evidence; return if the render exposes a new gap. No universal image count is required.

## Inspect pixels and preserve context

Actually open the selected images through an image viewer or a rendered browser/preview.
Search snippets, captions, alt text, filenames and image URLs cannot establish visual facts.
Inspect the full composition and relevant details at sufficient resolution. Prefer a second
view when perspective or occlusion makes an important dimension ambiguous.

Keep the working references accessible as a board, contact sheet, image-editor view, browser
view, or Blender reference images, using what the current tools support. Reopen the relevant
view before each major modeling pass and during comparisons; initial inspection followed by
modeling from memory is insufficient. Never claim a persistent visible board unless it exists.
If reference images are placed in Blender, keep them separate from deliverable geometry and
out of the final render/export.

Use a small reference index in the existing project notes or beside the board. For each selected
reference retain an ID, source URL or local path, creator/source when available, its role,
the features actually observed, the scene decision they informed, and any uncertainty. Keep
local image locations when permitted and useful, otherwise retain the source link and viewing
method. A reference for observation and an asset incorporated into the scene have different
roles; a photographed finish need not be downloaded or projected to be useful. Separate observed facts,
derived estimates, and invented design choices. Record licensing/attribution when an image,
texture or downloaded model will be incorporated or redistributed; viewing a reference does
not establish permission to ship it as an asset.

For incorporating the image itself as texture/projection or reconstructing geometry, use
[reference-derived assets](reference-derived-assets.md). It separates licensed-map reuse,
flat-photo processing, camera projection and multi-view reconstruction by their required evidence.

## Turn observation into modeling decisions

Write a short visual breakdown before detail work:

- Primary masses and silhouette, their relative proportions, and a credible scale anchor.
- Secondary structure: thicknesses, joints, openings, support and attachment relationships.
- Repeated families and their interval, orientation, transitions and likely source boundaries.
- Material regions and which details require geometry versus shading, texture or omission at
  the target viewing distance.
- Unknown or contradictory features and the assumption/test that will resolve each important one.

Use ratios as estimates unless calibrated dimensions are available. Perspective photographs
are not orthographic drawings; a close wide-angle view can distort proportions. For matching a
concept or photo, establish camera framing/perspective before deforming the asset to fit every
pixel. Align scale and views when comparing; do not treat artistic reference images as reliable
measurements. Do not average incompatible variants into an accidental hybrid: select the
intended version or document the deliberate combination.

For a fictional terminal, a useful observation could be: “The side image suggests a sloped
upper housing and a recessed display; rear construction is unseen.” The resulting decisions
are to test that silhouette in the side blockout, measure the display-to-body ratio, and use
a labeled assumption or another reference for the rear. Inventing an exact depth would not
improve the evidence.

## Compare during production

Turn the breakdown into a few visible acceptance cues for this task: positions/ratios of
dominant silhouettes and openings, which forms overlap, a critical contact or pose, and the
major light/value regions. Use image-space landmarks or a rough overlay when helpful; they
are estimates, not a requirement to recover every pixel or hidden dimension. Separate scene
evidence from overlaid UI/annotations and from image effects such as glare or grading.

For an important asymmetric part, check which face is visible before detailing it. Identify
front/side/top from construction cues such as a door, cap, handle or cable entry, then compare
their projected widths, edge directions and overlap with the support. A correctly placed box
with the wrong face toward the camera is still a form mismatch. When the reading is ambiguous,
try simple oriented proxies or seek another view; do not infer an exact rotation from one image.
Compare neighboring forms to distinguish a local orientation error from a camera mismatch.
Resolve the attachment face as well as the viewing angle. After reorienting an assembly,
recheck its fittings, contact and connected routes; endpoint contact alone cannot establish
reference fidelity. In a bounded surfacing/lighting study, record an out-of-scope form mismatch
separately rather than silently treating it as solved by the new look.

At each meaningful comparison, identify the largest remaining mismatch and whether it comes
from camera, geometry/pose, surfacing, light or output treatment. Fix that cause and compare
again before adding detail elsewhere. A declared correction is not evidence that the next
render improved. Inspect both the whole image and relevant crops; choose cues for the current
finish level rather than copying a universal scoring checklist. Technical validity and a
recognizable theme do not by themselves establish the requested reference fidelity.

At blockout, compare silhouette, proportions, negative space, scale and composition. During
asset work, compare secondary forms, construction and material boundaries. During look
development/finaling, compare surface scale, material response, color/value hierarchy and
detail readability under the intended lighting. Use a matched view or side-by-side comparison;
use overlays only when projection and framing make them meaningful.

Record which reference/view was used, the largest visible mismatch, the correction, and the
next inspected result. Deliberate stylization can differ from reference; explain how that
serves the brief. Do not hide proportion errors with extra detail, textures or dramatic light.
For existing matching assets, preserve their established look unless a change is requested.

## When reference access is incomplete

Try another available source or viewing channel. Continue independent layout/technical work
with explicit assumptions where useful. If key visual evidence remains inaccessible, label
that limitation and request the missing material when necessary; keep dependent work at an
exploratory level. Neither an unviewed URL nor an uninspected generated concept can support
a claim of reference fidelity or completed visual validation.
