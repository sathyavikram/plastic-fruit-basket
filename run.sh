#!/bin/zsh
FREECAD_CMD="/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
FREECAD_GUI="/Applications/FreeCAD.app/Contents/MacOS/FreeCAD"

if [[ $# -eq 0 ]]; then
    echo "Usage:"
    echo "  ./run.sh <part_file.py>   Run a part script headlessly"
    echo "  ./run.sh export_all       Regenerate all parts"
    echo "  ./run.sh assembly         Build full assembly"
    echo "  ./run.sh open <name>      Open exports/<name>.step in GUI"
    exit 1
fi

case "$1" in
    open)
        [[ -z "$2" ]] && { echo "Error: specify a name"; exit 1; }
        "$FREECAD_GUI" "exports/$2.step" ;;
    assembly)   "$FREECAD_CMD" -c "import sys; sys.path.insert(0, '.'); import assembly; assembly.main()" ;;
    export_all) "$FREECAD_CMD" -c "import sys; sys.path.insert(0, '.'); import export_all; export_all.run_all()" ;;
    *.py)       mod="${1%.py}"; "$FREECAD_CMD" -c "import sys; sys.path.insert(0, '.'); import $mod; $mod.main()" ;;
    *)          echo "Unknown command: $1"; exit 1 ;;
esac
