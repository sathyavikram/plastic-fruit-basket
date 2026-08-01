# Roadmap

Each phase is a small, independently buildable unit of work.
Build, validate, and commit before moving to the next phase.

---

## Phase 0 — Project Constitution ✅
- Create `specs/mission.md`, `specs/tech-stack.md`, `specs/roadmap.md`
- Lock canonical dimensions: 375 mm H, 160 mm D, 320 mm W
- Establish 100% 3D printability mandate for frame & bowls with parametric `SCALE` variable architecture and M16 × 3.5 mm fat screws
- Bind core skills: `freecad-project`, `freecad-fits-tolerances`, `freecad-threading`, `freecad-visual-validation`, `changelog-maintenance`, and `feature-spec`

---

## Phase 1 — Project Skeleton (`freecad-project`) ✅
- Create `params.py` with single source of truth: `SCALE = 1.0`, target dimensions (375 mm H, 160 mm D, 320 mm W), `SCREW_THREAD_DIAMETER = 12.0`, `THREAD_PITCH = 2.5`, `CROSSBAR_LENGTH = 170.0`, `CROSSBAR_DIAMETER = 18.0`, build-plate limit (175 mm), tolerances (`FIT_CLEARANCE = 0.4`, `THREAD_CLEARANCE = 0.6`), `PROJECT_DIR`, `EXPORT_DIR`
- Create `exports/`, `3d-print/`, `media/` directories
- Create executable `run.sh` build script and `.gitignore`
- Smoke-test: `python params.py` executes without error

---

## Phase 2 — Horizontal Crossbars (`part_01_crossbar.py` — `freecad-threading`) ✅
- 4 cylindrical support rods / crossbars (length 170 mm, outer diameter 18 mm) spanning between left and right side frames
- Features integrated M12 female threaded sockets on both ends (providing 3.0 mm solid plastic wall around threads) via `freecad-threading`
- Print orientation: flat on the bed; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 3 — 3-Piece Split Side Stand Frames (`part_02_stand_lower_leg.py`, `part_03_stand_middle_leg.py`, `part_04_stand_upper_leg.py` — `freecad-fits-tolerances`) ✅
- Because total stand height (375 mm) exceeds the 175 mm bed limit, split each organic S-curved side frame into 3 stackable interlocking sections:
  - `part_02_stand_lower_leg.py`: Wide-base foot section (~135 mm H) with **integrated flared base pads & recessed rubber pad pockets**, base crossbar mounts, and male alignment pegs (`FIT_CLEARANCE = 0.4 mm`).
  - `part_03_stand_middle_leg.py`: Middle S-curve section (~135 mm H) with middle crossbar mounts and female/male alignment joints.
  - `part_04_stand_upper_leg.py`: Upper section (~135 mm H) with top crossbar mounts and female alignment sockets.
- Print orientation: flat on XY plane; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 4 — Threaded Fasteners & Thumb Pins (`part_05_threaded_pin.py` — `freecad-threading`) ✅
- **M12 × 2.5 mm coarse thread** thumb screw with 24 mm ergonomic knurled head
- Used to lock side stand frames to crossbars through side panel bosses
- Thread profile optimized for FDM printing with 60° self-supporting overhangs and 0.6 mm diametral thread clearance (`THREAD_CLEARANCE = 0.6 mm`)
- Export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 5 — Center Straight Slat Bars (`part_06_slat_straight.py` — `freecad-fits-tolerances`) ✅
- Straight horizontal slat rods (~170 mm span) that form the middle floor of each basket tier
- Features keyed end pins/tabs designed to drop into cradle arm comb slots with `FIT_CLEARANCE = 0.4 mm`
- Print orientation: flat on XY plane; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 6 — Curved Side Slat Bars (`part_07_slat_curved.py` — `freecad-fits-tolerances`) ✅
- Slat bars that run straight across the center and curve upward at both ends to form the side/end walls of the fruit basket
- Keyed end tabs for drop-in slot insertion into cradle arms
- Print orientation: flat on bed; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 7 — Cradle Arm Inner Blind Sockets & Slat Integration (`part_02_stand_lower_leg.py`, `part_03_stand_middle_leg.py`, `part_04_stand_upper_leg.py` — `freecad-fits-tolerances`) ✅
- Update side frame cradle arms with Option B 10.0 mm inner blind sockets (`FIT_CLEARANCE = 0.4 mm`) to receive center and curved side slat end pins
- Verify 100% smooth top cradle arm surfaces and zero interference in captured sandwich assembly lock

---

## Phase 8 — Final Review & Full Assembly (`assembly.py`, `export_all.py` — `freecad-visual-validation` & `changelog-maintenance`) ✅
- Position all components in `assembly.py` (6 Frame Leg Segments with Integrated Base Feet, 4 Crossbars, 8 Thumb Pins, Center Slats, Curved Side Slats)
- Execute `export_all.py` to regenerate all clean STEP + STL files in `exports/`
- Generate full `assembly.step` and `assembly.stl` and perform final visual collision and manifold inspection using `freecad-visual-validation`
- Append concise dated release notes to `CHANGELOG.md` via `changelog-maintenance`

---

## Out of Scope (v1)
- Wall-mounting brackets
- Dynamic tray height adjustability
- FEA load simulation