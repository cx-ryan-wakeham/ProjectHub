# PowerShell script to run all tests (backend and frontend)
# Usage: .\run_all_tests.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "ProjectHub - Running All Tests" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = Get-Location

# Run backend tests
Write-Host "1. BACKEND TESTS" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow
Set-Location "$projectRoot\backend"
python -m unittest discover -v tests
$backendExitCode = $LASTEXITCODE

Write-Host ""
Write-Host ""

# Run frontend tests
Write-Host "2. FRONTEND TESTS" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow
Set-Location "$projectRoot\frontend"
npm test -- --watchAll=false
$frontendExitCode = $LASTEXITCODE

# Return to project root
Set-Location $projectRoot

# Summary
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

if ($backendExitCode -eq 0) {
    Write-Host "Backend Tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "Backend Tests: FAILED" -ForegroundColor Red
}

if ($frontendExitCode -eq 0) {
    Write-Host "Frontend Tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "Frontend Tests: FAILED" -ForegroundColor Red
}

Write-Host ""

# Exit with error if any tests failed
if ($backendExitCode -ne 0 -or $frontendExitCode -ne 0) {
    exit 1
} else {
    Write-Host "All tests passed successfully!" -ForegroundColor Green
    exit 0
}

