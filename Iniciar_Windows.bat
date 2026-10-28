@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Canon EOS - Contador de disparos
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 app.py
    goto :end
)
where python >nul 2>nul
if %errorlevel%==0 (
    python app.py
    goto :end
)
echo.
echo Python nao encontrado.
echo.
echo 1. Instale Python em https://www.python.org/downloads/
echo 2. Durante a instalacao, marque "Add python.exe to PATH".
echo 3. Abra este arquivo novamente.
echo.
:end
if errorlevel 1 (
    echo.
    echo Nao foi possivel abrir o aplicativo.
    echo Veja o guia de instalacao no README.pt-BR.md.
)
echo.
pause
