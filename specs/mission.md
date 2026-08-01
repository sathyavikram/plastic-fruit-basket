# Mission

## Project Purpose

Design a complete, commercially sellable **100% FDM 3D-Printable 3-Tier Countertop Organizer & Fruit Basket** — a faithful replica of the bamboo frame & white oval bowl kitchen organizer shown in the reference images (`specs/reference-images/`), re-engineered entirely into 3D-printable plastic parts.

**Crucial Mandate**: **Both the support frame AND all 3 serving bowls/trays must be 100% 3D printable.** No external ceramic/porcelain bowls, wood/bamboo panels, or metal hardware are used. The entire product — frame legs, crossbars, thumb screws, and all 3 oval bowls — is produced via 3D printing.

All parts must be:
- **100% 3D Printable Frame & Bowls**: Every component is designed to be printed on standard FDM 3D printers with a 175 × 175 × 175 mm build volume. Larger components (both frame sections and larger bowls) are split into interlocking segments with precision joinery (dovetails, alignment dowels/pegs, and threaded fasteners).
- **100% Toolless / All-Plastic Assembly**: Replaces the metal screws and screwdriver of the reference product (`specs/reference-images/3.jpg`) with 3D-printable threaded thumb screws and internal crossbar thread sockets.
- **Sellable & Functional**: Features clean manifold geometry, filleted touch points, smooth boat-shaped oval serving bowls, organic curved side ladder frames with cradle arms, and optional anti-slip foot caps.

## Reference Product Specifications & 3D Printing Strategy

Based on reference images (`specs/reference-images/1.jpg`, `2.jpg`, `3.jpg`) and product design specs:

### 1. Overall System Dimensions
- **Total Stand Height**: 375 mm (~14.8")
- **Total Base Depth**: 160 mm (~6.3")
- **Total Stand Width**: ~320 mm (~12.6") — *governed by the Large Bottom Bowl envelope length and crossbar span*.

### 2. Removable Slatted Bar Baskets (3 Tiers — All 3D Printed, Zero Split Seams)
- **Modular Slatted Basket Architecture**: Instead of large solid plastic bowls split down the middle, each tier is constructed from a modern slatted bar basket composed of 100% 3D-printable individual slat bars trapped inside blind sockets:
  - **Center Straight Slats (`part_06_slat_straight.py`)**: Straight horizontal slat rods spanning across the stand width between left and right cradle arms.
  - **Left & Right Curved Side Slats (`part_07_slat_curved.py`)**: Slat bars that run straight across the center floor and curve smoothly upward at both ends to form the side retaining walls of the basket.
  - **Option B Captured Sandwich Sockets**: Deep 10.0 mm blind cylindrical sockets (`FIT_CLEARANCE = 0.4 mm`) cut into the *inside face* of each cradle arm. Tightening the 4 main M12 thumb screws clamps the stand frames together, permanently locking all slats in place with zero rattle and 100% smooth, continuous top cradle arm surfaces.

### 3. Side Support Frames & Cradle Arms (100% 3D Printed)
- **2 Side Frames (Left & Right — Printed)**: Organic, S-curved vertical side panels with 3 pairs of integrated forward-extending curved cradle arms that securely hold each tier of 3D-printed oval bowls.
- **Modular Split Frame Construction**: Total height of 375 mm exceeds the 175 mm build height limit; each side frame is split into 3 stackable interlocking sections (`Lower Leg` ~135 mm, `Middle Segment` ~135 mm, `Upper Segment` ~135 mm) connected via mortise-and-tenon and alignment peg joints.

### 4. Crossbars & Fasteners (100% 3D Printed)
- **4 Round Support Rods / Crossbars (Printed)**: Length 170 mm (fits flat on 175 mm bed), 18 mm outer diameter; connects left and right side frames (2 at the base for wide-stance stability, 2 along the vertical structure).
- **Large Fat Threaded Fasteners (Printed)**: **M12 × 2.5 mm coarse thread** thumb screws with a 24 mm ergonomic knurled head.
  - **Why M12 × 2.5 mm**: 12 mm shaft diameter provides high shear strength, and 2.5 mm pitch creates deep, self-supporting 60° thread teeth that print cleanly with a standard 0.4 mm nozzle without support structures or binding (0.6 mm diametral clearance).

### 5. Integrated Anti-Slip Base Feet (Single Component)
- **Integrated Base Feet**: Flared, wide-stance foot pads are integrated directly into the bottom of the lower stand legs (`Lower Leg`) as single monolithic 3D-printed parts — eliminating separate snap-on caps.
- **Surface Feature**: Bottom face of each leg foot features a chamfered contact rim and a recessed pocket for optional adhesive rubber/silicone bumper pads.

## Parametric Scaling Architecture (`SCALE`)

The model is 100% parametrically driven by a global `SCALE` variable defined in `params.py`:
- `SCALE = 1.0` (default target: 375 mm H, 160 mm D, 320 mm W).
- Changing `SCALE` (e.g., `0.8`, `1.0`, `1.2`) automatically scales all part dimensions — bowl lengths/widths/heights, frame section heights, crossbar lengths/diameters, screw sizes, thread pitches, and dovetail keys — proportionally in a single update.
- Fit tolerances (`FIT_CLEARANCE = 0.4 mm`, `THREAD_CLEARANCE = 0.6 mm`) remain calibrated so mating parts fit cleanly regardless of the selected `SCALE`.

## Target Customer

Makers, 3D printing enthusiasts, and home organizers looking for a sleek, modular, and 100% 3D-printable kitchen storage solution.

## Success Criteria

- **Complete 3D Printability**: Both the frame structure (legs, crossbars, fasteners) AND all 3 bowls are 100% 3D printed with zero non-printable parts.
- **Parametric Scalability**: Modifying `SCALE` in `params.py` resizes all components, bowls, crossbars (18 mm OD), and screws (M12) in total geometric alignment.
- **Bed Volume Compliance**: Every individual part fits within the 175 × 175 × 175 mm FDM build volume at `SCALE = 1.0`.
- **Manifold Topology**: All exported STL files pass 100% manifold validation with zero non-manifold edges or self-intersections.
- **Dimensional Fidelity**: Assembled model matches target canonical reference dimensions (375 mm H, 160 mm D, 320 mm W at `SCALE = 1.0`) within ±1.0 mm.
- **Python Execution & Error Handling**: All Python scripts (`params.py`, `part_*.py`, `assembly.py`) execute cleanly headlessly via FreeCAD MCP Server with zero syntax errors, zero tracebacks, and zero OpenCASCADE CAD kernel boolean failures.
- **Visual & Interference Validation**: All parts and full assembly pass multi-view rendering (`render_freecad_script`), exploded dimension check (`inspect_freecad_assembly`), section cut inspection (`section_freecad_model`), and 0.0 mm³ interference clearance validation (`check_interference`) via FreeCAD MCP Server.
- **CAD Deliverables**: Parametric STEP (AP214) and binary STL files generated for all individual parts and full assembly.