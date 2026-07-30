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
- Create `params.py` with single source of truth: `SCALE = 1.0`, target dimensions (375 mm H, 160 mm D, 320 mm W), `SCREW_THREAD_DIAMETER = 16.0`, `THREAD_PITCH = 3.5`, `CROSSBAR_LENGTH = 170.0`, `CROSSBAR_DIAMETER = 24.0`, build-plate limit (175 mm), tolerances (`FIT_CLEARANCE = 0.4`, `THREAD_CLEARANCE = 0.6`), `PROJECT_DIR`, `EXPORT_DIR`
- Create `exports/`, `3d-print/`, `media/` directories
- Create executable `run.sh` build script and `.gitignore`
- Smoke-test: `python params.py` executes without error

---

## Phase 2 — Horizontal Crossbars (`part_01_crossbar.py` — `freecad-threading`) ✅
- 4 cylindrical support rods / crossbars (length 170 mm, outer diameter 24 mm) spanning between left and right side frames
- Features integrated M16 female threaded sockets on both ends (providing 4.0 mm solid plastic wall around threads) via `freecad-threading`
- Print orientation: flat on the bed; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 3 — 3-Piece Split Side Stand Frames (`part_02_stand_lower_leg.py`, `part_03_stand_middle_leg.py`, `part_04_stand_upper_leg.py` — `freecad-fits-tolerances`)
- Because total stand height (375 mm) exceeds the 175 mm bed limit, split each organic S-curved side frame into 3 stackable interlocking sections:
  - `part_02_stand_lower_leg.py`: Wide-base foot section (~135 mm H) with **integrated flared base pads & recessed rubber pad pockets**, base crossbar mounts, and male alignment pegs (`FIT_CLEARANCE = 0.4 mm`).
  - `part_03_stand_middle_leg.py`: Middle S-curve section (~135 mm H) with middle crossbar mounts and female/male alignment joints.
  - `part_04_stand_upper_leg.py`: Upper section (~135 mm H) with top crossbar mounts and female alignment sockets.
- Print orientation: flat on XY plane; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 4 — Threaded Fasteners & Thumb Pins (`part_05_threaded_pin.py` — `freecad-threading`)
- **M16 × 3.5 mm coarse thread** thumb screw with chunky 28 mm ergonomic knurled head
- Used to lock side stand frames to crossbars through 24 mm side panel bosses
- Thread profile optimized for FDM printing with 60° self-supporting overhangs and 0.6 mm diametral thread clearance (`THREAD_CLEARANCE = 0.6 mm`)
- Export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 5 — Small Top Oval Tray (`part_06_tray_small.py` — `freecad-fits-tolerances`)
- Small top oval tray (~225 mm width × 165 mm depth × 57 mm height)
- Designed as a 2-piece split shell (Left Half & Right Half) joined along the center axis using internal dovetail keys and alignment pins to fit within 175 mm bed limits
- Export STEP + STL for both halves; execute `freecad-visual-validation` pass

---

## Phase 6 — Medium Middle Oval Tray (`part_07_tray_medium.py` — `freecad-fits-tolerances`)
- Middle oval tray (~260 mm width × 185 mm depth × 63 mm height)
- Designed as a 2-piece split shell (Left Half & Right Half) joined along the center axis using internal dovetail keys and alignment pins
- Export STEP + STL for both halves; execute `freecad-visual-validation` pass

---

## Phase 7 — Large Bottom Oval Tray (`part_08_tray_large.py` — `freecad-fits-tolerances`)
- Large bottom oval tray (~320 mm width × 208 mm depth × 68 mm height)
- Designed as a 2-piece split shell (Left Half & Right Half) joined along the center axis using heavy-duty dovetail keys and 4.0 mm alignment dowels
- Export STEP + STL for both halves; execute `freecad-visual-validation` pass

---

## Phase 8 — Final Review & Full Assembly (`assembly.py`, `export_all.py` — `freecad-visual-validation` & `changelog-maintenance`)
- Position all components in `assembly.py` (6 Frame Leg Segments with Integrated Base Feet, 4 Crossbars, 8 M16 Thumb Screws, 6 Tray Halves — 24 sub-parts total)
- Execute `export_all.py` to regenerate all clean STEP + STL files in `exports/`
- Generate full `assembly.step` and `assembly.stl` and perform final visual collision and manifold inspection using `freecad-visual-validation`
- Append concise dated release notes to `CHANGELOG.md` via `changelog-maintenance`

---

## Out of Scope (v1)
- Wall-mounting brackets
- Dynamic tray height adjustability
- FEA load simulation