@echo off
rem Compilation driver file for Windows
rem Called by latex2pdf scripts
rem Not inteded to be called directly

if EXIST tmp goto DoNotCreateTempDir
mkdir tmp
if ERRORLEVEL 1 goto DoPause

:DoNotCreateTempDir
set PDFLATEX=pdflatex
IF "%LATEX2PDF_PERPETUAL%"=="" GOTO InteractiveMode

set PDFLATEX=pdflatex -interaction=nonstopmode

:InteractiveMode
perl %ROOT%_latexfiles/latexmk.pl -pdf -f -output-directory=tmp -r %ROOT%_latexfiles/latexmkrc %LATEXMK_EXTRA_FLAGS% %MAIN_FILE%
if ERRORLEVEL 1 goto DoPause

xcopy tmp\%MAIN_FILE%.pdf . /f /d /y
if ERRORLEVEL 1 goto DoPause

xcopy tmp\%MAIN_FILE%.synctex.gz . /f /d /y
if ERRORLEVEL 1 goto DoPause

xcopy tmp\%MAIN_FILE%.log . /f /d /y
if ERRORLEVEL 1 goto DoPause

exit /b 0

:DoPause
exit /b 1
