#!/bin/bash

# File Storage System Startup Script

echo "==================================="
echo "File Storage System"
echo "==================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo
echo "Starting File Storage System..."
echo "Web Interface: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo

# Start the server
python app.py