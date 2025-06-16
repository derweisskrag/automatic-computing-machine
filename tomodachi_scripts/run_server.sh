#!/bin/bash
# Move to the project root directory (one level above this script)
cd "$(dirname "$0")/.." || exit 1

# Run the model creation
# Uncomment:
# python ./tomodachi_core/models...

# run the fast api
# Probably handle different python versions
py -3.13 -m uvicorn tomodachi_core.server.main:app --reload
