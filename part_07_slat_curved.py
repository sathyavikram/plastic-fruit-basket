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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_07_slat_curved.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_07_slat_curved.stl")


def construct_curved_slat(is_threaded=False):
    """
    Constructs part_07_slat_curved.
    Curved side slat bar that forms the basket floor and upward-curving side walls.
    If is_threaded=True, adds M12 female thread sockets to both ends for M12 thumb screw attachment.
    """
    span      = params.SLAT_SPAN           # 170mm
    diameter  = params.SLAT_DIAMETER       # 10mm
    tab_len   = params.SLAT_TAB_LENGTH     # 15mm
    clearance = params.FIT_CLEARANCE       # 0.4mm
    screw_dia = params.SCREW_THREAD_DIAMETER # 12mm
    pitch     = params.THREAD_PITCH          # 2.5mm
    
    radius    = diameter / 2.0
    tab_r     = (screw_dia / 2.0 + 2.0 * params.SCALE) if is_threaded else (radius - clearance)
    
    # Dimensions of the curved U-profile
    basket_depth = 120.0 * params.SCALE
    bend_r       = params.SLAT_CURVE_RADIUS
    
    # --- 1. Spine Wire in Y-Z Plane ---
    p_start = App.Vector(0, -(basket_depth/2.0 - bend_r), 0)
    p_end   = App.Vector(0, +(basket_depth/2.0 - bend_r), 0)
    line_bottom = Part.makeLine(p_start, p_end)
    
    center_front = App.Vector(0, basket_depth/2.0 - bend_r, bend_r)
    arc_front = Part.makeCircle(bend_r, center_front, App.Vector(1, 0, 0), -90, 0)
    
    center_back = App.Vector(0, -(basket_depth/2.0 - bend_r), bend_r)
    arc_back = Part.makeCircle(bend_r, center_back, App.Vector(1, 0, 0), 180, 270)
    
    spine_wire = Part.Wire([arc_back, line_bottom, arc_front])
    
    # --- 2. Pipe Sweep ---
    circle_sec = Part.makeCircle(radius, p_start, App.Vector(0, 1, 0))
    circle_wire = Part.Wire(circle_sec)
    
    make_pipe = Part.Wire([circle_wire])
    sweeper = Part.BRepOffsetAPI.MakePipeShell(spine_wire)
    sweeper.add(circle_wire)
    sweeper.build()
    curved_body = Part.Solid(sweeper.shape()).removeSplitter()
    
    # --- 3. End Tabs / Sockets ---
    left_tab = Part.makeCylinder(tab_r, tab_len, App.Vector(-span / 2.0 - tab_len, 0, 0), App.Vector(1, 0, 0))
    right_tab = Part.makeCylinder(tab_r, tab_len, App.Vector(span / 2.0, 0, 0), App.Vector(1, 0, 0))
    center_span = Part.makeCylinder(radius, span, App.Vector(-span / 2.0, 0, 0), App.Vector(1, 0, 0))
    
    slat = curved_body.fuse([center_span, left_tab, right_tab]).removeSplitter()
    
    # 4. If threaded, cut M12 female thread sockets
    if is_threaded:
        bore_r = (screw_dia / 2.0) - (0.3 * pitch)
        cut_l = Part.makeCylinder(bore_r, tab_len + 2.0 * params.SCALE, App.Vector(-span / 2.0 - tab_len - 1.0 * params.SCALE, 0, 0), App.Vector(1, 0, 0))
        cut_r = Part.makeCylinder(bore_r, tab_len + 2.0 * params.SCALE, App.Vector(span / 2.0 + tab_len + 1.0 * params.SCALE, 0, 0), App.Vector(-1, 0, 0))
        slat = slat.cut(cut_l).cut(cut_r)
        
    return slat


def main():
    doc = App.newDocument("SlatCurved")
    shape = construct_curved_slat(is_threaded=False)
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
