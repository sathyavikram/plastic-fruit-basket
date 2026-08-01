# Mission

## Project Purpose

Design a complete, commercially sellable **100% FDM 3D-Printable 3-Tier Countertop Slatted Fruit Basket** — a modern, slatted-bar kitchen organizer constructed entirely from 3D-printable plastic parts.

**Crucial Mandate**: **Both the side support frames AND all 3 slatted baskets are 100% 3D printable.** No external ceramic/porcelain bowls, wood/bamboo panels, metal hardware, or separate crossbars are used. The entire product — frame legs, stackable stand segments, and slat bars — is produced via 3D printing.

All parts are:
- **100% 3D Printable Modular Slatted Architecture**: Every component is designed to be printed on standard FDM 3D printers with a 175 × 175 × 175 mm build volume.
- **100% Toolless / All-Plastic Assembly**: Uses a 100% 3D-printable drop-in Dovetail Joint architecture to connect horizontal slats to vertical side frames. No screws, glue, or hardware required!
- **Sellable & Functional**: Features clean manifold geometry, filleted touch points, organic curved side ladder frames with integrated cradle arms containing flush dovetail slots on their top surface, and integrated anti-slip foot pads.

## Reference Product Specifications & 3D Printing Strategy

### Overall System Dimensions
- **Total Stand Height**: 375 mm (~14.8")
- **Total Base Depth**: 160 mm (~6.3")
- **Total Stand Width**: ~320 mm (~12.6") — *governed by the basket envelope length and slat span*.

### 1. Stands Design (100% 3D Printed Stackable Architecture)
- **Stackable Stand Tiers (Lower, Middle, Upper Stands)**: The stand architecture is split vertically into 3 stackable tiers designed to stack directly on top of each other using interlocking mortise-and-tenon and alignment peg joints:
  - **Lower Stand** (~135 mm): Base tier with integrated flared anti-slip feet.
  - **Middle Stand** (~135 mm): Center tier stacked on top of the Lower Stand.
  - **Upper Stand** (~135 mm): Top tier stacked on top of the Middle Stand.
- **Left and Right Stand Structure**: Each tier consists of a left stand frame and a right stand frame.
- **Extended Upward-Curving Cradle Arms**: Each stand frame features forward-extending cradle arms whose ends are curved and lift upwards continuously until they form the complete bowl side walls when the slats are fitted.
- **Multiple Snap-Fit Dovetail Slots on Stand Arm Top Surfaces**: Multiple precision 60-degree dovetail slots (0.2 mm clearance) are integrated directly into the *top surface* of each stand frame's cradle arms (`Lower Stand`, `Middle Stand`, `Upper Stand`) so that the slats snap fit securely into the top surface along the arm profile.

### 2. Slat Design (3 Slat Types for Curved Bowl Effect)
- **Modular Slat-Tie Basket System**: Each tier forms a curved slatted basket/bowl using 100% 3D-printable slat bars with dovetail pegs on their ends:
  - **Middle Slats**: Straight central slat rods with dovetail pegs on both ends that span across the width, directly connecting the left stand and right stand together.
  - **Left Curved Slats**: Curved boundary slat rods featuring dovetail pegs on their ends attached to the left stand, curving upwards/outwards to form the left side of the curved bowl.
  - **Right Curved Slats**: Curved boundary slat rods featuring dovetail pegs on their ends attached to the right stand, curving upwards/outwards to form the right side of the curved bowl.
  - **Curved Bowl Effect**: Combining the central connecting middle slats with the upward-sloping left and right curved slats creates a modern curved fruit bowl profile on each tier.
- **Rounded-Rectangle Slat Profile**: Slat bars feature a rounded-rectangle / stadium cross-section with flat top and bottom faces and generous filleted edge radii (~1.5–2.5 mm). This provides zero-support flat FDM 3D printing, soft bruise-free fruit care, and rigid anti-twist indexing in the dovetail slots.
- **Structural Tie-Bars (Zero Fasteners)**: The key slat bars serve as both the basket floor slats AND the structural crossbars connecting the left and right stand frames via through-dovetail joints on the stand top surface with zero screws, glue, or external hardware.

### 3. Anti-Slip Base Feet (Single Component)
- **Integrated Base Feet**: Flared, wide-stance foot pads are integrated directly into the bottom of the lower stand legs (`Lower Stand`) as single monolithic 3D-printed parts.
- **Surface Feature**: Bottom face of each leg foot features a chamfered contact rim and a recessed pocket for optional adhesive rubber/silicone bumper pads.

## Parametric Scaling Architecture

The model is 100% parametrically driven by a global scale multiplier:
- Default 1.0 scale (target: 375 mm H, 160 mm D, 320 mm W).
- Changing the scale factor (e.g., 0.8, 1.0, 1.2) automatically scales all part dimensions proportionally in a single update.
- Fit tolerances (0.4 mm sliding clearance, 0.2 mm dovetail clearance) remain calibrated so mating parts fit cleanly regardless of the selected scale.

## Target Customer

Makers, 3D printing enthusiasts, and home organizers looking for a sleek, modular, and 100% 3D-printable kitchen storage solution.

## Success Criteria

- **Complete 3D Printability**: Both the frame structure (legs) AND all 3 slatted baskets are 100% 3D printed with zero non-printable parts.
- **Parametric Scalability**: Modifying the scale factor resizes all components in total geometric alignment.
- **Bed Volume Compliance**: Every individual part fits within the 175 × 175 × 175 mm FDM build volume at the default 1.0 scale.
- **Manifold Topology**: All exported STL files pass 100% manifold validation with zero non-manifold edges or self-intersections.
- **Dimensional Fidelity**: Assembled model matches target canonical reference dimensions (375 mm H, 160 mm D, 320 mm W at the default 1.0 scale) within ±1.0 mm.
- **Automated CAD Generation**: The CAD models and assemblies can be generated cleanly from source without manual GUI intervention or boolean failures.
- **Visual & Interference Validation**: All parts and full assembly pass multi-view rendering, exploded dimension checks, section cut inspections, and 0.0 mm³ interference clearance validation.
- **CAD Deliverables**: Parametric STEP (AP214) and binary STL files generated for all individual parts and full assembly.