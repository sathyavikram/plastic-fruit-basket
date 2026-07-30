# Requirements — Phase 1: Project Skeleton

## Scope
Set up the foundational project architecture, single source of truth (`params.py`), build runner (`run.sh`), and directory structure for the 100% 3D-printable 3-tier countertop fruit basket organizer.

## Decisions
- `SCALE = 1.0` is strictly the first statement in `params.py`.
- All dimensions are defined in millimetres and scaled proportionally with `SCALE`.
- Absolute paths are derived dynamically using `os.path.dirname(os.path.abspath(__file__))`.
- Build volume limits default to 175 × 175 × 175 mm per part.
- Runner script `run.sh` wraps FreeCAD headless (`freecadcmd`) and GUI executables.

## Constraints
- Must align 100% with `specs/mission.md` and `specs/tech-stack.md`.
- `params.py` must execute cleanly under standard Python 3 / FreeCAD environment.
- FDM tolerances (`FIT_CLEARANCE = 0.4`, `THREAD_CLEARANCE = 0.6`) must be accessible to all subsequent part scripts.

## Non-goals
- Generating 3D CAD shapes or part files in Phase 1 (handled in Phase 2+).
- Modifying project constitution files (`specs/mission.md`, `specs/tech-stack.md`, `specs/roadmap.md`).

## Context
This phase establishes the skeleton infrastructure required before constructing individual part scripts (`part_01_crossbar.py` through `part_08_tray_large.py`) and full assembly (`assembly.py`).
