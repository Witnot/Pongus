# PONGUS

The classic Pong game just got absolutely demolished and rebuilt with pure Python fire. This isn't your grandpa's paddle game - we're serving up multiplayer chaos and brick-breaking madness that'll have you questioning reality.

## Getting Started

### Prerequisites
You need Python on your machine and you better have already snagged the code (that green download button) as a ZIP and extracted it to your root folder like a proper developer.

### Installing Python
Hit up [python.org/downloads](https://python.org/downloads) and grab the latest Python 3.x. Windows users - do NOT forget to check "Add Python to PATH" during installation unless you enjoy pain.

Verify you didn't mess up:
```bash
python --version
```
or if you're feeling fancy:
```bash
python3 --version
```

## Installation - The Real Deal

### 1. Navigate Like a Pro
```bash
cd path/to/your/project
```

### 2. Virtual Environment Setup
```bash
python -m venv venv
```
This creates your own little Python universe where nothing can go wrong.

### 3. Activate That Environment
**Windows Command Prompt:**
```cmd
venv\Scripts\activate
```

**Windows PowerShell (for the cultured):**
```powershell
venv\Scripts\Activate.ps1
```

**macOS / Linux (the enlightened):**
```bash
source venv/bin/activate
```

You'll see `(venv)` in your terminal - that's when you know you've made it.

### 4. Install the Magic
```bash
pip install pygame
```

### 5. Test Drive
Make sure Pygame isn't broken:
```bash
python -m pygame.examples.aliens
```

## Launch Protocol
Fire up the chaos with:
```bash
python interface.py
```

## How to Absolutely Dominate

### Controls That Actually Matter
**Player 1 (Left Side Supremacy):**
- `W` - Ascend
- `S` - Descend  
- `SPACE` - Full-height power move

**Player 2 (Right Side Rebellion):**
- Arrow Up - Rise
- Arrow Down - Fall
- Left Arrow - Full-height flex

### The Rules of Engagement
- Fresh balls spawn at center every 4 paddle hits because we're generous like that
- First to 15 points claims the round
- Best of 3 rounds determines the ultimate champion
- Bricks Mode: Obliterate every brick to prove your worth
- `ESC` - Tactical retreat to Main Menu

## Game Modes That Hit Different

**Classic Pong:** Pure two-player warfare where only the strong survive

**Bricks Mode:** Level-based brick annihilation that'll test your soul

---

Ready to get absolutely wrecked? Welcome to Pongus.
