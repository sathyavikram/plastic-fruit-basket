# Plan — Phase 2: Horizontal Crossbars (`part_01_crossbar.py`)

## Task Group 1: Parametric Script Setup & Core Cylinder
1. Create `part_01_crossbar.py` importing `params.py` with `importlib.reload(params)`.
2. Define `construct_crossbar()` function returning the finalized `Part.Shape`.
3. Construct the outer main solid cylinder along the X-axis:
   - Outer diameter: `CROSSBAR_DIAMETER = 24.0 * SCALE` (radius $12.0\text{ mm}$)
   - Total length: `CROSSBAR_LENGTH = 170.0 * SCALE`
4. Apply 1.5 mm chamfers on both outer rim ends for smooth aesthetics and print bed contact.

## Task Group 2: Internal M16 Female Thread Sockets (`freecad-threading`)
1. Generate internal female thread cutter at origin using `freecad-threading` pattern:
   - Nominal major radius: `t_radius = SCREW_THREAD_DIAMETER / 2.0 = 8.0 * SCALE`
   - Pitch: `THREAD_PITCH = 3.5 * SCALE`
   - Root radius: `t_r_inner = t_radius - (t_pitch * 0.45)`
   - Helical path via `Part.makeHelix()` and 4-point trapezoidal thread profile wire via `Part.Wire(Part.makePolygon(...))`
   - Sweep via `Part.Wire(helix).makePipeShell()`
   - Core cylinder `Part.makeCylinder(t_r_inner, depth)` fused with sweep using `.fuse().removeSplitter()`
2. Cut M16 female thread socket into the left end ($X = 0$) to 25 mm depth.
3. Cut M16 female thread socket into the right end ($X = 170.0\text{ mm}$) to 25 mm depth.
4. Apply 1.5 mm 45° entry chamfer on both internal socket entrances for smooth screw insertion.

## Task Group 3: Export & MCP Server Validation
1. Export clean STEP (`exports/part_01_crossbar.step`) and STL (`exports/part_01_crossbar.stl`) files.
2. Execute `./run.sh part_01_crossbar.py` to confirm zero Python tracebacks or OpenCASCADE boolean exceptions.
3. Perform FreeCAD MCP Server validation:
   - Multi-view burst rendering via `render_freecad_script`.
   - Cross-section cut via `section_freecad_model` (`XZ` plane) to verify internal thread teeth.
   - Bounding box dimension overlay check via `inspect_freecad_assembly`.
