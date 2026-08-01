# Validation

## Required Checks
- **Headless Execution**: Ensure `./run.sh part_06_tray_small.py` completes without syntax errors or OpenCASCADE boolean crashes.
- **Export Verification**: Verify `exports/` contains:
  - `part_06_tray_small_left.step` and `.stl`
  - `part_06_tray_small_right.step` and `.stl`
  - `part_06_tray_small_full.step` and `.stl` (for visualization)
- **Bounding Box Verification**: Both left and right STLs must measure well under 175 mm in all dimensions.

## Manual Review
- Use `freecad-visual-validation` (via `render_freecad_script`) to render isometric, top, front, and cross-section views of the full tray.
- Use `section_freecad_model` to verify the internal joint mechanism (dovetails and pins).
- Visually confirm the aesthetic profile matches a "smooth boat-like oval curve".

## Merge Criteria
- 100% Manifold topology for all STLs.
- Bounding box compliance for 175 mm bed size.
- 0.0 mm³ interference (`check_interference`) between the Left and Right halves at the joint surface.
