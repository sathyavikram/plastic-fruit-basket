import sys
import os
import FreeCAD
import Part
import params

SCALE = params.SCALE
thickness = params.FRAME_THICKNESS

gap_start_z = 25.0 * params.SCALE
gap_end_z = 125.0 * params.SCALE
R = (gap_end_z - gap_start_z) / 2.0
mid_z = gap_start_z + R

y_front_mid = params.get_leg_y_at_z(mid_z) + 9.9 * params.SCALE
Y_c = y_front_mid + R
Z_c = mid_z

web_y_min = -100.0 * params.SCALE
web_y_max = Y_c
web_box = Part.makeBox(thickness, web_y_max - web_y_min, gap_end_z - gap_start_z, App.Vector(0, web_y_min, gap_start_z))

outer_cyl_full = Part.makeCylinder(params.R_BACK, thickness, App.Vector(0, params.C_Y, params.C_Z), App.Vector(1, 0, 0))
web_box = web_box.common(outer_cyl_full)

cut_cyl = Part.makeCylinder(R, thickness + 2.0 * params.SCALE, App.Vector(-1.0 * params.SCALE, Y_c, Z_c), App.Vector(1, 0, 0))
c_fillet = web_box.cut(cut_cyl)

Part.export([c_fillet], "c_fillet.step")
