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
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_06_slat_straight.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_06_slat_straight.stl")


def make_female_thread_socket(screw_dia, pitch, thread_len, wall_thick):
    """Generates an M12 female thread socket cutter."""
    major_r = screw_dia / 2.0
    minor_r = major_r - (0.54127 * pitch)
    
    # Outer solid cylinder housing
    outer_r = major_r + wall_thick
    socket_housing = Part.makeCylinder(outer_r, thread_len)
    
    # Thread cutter
    if os.environ.get("SIMPLIFIED_THREADS") == "1" or getattr(params, "SIMPLIFIED_THREADS", False):
        bore_r = major_r - (0.3 * pitch)
        cutter = Part.makeCylinder(bore_r, thread_len + 2.0, App.Vector(0, 0, -1.0))
    else:
        turns = (thread_len / pitch) + 1.0
        helix = Part.makeHelix(pitch, thread_len + pitch, major_r, 0)
        
        # 60 degree internal thread tooth profile
        p1 = App.Vector(minor_r, 0, -0.25 * pitch)
        p2 = App.Vector(major_r + 0.2 * pitch, 0, 0.4 * pitch)
        p3 = App.Vector(minor_r, 0, 0.65 * pitch)
        tooth_wire = Part.Wire([Part.makeLine(p1, p2), Part.makeLine(p2, p3), Part.makeLine(p3, p1)])
        tooth_face = Part.Face(tooth_wire)
        
        make_pipe = Part.Wire([tooth_wire])
        sweeper = Part.BRepOffsetAPI.MakePipeShell(helix)
        sweeper.add(tooth_wire)
        sweeper.build()
        thread_solid = Part.Solid(sweeper.shape())
        
        core_bore = Part.makeCylinder(minor_r, thread_len + 2.0, App.Vector(0, 0, -1.0))
        cutter = core_bore.fuse(thread_solid)

    return socket_housing.cut(cutter)


def construct_straight_slat(is_threaded=False):
    """
    Constructs part_06_slat_straight.
    Straight center slat bar for the slatted fruit basket floor.
    If is_threaded=True, adds M12 female thread sockets to both ends for M12 thumb screw attachment.
    """
    span       = params.SLAT_SPAN           # 170mm
    diameter   = params.SLAT_DIAMETER       # 10mm
    tab_len    = params.SLAT_TAB_LENGTH     # 15mm
    clearance  = params.FIT_CLEARANCE       # 0.4mm
    screw_dia  = params.SCREW_THREAD_DIAMETER # 12mm
    pitch      = params.THREAD_PITCH          # 2.5mm
    
    radius = diameter / 2.0
    tab_radius = (screw_dia / 2.0 + 2.0 * params.SCALE) if is_threaded else (radius - clearance)
    
    # 1. Main Center Cylinder
    center_bar = Part.makeCylinder(radius, span, App.Vector(-span / 2.0, 0, 0), App.Vector(1, 0, 0))
    
    # 2. Left End Tab / Socket
    left_tab = Part.makeCylinder(tab_radius, tab_len, App.Vector(-span / 2.0 - tab_len, 0, 0), App.Vector(1, 0, 0))
    
    # 3. Right End Tab / Socket
    right_tab = Part.makeCylinder(tab_radius, tab_len, App.Vector(span / 2.0, 0, 0), App.Vector(1, 0, 0))
    
    slat = center_bar.fuse([left_tab, right_tab]).removeSplitter()
    
    # 4. If threaded, cut M12 female thread sockets into both ends
    if is_threaded:
        bore_r = (screw_dia / 2.0) - (0.3 * pitch)
        cut_l = Part.makeCylinder(bore_r, tab_len + 2.0 * params.SCALE, App.Vector(-span / 2.0 - tab_len - 1.0 * params.SCALE, 0, 0), App.Vector(1, 0, 0))
        cut_r = Part.makeCylinder(bore_r, tab_len + 2.0 * params.SCALE, App.Vector(span / 2.0 + tab_len + 1.0 * params.SCALE, 0, 0), App.Vector(-1, 0, 0))
        slat = slat.cut(cut_l).cut(cut_r)
        
    return slat


def main():
    doc = App.newDocument("SlatStraight")
    shape = construct_straight_slat(is_threaded=False)
    feat = doc.addObject("Part::Feature", "StraightSlat")
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
