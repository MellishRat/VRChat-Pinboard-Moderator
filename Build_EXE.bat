@echo off
title Build VRChat Pinboard Moderator EXE

echo.
echo ========================================
echo Installing PyInstaller if needed...
echo ========================================
py -m pip install --upgrade pyinstaller

echo.
echo ========================================
echo Building EXE...
echo ========================================
py -m PyInstaller pinboard_moderator_gui.spec --clean

echo.
echo ========================================
echo Build Complete
echo ========================================
echo.
echo EXE location:
echo dist\VRChat_Pinboard_Moderator.exe
echo.
echo IMPORTANT:
echo Keep flagged_words.json beside the EXE if you want to edit flagged terms.
echo If it is missing, the app will create a default copy on launch.
echo.
pause
