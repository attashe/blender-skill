# Graphical blink from one property

**Use:** an existing graphical closure/ShapeKey. Inputs: shape key, Object with a numeric 0..1
control, timing. The mechanism does not create eyelids; the shape and withdrawing highlights
must already make visual sense.

**Small implementation:** [motion.py](../../scripts/techniques/motion.py):

```python
motion.drive_from_property(key, 'value', control, 'blink')
motion.property_keys(control, 'blink', [(1,0), (11,0), (13,1), (15,0), (61,0)], cycle='REPEAT')
```

Reuse an existing valid driver rather than adding another; occupied channels are rejected.
Rig pose and blink Actions can have distinct owners/slots: preserve both during saving/retiming.

**First proof:** test 0, partial and full closure, including head motion. Read the evaluated
shape and inspect eyes/highlights in the shot. Count closure intervals as events, not closed
frames. Verify timing against the gesture and reopen the saved file. The source Momo blink
demonstrates graphical closure, not an anatomical facial rig.

[Recipe](../recipes/character-gesture.md) · [Evidence](provenance.md)
