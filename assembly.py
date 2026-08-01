import os
import sys

os.environ["SIMPLIFIED_THREADS"] = "1"

import FreeCAD as App
import Part

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

import part_02_stand_lower_leg
import part_03_stand_middle_leg
import part_04_stand_upper_leg
import part_05_threaded_pin
import part_06_slat_straight
import part_07_slat_curved

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "assembly.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "assembly.stl")


def build_assembly():
    """
    Assembles all completed parts (Lower Legs, Middle Legs, Upper Legs, Unified Slat-Tie Bars, Thumb Pins)
    into full 3D assembly space.
    """
    doc = App.newDocument("Assembly")
    comp_items = []

    # 1. Generate Base Parts
    shape_lower_leg  = part_02_stand_lower_leg.construct_lower_leg()
    shape_middle_leg = part_03_stand_middle_leg.construct_middle_leg()
    shape_upper_leg  = part_04_stand_upper_leg.construct_upper_leg()
    shape_pin        = part_05_threaded_pin.construct_threaded_pin()
    shape_slat_str   = part_06_slat_straight.construct_straight_slat(is_threaded=False)
    shape_slat_str_t = part_06_slat_straight.construct_straight_slat(is_threaded=True)
    shape_slat_crv   = part_07_slat_curved.construct_curved_slat(is_threaded=False)
    shape_slat_crv_t = part_07_slat_curved.construct_curved_slat(is_threaded=True)

    # Dimensions
    frame_thick = params.FRAME_THICKNESS
    bar_len     = params.CROSSBAR_LENGTH
    right_x     = bar_len + frame_thick  # X = 190mm
    mid_x       = (right_x + frame_thick) / 2.0 # X = 105mm center span

    # 2. Left Side Stand Frame (X=0 to 20mm)
    leg_l_lower  = shape_lower_leg.copy()
    leg_l_middle = shape_middle_leg.copy()
    leg_l_upper  = shape_upper_leg.copy()

    comp_items.extend([leg_l_lower, leg_l_middle, leg_l_upper])

    # 3. Right Side Stand Frame (Shifted by X = bar_len + frame_thick = 190mm)
    leg_r_lower  = shape_lower_leg.copy()
    leg_r_middle = shape_middle_leg.copy()
    leg_r_upper  = shape_upper_leg.copy()

    for shape in (leg_r_lower, leg_r_middle, leg_r_upper):
        shape.translate(App.Vector(right_x, 0, 0))
        comp_items.append(shape)

    # 4. Slatted Basket Bars & Threaded Tie-Slats (3 Tiers)
    # Tier 1 (Bottom): arm_z = 25mm, center_z = 30mm, sockets at Y = 60, 90, 120
    for i, y in enumerate((60.0 * params.SCALE, 90.0 * params.SCALE, 120.0 * params.SCALE)):
        # Middle slat (i=1) is threaded tie-slat; outer slats are curved
        slat = (shape_slat_str_t if i == 1 else shape_slat_crv).copy()
        slat.translate(App.Vector(mid_x, y, 30.0 * params.SCALE))
        comp_items.append(slat)

    # Base Tie-Slats at Y=25mm and Y=135mm (Z=15mm)
    slat_b1 = shape_slat_str_t.copy()
    slat_b1.translate(App.Vector(mid_x, 25.0 * params.SCALE, 15.0 * params.SCALE))
    comp_items.append(slat_b1)

    slat_b2 = shape_slat_str_t.copy()
    slat_b2.translate(App.Vector(mid_x, params.TOTAL_BASE_DEPTH - 25.0 * params.SCALE, 15.0 * params.SCALE))
    comp_items.append(slat_b2)

    # Tier 2 (Middle): arm_z = 125mm, center_z = 130mm, sockets at Y = 60, 85, 110
    for i, y in enumerate((60.0 * params.SCALE, 85.0 * params.SCALE, 110.0 * params.SCALE)):
        slat = (shape_slat_str_t if i == 1 else shape_slat_crv).copy()
        slat.translate(App.Vector(mid_x, y, 130.0 * params.SCALE))
        comp_items.append(slat)

    # Tier 3 (Top): arm_z = 250mm, center_z = 255mm, sockets at Y = 50, 70, 90
    for i, y in enumerate((50.0 * params.SCALE, 70.0 * params.SCALE, 90.0 * params.SCALE)):
        slat = (shape_slat_str_t if i == 1 else shape_slat_crv).copy()
        slat.translate(App.Vector(mid_x, y, 255.0 * params.SCALE))
        comp_items.append(slat)

    # 5. Threaded Fasteners (Thumb Pins into Slat Tie-Bars)
    pin_coords = [
        (25.0 * params.SCALE, 15.0 * params.SCALE),
        (params.TOTAL_BASE_DEPTH - 25.0 * params.SCALE, 15.0 * params.SCALE),
        (85.0 * params.SCALE, 130.0 * params.SCALE),
        (70.0 * params.SCALE, 255.0 * params.SCALE)
    ]

    for y, z in pin_coords:
        pin_l = shape_pin.copy()
        pin_l.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
        pin_l.translate(App.Vector(0, y, z))
        comp_items.append(pin_l)

        pin_r = shape_pin.copy()
        pin_r.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), -90)
        pin_r.translate(App.Vector(right_x + frame_thick, y, z))
        comp_items.append(pin_r)

    # 6. Slatted Basket Bars (3 Tiers inserted into Option B inner blind sockets)
    # Tier 1 (Bottom): arm_z = 25mm, center_z = 30mm, sockets at Y = 60, 90, 120
    for i, y in enumerate((60.0 * params.SCALE, 90.0 * params.SCALE, 120.0 * params.SCALE)):
        slat = (shape_slat_crv if i in (0, 2) else shape_slat_str).copy()
        slat.translate(App.Vector(mid_x, y, 30.0 * params.SCALE))
        comp_items.append(slat)

    # Tier 2 (Middle): arm_z = 125mm, center_z = 130mm, sockets at Y = 60, 85, 110
    for i, y in enumerate((60.0 * params.SCALE, 85.0 * params.SCALE, 110.0 * params.SCALE)):
        slat = (shape_slat_crv if i in (0, 2) else shape_slat_str).copy()
        slat.translate(App.Vector(mid_x, y, 130.0 * params.SCALE))
        comp_items.append(slat)

    # Tier 3 (Top): arm_z = 250mm, center_z = 255mm, sockets at Y = 50, 70, 90
    for i, y in enumerate((50.0 * params.SCALE, 70.0 * params.SCALE, 90.0 * params.SCALE)):
        slat = (shape_slat_crv if i in (0, 2) else shape_slat_str).copy()
        slat.translate(App.Vector(mid_x, y, 255.0 * params.SCALE))
        comp_items.append(slat)

    # 6. Compound Assembly Shape
    assembly_shape = Part.makeCompound(comp_items)

    # Export clean STEP and STL
    os.makedirs(EXPORT_BASE, exist_ok=True)
    for path in (EXPORT_STEP, EXPORT_STL):
        if os.path.exists(path):
            os.remove(path)

    assembly_shape.exportStep(EXPORT_STEP)
    assembly_shape.exportStl(EXPORT_STL)
    print(f"Exported Assembly to {EXPORT_STEP} and {EXPORT_STL}")
    return assembly_shape


def main():
    doc = App.newDocument("Assembly")
    shape = build_assembly()
    feature = doc.addObject("Part::Feature", "Assembly")
    feature.Shape = shape
    doc.recompute()

if __name__ == "__main__" or sys.argv[-1] == os.path.basename(__file__):
    main()
