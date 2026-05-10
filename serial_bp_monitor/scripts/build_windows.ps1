# Build single-file executable (BPSerialMonitor.exe) with PyInstaller.
# Must run on Windows. Use Python from python.org (includes tkinter).
$AppDir = Split-Path -Parent $PSScriptRoot
Set-Location $AppDir

python -m pip install -r requirements.txt -r requirements-packaging.txt
python -m PyInstaller --noconfirm serial_bp_monitor.spec

$Exe = Join-Path $AppDir "dist\BPSerialMonitor.exe"
if (-not (Test-Path $Exe)) {
    Write-Error "Expected executable not found: $Exe"
    exit 1
}
Write-Host ""
Write-Host "Built: $Exe"
Write-Host "Distribute dist\BPSerialMonitor.exe (single portable executable)."
