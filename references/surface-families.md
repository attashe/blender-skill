# Reuse material knowledge without repeating a generic look

Use for frequently encountered surfaces or a scene with several related materials. Read only
the relevant family. These are starting decisions and verification views, not universal node
recipes or fixed parameter values. Use [shader nodes](shader-nodes-workflow.md) for wiring and
[material composition](material-composition.md) for optical layers and mixing.
For natural stone, first use [rock recipes](rock-recipes.md) to establish shape, geological
structure and weathering; a concrete shader or stronger generic noise is not a rock-form recipe.

## A short route from identity to a reusable material

Identify **substance + manufacture/finish + condition + viewing scale** from the reference:
for example, sawn timber with worn varnish, molded matte plastic, or dusty cast concrete.
"Brown box" identifies neither its construction nor its surface. If ambiguous, inspect another
view/detail or record an assumption; do not spread a guessed material through the assembly.

Name the few cues that must survive the target view: end grain, broad polished reflections,
aggregate, folded edges, or thin-region scattering. Choose the cheapest source that can supply
those cues: a suitable existing material/scan, a controlled procedural field, directed painting,
or a hybrid. Search/review available assets when distinctive structure would be costly to invent;
keep licensing, physical size and actual renderer support explicit. A library is an option, not
a download quota. Do not spend the whole task shopping for a match.

Prove a family on a representative part, including a relevant edge, cut, joint or thickness.
Separate the reusable response from local condition masks. Reuse the proven base with consistent
mapping; vary finish, coverage and local history intentionally. Expose only meaningful controls,
such as feature size/direction, roughness bounds, relief scale or coating coverage. A single
"grunge amount" that changes every channel identically conceals the decisions.

Keep the validated group/material and a small preview with its coordinate/unit assumptions,
source dependencies and tested engine/version in the project's existing asset library or blend.
Save an asset only when reuse justifies it. A new task can adapt this base instead of rebuilding
an untested graph. Confirm the changed part in its scene before distributing it to all users.

## Family starting points

| Family and identifying cues | Efficient starting route | Decisive check / common wrong shortcut |
| --- | --- | --- |
| **Wood:** cut/grain direction, board boundaries, face versus end grain; raw, painted, oiled or varnished finish | Use the [board-grain route](techniques/wood-grain-frame.md): suitable maps/scan or a directional model in each board's frame; provide an end-grain treatment where exposed. Add finish as its own response, and knots/splits only where the reference warrants them. | Inspect a rotated board, its end and a grazing highlight. Grain should follow the part without identical knots repeated on every plank. Stretched Noise may suggest fibers but does not by itself establish sawn wood or coherent end grain. |
| **Plastic:** molded shape, surface finish, seams, grip/polish zones; opaque or transmitting | Use the [molded finish route](techniques/molded-plastic-finish.md) for opaque satin parts, starting with a dielectric response and the observed finish. Add fine mold texture or local abrasion at the required scale; use transmission/volume only when the particular plastic needs it. Geometry owns thick edges, ribs and seams. | Move a broad highlight across an unworn area and a handled area. Avoid stone-like pores, arbitrary metallic response and uniform scratches. A smooth plastic may need almost no base-color noise; paint over plastic is distinct from the plastic substrate. |
| **Coated upholstery / leatherette:** shallow emboss, flexible covering, top finish, seams and padding | Use [embossed upholstery](techniques/embossed-upholstery.md): a suitable map or bounded cellular height source, separate pigment/relief/coating. | Compare relief off/on, grain spacing and coat independently. Avoid skin SSS, velvet sheen or darkening every valley by category alone. A procedural cellular field is not arbitrary natural leather. |
| **Ceramic tile and grout:** manufactured size, bond pattern, glazed face, edge and recessed joint | Establish wall/floor mapping axes and physical tile/joint dimensions. A procedural pattern, maps or repeated geometry can supply the layout; choose geometry where the edge/parallax needs it. Separate glazed ceramic response from grout, even when they share a coverage mask. | Inspect one full tile/joint and a grazing reflection on the installed surface. Check pattern orientation and physical size before expanding it. A Brick Texture alone does not establish glaze, recessed grout or correct placement against the wall; uniform glossy roughness across both loses the material distinction. |
| **Concrete, mortar, paving:** cast/troweled surface, aggregate, pores, joints, repairs and traffic/weather history | Establish the actual finish first. A suitable scanned/tileable base with directed repair/dirt masks is often efficient; procedural fields work when they reproduce the chosen features. Use local geometry/displacement for visible broken edges or depressions. | Review diffuse color, a grazing highlight and one damaged region. Polished/sealed concrete differs from rough cast concrete. Cracks and spalling are not raised dark threads; dust, exposed aggregate and recesses need different channel responses. |
| **Metal:** alloy/finish, manufacturing direction, exposed metal versus paint/oxide/dirt | Use an appropriate metal response for exposed substrate, a directional tangent for brushed finish when visible, and separate covering regions. Reuse coverage across channels while retaining each substance's response. | Move/rotate a light or object: brushing changes highlight direction; coated regions should not inherit bare-metal behavior. Color noise and a high Metallic value do not establish machined metal. |
| **Human skin:** regional coloration, specular/oily zones, pores/folds and thin versus thick regions | For close human work, use suitable calibrated/painted skin sources or a validated skin base; keep surface reflection and subsurface response distinct. Relate scattering length and pore scale to the mesh, then adapt regional masks and subject appearance. | Inspect front/side/back light on useful thin/thick geometry, plus a reflection change. Uniform peach color with strong SSS tends to hide structure; a pore noise sphere does not validate a face. A distant figure may need far less detail. Do not invent one universal skin color, pore distribution or SSS preset. |
| **Paper/cardboard and packaging:** sheet/fold structure, exposed cut/torn edges, print, tape and compression | Use a restrained paper base plus purposeful print/tape/soil regions. Model folds/flaps and exposed corrugation only where they read; map graphics to the assembled faces. Select material from construction, not the generic word "box". | Check an open or damaged edge and a folded corner. Brown noisy cuboids miss the sheet construction. Tape is a different finish; a printed label cannot repair implausible fold geometry. |

