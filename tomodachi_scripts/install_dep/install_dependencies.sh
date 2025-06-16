#!/bin/bash
echo "🔍 Installing Python Dependencies (Git Bash)..."

# Move to the project root directory (one level above this script)
cd "$(dirname "$0")/../.." || exit 1

# Set PYTHONPATH to include the src directory
export PYTHONPATH="$PWD/src"
echo "📁 PYTHONPATH set to: $PYTHONPATH"

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip could not be found. Please install pip to proceed."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure it exists in the project root."
    exit 1
fi

# Install dependencies from requirements.txt
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully!"
else
    echo "❌ Failed to install some dependencies."
    exit 1
fi

# install dev dependencies
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    if [ $? -eq 0 ]; then
        echo "✅ All dev dependencies installed successfully!"
    else
        echo "❌ Failed to install some dev dependencies."
        exit 1
    fi
else
    echo "⚠️ No dev dependencies found in requirements-dev.txt."
fi

