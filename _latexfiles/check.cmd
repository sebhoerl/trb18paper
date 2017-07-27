@echo off
perl mergeAll.pl
if ERRORLEVEL 1 goto End

pushd unsortbibs
del *.aux *.bbl *.blg
pdflatex example
if ERRORLEVEL 1 goto End
echo *
echo *
echo *
echo *
echo *
echo *
echo *
bibtex8 --wolfgang --mentstrs 20000 example
if ERRORLEVEL 1 goto End
exit /b 0

:End
pause
