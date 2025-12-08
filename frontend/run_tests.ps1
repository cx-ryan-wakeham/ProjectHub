# PowerShell script to run frontend tests
# Usage: .\run_tests.ps1

Write-Host "Running ProjectHub Frontend Tests..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the frontend directory
$currentDir = Split-Path -Leaf (Get-Location)
if ($currentDir -ne "frontend") {
    Write-Host "Changing to frontend directory..." -ForegroundColor Yellow
    Set-Location frontend
}

# Run tests without watch mode
Write-Host "Executing tests..." -ForegroundColor Green
npm test -- --watchAll=false

$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "All tests passed!" -ForegroundColor Green
} else {
    Write-Host "Some tests failed." -ForegroundColor Red
}

exit $exitCode

