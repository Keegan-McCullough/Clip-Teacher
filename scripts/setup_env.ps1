<#
.SYNOPSIS
  Setup development environment for Clip-Teacher on Windows (PowerShell).

.DESCRIPTION
  Creates a Python virtual environment (venv), upgrades pip, installs CPU PyTorch
  + torchaudio, then installs the remaining requirements from `requirements.txt`
  while excluding `torch`, `torchaudio`, and `torchvision` entries to avoid
  dependency conflicts. Optionally attempts to install ffmpeg via winget.

USAGE
  .\scripts\setup_env.ps1            # default: CPU PyTorch, no ffmpeg install
  .\scripts\setup_env.ps1 -InstallFFmpeg  # attempt to install ffmpeg via winget

PARAMETERS
  -UseGPU (switch): Not implemented automatically. If you have a CUDA GPU,
    install matching PyTorch wheels manually (see PyTorch docs) and then run
    the rest of this script (or run without installing CPU PyTorch).

  -InstallFFmpeg (switch): If provided, the script will try to install ffmpeg
    using winget. If winget is unavailable, it will print manual instructions.
#>

[CmdletBinding()]
param(
    [switch]$UseGPU = $false,
    [switch]$InstallFFmpeg = $false
)

Set-StrictMode -Version Latest

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not on PATH. Install Python 3.11+ and re-run this script."
    exit 1
}

if (-Not (Test-Path ".\venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
} else {
    Write-Host "Using existing virtual environment at .\venv"
}

Write-Host "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

Write-Host "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

if ($UseGPU) {
    Write-Host "GPU install requested. This script will NOT automatically install GPU PyTorch wheels."
    Write-Host "Please follow https://pytorch.org/get-started/locally/ to install the correct CUDA-enabled wheel for your system, then re-run this script (without the CPU install)."
} else {
    Write-Host "Installing CPU PyTorch and torchaudio (torch==2.5.1+cpu, torchaudio==2.5.1)..."
    pip install --index-url https://download.pytorch.org/whl/cpu torch==2.5.1+cpu torchaudio==2.5.1 --extra-index-url https://pypi.org/simple
}

Write-Host "Installing remaining Python dependencies from requirements.txt (excluding torch/torchaudio/torchvision)..."
$reqs = Get-Content requirements.txt | Where-Object { $_ -and ($_ -notmatch '^(torch|torchaudio|torchvision)') }
$tmp = [System.IO.Path]::Combine($env:TEMP, "clip_teacher_reqs_no_torch.txt")
$reqs | Out-File -Encoding utf8 $tmp
pip install -r $tmp
pip install python-dotenv
Remove-Item $tmp -ErrorAction SilentlyContinue

Write-Host "All Python packages installed."

if ($InstallFFmpeg) {
    if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
        Write-Host "ffmpeg already on PATH"
    } else {
        Write-Host "Attempting to install ffmpeg via winget..."
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
        } else {
            Write-Host "winget not available. Please install ffmpeg manually (Chocolatey: choco install ffmpeg -y) or download a static build from https://www.gyan.dev/ffmpeg/builds/ and add it to PATH."
        }
    }
}

Write-Host "Done. To activate the venv in a new shell run: .\venv\Scripts\Activate.ps1"
Write-Host "Then run the app: python app.py --force"
