# Validation — Phase 3: 3-Piece Split Side Stand Frames (`part_02`, `part_03`, `part_04`)

## Required Checks

1. **Script Execution & Export Check**:
   - Run `./run.sh part_02_stand_lower_leg.py`
   - Run `./run.sh part_03_stand_middle_leg.py`
   - Run `./run.sh part_04_stand_upper_leg.py`
   - **Pass Criteria**: All 3 scripts execute with code 0, generating STEP and STL files in `exports/`.

2. **Build Volume Compliance Check**:
   - Verify bounding box height of each individual section is $\le 175.0\text{ mm}$.
   - **Pass Criteria**: All 3 leg parts fit within 175 × 175 × 175 mm build volume.

3. **FreeCAD MCP Server Visual Validation (`render_freecad_script`)**:
   - Execute `render_freecad_script` for `part_02`, `part_03`, and `part_04`.
   - **Pass Criteria**: High-res PNG renders produced with valid solid metadata.

4. **FreeCAD MCP Server Joint Clearance Check (`check_interference`)**:
   - Execute `check_interference` on stacked leg sections.
   - **Pass Criteria**: Zero volume collision ($0.000\text{ mm}^3$) between tenon and mortise joints given `FIT_CLEARANCE = 0.4 mm`.

## Manual Review
- Verify $1.0\text{ mm}$ recessed rubber pad pockets on `part_02_stand_lower_leg.py`.
- Confirm 65° incline on cradle arms and $13\text{ mm}$ clearance bores for M12 screws.

## Merge Criteria
- All required checks pass cleanly.
- Feature branch `feature/phase-3-side-stand-frames` is ready to be committed and merged into `main`.
