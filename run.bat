@echo off
cd /d %~dp0
powershell -Command "$path='run\config_s6.json'; $json=Get-Content $path | ConvertFrom-Json; $json.s6_combo_index=3; $json | ConvertTo-Json | Set-Content $path"
cls
run\python.exe run\wage.py
pause
