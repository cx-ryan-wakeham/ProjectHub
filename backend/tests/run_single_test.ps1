# PowerShell script to run a single test file
# Usage: .\run_single_test.ps1 test_models

param(
    [Parameter(Mandatory=$false)]
    [string]$TestFile = ""
)

Write-Host "Running Single Backend Test..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the backend/tests directory
$currentDir = Split-Path -Leaf (Get-Location)
if ($currentDir -ne "tests") {
    $parentDir = Split-Path -Leaf (Split-Path -Parent (Get-Location))
    if ($parentDir -eq "backend") {
        Write-Host "Changing to tests directory..." -ForegroundColor Yellow
        Set-Location tests
    } elseif ($currentDir -ne "backend") {
        Write-Host "Changing to backend directory..." -ForegroundColor Yellow
        Set-Location backend
    }
}

if ($TestFile -eq "") {
    Write-Host "No test file specified. Available test files:" -ForegroundColor Yellow
    Write-Host ""
    Get-ChildItem -Filter "test_*.py" | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Green }
    Write-Host ""
    Write-Host "Usage: .\run_single_test.ps1 test_models" -ForegroundColor Yellow
    exit 1
}

# Add .py extension if not provided
if (-not $TestFile.EndsWith(".py")) {
    $TestFile = "$TestFile.py"
}

# Run the specific test
Write-Host "Executing $TestFile..." -ForegroundColor Green
python $TestFile

$exitCode = $LASTEXITCODE

Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "Test passed!" -ForegroundColor Green
} else {
    Write-Host "Test failed." -ForegroundColor Red
}

exit $exitCode

