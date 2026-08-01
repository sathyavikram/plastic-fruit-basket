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
import dovetail
importlib.reload(dovetail)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_01_stand_lower.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_01_stand_lower.stl")


def construct_lower_stand():
    """
    Constructs part_01_stand_lower (Z=0 to Z=125mm).
    Base stand tier featuring wide-stance foot base with integrated flared feet,
    recessed rubber pad pockets, extended upward-curving cradle arms with top-surface 
    precision 60-degree dovetail slots, and top male tenon alignment pegs.
    """
    thickness = params.FRAME_THICKNESS       # 20mm
    depth     = params.TOTAL_BASE_DEPTH      # 160mm
    height    = 125.0 * params.SCALE

    # 1. Main Base Bar
    center_y = depth - 10.0 * params.SCALE
    base_bar_raw = Part.makeBox(thickness, center_y + 100.0 * params.SCALE, 25.0 * params.SCALE, App.Vector(0, -100.0 * params.SCALE, 0))
    outer_cyl_full_base = Part.makeCylinder(params.R_BACK, thickness, App.Vector(0, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    base_bar = base_bar_raw.common(outer_cyl_full_base)

    try:
        b_edges = []
        for e in base_bar.Edges:
            if hasattr(e, "Vertexes") and len(e.Vertexes) >= 2:
                p1, p2 = e.Vertexes[0].Point, e.Vertexes[-1].Point
                if abs(p1.z - 25.0 * params.SCALE) < 0.1 and abs(p2.z - 25.0 * params.SCALE) < 0.1 and e.Length > 20.0 * params.SCALE:
                    b_edges.append(e)
        if b_edges:
            base_bar = base_bar.makeFillet(2.0 * params.SCALE, b_edges)
    except Exception:
        pass

    # 2. Flared Base Feet
    foot_front = Part.makeBox(thickness + 6.0 * params.SCALE, 45.0 * params.SCALE, 6.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, -10.0 * params.SCALE, 0))
    foot_rear  = Part.makeBox(thickness + 6.0 * params.SCALE, 45.0 * params.SCALE, 6.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, 120.0 * params.SCALE, 0))

    def fillet_foot(solid_foot):
        edges = []
        for edge in solid_foot.Edges:
            if abs(edge.BoundBox.ZMin - 6.0 * params.SCALE) < 0.1 and abs(edge.BoundBox.ZMax - 6.0 * params.SCALE) < 0.1:
                edges.append(edge)
        if edges:
            try:
                return solid_foot.makeFillet(2.0 * params.SCALE, edges)
            except Exception:
                pass
        return solid_foot

    foot_front = fillet_foot(foot_front)
    foot_rear  = fillet_foot(foot_rear)

    flare_back_box = Part.makeBox(thickness + 6.0 * params.SCALE, 23.6 * params.SCALE, 20.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, -15.0 * params.SCALE, 0))
    flare_back_cyl = Part.makeCylinder(24.0 * params.SCALE, thickness + 6.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, -15.0 * params.SCALE, 24.0 * params.SCALE), App.Vector(1, 0, 0))
    flare_back     = flare_back_box.cut(flare_back_cyl)

    flare_front_box = Part.makeBox(thickness + 6.0 * params.SCALE, 20.0 * params.SCALE, 6.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, 164.0 * params.SCALE, 0))
    flare_front_cyl = Part.makeCylinder(29.0 * params.SCALE, thickness + 6.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, 184.0 * params.SCALE, 29.0 * params.SCALE), App.Vector(1, 0, 0))
    flare_front     = flare_front_box.cut(flare_front_cyl)

    leg_body = base_bar.fuse(foot_front).fuse(flare_back).fuse(foot_rear).fuse(flare_front)

    # 3. Recessed Bumper Pockets
    pocket_front = Part.makeBox(15.0 * params.SCALE, 15.0 * params.SCALE, 1.0 * params.SCALE, App.Vector(2.5 * params.SCALE, 12.5 * params.SCALE, 0))
    pocket_rear  = Part.makeBox(15.0 * params.SCALE, 15.0 * params.SCALE, 1.0 * params.SCALE, App.Vector(2.5 * params.SCALE, depth - 27.5 * params.SCALE, 0))
    leg_body = leg_body.cut(pocket_front).cut(pocket_rear)

    # 4. Vertical Riser Frame
    outer_cyl = Part.makeCylinder(params.R_BACK, thickness, App.Vector(0, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    inner_cyl = Part.makeCylinder(params.R_FRONT, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    curved_ring = outer_cyl.cut(inner_cyl)
    
    bbox  = Part.makeBox(thickness + 4.0 * params.SCALE, 160.0 * params.SCALE, height, App.Vector(-2.0 * params.SCALE, -80.0 * params.SCALE, 0.0))
    riser = curved_ring.common(bbox)
    
    try:
        r_edges = [e for e in riser.Edges if e.Length > (height - 5.0 * params.SCALE)]
        if r_edges:
            riser = riser.makeFillet(2.0 * params.SCALE, r_edges)
    except Exception:
        pass

    # 5. Extended Upward-Curving Cradle Arm
    hook_center_z = 40.0 * params.SCALE
    hook_r_out    = 40.0 * params.SCALE
    hook_r_in     = 15.0 * params.SCALE
    
    outer_cyl  = Part.makeCylinder(hook_r_out, thickness, App.Vector(0, center_y, hook_center_z), App.Vector(1, 0, 0))
    inner_cyl  = Part.makeCylinder(hook_r_in, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, center_y, hook_center_z), App.Vector(1, 0, 0))
    ring       = outer_cyl.cut(inner_cyl)
    bbox_hook  = Part.makeBox(thickness + 4.0 * params.SCALE, hook_r_out + 10.0 * params.SCALE, hook_center_z, App.Vector(-2.0 * params.SCALE, center_y, 0))
    curved_tip = ring.common(bbox_hook)

    cap_radius = (hook_r_out - hook_r_in) / 2.0
    cap_y      = center_y + hook_r_in + cap_radius
    cap        = Part.makeCylinder(cap_radius, thickness, App.Vector(0, cap_y, hook_center_z), App.Vector(1, 0, 0))

    leg_body = base_bar.fuse(foot_front).fuse(foot_rear).fuse(riser).fuse(curved_tip).fuse(cap).cut(pocket_front).cut(pocket_rear)

    # 6. Top-Surface Dovetail Slots on Cradle Arm (Multiple Snap-Fit Slots)
    slot_tool = dovetail.make_top_dovetail_slot()
    
    # 3 Cradle Arm Top Surface Slots along the upward arm profile (Y=60, Y=90, Y=120)
    center_z_base = 25.0 * params.SCALE
    for y_pos in (60.0 * params.SCALE, 90.0 * params.SCALE, 120.0 * params.SCALE):
        # Calculate top surface Z height at y_pos
        slot = slot_tool.copy()
        slot.translate(App.Vector(0, y_pos, center_z_base))
        leg_body = leg_body.cut(slot)

    # 7. Top Male Alignment Tenon Peg at Z=125mm
    tenon_size = 10.0 * params.SCALE
    top_y      = params.get_leg_y_at_z(height)
    tenon      = Part.makeBox(tenon_size, tenon_size, tenon_size, 
                              App.Vector((thickness - tenon_size) / 2.0, top_y - (tenon_size / 2.0), height))

    leg_body = leg_body.fuse(tenon).removeSplitter()

    return leg_body


def main():
    doc = App.newDocument("LowerStand")
    shape = construct_lower_stand()
    feature = doc.addObject("Part::Feature", "LowerStand")
    feature.Shape = shape
    doc.recompute()

    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)
    shape.exportStep(EXPORT_STEP)
    shape.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")

if __name__ == "__main__" or sys.argv[-1] == os.path.basename(__file__):
    main()
