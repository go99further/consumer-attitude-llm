@echo off
cd /d %~dp0
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
for /f "tokens=1-6 delims=/: " %%a in ("%date% %time%") do (
    set YY=%%a
    set MM=%%b
    set DD=%%c
    set HH=%%d
    set MIN=%%e
    set SS=%%f
)
set TS=%YY%%MM%%DD%_%HH%%MIN%%SS%
copy main.pdf main_%TS%.pdf
echo.
echo Build complete: main_%TS%.pdf
