@echo off
REM Sorter - Git Setup & Push Script (Windows)
REM Usage: setup.bat <github-repo-url>

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Sorter - Git Setup ^& Push
echo ==========================================
echo.

REM Check if repo URL provided
if "%1"=="" (
    echo Usage: setup.bat ^<github-repo-url^>
    echo Example: setup.bat https://github.com/your-username/Sorter.git
    pause
    exit /b 1
)

set REPO_URL=%1

echo Setting up Git repository...
echo.

REM Configure git
echo Configuring Git...
git config user.name "Sorter Developer"
git config user.email "dev@sorter.local"

REM Add all files
echo Adding files...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: Sorter v1.0.0 - Keyword Sorter, TimeSort, SmartSort with modern UI"

REM Add remote
echo Adding remote repository...
git remote add origin "%REPO_URL%"

REM Push to main branch
echo Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Push failed!
    echo Make sure:
    echo - You have Git installed
    echo - You have GitHub credentials configured
    echo - The repository URL is correct
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✓ Successfully pushed to GitHub!
echo Repository: %REPO_URL%
echo ==========================================
echo.
echo Next steps:
echo 1. Create a GitHub Release
echo 2. Upload split files to release
echo 3. Deploy web page to Vercel/Netlify
echo.
pause
