# Color Tap

A 2D puzzle game where players match colored shapes to clear levels. Built with Python and Pygame.

## Features

- **Multiple Shape Types**: Circles, squares, triangles, and rectangles with varying sizes
- **Fractal Pattern Generation**: 5 different algorithms create beautiful, natural-looking level layouts
- **Polymorphic Architecture**: Clean, extensible codebase using design patterns
- **Level Persistence**: Save and replay any level you've played
- **Main Menu System**: Easy navigation between new games and saved levels
- **Physics Simulation**: Realistic bounce mechanics and drag-and-drop controls
- **Smart Level Generation**: Ensures all levels are winnable with validation

## How to Play

1. **Objective**: Make same-colored shapes collide to merge and disappear
2. **Win Condition**: The final pair to merge must match the border color
3. **Controls**: 
   - Drag shapes with mouse
   - Different colored shapes bounce off each other
   - Same colored shapes merge and vanish
4. **Strategy**: Plan your moves carefully - you need to merge shapes in the right order!

## Menu Controls

- **↑/↓**: Navigate menu options
- **Enter/Space**: Select option
- **ESC**: Back/Exit

## Game Controls

- **Mouse**: Drag and drop shapes
- **R**: Restart current level
- **N**: Generate new level  
- **Q**: Back to menu (when level complete)
- **M**: Back to menu (anytime)
- **ESC**: Close popups

## Installation

```bash
pip install pygame
python main.py
```

## Architecture

The game uses a clean, polymorphic architecture:

- `shape_behaviors.py`: Abstract shape classes with polymorphic methods
- `generation_strategies.py`: Strategy pattern for level generation algorithms  
- `shape_factory.py`: Factory pattern for shape creation
- `level_generator.py`: Level creation and validation logic
- `level_data.py`: Level persistence and serialization
- `main_menu.py`: Menu system with level selection
- `game.py`: Core game logic and physics
- `color_tap_app.py`: Main application controller

## Generation Algorithms

1. **Fractal Spiral**: Recursive spiral patterns with fractal noise
2. **Fibonacci Spiral**: Golden ratio-based natural spirals  
3. **Organic Clusters**: Gaussian-distributed biological-style clusters
4. **Perlin Noise**: Smooth noise-based positioning
5. **Mandelbrot Set**: Complex number iterations for fractal boundaries

## Testing

Run the comprehensive test suite:

```bash
python run_tests.py
```

Features 89% code coverage with tests for all major components.

## Development

- **Language**: Python 3.9+
- **Framework**: Pygame 2.6+
- **Testing**: Pytest with coverage reporting
- **Architecture**: Object-oriented with design patterns
- **Code Quality**: Clean, documented, and well-tested

## License

MIT License - see LICENSE file for details.