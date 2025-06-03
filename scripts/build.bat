@echo off
echo Building Modkit Automod with Nuitka...

:: Clean previous builds
if exist "dist" rmdir /s /q "dist"

:: Install dependencies
echo Installing dependencies...
uv sync --dev

:: Build with Nuitka
echo Building executable...
uv run python build_config.py

:: Test the executable
echo Testing executable...
dist\modkit-automod.exe --version

echo Build completed! Check dist\ folder.
pause
