@echo off
powershell -ExecutionPolicy Bypass -File "C:\Users\benke\devEnv\llmproc\record-deps.ps1"
@REM Check if argument is provided
if "%~1"=="" (
    echo Please provide a commit message
    exit /b 1
)

git add -u
git commit -m "%~1"
git push origin

@REM Check if any command failed
if errorlevel 1 (
    echo An error occurred
    pause
    exit /b 1
)

echo Successfully committed and pushed changes
