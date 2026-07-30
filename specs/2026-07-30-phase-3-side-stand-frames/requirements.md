# Requirements — Phase 3: 3-Piece Split Side Stand Frames (`part_02`, `part_03`, `part_04`)

## Scope
Design and export the 3 stackable 3D-printable side stand frame sections (`part_02_stand_lower_leg.py`, `part_03_stand_middle_leg.py`, `part_04_stand_upper_leg.py`) that form the 375 mm tall vertical support structure for the fruit basket organizer.

## Decisions
- Bed Limit Split: Stand height (375 mm) split into 3 stackable sections (~135 mm height each), cleanly fitting within 175 × 175 × 175 mm FDM build volume.
- Integrated Base Feet (`part_02`): Monolithic flared base foot pads with $1.0\text{ mm}$ recessed pockets for $15\text{ mm}$ adhesive anti-slip rubber pads (no separate foot caps required).
- Panel Thickness: $20.0 * SCALE$ mm main frame thickness, with $24.0 * SCALE$ mm reinforced bosses around crossbar screw mounting holes.
- Crossbar Mounting Sockets: $13.0 * SCALE$ mm clearance bores (accepting M12 screws without binding).
- Section Joints: Mortise-and-tenon interlocking alignment joints with `FIT_CLEARANCE = 0.4 * SCALE` mm for sliding assembly.
- Cradle Arms: Forward-curved organic cradle arms on each section angled at 65° incline to support the 3 oval fruit bowls securely.

## Constraints
- Must comply 100% with `specs/mission.md`, `specs/tech-stack.md`, and `specs/roadmap.md`.
- All overhangs $\le 45^\circ$ for supportless FDM 3D printing flat on the XY plane.
- Manifold solid topology with smooth filleted transitions.

## Non-goals
- Generating fasteners (`part_05_threaded_pin.py`) or oval bowls (`part_06` through `part_08`), which are handled in subsequent phases.

## Context
Splitting the side frame into 3 stackable segments enables 100% 3D printability on compact FDM printers while preserving structural strength under full fruit load.
