# Validation

## Required Checks
- `run.sh` execution must pass without any tracebacks, boolean errors, or unhandled exceptions.
- The exported `part_05_threaded_pin.step` and `.stl` must be verified manifold.
- Use `render_freecad_script` to check the visual topology of the 12-scallop knurled head and the coarse M12 threads.

## Integration & Assembly Checks
- `check_interference` must report exactly 0.0 mm³ collision between the threaded pins, the side stand frames, and the crossbars, confirming the 0.6 mm thread clearance is adequate.
- Use `section_freecad_model` to verify the threaded engagement between the pin and the crossbar.

## Merge Criteria
- All scripts run headlessly via FreeCAD MCP.
- The part scales correctly with `params.SCALE`.
- The assembly visually passes inspection.
- Interference volume is strictly zero.
