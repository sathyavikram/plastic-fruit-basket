SCALE = 1.0

import os

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
SCREW_HEAD_DIAMETER   = 24.0 * SCALE   # 24 mm ergonomic knurled thumb head
CROSSBAR_LENGTH       = 170.0 * SCALE  # 170 mm crossbar length (fits flat on 175 mm bed)
CROSSBAR_DIAMETER     = 18.0 * SCALE   # 18 mm outer diameter (provides 3.0 mm wall around M12 thread)
FRAME_THICKNESS       = 20.0 * SCALE   # 20 mm side frame panel thickness
FRAME_BOSS_DIAMETER   = 24.0 * SCALE   # 24 mm reinforced boss around screw seats
WALL_THICKNESS        = 3.5 * SCALE    # 3.5 mm structural wall thickness

# --- FDM Print Fit Tolerances ---
FIT_CLEARANCE      = 0.4 * SCALE       # Sliding joints & mortise-and-tenon alignment pegs
THREAD_CLEARANCE   = 0.6 * SCALE       # Radial/diametral clearance for 3D-printed threads
PRESS_CLEARANCE    = 0.2 * SCALE       # Press/glue fit clearance
DOVETAIL_CLEARANCE = 0.2 * SCALE       # Interlocking tray split dovetail clearance

# --- 3-Tier Removable Oval Bowl Dimensions ---
TRAY_SMALL_LENGTH  = 225.0 * SCALE
TRAY_SMALL_WIDTH   = 165.0 * SCALE
TRAY_SMALL_HEIGHT  = 57.0 * SCALE

TRAY_MEDIUM_LENGTH = 260.0 * SCALE
TRAY_MEDIUM_WIDTH  = 185.0 * SCALE
TRAY_MEDIUM_HEIGHT = 63.0 * SCALE

TRAY_LARGE_LENGTH  = 320.0 * SCALE
TRAY_LARGE_WIDTH   = 208.0 * SCALE
TRAY_LARGE_HEIGHT  = 68.0 * SCALE

# --- Project Paths ---
PROJECT_DIR  = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR   = os.path.join(PROJECT_DIR, "exports")
PRINT_3D_DIR = os.path.join(PROJECT_DIR, "3d-print")
MEDIA_DIR    = os.path.join(PROJECT_DIR, "media")

# --- Directory Initialization ---
for d in (EXPORT_DIR, PRINT_3D_DIR, MEDIA_DIR):
    os.makedirs(d, exist_ok=True)

if __name__ == "__main__":
    print("params.py loaded successfully!")
    print(f"SCALE: {SCALE}")
    print(f"Target System Envelope: {TOTAL_STAND_HEIGHT}mm H x {TOTAL_BASE_DEPTH}mm D x {TOTAL_STAND_WIDTH}mm W")
    print(f"Build Plate Limits: {BUILD_PLATE_X} x {BUILD_PLATE_Y} x {BUILD_PLATE_Z} mm")
