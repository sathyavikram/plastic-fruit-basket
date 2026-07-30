# Requirements — Phase 2: Horizontal Crossbars (`part_01_crossbar.py`)

## Scope
Design and export 3D-printable horizontal support crossbars (`part_01_crossbar.py`) that span between the left and right side frames of the 3-tier fruit basket organizer.

## Decisions
- Quantity: 4 identical crossbars required in full assembly.
- Outer Diameter: `24.0 * SCALE` mm ($12.0\text{ mm}$ radius).
- Length: `170.0 * SCALE` mm (fits flat on 175 × 175 mm FDM build plate).
- Internal Sockets: M16 × 3.5 mm female threads cut to 25 mm depth at both ends.
- Wall Clearance: $4.0\text{ mm}$ solid plastic structural wall surrounding the internal thread sockets ($24\text{ mm}$ OD vs $16\text{ mm}$ thread major diameter).
- Entry Chamfer: 1.5 mm at 45° at both thread socket entrances for toolless self-guiding thread engagement.
- Print Orientation: Flat on XY plane along length axis.

## Constraints
- Must comply 100% with `specs/mission.md`, `specs/tech-stack.md`, and `specs/roadmap.md`.
- Uses `freecad-threading` skill patterns (thread generated at origin, fused, then cut into nominal body).
- Female thread cut at nominal M16 radius ($8.0\text{ mm}$), relying on male screw `THREAD_CLEARANCE = 0.6 mm` for rotation clearance.

## Non-goals
- Generating side stand frames (`part_02` through `part_04`) or screws (`part_05`), which are handled in subsequent phases.

## Context
The 4 crossbars lock the left and right side frames together, preventing racking and maintaining wide-stance structural stability under fruit loads.
