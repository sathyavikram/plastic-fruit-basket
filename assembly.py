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

import part_01_stand_lower
import part_02_stand_middle
import part_03_stand_upper

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_STEP = os.path.join(EXPORT_BASE, "assembly.step")
EXPORT_STL  = os.path.join(EXPORT_BASE, "assembly.stl")


def build_assembly():
    """
    Assembles Left & Right Lower Stands, Middle Stands, and Upper Stands
    into full 3D stack assembly space.
    """
    doc = App.newDocument("Assembly")
    comp_items = []

    # 1. Generate Base Parts
    shape_lower  = part_01_stand_lower.construct_lower_stand()
    shape_middle = part_02_stand_middle.construct_middle_stand()
    shape_upper  = part_03_stand_upper.construct_upper_stand()

    frame_thick = params.FRAME_THICKNESS
    bar_len     = params.SLAT_SPAN
    right_x     = bar_len + frame_thick  # X = 190mm

    # 2. Left Side Stand Frame (X=0 to 20mm)
    comp_items.extend([shape_lower, shape_middle, shape_upper])

    # 3. Right Side Stand Frame (Mirrored and shifted by X = right_x + frame_thick = 210mm)
    for shape in (shape_lower, shape_middle, shape_upper):
        mirrored = shape.mirror(App.Vector(0, 0, 0), App.Vector(1, 0, 0))
        mirrored.translate(App.Vector(right_x + frame_thick, 0, 0))
        comp_items.append(mirrored)

    # 4. Compound Assembly Shape
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
