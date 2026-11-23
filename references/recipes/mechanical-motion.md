# Recipe: an editable moving assembly

Establish moving/fixed groups, real axes, initial contacts, time units and explanatory view.

- For an unfinished drilled component, prove [opening/bevel](../techniques/cut-bevel.md)
  before binding motion; motion-only work need not reconstruct geometry.
- For a shaft, use [constant rotation](../techniques/constant-rotation.md) on its real pivot.
- For thread following, use [one pitch-coupled control](../techniques/pitch-coupling.md).
- For exploded views, choose part order/spacing; distinguish illustration from disengagement.
- Check each changed relation, then the complete saved assembly and target images.

The [motor interface](../examples/motor-motion.md) supplies optional integration context;
the techniques do not require its names or all-four-nuts demonstration controller.

## A steadily rotating shaft

**Purpose:** show a rotating component while the housing, bearings and mounting hardware remain
fixed. Establish the real axis/pivot and a clear moving-part hierarchy. Include dependent
cutters, keys and attached parts; rotating a shaft while its Boolean cutter remains in the
housing can change its shape instead of carrying the keyway around.

For constant angular speed, use time in seconds: `theta = theta0 + 2*pi*(rpm/60)*t`, with
`t = (frame-start)/fps` for a frame-driven setup. Linear angular keys or an equivalent analytic
control can implement this. Keep full turns unwrapped; 0 and 360 degrees share a pose but are
different values on a continuous rotation curve. Repeat with Offset can continue that slope;
an ordinary repeated angle curve may introduce a numerical wrap at the seam.

Verify intermediate angles, angular speed, stationary parts and invariant shaft/cutter
relationships after reopening. Use an existing asymmetric feature such as the keyway to read
rotation. A symmetric cylinder can appear stationary. Choose a diagnostic speed deliberately;
high RPM at low frame rates can alias or appear to reverse. A slow demonstration is not proof
of a realistic operating speed or production motion blur.

## A nut following its thread

**Purpose:** demonstrate a coupled relationship rather than independently keyed translation
and rotation. For pitch `p`, axial travel is `p*theta/(2*pi)` in a specified positive thread
axis; handedness determines the sign. Drive both from one turns control and preserve the seated
offset. Translate along that axis, not a convenient unrelated world direction.

Check the actual mating surfaces, not only the control values. The source needs a continuous
helical thread, lead-in/clearance and room for the nut and washers. Sample fractional turns,
contact changes and radial clearance over the intended travel. One millimeter per turn in
the example is its authored pitch, not a universal fastener setting or a manufacturing tolerance.

## An exploded mounting assembly

**Purpose:** explain part order and fit. Group bolt, washers and nut by the joint they belong
to; define assembled offsets and outward travel in a consistent local frame. One spread
control can keep the view editable while timing determines when parts separate, hold and return.
Check framing, occlusion and clear spacing at the exploded pose as well as seating at zero.

An illustrative exploded view may separate parts directly. If the brief asks for realistic
unscrewing, first couple rotation and pitch until threads disengage, then allow free travel.
Do not present abstract axial separation as a physical assembly simulation or invent unseen
motor internals merely to fill an exploded shot.
