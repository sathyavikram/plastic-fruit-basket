# Plan

## Task Group 1: Part Creation & Validation
1. Create `part_05_threaded_pin.py` containing the `M12 × 2.5mm` thumb screw logic using the `freecad-threading` skill (`Part.makeHelix` and `makePipeShell`).
2. Add parametric scaling using `params.py` (e.g., `SCREW_THREAD_DIAMETER`, `THREAD_PITCH`).
3. Run script via `run.sh` to ensure headless Python execution without tracebacks or CAD boolean failures.
4. Export STEP + STL.
5. Visually validate the single part using `render_freecad_script`.

## Task Group 2: Assembly Integration
1. Integrate `part_05_threaded_pin.py` into `assembly.py`.
2. Instantiate instances for all required crossbar connection points in the stand frames.
3. Position and rotate the thumb screws to fit through the side panel bosses and into the crossbars.
4. Ensure the `export_all.py` includes the new part.
5. Export the updated assembly.

## Task Group 3: Interference Checking & Assembly Validation
1. Run `check_interference` on the updated assembly to verify 0.0 mm³ collision, specifically ensuring the 0.6 mm thread clearance works perfectly.
2. Render exploded and section views of the assembly to visually verify the connections.
