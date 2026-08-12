#!/bin/bash
TESTING_TOOL="unittest"
USE_COVERAGE="false"
python_version="3.13" # Python accesses different versions like this: py -3.13; py -3.12; py -3.10

# Read the input:
# If we past --testing=pytest -> then we test with pytest
# else we test with --testing=unittest
while [[ "$#" -gt 0 ]]; do
	case $1 in
		--testing=*) TESTING_TOOL="${1#*=}"; shift ;;
		--use-coverage) USE_COVERAGE="true"; shift ;;
		--python_version=*) python_version="${1#*=}"; shift ;;
		*) echo "Unknown parameter passed: $1"; exit 1 ;;
	esac
done

# Log that we write tests
echo "🔍 Running Python Unit Tests (Git Bash)..."

# Move to the project root directory (one level above this script)
cd "$(dirname "$0")/.." || exit 1

# Set PYTHONPATH to include the src directory
export PYTHONPATH="$PWD/tomodachi"
echo "📁 PYTHONPATH set to: $PYTHONPATH"

case "$python_version" in 
	3.12|3.13|3.11)
		;;
	*)
		echo "Failed to run tests! Please the Python version as in: --python_version=3.12"
esac

if [[ "$(uname -s)" == MINGW* || "$(uname -s)" == CYGWIN* ]]; then
    PYTHON_CMD="py -$python_version"
else
    PYTHON_CMD="python3"
fi

# Run tests with coverage if specified

if [[ "$TESTING_TOOL" == "pytest" ]]; then
    if [[ "$USE_COVERAGE" == "true" ]]; then
        echo "Running tests with coverage..."
        $PYTHON_CMD -m pytest \
            --cov=tomodachi_core/tomodachi \
            --cov-report=html \
            --cov-report=term-missing \
            tomodachi_core/tomodachi/tests \
            --junitxml=test-reports/report.xml
    else
        echo "Running tests with pytest..."
        $PYTHON_CMD -m pytest -v --disable-warnings \
            tomodachi_core/tomodachi/tests \
            --junitxml=test-reports/report.xml
    fi
elif [[ "$TESTING_TOOL" == "unittest" ]]; then
    echo "Running tests with unittests..."
    $PYTHON_CMD -m unittest discover -s tomodachi_core/tomodachi/tests -p "test_*.py"
else
    echo "❌ Invalid testing tool specified: $TESTING_TOOL"
    exit 1
fi

# Log the results
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed."
    exit 1
fi

# if not executable:
# run this bash script before running tests
# chmod +x bin/run_unittests.sh 
