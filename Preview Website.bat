@echo off
cd /d "%~dp0site"
where py >nul 2>nul
if %errorlevel%==0 (
 start "" "http://localhost:8000"
 py -3 -m http.server 8000
 goto :end
)
where python >nul 2>nul
if %errorlevel%==0 (
 start "" "http://localhost:8000"
 python -m http.server 8000
 goto :end
)
echo Install Python 3 from python.org to preview this site.
pause
:end
