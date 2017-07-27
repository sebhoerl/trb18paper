@echo off
rem Compilation driver file for Windows
rem Called by latex2pdf scripts
rem Not inteded to be called directly

mk4ht oolatex %MAIN_FILE% "%LINUX_ROOT%_latexfiles/tex2word/oo-win.cfg,ooffice,bib-,hidden-ref"
if ERRORLEVEL 1 goto DoPause

mk4ht oolatex %MAIN_FILE% "%LINUX_ROOT%_latexfiles/tex2word/oo-win.cfg,ooffice,bib-,hidden-ref"
if ERRORLEVEL 1 goto DoPause

exit /b 0

:DoPause
exit /b 1
