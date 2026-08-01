# Plan — Phase 1: Stackable Stand Tiers

## Overview
Implement the 3-piece modular stackable stand architecture (`Lower Stand`, `Middle Stand`, `Upper Stand`) for the 3-tier countertop slatted fruit basket using FreeCAD Python scripting.

---

## Task Group 1 — Enabling Geometry & Shared Stand Utilities
1. Define stand frame height, depth, and arm profile parameters in `params.py` (`STAND_LOWER_HEIGHT = 135 mm`, `STAND_MIDDLE_HEIGHT = 135 mm`, `STAND_UPPER_HEIGHT = 135 mm`, `ALIGNMENT_CLEARANCE = 0.4 mm`, `DOVETAIL_CLEARANCE = 0.2 mm`).
2. Implement shared cutter/joint functions for top-surface 60° dovetail slots and mortise-and-tenon interlocking alignment joints.

## Task Group 2 — Lower Stand Implementation (`part_01_stand_lower.py`)
1. Model the base stand tier (~135 mm H) with wide-stance flared feet and recessed rubber bumper pockets.
2. Construct extended cradle arms with upward-curving tips that lift continuously to hold the lower fruit bowl profile.
3. Integrate multiple top-surface precision 60° dovetail slots into cradle arms.
4. Add top male alignment pegs/tenons for stacking into Middle Stand.

## Task Group 3 — Middle Stand Implementation (`part_02_stand_middle.py`)
1. Model the middle stand tier (~135 mm H) with bottom female alignment sockets and top male alignment pegs.
2. Construct extended cradle arms with upward-curving tips matching the lower stand profile.
3. Integrate multiple top-surface precision 60° dovetail slots into cradle arms.

## Task Group 4 — Upper Stand Implementation (`part_03_stand_upper.py`)
1. Model the upper stand tier (~135 mm H) with bottom female alignment sockets.
2. Construct extended cradle arms with upward-curving tips.
3. Integrate multiple top-surface precision 60° dovetail slots into cradle arms.

## Task Group 5 — Vertical Stack Assembly & FreeCAD MCP Validation
1. Assemble left and right stand frames in `assembly.py` for all 3 tiers.
2. Run `export_all.py` to generate STEP and STL files for each stand component and stand assembly.
3. Validate 3-tier vertical stack alignment, multi-view rendering, and 0.0 mm³ Boolean interference via FreeCAD MCP Server.
