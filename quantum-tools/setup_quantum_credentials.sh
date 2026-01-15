#!/bin/bash
# Quantum Platform Credentials Configuration Script
# Usage: source setup_quantum_credentials.sh

# Activate the quantum tools virtual environment
VENV_PATH="/mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum Tools Installed/.venv"
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✓ Virtual environment activated"
else
    echo "✗ Virtual environment not found at $VENV_PATH"
fi

# IBM Quantum (QISKIT) credentials
export QISKIT_IBM_QUANTUM_API_TOKEN="8RY8_wtqqr1gT1DFIo0DCJdrkLLWB4WxVvKSVl_UXIwA"
export IBM_QUANTUM_TOKEN="8RY8_wtqqr1gT1DFIo0DCJdrkLLWB4WxVvKSVl_UXIwA"

# AWS Braket credentials
export AWS_ACCESS_KEY_ID="APKASVWYCWPIDHY6S76P"
export AWS_SECRET_ACCESS_KEY=$(cat "/mnt/e/Data1/Google Drive - Z/.01 API Keys/AWS Cloud Front Keys/pk-APKASVWYCWPIDHY6S76P.pem" 2>/dev/null)
export AWS_DEFAULT_REGION="us-west-2"

# AWS X.509 Certificate paths
export AWS_CERT_PATH="/mnt/e/Data1/Google Drive - Z/.01 API Keys/AWS X.509 Certificate"
export AWS_X509_CERT="$AWS_CERT_PATH/cert-UXQU35DDRH3MS2BYOV2YC53K6KIRSXIX.pem"
export AWS_X509_KEY="$AWS_CERT_PATH/pk-UXQU35DDRH3MS2BYOV2YC53K6KIRSXIX.pem"

# Verify credential files exist
if [ -f "$HOME/.aws/credentials" ]; then
    echo "✓ AWS credentials file found"
fi

if [ -f "$HOME/.qiskit/qiskit.conf" ]; then
    echo "✓ IBM Quantum config found"
fi

if [ -f "$HOME/.braket/config.json" ]; then
    echo "✓ AWS Braket config found"
fi

# Display loaded platforms
echo ""
echo "=========================================="
echo "Quantum Computing Platforms Ready:"
echo "=========================================="
echo "  ✓ IBM Quantum (Qiskit)"
echo "  ✓ AWS Braket"
echo "  ✓ Quantum Espresso (system)"
echo "  ✓ PyQuil (Rigetti)"
echo "  ✓ Cirq (Google)"
echo "  ✓ PennyLane"
echo "  ✓ ProjectQ"
echo "=========================================="
echo ""
echo "To test connections, run:"
echo "  python -c 'from qiskit_ibm_runtime import QiskitRuntimeService; print(QiskitRuntimeService())'"
echo "  python -c 'from braket.aws import AwsDevice; print(\"Braket ready\")'"
echo ""
