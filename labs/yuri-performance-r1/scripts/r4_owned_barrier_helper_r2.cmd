@echo off
setlocal
set "GATES=%~1"
for /f "usebackq" %%P in ("%GATES%\OWNED_PID.txt") do set "OWNEDPID=%%P"
>"%GATES%\INITIAL_READY.tmp" echo {"pid":%OWNEDPID%,"kind":"helper","phase":"LIVE_BLOCKED_BEFORE_PAYLOAD"}
move /y "%GATES%\INITIAL_READY.tmp" "%GATES%\INITIAL_READY.json" >nul
:before_wait
if not exist "%GATES%\START_RELEASE.json" goto before_wait
set /a "VALUE=16*15/2" >nul
>"%GATES%\HELPER_PAYLOAD.json" echo {"pid":%OWNEDPID%,"operation":"CMD built-in integer arithmetic only; no child launch","result":%VALUE%,"native_Blender_calls":0}
>"%GATES%\PAYLOAD_DONE.tmp" echo {"pid":%OWNEDPID%,"kind":"helper","payload_status":"PASS","error":null,"phase":"LIVE_BLOCKED_BEFORE_EXIT"}
move /y "%GATES%\PAYLOAD_DONE.tmp" "%GATES%\PAYLOAD_DONE.json" >nul
:after_wait
if not exist "%GATES%\FINAL_RELEASE.json" goto after_wait
exit /b 0
