WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

class Color:
    # Original colors (kept for backward compatibility)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # Beautiful aesthetic colors for gameplay
    AURORA_MINT = (71, 225, 166)
    AURORA_PINK = (255, 121, 198)
    AURORA_GOLD = (255, 195, 0)
    
    SUNSET_CORAL = (255, 158, 128)
    SUNSET_YELLOW = (255, 206, 84)
    SUNSET_PURPLE = (108, 92, 231)
    
    OCEAN_TURQUOISE = (64, 224, 208)
    OCEAN_SKY = (135, 206, 235)
    OCEAN_PINK = (255, 182, 193)
    
    FOREST_LIGHT_GREEN = (144, 238, 144)
    FOREST_GREEN = (34, 139, 34)
    FOREST_ORANGE = (255, 140, 0)
    
    COSMIC_VIOLET = (138, 43, 226)
    COSMIC_INDIGO = (75, 0, 130)
    COSMIC_PINK = (255, 20, 147)

# Beautiful color sets for different aesthetic themes
AESTHETIC_COLOR_SETS = {
    'aurora': [Color.AURORA_MINT, Color.AURORA_PINK, Color.AURORA_GOLD],
    'sunset': [Color.SUNSET_CORAL, Color.SUNSET_YELLOW, Color.SUNSET_PURPLE],
    'ocean': [Color.OCEAN_TURQUOISE, Color.OCEAN_SKY, Color.OCEAN_PINK],
    'forest': [Color.FOREST_LIGHT_GREEN, Color.FOREST_GREEN, Color.FOREST_ORANGE],
    'cosmic': [Color.COSMIC_VIOLET, Color.COSMIC_INDIGO, Color.COSMIC_PINK]
}

# Current available colors (can be switched based on theme)
AVAILABLE_COLORS = AESTHETIC_COLOR_SETS['aurora']

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