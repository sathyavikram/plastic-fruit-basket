import FreeCAD as App
import Part
import Import
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
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_01_crossbar.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_01_crossbar.stl")


def create_female_thread_cutter(t_radius, t_pitch, depth):
    """
    Creates a female thread cutter along the Z-axis (Z=0 to Z=depth)
    using the freecad-threading skill pattern.
    """
    t_r_inner = t_radius - (t_pitch * 0.45)
    t_helix = Part.makeHelix(t_pitch, depth, t_r_inner, 0)

    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)

    # Core bore cylinder slightly longer to clean entry/exit faces
    t_core = Part.makeCylinder(t_r_inner, depth + 2.0, App.Vector(0, 0, -1.0))

    # Lead-in entry chamfer cone (1.5mm chamfer for self-guiding thread engagement)
    chamfer_depth = 1.5 * params.SCALE
    lead_in = Part.makeCone(t_radius + chamfer_depth, t_radius, chamfer_depth, App.Vector(0, 0, -0.5))

    thread_cutter = t_core.fuse(t_sweep).fuse(lead_in).removeSplitter()
    return thread_cutter


def construct_crossbar():
    """
    Constructs a 24mm OD x 170mm L cylindrical crossbar spanning the X-axis
    with M16 x 3.5mm female thread sockets cut 25mm deep into both ends.
    """
    r_outer = (params.CROSSBAR_DIAMETER / 2.0)
    length  = params.CROSSBAR_LENGTH
    t_radius = (params.SCREW_THREAD_DIAMETER / 2.0)
    t_pitch  = params.THREAD_PITCH
    depth    = 25.0 * params.SCALE

    # Main cylindrical rod along Z axis
    main_cyl = Part.makeCylinder(r_outer, length)

    # Apply 1.5mm outer end chamfers before thread cutting
    chamfer_len = 1.5 * params.SCALE
    try:
        edges_to_chamfer = []
        for edge in main_cyl.Edges:
            if isinstance(edge.Curve, Part.Circle):
                edges_to_chamfer.append(edge)
        if edges_to_chamfer:
            main_cyl = main_cyl.makeChamfer(chamfer_len, edges_to_chamfer)
    except Exception as e:
        print(f"Warning: Outer chamfer skipped: {e}")

    # Build internal female thread cutters
    cutter_left  = create_female_thread_cutter(t_radius, t_pitch, depth)
    cutter_right = create_female_thread_cutter(t_radius, t_pitch, depth)

    # Position right cutter at Z = length, pointing inward (-Z)
    cutter_right.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), 180)
    cutter_right.translate(App.Vector(0, 0, length))

    # Perform thread cuts
    body = main_cyl.cut(cutter_left).cut(cutter_right).removeSplitter()

    # Re-orient body to lie along X-axis (rotate +Z to +X)
    body.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)

    # Export clean STEP and STL
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    body.exportStep(EXPORT_STEP)
    body.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return body


def main():
    doc = App.newDocument("Crossbar")
    shape = construct_crossbar()
    feature = doc.addObject("Part::Feature", "Crossbar")
    feature.Shape = shape
    doc.recompute()

main()

