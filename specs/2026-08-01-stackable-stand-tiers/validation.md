# Validation — Phase 1: Stackable Stand Tiers

## Required Checks

### 1. Script Execution & Export Verification
- Execute `part_01_stand_lower.py`, `part_02_stand_middle.py`, `part_03_stand_upper.py`, and `assembly.py`.
- Verify clean execution with 0 Python errors or OpenCASCADE boolean exceptions.
- Verify STEP and binary STL exports are written cleanly into `exports/`.

### 2. FreeCAD MCP Visual Validation
- Run `render_freecad_script` for multi-view burst (`Isometric`, `Front`, `Top`, `Right`) of each stand component and stand assembly.
- Run `inspect_freecad_assembly` to verify 3-tier vertical stack alignment and bounding box dimensions (Target Height: 375 mm total).
- Run `check_interference` on stacked stand joint pairs to verify `0.0 mm³` unexpected volumetric collision.

## Manual Review
- Inspect multi-view renderings to verify cradle arm upward curvature, top-surface dovetail slot placement, and base foot pad alignment.

## Merge Criteria
- All 3 stand part scripts compile cleanly.
- Exports pass 100% manifold STL checks.
- Zero interference detected across mortise-and-tenon stack joints.
