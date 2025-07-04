WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

AVAILABLE_COLORS = [
    Color.RED, Color.GREEN, Color.BLUE, 
    Color.YELLOW, Color.PURPLE, Color.ORANGE
]

GAME_SETTINGS = {
    'friction': 0.95,
    'bounce_force': 5,
    'min_shape_size': 20,
    'max_shape_size': 40,
    'num_shapes': 8,
    'max_level_attempts': 10,
    'fractal_depth': 3,
    'base_radius': 150,
    'spiral_factor': 0.3,
    'border_width': 5
}