@echo off
set dt=%DATE%
set tm=%TIME: =0%
set tm=%tm:~0,8%
set TIMESTAMP=%dt%,%tm%
set year=%dt:~0,4%
set mouth=%dt:~5,2%
set filename=%~dp0worktime%year%%mouth%.csv

if not exist %filename% (
    echo date,time,state > %filename%
)
echo %TIMESTAMP%,%1 >> %filename%
powershell -command "write-output 'Recorded to %filename%'; gc %filename%|convertFrom-csv | select-object -last 1"  