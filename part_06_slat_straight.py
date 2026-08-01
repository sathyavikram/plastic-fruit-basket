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


def construct_straight_slat():
    """
    Constructs part_06_slat_straight.
    Straight center slat bar for the slatted fruit basket floor.
    Spans X = -SLAT_SPAN/2 to +SLAT_SPAN/2 with keyed end tabs for drop-in slots.
    """
    span       = params.SLAT_SPAN           # 170mm
    diameter   = params.SLAT_DIAMETER       # 10mm
    tab_len    = params.SLAT_TAB_LENGTH     # 15mm
    clearance  = params.FIT_CLEARANCE       # 0.4mm
    
    radius = diameter / 2.0
    tab_radius = radius - clearance         # 4.6mm (9.2mm diameter tab for 10mm slot)
    
    # 1. Main Center Cylinder (spanning between side frames)
    center_bar = Part.makeCylinder(radius, span, App.Vector(-span / 2.0, 0, 0), App.Vector(1, 0, 0))
    
    # 2. Left Keyed End Tab (X < -span/2)
    left_tab = Part.makeCylinder(tab_radius, tab_len, App.Vector(-span / 2.0 - tab_len, 0, 0), App.Vector(1, 0, 0))
    
    # 3. Right Keyed End Tab (X > +span/2)
    right_tab = Part.makeCylinder(tab_radius, tab_len, App.Vector(span / 2.0, 0, 0), App.Vector(1, 0, 0))
    
    # Fuse components into single monolithic slat
    slat = center_bar.fuse([left_tab, right_tab]).removeSplitter()
    
    # Apply chamfers to tip edges for smooth entry into comb slots
    try:
        chamf_edges = []
        for e in slat.Edges:
            if hasattr(e, "Curve") and isinstance(e.Curve, Part.Circle):
                center = e.Curve.Center
                if abs(abs(center.x) - (span / 2.0 + tab_len)) < 0.5:
                    chamf_edges.append(e)
        if chamf_edges:
            slat = slat.makeChamfer(0.8 * params.SCALE, chamf_edges)
    except Exception as ex:
        print(f"Warning: Slat tip chamfer failed: {ex}")
        
    return slat


def main():
    doc = App.newDocument("SlatStraight")
    shape = construct_straight_slat()
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
