# PowerShell build script
Write-Host "Building Modkit Automod with Nuitka..." -ForegroundColor Green

# Clean previous builds
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

# Install and build
Write-Host "Installing dependencies..." -ForegroundColor Yellow
uv sync --dev

Write-Host "Building executable with Nuitka..." -ForegroundColor Yellow
uv run python build_config.py

# Test
Write-Host "Testing executable..." -ForegroundColor Yellow
& "dist\modkit-automod.exe" --version

Write-Host "Build completed! Check dist\ folder." -ForegroundColor Green
