# Validation — Phase 2: Horizontal Crossbars (`part_01_crossbar.py`)

## Required Checks

1. **Script Execution & Export Check**:
   - Run `./run.sh part_01_crossbar.py`
   - **Pass Criteria**: Zero errors, zero tracebacks, `exports/part_01_crossbar.step` and `exports/part_01_crossbar.stl` generated.

2. **FreeCAD MCP Server Multi-View Validation (`render_freecad_script`)**:
   - Execute `render_freecad_script` for `part_01_crossbar.py` with `render_views: ["Isometric", "Front", "Top", "Right"]`.
   - **Pass Criteria**: PNG renders produced cleanly; geometry metadata returns valid non-zero volume and manifold shape.

3. **FreeCAD MCP Server Cross-Section Inspection (`section_freecad_model`)**:
   - Execute `section_freecad_model` with `section_plane: "XZ"`, `section_offset: 0.5`.
   - **Pass Criteria**: Section view clearly reveals the internal M16 female thread teeth and 25 mm socket depth at both ends.

4. **FreeCAD MCP Server Bounding Box Dimension Check (`inspect_freecad_assembly`)**:
   - Execute `inspect_freecad_assembly` with `show_dimensions: true`.
   - **Pass Criteria**: Outer dimensions match $24.0\text{ mm} \times 24.0\text{ mm} \times 170.0\text{ mm}$ ($\pm 0.5\text{ mm}$).

## Manual Review
- Confirm solid wall thickness around M16 thread is $\ge 3.5\text{ mm}$.
- Confirm chamfers exist on outer rims and thread entries.

## Merge Criteria
- All required checks pass cleanly.
- Feature branch `feature/phase-2-horizontal-crossbars` is ready to be committed and merged into `main`.
