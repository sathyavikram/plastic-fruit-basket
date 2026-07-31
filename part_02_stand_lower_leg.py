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

    # 1. Main Base Bar (horizontal foot along Y-axis)
    # Start it at Y=-100 and chop it with the outer leg cylinder so its back perfectly matches the leg curve
    center_y = depth - 10.0 * params.SCALE
    base_bar_raw = Part.makeBox(thickness, center_y + 100.0 * params.SCALE, 25.0 * params.SCALE, App.Vector(0, -100.0 * params.SCALE, 0))
    outer_cyl_full_base = Part.makeCylinder(params.R_BACK, thickness, App.Vector(0, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
    base_bar = base_bar_raw.common(outer_cyl_full_base)

    # Fillet the top edges of the base bar
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

    # Helper to create sweeping concave fillet webs
    def make_web(r, w, x, y, z, dir_y, dir_z):
        y_min = 0 if dir_y > 0 else -r
        z_min = 0 if dir_z > 0 else -r
        box = Part.makeBox(w, r, r, App.Vector(x, y + y_min, z + z_min))
        cy = y + (r if dir_y > 0 else -r)
        cz = z + (r if dir_z > 0 else -r)
        cyl = Part.makeCylinder(r, w + 2.0 * params.SCALE, App.Vector(x - 1.0 * params.SCALE, cy, cz), App.Vector(1, 0, 0))
        return box.cut(cyl)

    # 2. Sweeping Base Feet
    # Move rear foot back so it supports the curve (Y=2.53 at Z=8)
    foot_front = Part.makeBox(thickness + 6.0 * params.SCALE, 44.3 * params.SCALE, 8.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, -10.0 * params.SCALE, 0))
    # Move front foot forward so it supports the hook (Y=164 at Z=8)
    foot_rear  = Part.makeBox(thickness + 6.0 * params.SCALE, 30.0 * params.SCALE, 8.0 * params.SCALE, App.Vector(-3.0 * params.SCALE, 145.0 * params.SCALE, 0))
    
    # Add sweeping webs to blend the leg into the feet!
    web_back = make_web(12.0 * params.SCALE, thickness, 0, 2.53 * params.SCALE, 8.0 * params.SCALE, -1, 1)
    web_front = make_web(12.0 * params.SCALE, thickness, 0, 164.0 * params.SCALE, 8.0 * params.SCALE, 1, 1)
    
    foot_front = foot_front.fuse(web_back)
    foot_rear = foot_rear.fuse(web_front)
    
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
    
    bbox = Part.makeBox(thickness + 4.0 * params.SCALE, 160.0 * params.SCALE, riser_height, App.Vector(-2.0 * params.SCALE, -80.0 * params.SCALE, 0.0))
    riser = curved_ring.common(bbox)
    
    # Try adding fillets to the vertical edges of this slice
    try:
        r_edges = [e for e in riser.Edges if e.Length > (riser_height - 5.0 * params.SCALE)]
        if r_edges:
            riser = riser.makeFillet(2.0 * params.SCALE, r_edges)
    except Exception:
        pass
        
    # 5. Mathematically Perfect Upward Hook Tip
    hook_center_z = 40.0 * params.SCALE
    hook_r_out = 40.0 * params.SCALE
    hook_r_in = 15.0 * params.SCALE
    
    outer_cyl = Part.makeCylinder(hook_r_out, thickness, App.Vector(0, center_y, hook_center_z), App.Vector(1, 0, 0))
    inner_cyl = Part.makeCylinder(hook_r_in, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, center_y, hook_center_z), App.Vector(1, 0, 0))
    ring = outer_cyl.cut(inner_cyl)
    
    # Bottom-right quadrant (Y: center_y to +50, Z: 0 to hook_center_z)
    bbox = Part.makeBox(thickness + 4.0 * params.SCALE, hook_r_out + 10.0 * params.SCALE, hook_center_z, App.Vector(-2.0 * params.SCALE, center_y, 0))
    curved_tip = ring.common(bbox)

    # Cap the hook with a perfect half-cylinder
    cap_radius = (hook_r_out - hook_r_in) / 2.0
    cap_y = center_y + hook_r_in + cap_radius
    cap = Part.makeCylinder(cap_radius, thickness, App.Vector(0, cap_y, hook_center_z), App.Vector(1, 0, 0))

    leg_body = base_bar.fuse(foot_front).fuse(foot_rear).fuse(riser).fuse(curved_tip).fuse(cap).cut(pocket_front).cut(pocket_rear)
    
    # 6. Crossbar Mounting Bosses & 13mm M12 Clearance Bores
    # Boss 1: Front Base (Y=25, Z=15)
    cyl1 = Part.makeCylinder(bore_r, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, 25.0 * params.SCALE, 15.0 * params.SCALE), App.Vector(1, 0, 0))
    # Boss 2: Rear Base (Y=135, Z=15)
    cyl2 = Part.makeCylinder(bore_r, thickness + 4.0 * params.SCALE, App.Vector(-2.0 * params.SCALE, depth - 25.0 * params.SCALE, 15.0 * params.SCALE), App.Vector(1, 0, 0))

    leg_body = leg_body.cut(cyl1).cut(cyl2)

    # 7. Top Tenon Alignment Peg at Z=125mm for joining part_03
    # Use a single, perfectly centered 10x10x10 tenon
    tenon_size = 10.0 * params.SCALE
    top_y = params.get_leg_y_at_z(height) # This is the exact center of the leg curve
    
    # Place tenon centered at X=10 (thickness/2) and Y=top_y
    tenon = Part.makeBox(tenon_size, tenon_size, tenon_size, 
                         App.Vector((thickness - tenon_size) / 2.0, top_y - (tenon_size / 2.0), height))

    leg_body = leg_body.fuse(tenon).removeSplitter()

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
