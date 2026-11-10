# Felolvasó indító: ha a szolgáltatás már fut, csak megnyitja; különben a háttérben (ablak nélkül)
# elindítja a 127.0.0.1-en, megvárja, amíg válaszol, és megnyitja a böngészőben.
#   powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File Felolvaso.ps1
param([int]$Port = 8765)
$ErrorActionPreference = "Continue"
$root = $PSScriptRoot

function Alive([int]$p) {
    try { Invoke-RestMethod "http://127.0.0.1:$p/api/health" -TimeoutSec 3 | Out-Null; return $true } catch { return $false }
}

# egy korábban más porton (pl. az éjszakai futás 8767-en) indított példányt is megtalál
foreach ($p in @($Port, 8765, 8767) | Select-Object -Unique) {
    if (Alive $p) { Start-Process "http://127.0.0.1:$p"; exit 0 }
}

$logs = Join-Path $root "logs"
New-Item -ItemType Directory -Force $logs | Out-Null
Start-Process -FilePath "uv" -ArgumentList "run", "felolvaso", "--port", "$Port" -WorkingDirectory $root `
    -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logs "server.log") `
    -RedirectStandardError (Join-Path $logs "server.err.log")
for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep -Seconds 1
    if (Alive $Port) { Start-Process "http://127.0.0.1:$Port"; exit 0 }
}
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show("A Felolvasó nem indult el. Napló: $logs\server.err.log", "Felolvasó") | Out-Null
exit 1
