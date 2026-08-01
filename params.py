SCALE = 1.0

import os
import math

# --- Build Volume Constraints ---
BUILD_PLATE_X = 175.0 * SCALE
BUILD_PLATE_Y = 175.0 * SCALE
BUILD_PLATE_Z = 175.0 * SCALE

# --- System Target Envelope Dimensions ---
TOTAL_STAND_HEIGHT = 375.0 * SCALE
TOTAL_BASE_DEPTH   = 160.0 * SCALE
TOTAL_STAND_WIDTH  = 320.0 * SCALE

# --- Structural & Fit Parameters ---
SCREW_THREAD_DIAMETER = 12.0 * SCALE   # M12 fat 3D-printable thumb screw
THREAD_PITCH          = 2.5 * SCALE    # 2.5 mm coarse thread pitch
SCREW_HEAD_DIAMETER   = 16.0 * SCALE   # 16 mm simple rounded button head
FRAME_THICKNESS       = 20.0 * SCALE   # 20 mm side frame panel thickness
FRAME_BOSS_DIAMETER   = 24.0 * SCALE   # 24 mm reinforced boss around screw seats
WALL_THICKNESS        = 3.5 * SCALE    # 3.5 mm structural wall thickness

# --- FDM Print Fit Tolerances ---
FIT_CLEARANCE      = 0.4 * SCALE       # Sliding joints & Option B blind socket fits
THREAD_CLEARANCE   = 0.6 * SCALE       # Radial/diametral clearance for 3D-printed threads
PRESS_CLEARANCE    = 0.2 * SCALE       # Press/glue fit clearance
DOVETAIL_CLEARANCE = 0.2 * SCALE       # Interlocking leg split dovetail clearance
SIMPLIFIED_THREADS = False             # Set to True to skip generating heavy B-Rep threads for fast assembly rendering

# --- Slatted Bar Basket System Parameters ---
SLAT_SPAN         = 170.0 * SCALE   # 170 mm slat span between left and right cradle arms
SLAT_DIAMETER     = 10.0 * SCALE    # 10 mm rounded slat bar diameter
SLAT_SOCKET_DEPTH = 10.0 * SCALE    # 10 mm Option B inner face blind socket depth
SLAT_TAB_LENGTH   = 15.0 * SCALE    # 15 mm end tab length
SLAT_CURVE_RADIUS = 35.0 * SCALE    # 35 mm upward curvature radius for side slats

# --- Project Paths ---
PROJECT_DIR  = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR   = os.path.join(PROJECT_DIR, "exports")
PRINT_3D_DIR = os.path.join(PROJECT_DIR, "3d-print")
MEDIA_DIR    = os.path.join(PROJECT_DIR, "media")

# --- Directory Initialization ---
for d in (EXPORT_DIR, PRINT_3D_DIR, MEDIA_DIR):
    os.makedirs(d, exist_ok=True)

# --- Curved Leg Geometry Helper ---
C_Y = 265.2 * SCALE
C_Z = 200.0 * SCALE
R_FRONT = 305.2 * SCALE
R_BACK = 325.2 * SCALE

def get_leg_y_at_z(z_val):
    """Returns the midpoint Y coordinate of the curved leg at a given Z height."""
    dz = z_val - C_Z
    if abs(dz) > R_FRONT:
        return 0.0
    y_front = C_Y - math.sqrt(R_FRONT**2 - dz**2)
    y_back = C_Y - math.sqrt(R_BACK**2 - dz**2)
    return (y_front + y_back) / 2.0


if __name__ == "__main__":
    print("params.py loaded successfully!")
    print(f"SCALE: {SCALE}")
    print(f"Target System Envelope: {TOTAL_STAND_HEIGHT}mm H x {TOTAL_BASE_DEPTH}mm D x {TOTAL_STAND_WIDTH}mm W")
    print(f"Build Plate Limits: {BUILD_PLATE_X} x {BUILD_PLATE_Y} x {BUILD_PLATE_Z} mm")
