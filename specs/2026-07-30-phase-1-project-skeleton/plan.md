# Plan — Phase 1: Project Skeleton

## Task Group 1: Single Source of Truth (`params.py`)
1. Create `params.py` with `SCALE = 1.0` as the first line.
2. Define canonical system dimensions:
   - `TOTAL_STAND_HEIGHT = 375.0 * SCALE`
   - `TOTAL_BASE_DEPTH = 160.0 * SCALE`
   - `TOTAL_STAND_WIDTH = 320.0 * SCALE`
3. Define build plate constraints:
   - `BUILD_PLATE_X = 175.0 * SCALE`
   - `BUILD_PLATE_Y = 175.0 * SCALE`
   - `BUILD_PLATE_Z = 175.0 * SCALE`
4. Define structural & fit parameters:
   - `SCREW_THREAD_DIAMETER = 16.0 * SCALE` (M16)
   - `THREAD_PITCH = 3.5 * SCALE`
   - `CROSSBAR_LENGTH = 170.0 * SCALE`
   - `CROSSBAR_DIAMETER = 24.0 * SCALE`
   - `FRAME_THICKNESS = 20.0 * SCALE`
   - `WALL_THICKNESS = 3.5 * SCALE`
   - `FIT_CLEARANCE = 0.4 * SCALE`
   - `THREAD_CLEARANCE = 0.6 * SCALE`
   - `DOVETAIL_CLEARANCE = 0.2 * SCALE`
5. Define directory paths (`PROJECT_DIR`, `EXPORT_DIR`, `PRINT_3D_DIR`, `MEDIA_DIR`).

## Task Group 2: Directory Structure & Runner (`run.sh`)
1. Create directories: `exports/`, `3d-print/`, `media/`.
2. Create executable shell runner script `run.sh` for headless execution (`freecadcmd`), GUI inspection (`FreeCAD`), export regeneration, and assembly building.
3. Make `run.sh` executable (`chmod +x run.sh`).

## Task Group 3: Smoke Test & Verification
1. Execute `python params.py` to confirm zero syntax/import errors.
2. Run `./run.sh` to confirm usage menu and environment setup.
