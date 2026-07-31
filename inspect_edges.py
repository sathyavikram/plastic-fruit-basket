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

for i, edge in enumerate(leg_body.Edges):
    print(f"Edge {i}: Z=[{edge.BoundBox.ZMin:.2f}, {edge.BoundBox.ZMax:.2f}], Y=[{edge.BoundBox.YMin:.2f}, {edge.BoundBox.YMax:.2f}], X=[{edge.BoundBox.XMin:.2f}, {edge.BoundBox.XMax:.2f}]")
