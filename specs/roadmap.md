# Roadmap

Each phase represents a core component of the 100% 3D-printable stackable slatted fruit basket architecture.

---

## Phase 0 — Project Specifications & Setup ✅
- Establish global `SCALE = 1.0` single source of truth in `params.py` with canonical dimensions: 375 mm H, 160 mm D, 320 mm W
- Configure 175 × 175 × 175 mm FDM build volume compliance and fit clearances (`DOVETAIL_CLEARANCE = 0.2 mm`, `ALIGNMENT_CLEARANCE = 0.4 mm`)
- Bind core skills and FreeCAD MCP validation toolset

---

## Phase 1 — Stackable Stand Tiers (`part_01_stand_lower.py`, `part_02_stand_middle.py`, `part_03_stand_upper.py`)
- **Modular 3-Tier Stackable Stand Architecture**:
  - `part_01_stand_lower.py`: Lower Stand section (~135 mm H) featuring wide-stance base feet with integrated flared anti-slip pads, extended upward-curving cradle arms, and male alignment joints.
  - `part_02_stand_middle.py`: Middle Stand section (~135 mm H) with extended upward-curving cradle arms and interlocking alignment joints.
  - `part_03_stand_upper.py`: Upper Stand section (~135 mm H) with extended upward-curving cradle arms and female alignment sockets.
- **Arm Geometry & Dovetail Top Slots**:
  - Extended cradle arms whose ends curve and lift upwards continuously until they form the bowl side walls when slats are snap-fitted.
  - Top surfaces of cradle arms feature multiple precision 60° dovetail slots to receive slat dovetail end pegs.

---

## Phase 2 — Slats for Curved Bowl Architecture (`part_04_slat_middle.py`, `part_05_slat_left_curved.py`, `part_06_slat_right_curved.py`)
- **3 Slat Types for Curved Fruit Bowl Profile**:
  - `part_04_slat_middle.py`: Straight central slat bars with dovetail pegs on both ends spanning across the width, directly connecting the left stand frame and right stand frame together.
  - `part_05_slat_left_curved.py`: Left curved boundary slat bars with dovetail pegs attached to the left stand frame, curving upwards/outwards to form the left side of the curved bowl.
  - `part_06_slat_right_curved.py`: Right curved boundary slat rods with dovetail pegs attached to the right stand frame, curving upwards/outwards to form the right side of the curved bowl.
- **Rounded-Rectangle / Stadium Cross-Section**:
  - Slat bars feature flat top and bottom faces with generous filleted edge radii (~1.5–2.5 mm) for zero-support flat FDM printing, fruit protection, and rigid anti-twist indexing in the dovetail slots.
- **Structural Tie-Bars (Zero Fasteners)**:
  - Slats serve as both basket floor/wall elements AND structural crossbars locking left and right stands together via snap-fit dovetail joints.

---

## Phase 3 — Full 3D Assembly & Export Validation (`assembly.py`, `export_all.py`)
- Position all 3D components in `assembly.py` (Left & Right Lower/Middle/Upper Stand frames, Middle Slats, Left Curved Slats, Right Curved Slats via snap-fit dovetail joints).
- Execute `export_all.py` to generate clean STEP (AP214) and binary STL files in `exports/` for all parts and full assembly.
- Perform visual rendering, section inspection, and 0.0 mm³ interference validation via FreeCAD MCP Server.

---

## Out of Scope (v1)
- Wall-mounting brackets
- Dynamic tray height adjustability
- FEA load simulation