For leaf surfaces and plant structure, use [vegetation](vegetation-workflow.md). Optical
glass/fabric/wet-film cases stay in [material composition](material-composition.md).

## Roughness and defects need specific roles

Roughness controls reflection shape; height/normal detail describes resolved surface slopes;
geometry controls depth, edge shape and contact. Let the reference decide which carries a cue.
A smooth albedo with a correct highlight can look more textured than a high-contrast noisy
albedo. A surface with no identifying cues is still unfinished even after ugly noise is removed.

For a defect, choose its footprint, depth/sign, boundary and exposed substance before a tool.
A fine distant crack may be a mask/normal/decal; an opening with visible sides or parallax
needs displacement or geometry. A curve can author the path or a cutting/mask source rather
than become a raised tube. Inspect its relationship to the undamaged surface and a low view.
Use marks where a cause explains them: loading/contact, drainage, assembly seams or repairs.
Avoid independent uniform randomness for every chip, stain and scratch.

Test one characteristic response and one relevant local condition before expanding coverage.
If an iteration merely trades cloudy noise for a featureless surface, return to the missing
cue/source choice rather than calling either endpoint finished. Keep the controlled comparisons
in [surface look development](texture-authoring-workflow.md#prove-the-surface-before-spreading-it).

The [Principled manual](https://docs.blender.org/manual/fr/5.2/render/shader_nodes/shader/principled.html)
defines the reflection, coat and scattering controls; use the installed engine's actual interface.
[Adobe's material structure guidance](https://experienceleague.adobe.com/en/docs/substance-3d/general-knowledge/openpbr/openpbr-overview#best-practices-for-material-creation)
supports matching structure and reference behavior, not a required OpenPBR implementation.
[Wood grain observations](https://www.wood-database.com/wood-articles/what-is-wood/) distinguish
the cut and grain planes. [Poly Haven's texture standards](https://docs.polyhaven.com/en/technical-standards/textures)
illustrate recorded physical size and reflection evidence; their publication resolutions and
map requirements are not mandatory settings for this skill.
