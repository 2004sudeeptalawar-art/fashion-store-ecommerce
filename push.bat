@echo off
cd /d "%~dp0"
git add .
git commit -m "Update deployment configuration and documentation"
git push origin main
echo.
echo ==============================================
echo  Git push completed! Check above for results.
echo ==============================================
pause
