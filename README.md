# 🏓 Pongus

A modern twist on the classic Pong game built with Python and Pygame, featuring multiplayer action and brick-breaking mode!

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have Python installed on your system.

### 📥 Installing Python

#### Windows / macOS / Linux
1. Visit [python.org/downloads](https://python.org/downloads) and download the latest Python 3.x
2. **Windows tip:** Make sure to check "Add Python to PATH" during installation

#### Verify Installation
Open your terminal (CMD, PowerShell, etc.) and run:
```bash
python --version
```
or
```bash
python3 --version
```

## 🔧 Installation

### 1. Navigate to Project Directory
```bash
cd path/to/your/project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```
This creates a folder `venv` containing an isolated Python environment.

### 3. Activate Virtual Environment

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

You should now see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### 4. Install Dependencies
```bash
pip install pygame
```

### 5. Verify Installation
Test your Pygame installation with:
```bash
python -m pygame.examples.aliens
```

## 🎮 Running the Game

Start the game by running:
```bash
python interface.py
```

## 🎯 Game Rules

### Controls
- **Player 1 (Left Paddle):**
  - `W` - Move Up
  - `S` - Move Down
  - `SPACE` - Full-height boost

- **Player 2 (Right Paddle):**
  - `↑` - Move Up
  - `↓` - Move Down
  - `←` - Full-height boost

### Gameplay
- 🏓 New balls spawn at the center after every 4 paddle hits
- 🎯 Score 15 points to win a round
- 🏆 First player to win 3 rounds wins the game
- 🧱 **Bricks Mode:** Break all bricks to advance levels
- `ESC` - Return to Main Menu

## 🎪 Game Modes

- **Classic Pong:** Two-player paddle battle
- **Bricks Mode:** Break through brick levels for extra challenge

---

**Enjoy playing Pongus! 🏓**
