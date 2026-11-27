@echo off
py -3 "%~dp0core\kodowit.py" %*
exit /b %errorlevel%
