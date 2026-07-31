import os
import sys
import glob
import importlib

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

import params
importlib.reload(params)


def run_all():
    """
    Finds and runs all part_*.py scripts and assembly.py to regenerate all STEP + STL exports.
    """
    print("=== Starting export_all.py ===")
    
    # 1. Discover all part_*.py scripts in order
    part_files = sorted(glob.glob(os.path.join(CURRENT_DIR, "part_*.py")))
    
    for part_path in part_files:
        mod_name = os.path.basename(part_path)[:-3]
        print(f"--> Exporting: {mod_name}...")
        try:
            mod = importlib.import_module(mod_name)
            importlib.reload(mod)
            if hasattr(mod, "main"):
                mod.main()
        except Exception as e:
            print(f"Error running {mod_name}: {e}")

    # 2. Rebuild full assembly
    if os.path.exists(os.path.join(CURRENT_DIR, "assembly.py")):
        print("--> Rebuilding full assembly...")
        
        try:
            import part_01_crossbar
            import part_05_threaded_pin
            importlib.reload(part_01_crossbar)
            importlib.reload(part_05_threaded_pin)

            mod = importlib.import_module("assembly")
            importlib.reload(mod)
            if hasattr(mod, "main"):
                mod.main()
        except Exception as e:
            print(f"Error running assembly.py: {e}")

    print("=== All exports completed successfully! ===")


if __name__ == "__main__":
    run_all()
else:
    run_all()
