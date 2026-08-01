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

import part_01_crossbar
import part_02_stand_lower_leg
import part_03_stand_middle_leg
import part_04_stand_upper_leg
import part_05_threaded_pin

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "assembly.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "assembly.stl")


def build_assembly():
    """
    Assembles all completed parts (Crossbars, Lower Legs, Middle Legs, Upper Legs)
    into full 3D assembly space.
    """
    doc = App.newDocument("Assembly")
    comp_items = []

    # 1. Generate Base Parts
    shape_crossbar   = part_01_crossbar.construct_crossbar()
    shape_lower_leg  = part_02_stand_lower_leg.construct_lower_leg()
    shape_middle_leg = part_03_stand_middle_leg.construct_middle_leg()
    shape_upper_leg  = part_04_stand_upper_leg.construct_upper_leg()
    shape_pin        = part_05_threaded_pin.construct_threaded_pin()

    # Dimensions
    frame_thick = params.FRAME_THICKNESS
    bar_len     = params.CROSSBAR_LENGTH
    right_x     = bar_len + frame_thick  # X = 190mm

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

    # 4. 4 Horizontal Crossbars (Spanning from X=20mm to X=190mm)
    # Crossbar 1: Front Base (Y=25, Z=15)
    cb1 = shape_crossbar.copy()
    cb1.translate(App.Vector(frame_thick, 25.0 * params.SCALE, 15.0 * params.SCALE))
    comp_items.append(cb1)

    # Crossbar 2: Rear Base (Y=135, Z=15)
    cb2 = shape_crossbar.copy()
    cb2.translate(App.Vector(frame_thick, params.TOTAL_BASE_DEPTH - 25.0 * params.SCALE, 15.0 * params.SCALE))
    comp_items.append(cb2)

    # Crossbar 3: Middle Tier (just above medium arm, Z=155)
    cb3 = shape_crossbar.copy()
    cb3_y = params.get_leg_y_at_z(155.0 * params.SCALE)
    cb3.translate(App.Vector(frame_thick, cb3_y, 155.0 * params.SCALE))
    comp_items.append(cb3)

    # Crossbar 4: Top Tier (just above small arm, Z=280)
    cb4 = shape_crossbar.copy()
    cb4_y = params.get_leg_y_at_z(280.0 * params.SCALE)
    cb4.translate(App.Vector(frame_thick, cb4_y, 280.0 * params.SCALE))
    comp_items.append(cb4)

    # 5. Threaded Fasteners (Thumb Pins)
    # Define the 4 crossbar center coordinates (Y, Z)
    pin_coords = [
        (25.0 * params.SCALE, 15.0 * params.SCALE),
        (params.TOTAL_BASE_DEPTH - 25.0 * params.SCALE, 15.0 * params.SCALE),
        (cb3_y, 155.0 * params.SCALE),
        (cb4_y, 280.0 * params.SCALE)
    ]

    for y, z in pin_coords:
        # Left side pin (points +X, head at X=0)
        pin_l = shape_pin.copy()
        pin_l.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
        pin_l.translate(App.Vector(0, y, z))
        comp_items.append(pin_l)

        # Right side pin (points -X, head at X=right_x + frame_thick)
        pin_r = shape_pin.copy()
        pin_r.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), -90)
        pin_r.translate(App.Vector(right_x + frame_thick, y, z))
        comp_items.append(pin_r)

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
