import FreeCAD as App
import Part
import os
import sys
import math

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    pass

import params
import importlib
importlib.reload(params)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_BASE = os.path.join(CURRENT_DIR, "exports")
EXPORT_LEFT_STEP = os.path.join(EXPORT_BASE, "part_06_tray_small_left.step")
EXPORT_LEFT_STL  = os.path.join(EXPORT_BASE, "part_06_tray_small_left.stl")
EXPORT_RIGHT_STEP = os.path.join(EXPORT_BASE, "part_06_tray_small_right.step")
EXPORT_RIGHT_STL  = os.path.join(EXPORT_BASE, "part_06_tray_small_right.stl")
EXPORT_KEY_STEP = os.path.join(EXPORT_BASE, "part_06_tray_small_key.step")
EXPORT_KEY_STL  = os.path.join(EXPORT_BASE, "part_06_tray_small_key.stl")
EXPORT_PIN_STEP = os.path.join(EXPORT_BASE, "part_06_tray_small_pin.step")
EXPORT_PIN_STL  = os.path.join(EXPORT_BASE, "part_06_tray_small_pin.stl")
EXPORT_FULL_STEP = os.path.join(EXPORT_BASE, "part_06_tray_small_full.step")
EXPORT_FULL_STL  = os.path.join(EXPORT_BASE, "part_06_tray_small_full.stl")

def construct_tray_small_assembly():
    """
    Constructs the small top oval tray, sliced in half, with joinery keys.
    Returns: (left_half, right_half, dovetail_key, alignment_pin, full_assembly)
    """
    length = params.TRAY_SMALL_LENGTH
    width = params.TRAY_SMALL_WIDTH
    height = params.TRAY_SMALL_HEIGHT
    wall = params.WALL_THICKNESS
    base_thick = 6.0 * params.SCALE # Thicker base for dovetail pockets
    
    # Base dimensions
    base_len = length * 0.55
    base_wid = width * 0.55
    
    # --- 1. Construct the Full Hollow Shell ---
    # Outer top profile
    e_top = Part.Ellipse(App.Vector(0,0,0), length/2.0, width/2.0)
    w_top = Part.Wire(e_top.toShape())
    w_top.translate(App.Vector(0,0,height))
    
    # Outer base profile
    e_base = Part.Ellipse(App.Vector(0,0,0), base_len/2.0, base_wid/2.0)
    w_base = Part.Wire(e_base.toShape())
    
    outer_solid = Part.makeLoft([w_base, w_top], True, False, False, False)
    
    # Inner top profile
    e_top_in = Part.Ellipse(App.Vector(0,0,0), length/2.0 - wall, width/2.0 - wall)
    w_top_in = Part.Wire(e_top_in.toShape())
    w_top_in.translate(App.Vector(0,0,height + 1.0))
    
    # Inner base profile
    e_base_in = Part.Ellipse(App.Vector(0,0,0), base_len/2.0 - wall, base_wid/2.0 - wall)
    w_base_in = Part.Wire(e_base_in.toShape())
    w_base_in.translate(App.Vector(0,0, base_thick))
    
    inner_solid = Part.makeLoft([w_base_in, w_top_in], True, False, False, False)
    
    tray = outer_solid.cut(inner_solid).removeSplitter()

    # --- 2. Create the Dovetail Sockets ---
    # Cut pockets in the bottom face spanning across the X=0 plane
    x_len = 10.0 * params.SCALE     # 10mm into each half (20mm total)
    y_wide = 8.0 * params.SCALE     # wide part of dovetail
    y_narrow = 4.0 * params.SCALE   # neck of dovetail
    d_depth = 4.0 * params.SCALE    # depth into the base
    
    dovetail_y_pos = (base_wid / 2.0) * 0.6 # Position near the edges
    
    def make_dovetail_polygon():
        p1 = App.Vector(-x_len, -y_wide, 0)
        p2 = App.Vector(-x_len, y_wide, 0)
        p3 = App.Vector(0, y_narrow, 0)
        p4 = App.Vector(x_len, y_wide, 0)
        p5 = App.Vector(x_len, -y_wide, 0)
        p6 = App.Vector(0, -y_narrow, 0)
        return Part.Wire(Part.makePolygon([p1, p2, p3, p4, p5, p6, p1]))
    
    socket1_wire = make_dovetail_polygon()
    socket1_wire.translate(App.Vector(0, dovetail_y_pos, 0))
    socket1 = Part.Face(socket1_wire).extrude(App.Vector(0, 0, d_depth))
    
    socket2_wire = make_dovetail_polygon()
    socket2_wire.translate(App.Vector(0, -dovetail_y_pos, 0))
    socket2 = Part.Face(socket2_wire).extrude(App.Vector(0, 0, d_depth))
    
    tray = tray.cut(socket1).cut(socket2).removeSplitter()
    
    # --- 3. Create Alignment Pin Holes ---
    # Horizontal bores through the X=0 plane
    pin_radius = 2.0 * params.SCALE
    pin_len = 8.0 * params.SCALE # 8mm into each half
    pin_z = height * 0.5
    pin_y_pos = (width / 2.0) * 0.6
    
    # Add clearance to socket
    hole_radius = pin_radius + params.FIT_CLEARANCE
    hole_len = pin_len + 1.0 * params.SCALE # Extra depth to prevent bottoming out
    
    hole1 = Part.makeCylinder(hole_radius, hole_len * 2, App.Vector(-hole_len, pin_y_pos, pin_z), App.Vector(1,0,0))
    hole2 = Part.makeCylinder(hole_radius, hole_len * 2, App.Vector(-hole_len, -pin_y_pos, pin_z), App.Vector(1,0,0))
    
    tray = tray.cut(hole1).cut(hole2).removeSplitter()
    
    # Save the full assembly with holes for visualization
    full_assembly = tray.copy()
    
    # --- 4. Slice into Left and Right Halves ---
    # Box to cut the left half (keeping X > 0)
    bbox_left = Part.makeBox(length, width + 10, height + 10, App.Vector(0, -(width/2 + 5), -5))
    left_half = tray.common(bbox_left).removeSplitter()
    
    # Box to cut the right half (keeping X < 0)
    bbox_right = Part.makeBox(length, width + 10, height + 10, App.Vector(-length, -(width/2 + 5), -5))
    right_half = tray.common(bbox_right).removeSplitter()
    
    # --- 5. Construct Separate Key and Pin ---
    # Dovetail key (subtract DOVETAIL_CLEARANCE)
    k_x = x_len - params.DOVETAIL_CLEARANCE
    k_yw = y_wide - params.DOVETAIL_CLEARANCE
    k_yn = y_narrow - params.DOVETAIL_CLEARANCE
    k_d = d_depth - params.DOVETAIL_CLEARANCE
    
    kp1 = App.Vector(-k_x, -k_yw, 0)
    kp2 = App.Vector(-k_x, k_yw, 0)
    kp3 = App.Vector(0, k_yn, 0)
    kp4 = App.Vector(k_x, k_yw, 0)
    kp5 = App.Vector(k_x, -k_yw, 0)
    kp6 = App.Vector(0, -k_yn, 0)
    
    key_wire = Part.Wire(Part.makePolygon([kp1, kp2, kp3, kp4, kp5, kp6, kp1]))
    dovetail_key = Part.Face(key_wire).extrude(App.Vector(0, 0, k_d))
    
    # Alignment pin
    alignment_pin = Part.makeCylinder(pin_radius, pin_len * 2)
    # Add chamfers to pin ends
    chamf = 0.5 * params.SCALE
    try:
        edges = [e for e in alignment_pin.Edges if isinstance(e.Curve, Part.Circle)]
        alignment_pin = alignment_pin.makeChamfer(chamf, edges)
    except Exception as e:
        print(f"Warning: Pin chamfer failed: {e}")
        
    return left_half, right_half, dovetail_key, alignment_pin, full_assembly

