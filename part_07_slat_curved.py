import FreeCAD as App
import Part
import os
import sys
import math

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_07_slat_curved.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_07_slat_curved.stl")


def construct_curved_slat():
    """
    Constructs part_07_slat_curved.
    Curved side slat bar that forms the basket floor and upward-curving side walls.
    Keyed end tabs extend along the X-axis to drop into cradle arm comb slots.
    """
    span      = params.SLAT_SPAN           # 170mm
    diameter  = params.SLAT_DIAMETER       # 10mm
    tab_len   = params.SLAT_TAB_LENGTH     # 15mm
    clearance = params.FIT_CLEARANCE       # 0.4mm
    radius    = diameter / 2.0
    tab_r     = radius - clearance
    
    # Dimensions of the curved U-profile
    basket_depth = 120.0 * params.SCALE   # 120mm total depth front-to-back
    bend_r       = params.SLAT_CURVE_RADIUS # 35mm bend radius
    upward_h     = 45.0 * params.SCALE     # 45mm total height of side lip
    
    # --- 1. Create the 3D Spine Wire in Y-Z Plane (at X = 0) ---
    # Straight bottom segment along Y
    p_start = App.Vector(0, -(basket_depth/2.0 - bend_r), 0)
    p_end   = App.Vector(0, +(basket_depth/2.0 - bend_r), 0)
    line_bottom = Part.makeLine(p_start, p_end)
    
    # Front upward arc (Y > 0)
    center_front = App.Vector(0, basket_depth/2.0 - bend_r, bend_r)
    arc_front = Part.makeCircle(bend_r, center_front, App.Vector(1, 0, 0), -90, 0)
    
    # Back upward arc (Y < 0)
    center_back = App.Vector(0, -(basket_depth/2.0 - bend_r), bend_r)
    arc_back = Part.makeCircle(bend_r, center_back, App.Vector(1, 0, 0), 180, 270)
    
    # Wire compound
    spine_wire = Part.Wire([arc_back, line_bottom, arc_front])
    
    # --- 2. Pipe Sweep Circular Section Along Spine ---
    circle_sec = Part.makeCircle(radius, p_start, App.Vector(0, 1, 0))
    circle_wire = Part.Wire(circle_sec)
    
    # Sweep along spine
    make_pipe = Part.Wire([circle_wire])
    sweeper = Part.BRepOffsetAPI.MakePipeShell(spine_wire)
    sweeper.add(circle_wire)
    sweeper.build()
    curved_body = Part.Solid(sweeper.shape()).removeSplitter()
    
    # --- 3. Create Left & Right Keyed End Tabs ---
    # Place mounting tabs at the base level X = -span/2 to +span/2
    left_tab = Part.makeCylinder(tab_r, tab_len, App.Vector(-span / 2.0 - tab_len, 0, 0), App.Vector(1, 0, 0))
    right_tab = Part.makeCylinder(tab_r, tab_len, App.Vector(span / 2.0, 0, 0), App.Vector(1, 0, 0))
    
    # Also add center span bar (X = -span/2 to +span/2) to connect the left and right cradle arms
    center_span = Part.makeCylinder(radius, span, App.Vector(-span / 2.0, 0, 0), App.Vector(1, 0, 0))
    
    slat = curved_body.fuse([center_span, left_tab, right_tab]).removeSplitter()
    
    # Tip chamfers for clean drop-in insertion
    try:
        chamf_edges = []
        for e in slat.Edges:
            if hasattr(e, "Curve") and isinstance(e.Curve, Part.Circle):
                c = e.Curve.Center
                if abs(abs(c.x) - (span / 2.0 + tab_len)) < 0.5:
                    chamf_edges.append(e)
        if chamf_edges:
            slat = slat.makeChamfer(0.8 * params.SCALE, chamf_edges)
    except Exception as ex:
        print(f"Warning: Curved slat chamfer failed: {ex}")
        
    return slat


def main():
    doc = App.newDocument("SlatCurved")
    shape = construct_curved_slat()
    feat = doc.addObject("Part::Feature", "CurvedSlat")
    feat.Shape = shape
    doc.recompute()

    os.makedirs(EXPORT_BASE, exist_ok=True)
    for p in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(p):
            os.remove(p)

    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Successfully exported {EXPORT_STEP} and {EXPORT_STL}")


if __name__ == "__main__" or sys.argv[-1] == os.path.basename(__file__):
    main()
