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

    # 5. Forward Cradle Arm for Bottom Large Tray (slanted at ~65°)
    cradle = Part.makeBox(thickness, 50.0 * params.SCALE, 16.0 * params.SCALE, App.Vector(0, 60.0 * params.SCALE, 90.0 * params.SCALE))
    cradle.rotate(App.Vector(0, 60.0 * params.SCALE, 90.0 * params.SCALE), App.Vector(1, 0, 0), -25.0)
    leg_body = leg_body.fuse(cradle)

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
