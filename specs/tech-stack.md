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
2. **`freecad-fits-tolerances`**: Defines clearances for sliding joints (`0.4 mm`), press/glue fits (`0.2 mm`), interlocking dovetail keys, and mortise-and-tenon alignment pegs.
3. **`freecad-threading`**: Governs 3D-printable M12 × 2.5 mm male and female threads via `Part.makeHelix` and `makePipeShell` with `THREAD_CLEARANCE = 0.6 mm` subtracted from male outer radii.
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
| Thread clearance | 0.6 mm (`THREAD_CLEARANCE`) |
| Press fit tolerance | 0.2 mm |
| Min structural wall | 3.5 mm (4 perimeter loops) |
| Overhang limit | ≤ 45° without support |

## Fit Parameters (canonical — defined in `params.py`)

| Parameter | Value |
|---|---|
| `FIT_CLEARANCE` | 0.4 mm (sliding joints & pin sockets) |
| `THREAD_CLEARANCE` | 0.6 mm (subtracted from male thread radii) |
| `SCREW_THREAD_DIAMETER` | 12.0 mm (M12 × 2.5 mm fat 3D-printable screw) |
| `THREAD_PITCH` | 2.5 mm (coarse profile for smooth supportless FDM printing) |
| `CROSSBAR_DIAMETER` | 18.0 mm (gives 3.0 mm solid wall thickness around M12 threads) |
| `CROSSBAR_LENGTH` | 170.0 mm (fits flat on 175 mm bed limit) |
| `FRAME_THICKNESS` | 20.0 mm (24 mm reinforced boss around M16 screw seats) |
| `WALL_THICKNESS` | 3.5 mm (main shell wall thickness) |
| `DOVETAIL_CLEARANCE`| 0.2 mm (interlocking tray split key) |

## Dimensions — Scaled 375 mm Variant (canonical model)

| Dimension | Imperial | Metric (mm) |
|---|---|---|
| Total Stand Height | 14.8" | 375 mm |
| Total Base Depth | 6.3" | 160 mm |
| Total Stand Width | 12.6" | 320 mm |
| Small Tray (Top) W × D × H | 8.9" × 6.5" × 2.2" | 225 × 165 × 57 mm |
| Medium Tray (Middle) W × D × H | 10.2" × 7.3" × 2.5" | 260 × 185 × 63 mm |
| Large Tray (Bottom) W × D × H | 12.6" × 8.2" × 2.7" | 320 × 208 × 68 mm |
| Frame Tier Angle | ~65° | 65° incline |

## File & Folder Structure

```
plastic-fruit-basket/
├── specs/                           ← project constitution (mission.md, tech-stack.md, roadmap.md)
├── params.py                        ← all dimensions + SCALE + paths
├── part_01_crossbar.py              ← 24mm OD crossbar with M16 female sockets
├── part_02_stand_lower_leg.py       ← lower leg with integrated base feet & recessed pad pockets
├── part_03_stand_middle_leg.py      ← middle S-curve leg section
├── part_04_stand_upper_leg.py       ← upper leg section
├── part_05_threaded_pin.py          ← M16 x 3.5mm fat knurled thumb screw
├── part_06_tray_small.py            ← top tray (2-piece split)
├── part_07_tray_medium.py           ← middle tray (2-piece split)
├── part_08_tray_large.py            ← bottom tray (2-piece split)
├── assembly.py                      ← full 24-part assembly script
├── export_all.py                    ← regenerates all STEP + STL exports
├── run.sh                           ← build & validation runner
├── README.md
├── .gitignore
├── exports/                         ← clean STEP + STL files
├── 3d-print/                        ← slice & print orientation configs
└── media/                           ← renderings & visual validation outputs
```
