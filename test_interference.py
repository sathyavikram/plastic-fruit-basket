import FreeCAD as App
import Part
import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

import part_01_crossbar
import part_05_threaded_pin

def build_test():
    doc = App.newDocument("TestInterference")
    
    shape_crossbar = part_01_crossbar.construct_crossbar()
    feature_cb = doc.addObject("Part::Feature", "Crossbar")
    feature_cb.Shape = shape_crossbar
    
    shape_pin = part_05_threaded_pin.construct_threaded_pin()
    
    # Position pin exactly as in assembly.py for left side, Front Base crossbar (Y=25, Z=15)
    # The crossbar itself is just placed at origin in this test (or we can translate it)
    # Let's just place them relative to each other as they would be in the assembly.
    # In assembly, crossbar is at: X=frame_thick, Y=25, Z=15. But wait, part_01_crossbar.py generates it at X=0 to 170.
    # In assembly, crossbar is translated by: X=frame_thick (20).
    # The pin is translated by X=0, rotated 90 deg around Y.
    # So relative to crossbar, the pin is at X=-20.
    
    pin_r = shape_pin.copy()
    pin_r.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
    pin_r.translate(App.Vector(-params.FRAME_THICKNESS, 0, 0))
    
    feature_pin = doc.addObject("Part::Feature", "Pin")
    feature_pin.Shape = pin_r
    
    doc.recompute()
    return doc

if __name__ == "__main__":
    build_test()
