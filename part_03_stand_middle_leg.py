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
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_03_stand_middle_leg.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_03_stand_middle_leg.stl")


def construct_middle_leg():
    """
    Constructs part_03_stand_middle_leg (Z=125mm to Z=250mm).
    Features female mortise sockets matching part_02 tenons, middle S-curve riser,
    middle crossbar mounting boss (13mm M12 clearance bore), middle tray cradle arms,
    and top male tenon alignment pegs.
    """
    thickness  = params.FRAME_THICKNESS       # 20mm
    h_start    = 125.0 * params.SCALE
    h_end      = 250.0 * params.SCALE
    leg_height = h_end - h_start              # 125mm
    bore_r     = (params.SCREW_THREAD_DIAMETER / 2.0) + (0.5 * params.SCALE) # 6.5mm (13mm bore)

    # 1. Main Middle Riser Body - Curved backward
    outer_cyl = Part.makeCylinder(params.R_BACK, thickness, App.Vector(0, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    inner_cyl = Part.makeCylinder(params.R_FRONT, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    curved_ring = outer_cyl.cut(inner_cyl)
    
    bbox = Part.makeBox(thickness + 4.0 * params.SCALE, 100.0 * params.SCALE, leg_height, App.Vector(-2.0 * params.SCALE, -80.0 * params.SCALE, h_start))
    riser = curved_ring.common(bbox)
    try:
        r_edges = [e for e in riser.Edges if e.Length > (leg_height - 5.0 * params.SCALE)]
        if r_edges:
            riser = riser.makeFillet(2.0 * params.SCALE, r_edges)
    except Exception:
        pass
    leg_body = riser

    # 2. Horizontal Cradle Arm for Medium Tray with upward curved tip
    start_z = 125.0 * params.SCALE
    start_y = params.get_leg_y_at_z(start_z) - 10.0 * params.SCALE
    center_y = 125.0 * params.SCALE
    length_straight = center_y - start_y
    bend_radius = 25.0 * params.SCALE
    arm_thickness_z = 16.0 * params.SCALE

    straight_arm = Part.makeBox(thickness, length_straight, arm_thickness_z, App.Vector(0, start_y, start_z))

    # Curved upward tip using a quarter cylinder (pipe)
    center_z = start_z + bend_radius
    outer_cyl = Part.makeCylinder(bend_radius, thickness, App.Vector(0, center_y, center_z), App.Vector(1, 0, 0))
    inner_cyl = Part.makeCylinder(bend_radius - arm_thickness_z, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, center_y, center_z), App.Vector(1, 0, 0))
    ring = outer_cyl.cut(inner_cyl)
    
    # Isolate the bottom-right quadrant of the ring
    bbox = Part.makeBox(thickness + 4.0 * params.SCALE, bend_radius + 5.0 * params.SCALE, bend_radius, App.Vector(-2.0 * params.SCALE, center_y, start_z))
    curved_tip = ring.common(bbox)

    # Add a spherical or cylindrical cap to make the tip rounded
    cap_radius = arm_thickness_z / 2.0
    cap_y = center_y + bend_radius - cap_radius
    cap = Part.makeCylinder(cap_radius, thickness, App.Vector(0, cap_y, center_z), App.Vector(1, 0, 0))

    cradle_arm = straight_arm.fuse(curved_tip).fuse(cap)
    leg_body = leg_body.fuse(cradle_arm)

    # 3. Middle Crossbar Mounting Boss (13mm M12 Clearance Bore) just above arm
    cb_z = 155.0 * params.SCALE
    cb_y = params.get_leg_y_at_z(cb_z)
    cyl = Part.makeCylinder(bore_r, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, cb_y, cb_z), App.Vector(1, 0, 0))
    leg_body = leg_body.cut(cyl)

    # 4. Bottom Female Mortise Sockets at Z=125mm
    clr = params.FIT_CLEARANCE
    m_w = (8.0 * params.SCALE) + clr
    m_d = (12.0 * params.SCALE) + clr
    m_h = (10.0 * params.SCALE) + (0.5 * params.SCALE)

    bot_y = params.get_leg_y_at_z(h_start)
    mortise1 = Part.makeBox(m_w, m_d, m_h, App.Vector(6.0 * params.SCALE - clr/2.0, bot_y - 10.0 * params.SCALE - clr/2.0, h_start - 0.1 * params.SCALE))
    mortise2 = Part.makeBox(m_w, m_d, m_h, App.Vector(6.0 * params.SCALE - clr/2.0, bot_y + 10.0 * params.SCALE - clr/2.0, h_start - 0.1 * params.SCALE))

    leg_body = leg_body.cut(mortise1).cut(mortise2)

    # 5. Top Male Tenon Alignment Pegs at Z=250mm for joining part_04
    tenon_w = 8.0 * params.SCALE
    tenon_d = 12.0 * params.SCALE
    tenon_h = 10.0 * params.SCALE

    top_y = params.get_leg_y_at_z(h_end)
    tenon1 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, top_y - 10.0 * params.SCALE, h_end))
    tenon2 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, top_y + 10.0 * params.SCALE, h_end))

    leg_body = leg_body.fuse(tenon1).fuse(tenon2).removeSplitter()

    # 6. Apply smooth 1.5mm chamfer to vertical wall edges
    try:
        c_edges = []
        for edge in leg_body.Edges:
            if isinstance(edge.Curve, Part.LineSegment):
                p1, p2 = edge.Vertexes[0].Point, edge.Vertexes[-1].Point
                if abs(p1.z - p2.z) > 10.0 * params.SCALE and p1.z > (h_start + 5.0 * params.SCALE) and p2.z > (h_start + 5.0 * params.SCALE) and p1.z < (h_end - 5.0 * params.SCALE) and p2.z < (h_end - 5.0 * params.SCALE):
                    c_edges.append(edge)
        if c_edges:
            leg_body = leg_body.makeChamfer(1.5 * params.SCALE, c_edges)
    except Exception as e:
        print(f"Notice: Middle leg chamfer fallback: {e}")

    # Export clean STEP and STL
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    leg_body.exportStep(EXPORT_STEP)
    leg_body.exportStl(EXPORT_STL)
    print(f"Exported to {EXPORT_STEP} and {EXPORT_STL}")
    return leg_body


def main():
    doc = App.newDocument("MiddleLeg")
    shape = construct_middle_leg()
    feature = doc.addObject("Part::Feature", "MiddleLeg")
    feature.Shape = shape
    doc.recompute()

main()
