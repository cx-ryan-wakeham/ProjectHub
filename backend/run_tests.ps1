# PowerShell script to run backend tests
# Usage: .\run_tests.ps1

Write-Host "Running ProjectHub Backend Tests..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the backend directory
$currentDir = Split-Path -Leaf (Get-Location)
if ($currentDir -ne "backend") {
    Write-Host "Changing to backend directory..." -ForegroundColor Yellow
    Set-Location backend
}

# Run tests using unittest discovery
Write-Host "Executing tests..." -ForegroundColor Green
python -m unittest discover -v tests

$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "All tests passed!" -ForegroundColor Green
} else {
    Write-Host "Some tests failed." -ForegroundColor Red
}

exit $exitCode

