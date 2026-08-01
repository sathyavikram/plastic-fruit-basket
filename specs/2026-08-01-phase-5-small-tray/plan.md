# Plan

## Task Group 1: Parametric Shell Construction
1. Define the Small Tray boundary parameters (225 mm W, 165 mm D, 57 mm H).
2. Generate the outer boat-shaped oval profile (e.g. using sweeping lofts or thick solid primitives).
3. Hollow the shape using the 3.5 mm wall thickness to create the flat bottom and smooth walls.

## Task Group 2: Split and Joinery
1. Bisect the full shell along the center Y-Z plane to produce a Left Half and a Right Half.
2. Design and model the joinery:
   - 2 dovetail mortise-and-tenons.
   - 2 cylindrical alignment pegs and corresponding sockets.
3. Apply standard clearances (`FIT_CLEARANCE` for pegs, `DOVETAIL_CLEARANCE` for dovetails) to ensure an interference-free sliding/press fit.

## Task Group 3: File Export and Integration
1. Configure `part_06_tray_small.py` to generate independent meshes for the Left and Right halves.
2. Generate a full, un-split assembly mesh for visualization purposes.
3. Hook `part_06_tray_small` into `export_all.py` (and eventually `assembly.py`).

## Task Group 4: Visual Validation
1. Execute headless rendering tools.
2. Present validation artifacts (bounding box data, isometric renders, section views) for review.
