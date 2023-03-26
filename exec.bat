@echo off
set arg1=%1
if "%arg1%" == "" set arg1=-p
if "%arg1%" == "-p" python main.py
if "%arg1%" == "--player" python main.py

if "%arg1%" == "-a" (
	if "%CONDA_DEFAULT_ENV%" == "%CONDA_DEFAULT_ENV%" ( 
		activate pygame_env
	)
	python agent1.py
)

if "%arg1%" == "--agent" (
	if "%CONDA_DEFAULT_ENV%" == "%CONDA_DEFAULT_ENV%" ( 
		activate pygame_env
	)
	python agent1.py
)
