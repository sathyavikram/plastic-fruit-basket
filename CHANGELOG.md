# Changelog

## 2026-08-01
- Implemented Phase 5 Small Top Oval Tray (`part_06_tray_small.py`) with a boat-like shape and a center split line incorporating two internal dovetail keys and alignment pins to fit the 175 mm bed limit.
- Optimized assembly generation by using simplified thread placeholders to prevent FreeCAD OpenCASCADE from hanging during 3D tessellation.
- Fixed a Python module import bug in `export_all.py` that was accidentally overwriting high-poly printable STLs with simplified visualization placeholders.

## 2026-07-31
- Resolved an OpenCASCADE boolean constraint hang in `part_05_threaded_pin.py` by applying chamfer cuts to individual components before fusing them into a compound.
- Removed unused scratch scripts and test files.
- Implemented Phase 4 threaded fasteners (`part_05_threaded_pin.py`) featuring a 16 mm rounded button head with a 2 mm flathead screwdriver slot and M12 × 2.5 mm coarse threads.
- Built the complete `assembly.py` integrating the 6 frame segments, 4 crossbars, and 8 thumb pins.
- Lowered the base foot pad heights in `part_02_stand_lower_leg.py` to ensure clearance for the thumb pin heads.
## 2026-07-30
- Implemented Phase 3 split side stand frames (`part_02_stand_lower_leg.py`, `part_03_stand_middle_leg.py`, `part_04_stand_upper_leg.py`) with integrated flared feet, rubber pad pockets, 13 mm M12 clearance bores, cradle arms, and 0.4 mm clearance mortise-and-tenon joints.
- Refined horizontal crossbar dimensions to sleeker 18 mm OD with M12 × 2.5 mm female thread sockets for improved visual proportions.
- Implemented Phase 2 horizontal support crossbars (`part_01_crossbar.py`).
- Marked Phase 1 (Project Skeleton) as complete in `specs/roadmap.md`.
- Implemented Phase 1 project skeleton with `params.py` single source of truth, build volume limits (175 mm), and `run.sh` runner.
- Established Project Constitution with canonical target dimensions (375 mm H, 160 mm D, 320 mm W) and 100% 3D printability mandate.
