@echo off

REM === Increase memory heap for MSVC ===
SET CL=/MP /Zm2000 /F10000000

SET MAIN_FILE=main.py
SET OUTPUT_DIR=paradigm-desktop/python-dist

REM === Clean old build ===
IF EXIST %OUTPUT_DIR% rmdir /s /q %OUTPUT_DIR%

REM === Build EXE with Nuitka ===
python -m nuitka %MAIN_FILE% ^
    --standalone ^
    --onefile ^
    --output-dir=%OUTPUT_DIR% ^
    --enable-plugin=numpy ^
    --include-package=torch ^
    --include-package=llama_cpp ^
    --nofollow-import-to=tkinter ^
    --nofollow-import-to=test ^
    --assume-yes-for-downloads ^
    --show-progress

echo.
echo ✅ Build completed. Output is in: %OUTPUT_DIR%
pause
