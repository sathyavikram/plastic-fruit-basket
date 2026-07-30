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
EXPORT_STEP = os.path.join(EXPORT_BASE, "part_02_stand_lower_leg.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "part_02_stand_lower_leg.stl")


def construct_lower_leg():
    """
    Constructs part_02_stand_lower_leg (Z=0 to Z=125mm).
    Wide-stance foot base with integrated flared feet, recessed rubber pad pockets,
    2 crossbar mounting bosses (13mm M12 clearance bores), bottom tray cradle arms,
    and top male tenon alignment pegs.
    """
    thickness = params.FRAME_THICKNESS       # 20mm
    depth     = params.TOTAL_BASE_DEPTH      # 160mm
    height    = 125.0 * params.SCALE
    bore_r    = (params.SCREW_THREAD_DIAMETER / 2.0) + (0.5 * params.SCALE) # 6.5mm (13mm bore)
    boss_r    = (params.CROSSBAR_DIAMETER / 2.0) + (3.0 * params.SCALE)     # 12mm (24mm OD boss)

    # 1. Main Base Bar (horizontal foot along Y-axis: Y=0 to 160mm, Z=0 to 25mm)
    base_bar = Part.makeBox(thickness, depth, 25.0 * params.SCALE, App.Vector(0, 0, 0))

    # 2. Flared Base Feet at front (Y=10) and rear (Y=150)
    foot_front = Part.makeBox(thickness + 6.0 * params.SCALE, 30.0 * params.SCALE, 8.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, 5.0 * params.SCALE, 0))
    foot_rear  = Part.makeBox(thickness + 6.0 * params.SCALE, 30.0 * params.SCALE, 8.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, depth - 35.0 * params.SCALE, 0))

    leg_body = base_bar.fuse(foot_front).fuse(foot_rear)

    # 3. Recessed Rubber Pad Pockets (1.0mm deep, 15x15mm) on bottom face (Z=0)
    pocket_front = Part.makeBox(15.0 * params.SCALE, 15.0 * params.SCALE, 1.0 * params.SCALE, App.Vector(2.5 * params.SCALE, 12.5 * params.SCALE, 0))
    pocket_rear  = Part.makeBox(15.0 * params.SCALE, 15.0 * params.SCALE, 1.0 * params.SCALE, App.Vector(2.5 * params.SCALE, depth - 27.5 * params.SCALE, 0))
    leg_body = leg_body.cut(pocket_front).cut(pocket_rear)

    # 4. Vertical Riser Leg (curving up to Z=125mm)
    riser = Part.makeBox(thickness, 40.0 * params.SCALE, height - 25.0 * params.SCALE, App.Vector(0, 30.0 * params.SCALE, 25.0 * params.SCALE))
    leg_body = leg_body.fuse(riser)

    # Apply smooth 1.5mm chamfer to vertical wall edges
    try:
        c_edges = []
        for edge in leg_body.Edges:
            if isinstance(edge.Curve, Part.LineSegment):
                p1, p2 = edge.Vertexes[0].Point, edge.Vertexes[-1].Point
                # Select purely vertical riser edges parallel to Z axis
                if abs(p1.x - p2.x) < 0.1 and abs(p1.y - p2.y) < 0.1 and abs(p1.z - p2.z) > 15.0 * params.SCALE and min(p1.z, p2.z) > 26.0 * params.SCALE and max(p1.z, p2.z) < (height - 2.0 * params.SCALE):
                    c_edges.append(edge)
        if c_edges:
            leg_body = leg_body.makeChamfer(1.5 * params.SCALE, c_edges)
    except Exception as e:
        print(f"Notice: Lower leg chamfer fallback: {e}")

    # 5. Forward-Upward Cradle Arm for Bottom Large Tray (TRAY_LARGE) with front retaining lip
    cradle_base = Part.makeBox(thickness, 55.0 * params.SCALE, 16.0 * params.SCALE, App.Vector(0, 30.0 * params.SCALE, 75.0 * params.SCALE))
    cradle_base.rotate(App.Vector(0, 30.0 * params.SCALE, 75.0 * params.SCALE), App.Vector(1, 0, 0), 25.0)

    # Front retaining lip stop at front tip of cradle arm
    lip = Part.makeBox(thickness, 14.0 * params.SCALE, 20.0 * params.SCALE, App.Vector(0, 75.0 * params.SCALE, 95.0 * params.SCALE))
    
    cradle_arm = cradle_base.fuse(lip)
    leg_body = leg_body.fuse(cradle_arm)

    # 6. Crossbar Mounting Bosses & 13mm M12 Clearance Bores
    # Boss 1: Front Base (Y=25, Z=15)
    cyl1 = Part.makeCylinder(bore_r, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, 25.0 * params.SCALE, 15.0 * params.SCALE), App.Vector(1, 0, 0))
    # Boss 2: Rear Base (Y=135, Z=15)
    cyl2 = Part.makeCylinder(bore_r, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, depth - 25.0 * params.SCALE, 15.0 * params.SCALE), App.Vector(1, 0, 0))

    leg_body = leg_body.cut(cyl1).cut(cyl2)

    # 7. Top Tenon Alignment Pegs at Z=125mm for joining part_03
    tenon_w = 8.0 * params.SCALE
    tenon_d = 12.0 * params.SCALE
    tenon_h = 10.0 * params.SCALE

    tenon1 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, 35.0 * params.SCALE, height))
    tenon2 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, 55.0 * params.SCALE, height))

    leg_body = leg_body.fuse(tenon1).fuse(tenon2).removeSplitter()

    # 8. Apply smooth 3.0mm fillets to outer side wall edges for an organic rounded profile
    try:
        fillet_edges = []
        for edge in leg_body.Edges:
            if hasattr(edge, "Vertexes") and len(edge.Vertexes) >= 2:
                p1 = edge.Vertexes[0].Point
                p2 = edge.Vertexes[-1].Point
                if edge.Length > 4.0 * params.SCALE and p1.z > 1.0 * params.SCALE and p2.z > 1.0 * params.SCALE and p1.z < (height - 1.0 * params.SCALE) and p2.z < (height - 1.0 * params.SCALE):
                    fillet_edges.append(edge)
        if fillet_edges:
            leg_body = leg_body.makeFillet(3.0 * params.SCALE, fillet_edges)
    except Exception as e:
        print(f"Notice: Lower leg wall fillet fallback: {e}")

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
    doc = App.newDocument("LowerLeg")
    shape = construct_lower_leg()
    feature = doc.addObject("Part::Feature", "LowerLeg")
    feature.Shape = shape
    doc.recompute()

main()
