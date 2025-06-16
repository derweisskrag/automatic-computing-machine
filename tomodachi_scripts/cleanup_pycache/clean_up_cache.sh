#!/bin/bash
echo "🧹 Cleaning up __pycache__ folders..."

find . -type d -name "__pycache__" -exec rm -rf {} +

echo "✅ All __pycache__ folders removed!"
