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

    # 1. Main Middle Riser Body (starts at Z=125mm)
    riser = Part.makeBox(thickness, 40.0 * params.SCALE, leg_height, App.Vector(0, 40.0 * params.SCALE, h_start))
    try:
        r_edges = [e for e in riser.Edges if e.Length >= 40.0 * params.SCALE]
        riser = riser.makeFillet(2.0 * params.SCALE, r_edges)
    except Exception:
        pass
    leg_body = riser

    # 2. Middle Cradle Arms for Medium Bowl (TRAY_MEDIUM) at Z=180mm
    cradle_base = Part.makeBox(thickness, 55.0 * params.SCALE, 16.0 * params.SCALE, App.Vector(0, 40.0 * params.SCALE, 175.0 * params.SCALE))
    cradle_base.rotate(App.Vector(0, 40.0 * params.SCALE, 175.0 * params.SCALE), App.Vector(1, 0, 0), 25.0)

    # Front retaining lip stop at front tip of cradle arm
    lip = Part.makeBox(thickness, 14.0 * params.SCALE, 20.0 * params.SCALE, App.Vector(0, 85.0 * params.SCALE, 195.0 * params.SCALE))

    cradle_arm = cradle_base.fuse(lip)
    leg_body = leg_body.fuse(cradle_arm)

    # 3. Middle Crossbar Mounting Boss (13mm M12 Clearance Bore) at Y=60mm, Z=185mm
    cyl = Part.makeCylinder(bore_r, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, 60.0 * params.SCALE, 185.0 * params.SCALE), App.Vector(1, 0, 0))
    leg_body = leg_body.cut(cyl)

    # 4. Bottom Female Mortise Sockets at Z=125mm (matching part_02 tenons + 0.4mm FIT_CLEARANCE)
    clr = params.FIT_CLEARANCE
    m_w = (8.0 * params.SCALE) + clr
    m_d = (12.0 * params.SCALE) + clr
    m_h = (10.0 * params.SCALE) + (0.5 * params.SCALE)

    mortise1 = Part.makeBox(m_w, m_d, m_h, App.Vector(6.0 * params.SCALE - clr/2.0, 35.0 * params.SCALE - clr/2.0, h_start - 0.1 * params.SCALE))
    mortise2 = Part.makeBox(m_w, m_d, m_h, App.Vector(6.0 * params.SCALE - clr/2.0, 55.0 * params.SCALE - clr/2.0, h_start - 0.1 * params.SCALE))

    leg_body = leg_body.cut(mortise1).cut(mortise2)

    # 5. Top Male Tenon Alignment Pegs at Z=250mm for joining part_04
    tenon_w = 8.0 * params.SCALE
    tenon_d = 12.0 * params.SCALE
    tenon_h = 10.0 * params.SCALE

    tenon1 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, 45.0 * params.SCALE, h_end))
    tenon2 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, 65.0 * params.SCALE, h_end))

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
