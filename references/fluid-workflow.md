# Liquids, smoke and fire: establish the base solve before detail

Use for coherent liquid surfaces or gas volumes with evolving transport. A shader, point
cloud or composited glow may satisfy an image study; it does not establish fluid behavior.
Start with [simulation decisions](simulation-workflow.md), the relevant pattern and the actual
runtime's Fluid/Mantaflow domain, flow and effector interfaces. A legacy Smoke modifier example
is not a current Fluid API contract.

## Liquid patterns

| Pattern | Setup decisions | First proof and useful controls |
| --- | --- | --- |
| Finite spill or blob impact | Initial liquid Geometry volume, open space/floor or vessel, deliberate initial velocity | Initial volume, fall height, impact/spread and plausible remaining volume |
| Pour or filling vessel | Timed Inflow, closed/thick enough vessel, optional drain/Outflow | Source starts/stops, strikes the intended region, remains contained; rate/area/velocity matter |
| Splash against an object | Low-cost liquid impact and fluid Effector proxy | Displacement around the object and coherent surface before foam/spray refinements |
| Thick liquid | Choose a solver/model with the needed viscosity at physical scale | Flow rate, stretching/settling and time; a slower Time Scale alone does not define viscosity |

Use source construction, gravity, viscosity/surface tension if supported and appropriate,
velocity and boundary conditions to shape behavior. Distinguish a persistent inflow from
an initial volume; hiding its rendered mesh does not necessarily stop emission. Choose the
actual Use Flow/timing controls and verify the emitted state across adjacent frames.

