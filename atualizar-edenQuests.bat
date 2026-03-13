@echo off
title Atualizar edenQuests
setlocal

echo ===============================
echo   Atualizador do edenQuests
echo ===============================
echo.

REM Chama o script PowerShell na mesma pasta deste .bat
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0atualizar-edenQuests.ps1"

if errorlevel 1 (
    echo.
    echo Ocorreu um erro ao atualizar o edenQuests.
    echo Verifique sua conexao com a internet ou tente novamente mais tarde.
    echo.
    pause
)

endlocal
