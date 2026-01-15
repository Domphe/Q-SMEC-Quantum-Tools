#!/bin/bash
# activate_quantum_tools.sh - Quick activation script for quantum tools environment
# Usage: source activate_quantum_tools.sh

VENV_PATH="/mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum Tools Installed/.venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

source "$VENV_PATH/bin/activate"

echo ""
echo "✓ Quantum Tools Environment Activated"
echo "  Location: $VENV_PATH"
echo "  Python: $(python --version)"
echo ""
echo "Available commands:"
echo "  • jupyter lab          - Launch Jupyter Lab"
echo "  • jupyter notebook     - Launch Classic Notebook"
echo "  • ipython              - Enhanced Python shell"
echo "  • python               - Python interpreter"
echo ""
echo "To deactivate, run: deactivate"
echo ""
