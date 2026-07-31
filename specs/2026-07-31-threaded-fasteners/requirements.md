# Requirements

## Scope
Implement the threaded fastener (`part_05_threaded_pin.py`) used to lock the 3D-printed side stand frames to the horizontal crossbars.

## Decisions
- **Thread Profile:** M12 × 2.5 mm coarse thread, generated via `freecad-threading`.
- **Clearance:** 0.6 mm diametral thread clearance (`THREAD_CLEARANCE = 0.6 mm`), subtracted from the male thread dimensions to ensure a smooth, self-supporting fit.
- **Shaft Profile:** Fully threaded shaft (easier to print/design).
- **Shaft Length:** Calculated exactly based on the side panel thickness and crossbar hole depth (e.g., side frame thickness + crossbar hole depth minus ~2mm).
- **Head Design:** 24 mm ergonomic knurled head, 8 mm thickness, featuring 12 large scalloped knurls for a finger-friendly grip.

## Constraints
- Must be 100% 3D printable without supports (60° self-supporting overhangs for threads).
- Must scale dynamically with `params.SCALE`.
- Must fit cleanly inside the 175 × 175 × 175 mm bed limit.

## Non-goals
- Do not implement custom hex sockets or flathead screwdriver slots; thumb-tightening via the knurled head is the sole method.
- Do not add unthreaded shaft sections.

## Context
These pins replace the metal screws seen in the reference images to ensure the final product is 100% toolless and 3D printable.
