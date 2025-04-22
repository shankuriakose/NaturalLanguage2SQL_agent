#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting development environment setup..."

# 2. Check for Python command
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: python3 or python command not found. Please install Python 3." >&2
    exit 1
fi
echo "Using Python command: $PYTHON_CMD"

# 3. Check for requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found in the current directory." >&2
    exit 1
fi
echo "requirements.txt found."

# 4. Create virtual environment
echo "Creating virtual environment 'venv'..."
if ! $PYTHON_CMD -m venv venv; then
    echo "Error: Failed to create virtual environment." >&2
    exit 1
fi
echo "Virtual environment created successfully."

# 5. Install dependencies using venv's pip
echo "Installing dependencies from requirements.txt..."
if ! venv/bin/python -m pip install -r requirements.txt; then
    echo "Error: Failed to install dependencies." >&2
    # Optional: Clean up venv if install fails? For now, just exit.
    exit 1
fi
echo "Dependencies installed successfully."

# 6. Check if .env.example exists
if [ -f ".env.example" ]; then
    echo ".env.example found."
    # 7. Copy .env.example if .env does not exist
    if [ ! -f ".env" ]; then
        echo "Copying .env.example to .env..."
        cp .env.example .env
        echo ".env file created from example."
    else
        # 8. .env already exists
        echo ".env file already exists. Not overwriting."
    fi
else
    echo "Warning: .env.example not found. Cannot create .env automatically."
    echo "Please create a .env file manually with your API keys and configurations."
fi

# 9. Print concluding message
echo ""
echo "--------------------------------------------------"
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "2. Edit the .env file:"
echo "   - Add your GOOGLE_API_KEY."
echo "   - Optionally, set DATABASE_URI if not using the default SQLite DB."
echo "3. Run the application (after activating venv):"
echo "   uvicorn ai_sql_agent.app:app --reload"
echo "--------------------------------------------------"

exit 0
