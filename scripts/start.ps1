# Start the AION platform from the project root (not the frontend folder).
param(
    [switch]$Gpu,
    [switch]$HostOllama,
    [switch]$Build
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$composeArgs = @("-f", "docker-compose.yml")
if ($Gpu) { $composeArgs += @("-f", "docker-compose.gpu.yml") }
if ($HostOllama) { $composeArgs += @("-f", "docker-compose.host-ollama.yml") }

$upArgs = @("compose") + $composeArgs + @("up", "-d", "--remove-orphans")
if ($Build) { $upArgs += "--build" }

Write-Host "Starting AION from $ProjectRoot ..."
& docker @upArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Banking UI:  http://localhost:8501"
    Write-Host "API health:  http://localhost:8000/health"
    Write-Host ""
    Write-Host "Run tests (stack must be UP — do not run 'docker compose down' first):"
    Write-Host "  docker compose exec backend pytest /app/tests -v"
}
