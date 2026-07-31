import sys
import os
import FreeCAD
import Part
import params

SCALE = params.SCALE
thickness = params.FRAME_THICKNESS
depth = params.TOTAL_BASE_DEPTH

# Make the curved leg
outer_cyl = Part.makeCylinder(params.R_BACK, thickness, FreeCAD.Vector(0, params.C_Y, params.C_Z), FreeCAD.Vector(1, 0, 0))
inner_cyl = Part.makeCylinder(params.R_FRONT, thickness + 4.0 * SCALE, FreeCAD.Vector(-2.0 * SCALE, params.C_Y, params.C_Z), FreeCAD.Vector(1, 0, 0))
leg_ring = outer_cyl.cut(inner_cyl)
bbox = Part.makeBox(thickness + 4.0 * SCALE, 160.0 * SCALE, 125.0 * SCALE, FreeCAD.Vector(-2.0 * SCALE, -80.0 * SCALE, 0.0))
leg_body = leg_ring.common(bbox)

# Make the bottom arm
bend_radius = 30.0 * SCALE
arm_thickness_z = 25.0 * SCALE
start_z = 0.0
center_z = start_z + bend_radius
center_y = 125.0 * SCALE
outer_cyl_arm = Part.makeCylinder(bend_radius, thickness, FreeCAD.Vector(0, center_y, center_z), FreeCAD.Vector(1, 0, 0))
inner_cyl_arm = Part.makeCylinder(bend_radius - arm_thickness_z, thickness + 4.0 * SCALE, FreeCAD.Vector(-2.0 * SCALE, center_y, center_z), FreeCAD.Vector(1, 0, 0))
arm_ring = outer_cyl_arm.cut(inner_cyl_arm)
bbox_arm = Part.makeBox(thickness + 4.0 * SCALE, bend_radius + 5.0 * SCALE, bend_radius, FreeCAD.Vector(-2.0 * SCALE, center_y, start_z))
curved_tip = arm_ring.common(bbox_arm)

# Fuse arm to leg
leg_body = leg_body.fuse(curved_tip)

# Try makeFillet
fillet_radius = 40.0 * SCALE
edges_to_fillet = []
for edge in leg_body.Edges:
    # We want the interior edge at the top of the bottom arm (Z approx 25.0)
    # The edge lies roughly between the arm's top surface and the leg's front surface.
    # Its bounding box Z should be around 25.0
    z_min = edge.BoundBox.ZMin
    z_max = edge.BoundBox.ZMax
    y_min = edge.BoundBox.YMin
    if abs(z_min - 25.0) < 5.0 and abs(z_max - 25.0) < 5.0:
        if y_min > -60.0 and y_min < 0.0: # Front surface of leg is around -40
            edges_to_fillet.append(edge)

print(f"Found {len(edges_to_fillet)} edges for top fillet")
if edges_to_fillet:
    try:
        leg_body = leg_body.makeFillet(fillet_radius, edges_to_fillet)
        print("Fillet applied successfully!")
    except Exception as e:
        print(f"Fillet failed: {e}")

Part.export([leg_body], "test_fillet.step")
