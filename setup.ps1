<#
.SYNOPSIS
  A Felolvasó telepítése: fő alkalmazás, motor workerek, modellsúlyok, GPU teszt, alapértelmezett hangok.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\setup.ps1
  powershell -ExecutionPolicy Bypass -File .\setup.ps1 -AcceptCpml -ReferenceWav .\hangom.wav -ReferenceText "A felolvasott mondat pontos szövege."

.NOTES
  Frissítéskor (git pull után) újrafuttatható; a már letöltött súlyokat nem tölti le újra.
#>
[CmdletBinding()]
param(
    [switch]$AcceptCpml,       # XTTS-v2 súlyok: Coqui Public Model License elfogadása
    [switch]$SkipModels,       # modellsúlyok letöltésének kihagyása
    [string[]]$Engines = @("piper", "f5"),  # az XTTS (CPML licenc) csak kérésre: -Engines piper,f5,xtts
    [string]$ReferenceWav = "", # minta F5 hangprofil referencia hangja (6-15 s WAV)
    [string]$ReferenceText = ""
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$env:UV_LINK_MODE = "copy"

function Step($text) { Write-Host "`n==> $text" -ForegroundColor Cyan }
function Fail($text) { Write-Host "HIBA: $text" -ForegroundColor Red; exit 1 }

# --- előfeltételek ---
Step "Előfeltételek ellenőrzése"
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Fail "Az uv nincs telepítve. Telepítés: powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`""
}
Write-Host "uv: $(uv --version)"
$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpeg) {
    $winget = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($winget) { Write-Host "ffmpeg: $($winget.FullName)" }
    else {
        Write-Host "Az ffmpeg nem található. Telepítés: winget install --id Gyan.FFmpeg -e" -ForegroundColor Yellow
    }
} else { Write-Host "ffmpeg: $($ffmpeg.Source)" }
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
} else {
    Write-Host "Nincs NVIDIA driver; az F5 és XTTS motor nem fog GPU-n futni." -ForegroundColor Yellow
}

# --- (a) fő alkalmazás ---
Step "(a) Fő alkalmazás (Python 3.12)"
uv sync --python 3.12
if ($LASTEXITCODE -ne 0) { Fail "uv sync sikertelen (fő alkalmazás)" }

# --- (b) motor workerek ---
Step "(b) Motor workerek (Python 3.11, PyTorch cu128)"
foreach ($e in $Engines) {
    Write-Host "-- engines/$e"
    Push-Location "engines\$e"
    uv sync --python 3.11
    $code = $LASTEXITCODE
    Pop-Location
    if ($code -ne 0) { Fail "uv sync sikertelen: engines/$e" }
}

# --- (c) modellsúlyok ---
if (-not $SkipModels) {
    Step "(c) Modellsúlyok letöltése"
    $only = @()
    if ($Engines -contains "piper") { $only += "piper" }
    if ($Engines -contains "f5") { $only += "f5" }
    if ($Engines -contains "xtts") {
        if (-not $AcceptCpml) {
            Write-Host "Az XTTS-v2 súlyai a Coqui Public Model License (CPML, nem kereskedelmi) alatt állnak:"
            Write-Host "  https://coqui.ai/cpml.txt"
            $answer = Read-Host "Elfogadod a licencet és letöltöd az XTTS-v2-t? (i/n)"
            if ($answer -match '^(i|igen|y|yes)$') { $AcceptCpml = $true }
        }
        if ($AcceptCpml) { $only += "xtts" } else { Write-Host "XTTS-v2 kihagyva." -ForegroundColor Yellow }
    }
    $only += "whisper"
    $dlArgs = @("run", "python", "scripts/download_models.py", "--only", ($only -join ","))
    if ($AcceptCpml) { $dlArgs += "--accept-cpml" }
    uv @dlArgs
    if ($LASTEXITCODE -ne 0) { Fail "A modellek letöltése sikertelen" }
}

# --- (d) GPU teszt ---
Step "(d) GPU teszt a GPU-s workerekben"
$gpuCheck = "import torch; ok=torch.cuda.is_available(); print('CUDA:', ok, torch.__version__); " +
            "cap=torch.cuda.get_device_capability(0) if ok else None; arch=f'sm_{cap[0]}{cap[1]}' if cap else '-'; " +
            "print('GPU:', torch.cuda.get_device_name(0) if ok else '-', arch, 'támogatott' if ok and arch in torch.cuda.get_arch_list() else 'NEM támogatott')"
foreach ($e in @("f5", "xtts")) {
    if ($Engines -notcontains $e) { continue }
    $py = "engines\$e\.venv\Scripts\python.exe"
    Write-Host "-- $e"
    & $py -c $gpuCheck
}

# --- (e) alapértelmezett hangprofilok ---
Step "(e) Alapértelmezett hangprofilok"
$voiceArgs = @("run", "python", "scripts/setup_voices.py")
# a PowerShell 5.1 az üres argumentumot elhagyja, ezért csak megadott értéket adunk át
if ($ReferenceWav) { $voiceArgs += @("--ref", $ReferenceWav, "--text", $ReferenceText) }
uv @voiceArgs
if ($LASTEXITCODE -ne 0) { Fail "A hangprofil létrehozása sikertelen" }
uv run python scripts/seed_lexicon.py
if ($LASTEXITCODE -ne 0) { Fail "A kiejtési szótár feltöltése sikertelen" }

Step "Kész. Indítás: start.bat"
