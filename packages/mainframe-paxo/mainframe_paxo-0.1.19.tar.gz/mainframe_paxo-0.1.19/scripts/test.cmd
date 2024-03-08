rem test the rye
setlocal
rem get bat file location
set batfile=%~dp0

rem set rye to the location of ./rye-x86_64-windows.exe relative to current bat file
set rye=%batfile%rye-x86_64-windows.exe

set RYE_NO_AUTO_INSTALL=1
%rye% --version
pause 2