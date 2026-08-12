Write-Host "Running Python PIP Install..."

# Go to project root (one level above bin/)
$projectRoot = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $projectRoot
Write-Host "Now in: $PWD"

# Set PYTHONPATH to ensure root is in path
$env:PYTHONPATH = "$PWD"

# This will install all depedencies if you do not have
python -m pip install -r requirements.txt

# This will install dev dependencies if you do not have
python -m pip install -r requirements-dev.txt