# Pongus
Install Python

Windows / macOS / Linux:
Go to python.org/downloads and download the latest Python 3.x.
Windows tip: Make sure to check “Add Python to PATH” during installation.

On CMD, Powershell, etc.
Verify installation:

python --version
or
python3 --version

2. Create a Virtual Environment

Navigate to your project folder:
cd path/to/your/project

Create a virtual environment:
python -m venv venv


This creates a folder venv containing an isolated Python environment.
3. Activate the Virtual Environment

Windows (Command Prompt):
venv\Scripts\activate


Windows (PowerShell):
venv\Scripts\Activate.ps1


macOS / Linux:
source venv/bin/activate


You should now see (venv) in your terminal prompt, meaning the virtual environment is active.

4. Install Pygame
With the virtual environment activated:
pip install pygame

Verify installation:
python -m pygame.examples.aliens

Start game:
python interface.py


Rules
        "Player 1 (Left Paddle): W = Up, S = Down, SPACE = Full-height boost",
        "Player 2 (Right Paddle): Up/Down arrows = Move, Left arrow = Full-height boost",
        "New Balls spawn at the center after every 4 paddle hits",
        "Score 15 points to win a round",
        "First player to win 3 rounds wins the game",
        "Bricks Mode: Break all bricks to advance levels",
        "Press ESC to return to Main Menu"
