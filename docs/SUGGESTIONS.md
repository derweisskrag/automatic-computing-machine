# Suggestions

## Modify Pipeline to include more tasks:

```bash
pipelines:
  default:
    - step:
        name: Run Tests
        image: python:3.9  # Use the appropriate Python version
        script:
          # Step 1: Create a logs directory and redirect output to a log file
          - mkdir -p logs
          - exec > >(tee logs/test_run_$(date +'%Y%m%d_%H%M%S').log) 2>&1

          # Step 2: Check if Python is available
          - if ! command -v python &> /dev/null; then echo "❌ Python not found in PATH. Exiting." && exit 1; fi

          # Step 3: Load environment variables from .env.testing if it exists
          - if [ -f .env.testing ]; then
                echo "Loading environment from .env.testing";
                export $(grep -v '^#' .env.testing | xargs);
            fi

          # Step 4: Run your unittest script
          - ./bin/run_unittests.sh

          # Step 5: Run pytest
          - ./bin/run_unittests.sh --testing=pytest

          # Step 6: Run pytest with coverage
          - ./bin/run_unittests.sh --testing=pytest --coverage
```

## Lua to enhance scripts

```bash
#  Template python-build

#  This template allows you to validate your python code.
#  The workflow allows running tests and code linting on the default branch.

image: python:3.13.2

pipelines:
  default:
    - parallel:
        - step:
            name: Test
            caches:
              - pip
            script:
              # Install dependencies only if requirements.txt exists
              - if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
              - if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
              - export CSV_PATH=$CSV_PATH
              - export SAVE_TO_CSV=$SAVE_TO_CSV
              - export TEST_PATH=$TEST_PATH

              # Install Lua and luarocks
              - apt-get update && apt-get install -y lua5.3 luarocks

              # Run a Lua script for additional tasks
              - luarocks install luaunit
              - lua ./scripts/prepare_env.lua

              # Run Python tests
              - chmod +x ./bin/run_unittests.sh
              - ./bin/run_unittests.sh
              - ./bin/run_unittests.sh --testing=pytest
              - pytest -v --disable-warnings tests/test_*.py --junitxml=test-reports/report.xml

              # Optionally run Lua-based tasks
              - lua ./scripts/post_test_tasks.lua

  branches:
    sergei/pre-release-tomodachi:
      - step:
          name: Pre-Release Pipeline
          caches:
            - pip
          script:
            # Install dependencies as usual
            - if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
            - if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
            - export USERNAME=$USERNAME # necessary for deploy
            - export TOKEN=$TOKEN

            # Install Lua and luarocks
            - apt-get update && apt-get install -y lua5.3 luarocks


            # Custom Lua script for pre-release logic
            - luarocks install luaunit luafilesystem 
            
            # Make them executable:
            - chmod +x ./bin/scripts/increment_version.lua
            - chmod +x ./bin/scripts/prepare_release.lua

            # Run the commands before deployment
            - ./bin/scripts/increment_version.lua  # Increment version logic
            - ./bin/scripts/prepare_release.lua    # Prepare release logic

            # Run Python tests
            - pytest -v --disable-warnings tests/test_*.py --junitxml=test-reports/report.xml

            # Build and package for deployment
            - python setup.py sdist bdist_wheel
            - twine upload --repository testpypi dist/*
```

## Git Bash CLI