def main():
    doc = App.newDocument("TraySmall")
    left, right, key, pin, full = construct_tray_small_assembly()
    
    f_left = doc.addObject("Part::Feature", "LeftHalf")
    f_left.Shape = left
    f_right = doc.addObject("Part::Feature", "RightHalf")
    f_right.Shape = right
    f_key = doc.addObject("Part::Feature", "DovetailKey")
    f_key.Shape = key
    f_pin = doc.addObject("Part::Feature", "AlignmentPin")
    f_pin.Shape = pin
    f_full = doc.addObject("Part::Feature", "FullAssembly")
    f_full.Shape = full
    
    doc.recompute()
    
    os.makedirs(EXPORT_BASE, exist_ok=True)
    
    exports = [
        (left, EXPORT_LEFT_STEP, EXPORT_LEFT_STL),
        (right, EXPORT_RIGHT_STEP, EXPORT_RIGHT_STL),
        (key, EXPORT_KEY_STEP, EXPORT_KEY_STL),
        (pin, EXPORT_PIN_STEP, EXPORT_PIN_STL),
        (full, EXPORT_FULL_STEP, EXPORT_FULL_STL)
    ]
    
    for shape, step_path, stl_path in exports:
        for p in (step_path, stl_path):
            if os.path.exists(p):
                os.remove(p)
        shape.exportStep(step_path)
        shape.exportStl(stl_path)
        print(f"Exported to {step_path} and {stl_path}")

if __name__ == "__main__" or sys.argv[-1] == os.path.basename(__file__):
    main()
