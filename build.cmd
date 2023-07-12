@echo off
del /S /Q *.spec
rmdir /S /Q build
pyinstaller --onefile --icon logo.ico -n school-net school-net.py
del /S /Q *.spec
rmdir /S /Q build
echo Packaging completed!
cmd /K