@echo off
python "%~dp0scripts\init_catalog.py"
if errorlevel 1 exit /b 1
python "%~dp0scripts\run_native.py" --reel
if errorlevel 1 exit /b 1
python "%~dp0scripts\validate_exports.py"
if errorlevel 1 exit /b 1
ffmpeg -hide_banner -loglevel error -y -framerate 12 -i "%~dp0local\output\greeting_frames\%%04d.png" -c:v libx264 -threads 2 -crf 20 -pix_fmt yuv420p "%~dp0local\output\greeting_wave__proxy_previs.mp4"
if errorlevel 1 exit /b 1
python "%~dp0scripts\finalize_receipt.py"
pause
