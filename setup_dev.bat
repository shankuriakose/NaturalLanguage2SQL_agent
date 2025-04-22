@echo off
setlocal

echo Starting development environment setup for Windows...

:: 3. Check for Python command
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: python command not found in PATH. Please install Python 3 and ensure it's added to PATH.
    exit /b 1
)
echo Found Python installation.

:: 4. Check for requirements.txt
if not exist "requirements.txt" (
    echo Error: requirements.txt not found in the current directory.
    exit /b 1
)
echo requirements.txt found.

:: 5. Create virtual environment
echo Creating virtual environment 'venv'...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment.
    exit /b 1
)
echo Virtual environment created successfully.

:: 6. Install dependencies using venv's pip
echo Installing dependencies from requirements.txt...
call venv\Scripts\python.exe -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    exit /b 1
)
echo Dependencies installed successfully.

:: 7. Check if .env.example exists
if exist ".env.example" (
    echo .env.example found.
    :: 8. Copy .env.example if .env does not exist
    if not exist ".env" (
        echo Copying .env.example to .env...
        copy ".env.example" ".env" > nul
        if %errorlevel% neq 0 (
            echo Error: Failed to copy .env.example to .env.
            exit /b 1
        )
        echo .env file created from example.
    ) else (
        :: 9. .env already exists
        echo .env file already exists. Not overwriting.
    )
) else (
    echo Warning: .env.example not found. Cannot create .env automatically.
    echo Please create a .env file manually with your API keys and configurations.
)

:: 10. Print concluding message
echo.
echo --------------------------------------------------
echo Setup complete!
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    .\venv\Scripts\activate.bat
echo 2. Edit the .env file:
echo    - Add your GOOGLE_API_KEY.
echo    - Optionally, set DATABASE_URI if not using the default SQLite DB.
echo 3. Run the application (after activating venv):
echo    uvicorn ai_sql_agent.app:app --reload
echo --------------------------------------------------

endlocal
exit /b 0
