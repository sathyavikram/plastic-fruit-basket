# Plan — Phase 3: 3-Piece Split Side Stand Frames (`part_02`, `part_03`, `part_04`)

## Task Group 1: Lower Leg Section (`part_02_stand_lower_leg.py`)
1. Create `part_02_stand_lower_leg.py` importing `params.py`.
2. Model wide-stance lower foot leg (~135 mm H):
   - Integrated flared base pads with $1.0\text{ mm}$ deep recessed pockets for adhesive rubber bumper pads ($15\text{ mm} \times 15\text{ mm}$).
   - 2 crossbar mounting bosses ($24\text{ mm}$ OD, $13\text{ mm}$ M12 clearance bore) at front-bottom and rear-bottom positions.
   - Organic forward-curved cradle arms for the bottom large oval bowl (`TRAY_LARGE`).
   - Top joint interface: dual rectangular mortise tenon alignment pegs ($8\text{ mm} \times 12\text{ mm} \times 10\text{ mm}$ height) with `FIT_CLEARANCE = 0.4 mm`.
3. Export `exports/part_02_stand_lower_leg.step` and `.stl`.

## Task Group 2: Middle Leg Section (`part_03_stand_middle_leg.py`)
1. Create `part_03_stand_middle_leg.py` importing `params.py`.
2. Model middle S-curve leg section (~135 mm H):
   - Bottom joint interface: female mortise sockets matching `part_02` tenons.
   - 1 middle crossbar mounting boss ($24\text{ mm}$ OD, $13\text{ mm}$ bore).
   - Middle cradle arms for the medium oval bowl (`TRAY_MEDIUM`).
   - Top joint interface: male tenon alignment pegs with `FIT_CLEARANCE = 0.4 mm`.
3. Export `exports/part_03_stand_middle_leg.step` and `.stl`.

## Task Group 3: Upper Leg Section (`part_04_stand_upper_leg.py`)
1. Create `part_04_stand_upper_leg.py` importing `params.py`.
2. Model upper leg section (~135 mm H):
   - Bottom joint interface: female mortise sockets matching `part_03` tenons.
   - 1 top crossbar mounting boss ($24\text{ mm}$ OD, $13\text{ mm}$ bore).
   - Upper cradle arms for the small top oval bowl (`TRAY_SMALL`).
   - Smooth tapered peak crown termination.
3. Export `exports/part_04_stand_upper_leg.step` and `.stl`.

## Task Group 4: Verification & MCP Server Inspection
1. Run `./run.sh` on `part_02`, `part_03`, `part_04` to confirm zero Python tracebacks or CAD kernel errors.
2. Execute FreeCAD MCP Server validation:
   - Multi-view burst rendering via `render_freecad_script`.
   - Cross-section cut inspection via `section_freecad_model` to verify mortise-and-tenon fit clearances.
   - Interference collision check via `check_interference` between stackable leg sections.
