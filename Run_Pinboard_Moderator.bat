@echo off
title VRChat Pinboard Moderator

echo.
echo ========================================
echo      VRChat Pinboard Moderator
echo ========================================
echo.

where py >nul 2>&1
if %errorlevel%==0 (
    py pinboard_moderator_gui.py
) else (
    python pinboard_moderator_gui.py
)

echo.
pause
