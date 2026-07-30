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
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_04_stand_upper_leg.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_04_stand_upper_leg.stl")


def construct_upper_leg():
    """
    Constructs part_04_stand_upper_leg (Z=250mm to Z=375mm).
    Features female mortise sockets matching part_03 tenons, top crossbar mounting boss
    (13mm M12 clearance bore), top cradle arms, and tapered crown termination.
    """
    thickness  = params.FRAME_THICKNESS       # 20mm
    h_start    = 250.0 * params.SCALE
    h_end      = 375.0 * params.SCALE
    leg_height = h_end - h_start              # 125mm
    bore_r     = (params.SCREW_THREAD_DIAMETER / 2.0) + (0.5 * params.SCALE) # 6.5mm (13mm bore)

    # 1. Main Upper Riser Body (starts at Z=250mm up to 375mm)
    riser = Part.makeBox(thickness, 35.0 * params.SCALE, leg_height, App.Vector(0, 45.0 * params.SCALE, h_start))
    leg_body = riser

    # 2. Upper Cradle Arms for Small Bowl (TRAY_SMALL) at Z=300mm
    cradle = Part.makeBox(thickness, 50.0 * params.SCALE, 16.0 * params.SCALE, App.Vector(0, 70.0 * params.SCALE, 300.0 * params.SCALE))
    cradle.rotate(App.Vector(0, 70.0 * params.SCALE, 300.0 * params.SCALE), App.Vector(1, 0, 0), -25.0)
    leg_body = leg_body.fuse(cradle)

    # 3. Top Crossbar Mounting Boss (13mm M12 Clearance Bore) at Y=62mm, Z=320mm
    cyl = Part.makeCylinder(bore_r, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, 62.0 * params.SCALE, 320.0 * params.SCALE), App.Vector(1, 0, 0))
    leg_body = leg_body.cut(cyl)

    # 4. Bottom Female Mortise Sockets at Z=250mm (matching part_03 tenons + 0.4mm FIT_CLEARANCE)
    clr = params.FIT_CLEARANCE
    m_w = (8.0 * params.SCALE) + clr
    m_d = (12.0 * params.SCALE) + clr
    m_h = (10.0 * params.SCALE) + (0.5 * params.SCALE)

    mortise1 = Part.makeBox(m_w, m_d, m_h, App.Vector(6.0 * params.SCALE - clr/2.0, 45.0 * params.SCALE - clr/2.0, h_start - 0.1 * params.SCALE))
    mortise2 = Part.makeBox(m_w, m_d, m_h, App.Vector(6.0 * params.SCALE - clr/2.0, 65.0 * params.SCALE - clr/2.0, h_start - 0.1 * params.SCALE))

    leg_body = leg_body.cut(mortise1).cut(mortise2).removeSplitter()

    # 5. Apply smooth 2.0mm fillets to outer edges for organic rounded aesthetics
    try:
        fillet_edges = []
        for edge in leg_body.Edges:
            if isinstance(edge.Curve, Part.LineSegment):
                p1, p2 = edge.Vertex1.Point, edge.Vertex2.Point
                if edge.Length >= 12.0 * params.SCALE and p1.Z > h_start and p2.Z > h_start:
                    fillet_edges.append(edge)
        if fillet_edges:
            leg_body = leg_body.makeFillet(2.0 * params.SCALE, fillet_edges)
    except Exception as e:
        print(f"Notice: Upper leg fillet fallback: {e}")

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
    doc = App.newDocument("UpperLeg")
    shape = construct_upper_leg()
    feature = doc.addObject("Part::Feature", "UpperLeg")
    feature.Shape = shape
    doc.recompute()

main()
