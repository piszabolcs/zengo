<#
.SYNOPSIS
  A Zengő hordozható mappájának összeállítása: Zengo.exe indító, Python futtatók, venvek, modellek, ffmpeg.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\scripts\build_portable.ps1
  powershell -ExecutionPolicy Bypass -File .\scripts\build_portable.ps1 -Dest D:\Zengo -EnginesFrom F:\masik\felolvaso

.NOTES
  Előfeltétel: a forrásmappában `uv sync` lefutott, a motor venvek (engines\f5, engines\piper) és a modellek
  (setup.ps1) megvannak. A célmappát frissíti (robocopy /MIR), a data\ alatti felhasználói adatokat nem törli.
#>
[CmdletBinding()]
param(
    [string]$Dest = "",
    [string]$EnginesFrom = "",   # ahonnan a motor venveket vesszük (alapértelmezés: ez a mappa)
    [string]$ModelsFrom = "$env:LOCALAPPDATA\Felolvaso\models"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
if (-not $Dest) { $Dest = Join-Path $Root "dist\Zengo" }
if (-not $EnginesFrom) { $EnginesFrom = $Root }

function Step($t) { Write-Host "`n==> $t" -ForegroundColor Cyan }
function Fail($t) { Write-Host "HIBA: $t" -ForegroundColor Red; exit 1 }
function Mirror($from, $to, [string[]]$xd = @(), [string[]]$xf = @()) {
    $args = @($from, $to, "/MIR", "/NFL", "/NDL", "/NJH", "/NJS", "/NP", "/R:1", "/W:1")
    if ($xd) { $args += "/XD"; $args += $xd }
    if ($xf) { $args += "/XF"; $args += $xf }
    & robocopy @args | Out-Null
    if ($LASTEXITCODE -ge 8) { Fail "robocopy: $from -> $to ($LASTEXITCODE)" }
}
function VenvHome($venv) {
    $line = Get-Content (Join-Path $venv "pyvenv.cfg") | Where-Object { $_ -match '^\s*home\s*=' } | Select-Object -First 1
    $h = ($line -split '=', 2)[1].Trim()
    $item = Get-Item $h
    if ($item.LinkType) { return [string]$item.Target } else { return $item.FullName }
}
function VenvVer($venv) {
    $line = Get-Content (Join-Path $venv "pyvenv.cfg") | Where-Object { $_ -match '^\s*version_info\s*=' } | Select-Object -First 1
    $p = (($line -split '=', 2)[1].Trim()) -split '\.'
    return "py$($p[0])$($p[1])"
}

New-Item -ItemType Directory -Force $Dest | Out-Null
$skip = @("__pycache__", ".pytest_cache", ".ruff_cache")

Step "Forrás"
Mirror "$Root\app" "$Dest\app" $skip
foreach ($f in @("pyproject.toml", "README.md")) { Copy-Item "$Root\$f" $Dest -Force }
Copy-Item "$Root\app\web\static\zengo.ico" "$Dest\zengo.ico" -Force
New-Item -ItemType Directory -Force "$Dest\engines" | Out-Null
foreach ($f in @("prosody.py", "worker_base.py")) { Copy-Item "$Root\engines\$f" "$Dest\engines" -Force }

Step "Fő Python környezet"
$mainVenv = "$Root\.venv"
if (-not (Test-Path "$mainVenv\Scripts\pythonw.exe")) { Fail "Nincs .venv: futtasd az 'uv sync'-et." }
Mirror $mainVenv "$Dest\.venv" $skip
# a fejlesztői (szerkeszthető) telepítés a forrásmappára mutatna; a hordozható app a saját mappájából fut
Get-ChildItem "$Dest\.venv\Lib\site-packages" -Filter "_editable_impl_felolvaso*" | Remove-Item -Force
$runtimes = @{}
$runtimes[(VenvVer $mainVenv)] = VenvHome $mainVenv

Step "Motorok (F5, Piper)"
foreach ($e in @("f5", "piper", "dummy")) {
    $src = Join-Path $EnginesFrom "engines\$e"
    if (-not (Test-Path $src)) { Fail "Hiányzó motor: $src" }
    Mirror $src "$Dest\engines\$e" ($skip + @(".venv"))
    if (Test-Path "$Root\engines\$e") { Mirror "$Root\engines\$e" "$Dest\engines\$e" ($skip + @(".venv")) }
    if (Test-Path "$src\.venv") {
        Mirror "$src\.venv" "$Dest\engines\$e\.venv" $skip
        $runtimes[(VenvVer "$src\.venv")] = VenvHome "$src\.venv"
        # az uv indítója a gépen lévő Python teljes útját égeti be; a szabványos venv-indító a pyvenv.cfg
        # "home" sorát követi, amit a Zengo.exe minden indításkor a mappához igazít
        foreach ($x in @("python.exe", "pythonw.exe")) {
            Copy-Item "$Dest\.venv\Scripts\$x" "$Dest\engines\$e\.venv\Scripts\$x" -Force
        }
    }
}

Step "Python futtatók"
foreach ($k in $runtimes.Keys) {
    Write-Host "-- $k <- $($runtimes[$k])"
    Mirror $runtimes[$k] "$Dest\runtime\$k" ($skip + @("site-packages", "Scripts", "Doc", "test", "tests", "idlelib", "turtledemo", "tcl"))
    New-Item -ItemType Directory -Force "$Dest\runtime\$k\Lib\site-packages" | Out-Null
}

Step "ffmpeg"
$ff = (Get-Command ffmpeg -ErrorAction SilentlyContinue).Source
if (-not $ff) {
    $ff = (Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin\ffmpeg.exe" -ErrorAction SilentlyContinue |
           Select-Object -First 1).FullName
}
if (-not $ff) { Fail "Az ffmpeg nem található." }
New-Item -ItemType Directory -Force "$Dest\runtime\ffmpeg" | Out-Null
foreach ($b in @("ffmpeg.exe", "ffprobe.exe")) { Copy-Item (Join-Path (Split-Path $ff) $b) "$Dest\runtime\ffmpeg" -Force }

Step "Modellek"
foreach ($m in @("f5_hu", "vocos", "whisper-large-v3-turbo", "piper_hu")) {
    if (-not (Test-Path "$ModelsFrom\$m")) { Fail "Hiányzó modell: $ModelsFrom\$m" }
    Mirror "$ModelsFrom\$m" "$Dest\data\models\$m"
}

Step "Indító (Zengo.exe)"
$csc = Join-Path $env:WINDIR "Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if (-not (Test-Path $csc)) { Fail "Nincs csc.exe (.NET Framework 4)." }
& $csc /nologo /target:winexe /optimize+ /codepage:65001 "/win32icon:$Root\app\web\static\zengo.ico" `
    "/out:$Dest\Zengo.exe" /reference:System.Windows.Forms.dll "$Root\launcher\Zengo.cs"
if ($LASTEXITCODE -ne 0) { Fail "A Zengo.exe fordítása nem sikerült." }

$size = (Get-ChildItem $Dest -Recurse -File -Force | Measure-Object Length -Sum).Sum / 1GB
Write-Host ("`nKész: {0}  ({1:N1} GB)" -f $Dest, $size) -ForegroundColor Green
