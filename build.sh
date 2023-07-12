#!/bin/bash
find . -name "*.spec" -type f -delete
find . -name "build" -type d -exec rm -r {} +
pyinstaller --onefile -n school-net school-net.py
find . -name "*.spec" -type f -delete
find . -name "build" -type d -exec rm -r {} +
echo "Packaging completed!"