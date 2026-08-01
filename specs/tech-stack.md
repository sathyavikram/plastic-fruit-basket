# Tech Stack

## CAD Toolchain

| Layer | Tool |
|---|---|
| Parametric modelling | FreeCAD 1.1.0 (Python scripting API) |
| Geometry kernel | OpenCASCADE (OCC) via `Part` workbench |
| Headless execution | `freecadcmd` (`/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd`) |
| GUI inspection | FreeCAD GUI (`/Applications/FreeCAD.app/Contents/MacOS/FreeCAD`) |
| Export format — CAD | STEP (AP214) via `shape.exportStep()` |
| Export format — print | STL (binary) via `shape.exportStl()` |
| Parameters | `params.py` — single source of truth; all dimensions × `SCALE` |

## FreeCAD Python Conventions & Required Skills

The development workflow integrates the following **6 core installed skills** and the **FreeCAD MCP Server** (`freecad` toolset):

1. **`freecad-project`**: Standardizes project layout, `params.py` single source of truth, `part_NN_name.py` design, `assembly.py`, `export_all.py`, `run.sh` runner, and print orientations.
2. **`freecad-fits-tolerances`**: Defines clearances for sliding joints (`0.4 mm`), interlocking dovetail keys & slots (`0.2 mm`), and mortise-and-tenon alignment joints (`0.4 mm`).
3. **`freecad-threading`**: Governs 3D-printable male and female threaded features via `Part.makeHelix` and `makePipeShell` with `THREAD_CLEARANCE = 0.6 mm` subtracted from male outer radii.
4. **`freecad-visual-validation`**: Mandates headless Python execution, runtime error catching, and validation using the **FreeCAD MCP Server** tools:
   - **Script Execution & Error Debugging**: Executes FreeCAD Python scripts (`part_*.py`, `assembly.py`), catching Python syntax errors, tracebacks, OpenCASCADE boolean failures, unhandled exceptions, and missing export files.
   - **`render_freecad_script`**: Multi-view bursts (`Isometric`, `Front`, `Top`, `Right`), camera zoom/angle controls, shape metadata (centroids, volumes, face counts), touching pairs, and joint verification.
   - **`inspect_freecad_assembly`**: Exploded assembly views (`explode_factor`), part highlighting, single-part focus, and W×D×H dimension label overlays.
   - **`section_freecad_model`**: Diagnostic cross-sections (`XY`, `XZ`, `YZ` planes), wireframe topology, curvature heat-maps, and print orientation checks (`orientation_check`).
   - **`check_interference`**: Analytical Boolean intersection volume (mm³) checks between touching part pairs to guarantee zero collision in clearance joints.
5. **`changelog-maintenance`**: Maintains `CHANGELOG.md` with `YYYY-MM-DD` dated entries for project progress tracking.
6. **`feature-spec`**: Generates feature specifications from `specs/roadmap.md` for phase execution.

- `SCALE = 1.0` is always the **first line** of `params.py`
- All dimensions are in **millimetres**
- Primitives: `Part.makeBox`, `Part.makeCylinder`, `Part.makeCone`, etc.
- Boolean operations: `.fuse()`, `.cut()`, `.common()`; use `Part.makeCompound()` for assembling cutter geometry to avoid silent boolean failures in OpenCASCADE.
- Fillets/Chamfers: wrap in `try/except` blocks to handle edge indexing variations robustly.
- **CRITICAL Pattern for Sweeps/Threads**: Sweeps and helical threads must be generated at origin (`App.Vector(0,0,0)`), wrapped as `Part.Solid()`, and fused before applying transformations via `.Placement`.

## FDM Print Constraints

| Parameter | Value |
|---|---|
| Build plate | 175 × 175 × 175 mm (max build volume per part) |
| Max bed diagonal | ~247 mm ($175\sqrt{2}$) |
| Default nozzle | 0.4 mm |
| Layer height | 0.2 mm |
| Sliding fit tolerance | 0.4 mm (`FIT_CLEARANCE`) |
| Dovetail clearance | 0.2 mm (`DOVETAIL_CLEARANCE`) |
| Press fit tolerance | 0.2 mm |
| Min structural wall | 3.5 mm (4 perimeter loops) |
| Overhang limit | ≤ 45° without support |

## Fit Parameters (canonical — defined in `params.py`)

| Parameter | Value | Description |
|---|---|---|
| `FIT_CLEARANCE` | 0.4 mm | Sliding joints & alignment peg fits |
| `DOVETAIL_CLEARANCE` | 0.2 mm | Clearance for top-surface snap-fit dovetail slots |
| `FRAME_THICKNESS` | 20.0 mm | Side stand frame main structural thickness |
| `SLAT_SPAN` | 170.0 mm | Slat bar span between left and right stand cradle arms |
| `SLAT_PROFILE` | Stadium / Rounded-Rect | Flat top/bottom with R1.5–2.5 mm filleted edges |
| `SLAT_DOVETAIL_ANGLE` | 60° | Self-supporting snap-fit dovetail key angle |

## Dimensions — Scaled 375 mm Variant (canonical model)

| Dimension | Imperial | Metric (mm) |
|---|---|---|
| Total Stand Height | 14.8" | 375 mm |
| Total Base Depth | 6.3" | 160 mm |
| Total Stand Width | 12.6" | 320 mm |
| Slat Bar Span | 6.7" | 170 mm |
| Frame Tier Angle | ~65° | 65° incline |

## File & Folder Structure

```
plastic-fruit-basket/
├── specs/                           ← project constitution (mission.md, tech-stack.md, roadmap.md)
├── params.py                        ← all dimensions + SCALE + paths
├── part_01_stand_lower.py           ← Lower Stand with integrated base feet & top surface dovetails
├── part_02_stand_middle.py          ← Middle Stand section with top surface dovetails
├── part_03_stand_upper.py           ← Upper Stand section with top surface dovetails
├── part_04_slat_middle.py           ← straight middle slat bars with dovetail pegs
├── part_05_slat_left_curved.py      ← left curved boundary slat bars with dovetail pegs
├── part_06_slat_right_curved.py     ← right curved boundary slat bars with dovetail pegs
├── assembly.py                      ← full 3D assembly script
├── export_all.py                    ← regenerates all STEP + STL exports
├── run.sh                           ← build & validation runner
├── README.md
├── .gitignore
├── exports/                         ← clean STEP + STL files
├── 3d-print/                        ← slice & print orientation configs
└── media/                           ← renderings & visual validation outputs
```
