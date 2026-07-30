# Validation — Phase 1: Project Skeleton

## Required Checks

1. **`params.py` Execution Smoke Test**:
   - Run `python3 params.py`
   - **Pass Criteria**: Zero errors, zero tracebacks, process exits with code 0.

2. **Directory Structure Verification**:
   - Check presence of `exports/`, `3d-print/`, and `media/` directories.
   - **Pass Criteria**: All 3 directories exist in project root.

3. **`run.sh` Executable Check**:
   - Run `./run.sh` without arguments.
   - **Pass Criteria**: Script is executable (`chmod +x`), outputs usage menu, and exits with code 1 without syntax errors.

## Manual Review
- Confirm `params.py` starts with `SCALE = 1.0`.
- Verify `SCREW_THREAD_DIAMETER = 16.0`, `THREAD_PITCH = 3.5`, `CROSSBAR_LENGTH = 170.0`, `CROSSBAR_DIAMETER = 24.0`, and target system dimensions (375 mm H, 160 mm D, 320 mm W) are defined.

## Merge Criteria
- All required checks pass.
- Branch `feature/phase-1-project-skeleton` is ready to be committed and merged into `main`.
