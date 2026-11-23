# Animate a character walking

Choose this guide when successive footfalls carry the character through the shot. For a different source of motion, use [block and review a complete action](techniques/motion-blocking.md) to work out the controls, timing and evidence from the scene.

Decide what the audience should read in the first two footfalls. Give the character a destination and a reason to move. “She is carrying a full cup through a doorway” gives you a gaze target, a hand to steady, and a reason to shorten one step. Act out a few strides or observe a comparable walk. Pick one cadence cue and one pose or attention cue you can recognize in silhouette. [Blender Studio's character walk](https://studio.blender.org/training/animation-fundamentals/5d69afaebdd59b8da08f9f99/)

For a new straight walk on a generated Rigify human, use the [Rigify travel example](techniques/rigify-travel.md) to block a route, review it from the saved file and correct a specific pose or contact.

## Block a whole stride

Choose the path, travel distance and duration at the scene's playback rate. One **step** goes from one footfall to the opposite footfall. One **stride** returns to the same foot. Average step length × steps per second gives average forward speed. For an in-place game cycle, preview with the intended travel speed added back to reveal sliding. A repeating stride needs matching pose and velocity across the seam. For a shot with an entrance or stop, shape the acceleration or braking over the available distance.

Sketch left contact, passing, right contact, the opposite passing pose and the next left contact as **whole figures**. Reuse one posing script for these events. If the rig opens with arms spread, establish the walking silhouette first. In a relaxed pose the elbows hang below the shoulders, with the hands beside the thighs and room to swing. On Rigify, check the active IK/FK mode with one reversible pose. Give forward progression one owner, lay out the landing points in world space, then key the advancing parent before placing the IK feet. Flat, planted IK feet are enough for the first playback. Add roll, toe-off and finer spacing to the saved blockout where they improve the read. [Rigify controls](techniques/rigify-ik-animation.md)

On a clean rig, set the pose and use `control.keyframe_insert(data_path="location", frame=f)` or key the rotation property matching its rotation mode. Blender creates the Action and slot on first keying. On an animated rig, keep the assigned Action and slot. [Keying the owning datablock](animation-workflow.md#use-the-current-animation-data-model)

| Moment | What the whole figure does in an ordinary walk |
| --- | --- |
| Contact | The leading leg reaches ahead while the trailing leg extends behind, its heel usually already raised. Both feet briefly share support. The belt is already advancing. In free walking the arm opposite the leading leg is usually forward. |
| Loading | The receiving knee yields as the body lowers and moves onto that side. The rear foot finishes its push over the forefoot, then the toes leave the ground. The chest and head carry momentum through the exchange. |
| Passing | The body advances over the stance leg as that leg lengthens. The free knee folds and passes the support leg with clearance. Seen from the front, the belt may tip slightly down on the swing side as the supporting hip bears weight. |
| Rise and reach | The pelvis travels through the high part of its arc and the swing leg unfolds toward the next contact. The arms reverse in time with the change of stride. Continue with the other side. |

Treat these as events to find in this performance. In continuous walking the body moves through each exchange. Judge balance from where the body is going, its speed, and when the next base of support arrives. A start can spend time unloading the first foot. A stop needs room for the last leg to absorb speed and the upper body to settle. [Walk blocking demonstration](https://www.animationmentor.com/blog/tutorial-animating-human-walk-cycle/) · [Measured step-to-step dynamics](https://pmc.ncbi.nlm.nih.gov/articles/PMC2726857/)

## Give the walk a point of view

The advancing side of the pelvis can turn with the reaching leg. Let the rib cage and shoulders respond to that turn. The timing and amplitude change with speed. Swing a loose arm from the shoulder and let the elbow and wrist finish the arc a little later where the hand has momentum. Watch the head in world space. It can steady the gaze as the chest moves underneath, or lead a change of attention. A hand carrying something has its own task. [Measurements of upper-body coordination at different walking speeds](https://pubmed.ncbi.nlm.nih.gov/28395170/)

Try two readings of the same distance. Someone slipping past a sleeping dog might glance down, suspend the reaching foot briefly, then lower it gently while the shoulders stay narrow. Someone arriving late might already be looking through the door, cover more ground between footfalls, then check their momentum on recognizing a friend. Place the change on a particular stride. A held look, an uneven interval, or one hand drawing in can communicate the decision before any facial detail. [An animator's breakdown of a sneak](https://www.animationmentor.com/blog/tutorial-animating-sneak-walk-cycle-with-personality/)

**Worked example.** Watch the short greeting at its recorded speed. Notice when the head first turns relative to the chest. The character keeps walking through that decision. The shoulders follow, one arm leaves the walking rhythm to greet, and the final stride shortens into the stop. Use the four stills to compare silhouettes and the movie to judge the time between them. [Greeting playback](../assets/walk-example/greeting.mp4) · [Editable scene](../assets/walk-example/greeting.blend) · [Four poses](../assets/walk-example/greeting-poses.png)

For a timing-only pass on recognition or hesitation during a walk, use [time the look before the response](animation-workflow.md#time-the-look-before-the-response).

## Review and revise quickly

1. **Watch the full figure at delivery speed.** As soon as the body advances over alternating supports, save the assigned Action in the requested `.blend`. Use that first playable version for the next pass on the arms and gaze. View the whole figure in a cheap fixed three-quarter view with a floor mark, controls hidden and hands and feet in frame. Describe where the figure heads, when it takes weight, and what draws its attention. For a travelling shot, compare the belt’s actual world displacement with the planned travel. If the path object advances but the belt stays behind, repair how the character inherits travel. If the intent disappears at thumbnail size, change the silhouette or rhythm.
2. **Choose the view that explains the biggest mismatch.** In profile, watch forward spacing, knee fold and whether the body stalls between feet. From the front, follow the belt toward each support and compare shoulders and wrists against the moving pelvis. A hand travelling through world space can still be glued to the ribs. If the upper body feels stiff, compare the same-side wrist relative to its shoulder in the two opposing contacts. If a foot skates, scrub the first and last actual contact on the deformed heel or ball against the floor mark.
3. **Make one targeted revision and replay the same section.** For stepping in place during a travelling shot, fix propulsion and placements first. For a mechanical rhythm, adjust the spacing into a weight change or the timing of an attention shift. Batch the event poses or sampled frames in one Blender call. Keep the last readable version while trying the change. Stop when the walk reads at speed and the specific defect is gone. Reopen the deliverable and replay its actual range, including the seam or stop. With only still-image tools, make a strip of consecutive poses, check the spacing against their times and report that limit.

For a relaxed walk with moving limbs and a stiff torso, compare the line between the shoulders with the line between the hip joints from above. Follow their angle through opposite contacts. If both lines stay fixed and the acting calls for a looser stride, let the reaching side of the pelvis turn forward and let the opposite shoulder follow the arm. Replay the walk and recheck the planted soles. A character carrying a rigid load may deliberately use less rotation.

For an edit between two supplied endpoint poses, the [single-step review](humanoid-animation.md) checks their preservation and measures a named transfer. For a longer walk, first review both sides together in context.
