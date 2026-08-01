# Requirements — Phase 1: Stackable Stand Tiers

## Scope
Design and model the 3 modular stackable stand tiers (`Lower Stand`, `Middle Stand`, `Upper Stand`) for a 100% 3D-printable slatted fruit basket.

## Decisions
- **Stand Tier Names**: `Lower Stand` (`part_01_stand_lower.py`), `Middle Stand` (`part_02_stand_middle.py`), `Upper Stand` (`part_03_stand_upper.py`).
- **Stacking Interface**: Mortise-and-tenon interlocking alignment joints (`ALIGNMENT_CLEARANCE = 0.4 mm`) between vertically stacked stand tiers.
- **Arm Geometry**: Extended cradle arms extending outward with upward-curving tips that lift continuously to form the side walls of the fruit bowl when slats are snap-fitted.
- **Dovetail Slot Feature**: Multiple precision 60° dovetail slots (`DOVETAIL_CLEARANCE = 0.2 mm`) integrated directly into the top surface of each stand frame's cradle arms to receive Middle, Left Curved, and Right Curved slats.
- **Anti-Slip Base Feet**: Integrated wide-stance flared feet pads on the bottom of `Lower Stand` with recessed pockets for adhesive rubber bumpers.

## Constraints
- **FDM Build Volume**: Each stand component must fit within a 175 × 175 × 175 mm build volume at 1.0 scale.
- **Manifold Topology**: Solid 3D CAD geometry with 0 non-manifold edges.
- **Toolless Assembly**: 100% all-plastic assembly requiring zero screws, glue, or external hardware.

## Non-goals
- Slat bar geometry implementation (handled in Phase 2).
- Non-printable metal fasteners or external hinges.
