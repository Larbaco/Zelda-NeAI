# Zelda NEAT AI Project

Recreation of *The Legend of Zelda* (1986) with NEAT AI integration for autonomous gameplay.

## 📖 Project Description
This project recreates core mechanics of *The Legend of Zelda* (NES) using Python and the `arcade` library. The goal is to implement a NEAT AI (*NeuroEvolution of Augmenting Topologies*) to autonomously solve dungeons, defeat enemies, and complete objectives through evolutionary neural networks.

Currently, the project includes a functional game engine with:
- Player movement
- Collision detection
- Multi-room map transitions

This serves as a foundation for AI integration.

---

## 🎮 Features

### ✅ Implemented
- **Tile-based overworld** with an 8x16 room grid (loaded from `Colisoes.txt`)
- **Player mechanics:**
  - 4-directional movement (arrow keys)
  - Dynamic sprite rotation (Link faces movement direction)
  - Room transitions (screen wraps at map edges)
- **Collision system** using grid-based detection
- **Adjustable movement speed** (+/- keys to modify speed)
- **Scalable graphics** (default 3x upscaled NES-style sprites)

### 🚧 Planned (NEAT Integration)
- AI-controlled gameplay using genetic algorithms
- Fitness functions for combat, exploration, and puzzle-solving
- Training simulations for dungeon navigation
- Autonomous enemy avoidance and item collection

---

## ⚙️ Installation

### Dependencies
```bash
pip install arcade numpy neat-python
```

### Setup
1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd ZeldaNEAI
   ```
2. Place sprite assets in `/sprites/`:
   - `link_esquerda.png` (left)
   - `link_direita.png` (right)
   - `link_cima.png` (up)
   - `link_baixo.png` (down)
   - Tile textures (e.g., `grass.png`, `water.png`, etc.)

---

## 🕹️ Usage
Run the game:
```bash
python ZeldaNEAI.py
```

### Controls
| Key | Action |
|-----|--------|
| Arrow Keys | Move Link |
| + / - | Increase/decrease movement speed |
| ESC | Quit game |

---

## 🗺️ Project Structure

| File | Description |
|------|------------|
| `ZeldaNEAI.py` | Main game launcher |
| `core.py` | Game loop, player class, and physics |
| `map.py` | Tilemap loader and collision system |
| `Colisoes.txt` | Grid-based collision map (`X` = blocked) |
| `sprites/` | Character and environment textures |

---

## 🧠 NEAT Implementation Strategy

### Input Layer (Sensor Data)
- Player position
- Nearby tiles (walls/obstacles)
- Enemy locations
- Goal direction (e.g., dungeon entrance)

### Output Layer (Actions)
- Movement direction
- Attack/defend signals
- Item interaction

### Fitness Metrics
- Rooms explored
- Enemies defeated
- Damage avoided
- Puzzle completion time

---

## 📝 Contributing
1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/improvement
   ```
3. Commit changes:
   ```bash
   git commit -m 'Add feature'
   ```
4. Push to branch:
   ```bash
   git push origin feature/improvement
   ```
5. Open a Pull Request

---

## 📜 License
MIT License - See `LICENSE` for details.

> *"It's dangerous to go alone! Take this NEAT AI."*

Project maintained with 🗡️ by **Thiago Cabral**

