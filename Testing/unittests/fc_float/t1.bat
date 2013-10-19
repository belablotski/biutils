@echo off
"C:\Program Files\Python27\python.exe" ..\..\fc_float.py a.txt b.txt
if ERRORLEVEL 1 (
  echo Files are different
) else (
  echo Files are equal
)