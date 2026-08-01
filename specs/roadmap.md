# Roadmap

Each phase represents a core component of the 100% 3D-printable slatted fruit basket architecture.

---

## Phase 0 — Project Specifications & Setup ✅
- Establish global `SCALE = 1.0` single source of truth in `params.py` with canonical dimensions: 375 mm H, 160 mm D, 320 mm W
- Configure 175 × 175 × 175 mm FDM build volume compliance and fit clearances (`FIT_CLEARANCE = 0.4 mm`, `THREAD_CLEARANCE = 0.6 mm`)
- Bind core skills and FreeCAD MCP validation toolset

---

## Phase 1 — Side Support Frame Legs (`part_01_stand_lower_leg.py`, `part_02_stand_middle_leg.py`, `part_03_stand_upper_leg.py`) ✅
- **Modular 3-Piece Split Frame**: Each organic S-curved side frame is split into 3 stackable interlocking sections:
  - `part_01_stand_lower_leg.py`: Wide-stance base foot (~135 mm H) with integrated flared base pads, recessed rubber bumper pockets, 10.0 mm inner face blind sockets, and male alignment pegs.
  - `part_02_stand_middle_leg.py`: Middle S-curve section (~135 mm H) with 10.0 mm inner face blind sockets and interlocking alignment joints.
  - `part_03_stand_upper_leg.py`: Upper section (~135 mm H) with 10.0 mm inner face blind sockets and female alignment sockets.

---

## Phase 2 — Threaded Fasteners & Thumb Screws (`part_04_threaded_pin.py`) ✅
- **M12 × 2.5 mm Coarse Thread Pins**: Ergonomic 24 mm knurled thumb screws designed for 100% toolless assembly.
- Threads directly through the side frame bosses into the threaded structural slat tie-bars, clamping the Left and Right stand frames together.

---

## Phase 3 — Straight Center Floor Slats (`part_05_slat_straight.py`) ✅
- Straight horizontal slat rods (170 mm span, 10 mm diameter) forming the floor of each basket tier.
- Includes 9.2 mm end tabs for insertion into cradle arm blind sockets (`FIT_CLEARANCE = 0.4 mm`).
- Key center slats feature integrated M12 female thread sockets for structural tie-rod clamping.

---

## Phase 4 — Curved Side Retaining Slats (`part_06_slat_curved.py`) ✅
- Slat bars running straight across the center floor and sweeping upward (35 mm curve radius) at both ends to form the side retaining walls of the basket.
- Features 9.2 mm end tabs for blind socket captured-sandwich insertion into side cradle arms.

---

## Phase 5 — Full 3D Assembly & Export Validation (`assembly.py`, `export_all.py`) ✅
- Position all components in `assembly.py` (6 Frame Leg Segments, 8 M12 Thumb Screws, Center Floor Slats, Curved Side Slats).
- Execute `export_all.py` to generate clean STEP (AP214) and binary STL files in `exports/` for all parts and assembly.
- Perform visual collision, section inspection, and 0.0 mm³ interference validation via FreeCAD MCP Server.

---

## Out of Scope (v1)
- Wall-mounting brackets
- Dynamic tray height adjustability
- FEA load simulation