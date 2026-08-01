# Requirements

## Scope
- Implement Phase 5: Small Top Oval Tray (`part_06_tray_small.py`).
- Dimensions: ~225 mm width × 165 mm depth × 57 mm height.
- Output formats: `part_06_tray_small_left.stl`, `part_06_tray_small_right.stl`, and full un-split assembly for visualization.

## Decisions
- **Profile**: Smooth boat-like oval curve with a flat bottom.
- **Wall Thickness**: 3.5 mm (standard thickness per tech-stack).
- **Split Configuration**: Split down the center axis (Y-axis) into a Left Half and Right Half.
- **Joinery**: 2 internal dovetail keys and 2 alignment pins to securely align and hold the halves together.
- **Clearance**: `FIT_CLEARANCE` (0.4 mm) for the pins, and `DOVETAIL_CLEARANCE` (0.2 mm) for the dovetails.

## Constraints
- Max part size must fit within the 175 × 175 × 175 mm bed limit (achieved via the split).
- Must adhere to the `SCALE` parameter from `params.py`.
- Must execute headlessly via FreeCAD Python without CAD kernel boolean failures.
- No support structures required for printing (adhere to 45-deg overhang limit on dovetails/pins).

## Non-goals
- Do not build the middle or large trays in this phase.
- Do not apply surface textures or text to the tray.

## Context
- The top tray sits in the uppermost cradle arms of the side frames. The smooth boat-like shape will match the aesthetic of the original bamboo/ceramic reference product while remaining 100% 3D printable.
