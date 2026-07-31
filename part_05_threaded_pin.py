import FreeCAD as App
import Part
import math
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
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_05_threaded_pin.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_05_threaded_pin.stl")

def construct_threaded_pin():
    """
    Constructs a 100% 3D printable M12 thumb screw.
    - Shaft length: FRAME_THICKNESS (20) + crossbar depth (25) - 2 = 43mm.
    - Head: 24mm diameter x 8mm thickness with 12 scalloped knurls.
    - Thread: M12 x 2.5mm coarse thread with THREAD_CLEARANCE (0.6mm).
    """
    # 1. Dimensions
    head_diameter = params.SCREW_HEAD_DIAMETER
    head_radius   = head_diameter / 2.0
    head_thickness = 8.0 * params.SCALE
    
    # Crossbar hole depth is 25mm, frame thickness is FRAME_THICKNESS (20mm).
    shaft_length  = params.FRAME_THICKNESS + 25.0 * params.SCALE - 2.0 * params.SCALE
    
    # Thread parameters
    t_pitch   = params.THREAD_PITCH
    # Shrink male outer radius for clearance
    t_radius  = (params.SCREW_THREAD_DIAMETER / 2.0) - (params.THREAD_CLEARANCE / 2.0)
    t_r_inner = t_radius - (t_pitch * 0.45)
    
    # 2. Build the simple rounded button head
    # We will use a smaller head diameter (16mm) to avoid colliding with the lower leg's 8mm base pad.
    # We can create a domed head by taking a sphere and intersecting it with a cylinder, or just a heavy chamfer.
    head_diameter = 16.0 * params.SCALE
    head_radius = head_diameter / 2.0
    head_thickness = 5.0 * params.SCALE
    
    # Simple cylinder for the head
    head = Part.makeCylinder(head_radius, head_thickness, App.Vector(0, 0, -head_thickness), App.Vector(0, 0, 1))
    
    # Fillet the top edge heavily to make it rounded
    try:
        edges = []
        for edge in head.Edges:
            if abs(edge.BoundBox.ZMin - (-head_thickness)) < 0.1 and abs(edge.BoundBox.ZMax - (-head_thickness)) < 0.1:
                if isinstance(edge.Curve, Part.Circle):
                    edges.append(edge)
        if edges:
            head = head.makeFillet(2.5 * params.SCALE, edges)
    except Exception as e:
        print(f"Warning: Head fillet skipped: {e}")
        
    # Cut a flathead screwdriver slot (2mm wide, 2.5mm deep, across the entire head)
    slot_width = 2.0 * params.SCALE
    slot_depth = 2.5 * params.SCALE
    slot = Part.makeBox(head_diameter + 2.0 * params.SCALE, slot_width, slot_depth, App.Vector(-head_radius - 1.0 * params.SCALE, -slot_width / 2.0, -head_thickness))
    head = head.cut(slot)
        
    # 3. Build the core shaft
    core_shaft = Part.makeCylinder(t_r_inner, shaft_length, App.Vector(0, 0, 0), App.Vector(0, 0, 1))
    
    # 4. Build the sweeping thread (using freecad-threading skill)
    t_helix = Part.makeHelix(t_pitch, shaft_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 2.0 * params.SCALE
    p1 = App.Vector(inner_X,  0, -t_pitch * 0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch * 0.10)
    p3 = App.Vector(t_radius, 0,  t_pitch * 0.10)
    p4 = App.Vector(inner_X,  0,  t_pitch * 0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    
    # 5. Add thread tip chamfer (entry bevel) so it self-guides
    chamfer = Part.makeCone(
        t_radius + 2.0 * params.SCALE, t_r_inner,
        t_pitch / 2.0 + 1.0 * params.SCALE,
        App.Vector(0, 0, shaft_length - t_pitch / 2.0 - 1.0 * params.SCALE)
    )
    end_cutter = Part.makeCylinder(
        t_radius + 5.0 * params.SCALE, t_pitch + 2.0 * params.SCALE,
        App.Vector(0, 0, shaft_length - 1.0 * params.SCALE)
    )
    
    # First cut the chamfer from the end cutter to make a chamfer cutter
    chamfer_cutter = end_cutter.cut(chamfer)
    
    # Cut the core shaft and sweep individually to avoid OpenCASCADE boolean hangs
    t_sweep_cut = t_sweep.cut(chamfer_cutter)
    core_shaft_cut = core_shaft.cut(chamfer_cutter)
    
    # Finally, combine head, cut core, and cut thread into a compound
    final_part = Part.makeCompound([head, core_shaft_cut, t_sweep_cut])

    # Re-orient body to lie along X-axis (rotate +Z to +X) to match crossbars, or leave as Z?
    # Usually pins are left on Z for printing (head on bed).
    # Since head extends from Z=0 to Z=-8, we need to translate +Z by 8 to put head flat on Z=0.
    final_part.translate(App.Vector(0, 0, head_thickness))
    
    # Export clean STEP and STL
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    final_part.exportStep(EXPORT_STEP)
    final_part.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return final_part


def main():
    doc = App.newDocument("ThreadedPin")
    shape = construct_threaded_pin()
    feature = doc.addObject("Part::Feature", "ThreadedPin")
    feature.Shape = shape
    doc.recompute()

main()
