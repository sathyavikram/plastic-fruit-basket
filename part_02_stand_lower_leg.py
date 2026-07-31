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

    # 1. Main Base Bar (horizontal foot along Y-axis: Y=-20 to 160mm, Z=0 to 25mm)
    base_bar = Part.makeBox(thickness, depth + 20.0 * params.SCALE, 25.0 * params.SCALE, App.Vector(0, -20.0 * params.SCALE, 0))

    # 2. Flared Base Feet at front (Y=10) and rear (Y=150)
    foot_front = Part.makeBox(thickness + 6.0 * params.SCALE, 30.0 * params.SCALE, 8.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, 5.0 * params.SCALE, 0))
    foot_rear  = Part.makeBox(thickness + 6.0 * params.SCALE, 30.0 * params.SCALE, 8.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, depth - 35.0 * params.SCALE, 0))
    leg_body = base_bar.fuse(foot_front).fuse(foot_rear)

    # 3. Recessed screw pockets for feet (Z=0 to 1mm)
    pocket_front = Part.makeBox(15.0 * params.SCALE, 15.0 * params.SCALE, 1.0 * params.SCALE, App.Vector(2.5 * params.SCALE, 12.5 * params.SCALE, 0))
    pocket_rear  = Part.makeBox(15.0 * params.SCALE, 15.0 * params.SCALE, 1.0 * params.SCALE, App.Vector(2.5 * params.SCALE, depth - 27.5 * params.SCALE, 0))
    leg_body = leg_body.cut(pocket_front).cut(pocket_rear)

    # 4. Vertical Riser Leg - Curved backward
    riser_height = height
    
    outer_cyl = Part.makeCylinder(params.R_BACK, thickness, App.Vector(0, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    inner_cyl = Part.makeCylinder(params.R_FRONT, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    curved_ring = outer_cyl.cut(inner_cyl)
    
    bbox = Part.makeBox(thickness + 4.0 * params.SCALE, 100.0 * params.SCALE, riser_height, App.Vector(-2.0 * params.SCALE, -80.0 * params.SCALE, 0.0))
    riser = curved_ring.common(bbox)
    
    # Try adding fillets to the vertical edges of this slice
    try:
        r_edges = [e for e in riser.Edges if e.Length > (riser_height - 5.0 * params.SCALE)]
        if r_edges:
            riser = riser.makeFillet(2.0 * params.SCALE, r_edges)
    except Exception:
        pass
        
    leg_body = leg_body.fuse(riser)

    # 5. Base Stand acts as Cradle Arm for Bottom Tray
    bend_radius = 20.0 * params.SCALE
    arm_thickness_z = 25.0 * params.SCALE
    center_y = depth - 10.0 * params.SCALE
    start_z = 25.0 * params.SCALE
    
    outer_r = bend_radius
    outer_cyl = Part.makeCylinder(outer_r, thickness, App.Vector(0, center_y, start_z + outer_r), App.Vector(1, 0, 0))
    
    # Isolate the bottom-right quadrant of the cylinder
    bbox = Part.makeBox(thickness + 4.0 * params.SCALE, outer_r + 5.0 * params.SCALE, outer_r, App.Vector(-2.0 * params.SCALE, center_y, start_z))
    curved_tip = outer_cyl.common(bbox)

    # Add a spherical or cylindrical cap to make the tip rounded
    cap_radius = arm_thickness_z / 2.0
    cap_y = center_y + outer_r - cap_radius
    cap = Part.makeCylinder(cap_radius, thickness, App.Vector(0, cap_y, start_z + outer_r), App.Vector(1, 0, 0))

    leg_body = leg_body.fuse(curved_tip).fuse(cap)

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
    
    top_y = params.get_leg_y_at_z(height)

    tenon1 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, top_y - 10.0 * params.SCALE, height))
    tenon2 = Part.makeBox(tenon_w, tenon_d, tenon_h, App.Vector(6.0 * params.SCALE, top_y + 10.0 * params.SCALE, height))

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
