# Roadmap

Each phase is a small, independently buildable unit of work.
Build, validate, and commit before moving to the next phase.

---

## Phase 0 — Project Constitution ✅
- Create `specs/mission.md`, `specs/tech-stack.md`, `specs/roadmap.md`
- Lock canonical dimensions: 375 mm H, 160 mm D, 320 mm W
- Establish 100% 3D printability mandate for frame & slatted baskets with parametric `SCALE` variable architecture and M12 × 2.5 mm fat screws
- Bind core skills: `freecad-project`, `freecad-fits-tolerances`, `freecad-threading`, `freecad-visual-validation`, `changelog-maintenance`, and `feature-spec`

---

## Phase 1 — Project Skeleton (`freecad-project`) ✅
- Create `params.py` with single source of truth: `SCALE = 1.0`, target dimensions (375 mm H, 160 mm D, 320 mm W), `SCREW_THREAD_DIAMETER = 12.0`, `THREAD_PITCH = 2.5`, `SLAT_SPAN = 170.0`, `SLAT_DIAMETER = 10.0`, `SLAT_SOCKET_DEPTH = 10.0`, build-plate limit (175 mm), tolerances (`FIT_CLEARANCE = 0.4`, `THREAD_CLEARANCE = 0.6`), `PROJECT_DIR`, `EXPORT_DIR`
- Create `exports/`, `3d-print/`, `media/` directories
- Create executable `run.sh` build script and `.gitignore`
- Smoke-test: `python params.py` executes without error

---

## Phase 2 — 3-Piece Split Side Stand Frames (`part_02_stand_lower_leg.py`, `part_03_stand_middle_leg.py`, `part_04_stand_upper_leg.py` — `freecad-fits-tolerances`) ✅
- Because total stand height (375 mm) exceeds the 175 mm bed limit, split each organic S-curved side frame into 3 stackable interlocking sections:
  - `part_02_stand_lower_leg.py`: Wide-base foot section (~135 mm H) with **integrated flared base pads & recessed rubber pad pockets**, Option B 10.0 mm inner face blind sockets, and male alignment pegs (`FIT_CLEARANCE = 0.4 mm`).
  - `part_03_stand_middle_leg.py`: Middle S-curve section (~135 mm H) with Option B 10.0 mm inner face blind sockets and female/male alignment joints.
  - `part_04_stand_upper_leg.py`: Upper section (~135 mm H) with Option B 10.0 mm inner face blind sockets and female alignment sockets.
- Print orientation: flat on XY plane; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 3 — Threaded Fasteners & Thumb Pins (`part_05_threaded_pin.py` — `freecad-threading`) ✅
- **M12 × 2.5 mm coarse thread** thumb screw with 24 mm ergonomic knurled head
- Used to lock side stand frames directly to the threaded slat tie-bars through side panel bosses
- Thread profile optimized for FDM printing with 60° self-supporting overhangs and 0.6 mm diametral thread clearance (`THREAD_CLEARANCE = 0.6 mm`)
- Export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 4 — Center Straight Slat Bars & Threaded Tie-Slats (`part_06_slat_straight.py` — `freecad-fits-tolerances` & `freecad-threading`) ✅
- Straight horizontal slat rods (~170 mm span) that form the middle floor of each basket tier
- Features keyed end pins/tabs designed to insert into cradle arm Option B inner face blind sockets with `FIT_CLEARANCE = 0.4 mm`
- Key center slats include integrated M12 female thread sockets for structural frame clamping
- Print orientation: flat on XY plane; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 5 — Curved Side Slat Bars (`part_07_slat_curved.py` — `freecad-fits-tolerances`) ✅
- Slat bars that run straight across the center and curve smoothly upward (35 mm radius) at both ends to form the side/end retaining walls of the fruit basket
- Keyed end tabs for blind socket insertion into cradle arms
- Print orientation: flat on bed; export STEP + STL; execute `freecad-visual-validation` pass

---

## Phase 6 — Cradle Arm Inner Blind Sockets & Unified Slat-Tie Integration (`part_02_stand_lower_leg.py`, `part_03_stand_middle_leg.py`, `part_04_stand_upper_leg.py`, `part_06_slat_straight.py`, `part_07_slat_curved.py` — `freecad-fits-tolerances`) ✅
- Cradle arms feature Option B 10.0 mm inner face blind sockets (`FIT_CLEARANCE = 0.4 mm`) to receive center and curved side slat end pins
- Key slat bars serve as structural tie-bars, unifying basket floor slats and structural crossbars into a single component
- 100% smooth top cradle arm surfaces and zero interference in captured sandwich assembly lock

---

## Phase 7 — Final Review & Full Assembly (`assembly.py`, `export_all.py` — `freecad-visual-validation` & `changelog-maintenance`) ✅
- Position all components in `assembly.py` (6 Frame Leg Segments with Integrated Base Feet, 8 Thumb Pins, Threaded Slat Tie-Bars, Center Slats, Curved Side Slats)
- Execute `export_all.py` to regenerate all clean STEP + STL files in `exports/`
- Generate full `assembly.step` and `assembly.stl` and perform final visual collision and manifold inspection using `freecad-visual-validation`
- Append concise dated release notes to `CHANGELOG.md` via `changelog-maintenance`

---

## Out of Scope (v1)
- Wall-mounting brackets
- Dynamic tray height adjustability
- FEA load simulation