For viscosity, inspect the active model and units. Ordinary Diffusion uses kinematic viscosity
(m²/s), encoded by Base × 10^-Exponent; dynamic viscosity in Pa·s or cP needs a density-aware
conversion. The separate high-viscosity solver's Strength is a different control, not that
same coefficient. Compare transport at matched source, scale and elapsed time before naming
a real substance. See [Diffusion](https://docs.blender.org/manual/id/5.0/physics/fluid/type/domain/liquid/diffusion.html).

## Case: timed pour into a vessel

The creator's [coffee-pour walkthrough](https://blog.cgcookie.com/posts/let-s-make-coffee-blender-fluid-sim-mantaflow-tutorial-for-beginners/)
is a concrete vessel example: fit the domain around the event, use a thick cup effector,
distinguish initial liquid from sustained inflow, mesh the result, then key source shutoff.
Keep these decisions while checking modern interfaces. Its old EEVEE toggles, example
resolutions and suggestion that caching itself ensures stability are not universal settings
or guarantees. Prove containment and the emission tail before polishing a liquid shader.

## Gas patterns

| Pattern | Setup decisions | First proof and useful controls |
| --- | --- | --- |
| Rising smoke plume | Smoke source, density/temperature, buoyancy, domain space and obstacle if needed | Rise, expansion, drift and dissipation without domain clipping |
| Short puff/dust-like gas | Finite/timed emission with deliberate velocity and dissipation | Burst onset, momentum and tail; an endless source is a different effect |
| Small flame or fire with smoke | Fire or Fire+Smoke source, fuel/temperature and combustion settings | Flame extent, smoke production/transport and extinction; volume appearance checked separately |

Fuel, burning rate, buoyancy and vorticity change different aspects of behavior. Do not replace
combustion with a static emissive plume when evolving flame is required. Turbulence/noise can
add small structure after base motion works; a noisy frozen volume is not proof of transport.
Keep light contribution, emission/glow and actual density changes distinguishable.

For a plume around an obstacle, first prove base density/velocity transport with noise off.
Only then add a finer noise stage and compare the same motion. The [solver authors' obstacle
example](https://github.com/tum-pbs/mantaflow/blob/master/scenes/waveletTurbulenceObs.py) separates
base grids, source/obstacle and optional up-resolution; it is a standalone solver example,
not a Blender script to paste. Blender's [gas-noise guide](https://docs.blender.org/manual/id/5.2/physics/fluid/type/domain/gas/noise.html)
also warns that enabling Noise without its baked data can display an empty domain. Diagnose
the missing stage before changing the plume's physics or shader.

## Domain and collision design

Fit the domain around the required motion and clearance. Record dimensions and estimate voxel
size from longest domain dimension divided by resolution divisions. Take that size from the
defining domain box, not the evaluated liquid mesh's changing bounds. Check source thickness,
vessel walls, drains and collision features against that scale. Sub-voxel geometry can vanish;
raising a surface-thickness setting cannot faithfully recover a poorly resolved vessel.
Use simple closed effectors with correct orientation and deliberately modeled walls/bottom.
Inspect openings and actual baked containment, not merely a watertight rendered object.

Set domain type before type-dependent settings and inspect live RNA. Flow must overlap the
working domain; inspect source surface/volume sampling and animated/deforming emission.
Mantaflow effectors need their own Fluid Effector settings; Bullet or classic Collision alone
does not make an obstacle. Choose wall/open boundary behavior intentionally. Gas may need
clearance/adaptive-domain settings so smoke is not chopped at the bounds; a liquid must have
the intended open top or domain walls and any drain must remove only the intended region.

For leaks, first inspect collision representation, normals, wall/source sampling, voxel size
and object motion per time step. For unstable or missing flow, check source timing, overlap,
domain state and required history. Use adaptive time stepping/CFL and timestep bounds as
appropriate to the runtime; blindly maximizing all steps and resolution wastes bake time.
Changing resolution can change behavior and detail, so the preview bake is not the final bake.

## Cache dependencies and render representation

Fluid uses its own bake operators. **Replay** is useful for iterative playback, **Modular**
separates base data from dependent mesh/noise/secondary stages, and **All** bakes enabled stages
together. Inspect available controls and intended frame range. Use an owned cache directory
per domain/variant and verify which files/stages were written. Do not confuse a generated
standalone Mantaflow script with the cache or with a working Blender scene.

Check the prerequisites for separate stages before the base bake. In the tested 5.2 Modular
route, **Resumable** stores extra data required for later mesh/particles/noise jobs; the installed
UI explicitly guards those jobs. Calling an operator directly can bypass that UI protection
and finish with empty output. Changing the checkbox after baking cannot supply missing base
fields: retain the useful result and rebuild the necessary stages from the source in an owned
cache. Verify nonempty fields/geometry, not just stage flags or file existence.

For liquids, base data/particles are not the rendered liquid surface. Enable and bake the
required mesh after base data, then inspect topology/smoothing and thin drops. Foam/spray/
bubbles require their own enabled/baked secondary stage and render representation. For gas,
high-resolution noise depends on base data. Rebuild downstream stages when base source,
collision, resolution or timing changes; material-only changes usually do not require a solve.
Use render-level collider/source geometry when estimating cost: hidden heavy subdivision can
affect a fluid bake. Preserve a useful low-cost bake before starting an expensive replacement.

Review a noise-off base view and a noise-on baked view at the same frame. Noise should add
structure while retaining the intended broad motion; it is not a substitute for sufficient
base resolution. The view toggle and the required auxiliary cache data are different concerns.

Shade a liquid mesh with the requested optical response and scene lighting; transparent glass
cannot rescue a wrong liquid surface. For gas, inspect actual grid names and connect density,
temperature/flame or other supported fields to the volume shader. A default domain material
or solid box is not proof that the density/fire grids render. Check transmission/refraction
or volume-step support and light contribution in the intended engine, plus compositing if used.

For a first gas material, inspecting the installed Quick Smoke setup can be cheaper than
inventing a graph. Decide whether native volume attributes or explicit Volume Info/remapping
supplies a channel. Raw heat, normalized temperature and Kelvin are different meanings; inspect
the current renderer's contract before scaling or combining them. Keep artistic flame-display
gain explicit. If fields evolve correctly but the volume is invisible or overbright, compare
a known working volume material before changing the solve.

## Verify the saved cache rather than regenerate it silently

Review initial state, first contact, peak motion and tail, with consecutive frames at the
critical event. Check volume loss/leaks where relevant, temporal surface/grid changes and
rendered appearance. After a useful bake, save and reopen in a fresh process; seek several
baked frames out of order and read actual mesh bounds/vertices or nonzero volume grids.
A domain object being present and a bake flag being true are insufficient.

For a finite liquid, compare the known source volume with initial and later occupied volume,
allowing for intended inflow/outflow. A closed surface mesh can be inflated by particle radius
or smoothing while the underlying solve has a different error. Where feasible inspect the
liquid level set/particles as a separate diagnostic; voxel estimates are approximate, but
several-fold unexplained growth is not a passing conservation result. Check obstacle interior
and domain-boundary influence as well as visible diversion. Correcting mesh thickness alone
does not repair the solve. Choose an earlier unaffected comparison or enlarge/rebake the
domain when boundaries contaminate the motion; do not certify later free spreading from it.

For handoff, include the cache directories needed for mesh/data/noise/particles or a tested
alternative such as sampled mesh/volume files. Packing textures does not pack a Mantaflow
directory. Keep relative-path meaning and the owning blend clear. Exported OpenVDB grids or
animated meshes still require a receiver test; they do not retain the editable simulation.
State whether the result is a coarse behavior template, a render-ready shot or an export test.

Sources: [Flow types and behavior](https://docs.blender.org/manual/id/5.2/physics/fluid/type/flow.html),
[domain settings and base/dependent stages](https://docs.blender.org/manual/ka/5.2/physics/fluid/type/domain/settings.html),
[cache modes and formats](https://docs.blender.org/manual/vi/5.2/physics/fluid/type/domain/cache.html),
[liquid meshing](https://docs.blender.org/manual/es/5.2/physics/fluid/type/domain/liquid/mesh.html),
and [effector thickness](https://docs.blender.org/manual/de/4.0/physics/fluid/type/effector.html).
Use older effector documentation for the concept, then verify the current build's interface.
