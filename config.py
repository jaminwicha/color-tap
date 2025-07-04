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
    
    # Warm Palette
    WARM_CORAL = (255, 127, 80)
    WARM_PEACH = (255, 218, 185)
    WARM_GOLD = (255, 215, 0)
    WARM_AMBER = (255, 191, 0)
    
    # Cool Palette
    COOL_LAVENDER = (230, 230, 250)
    COOL_PERIWINKLE = (204, 204, 255)
    COOL_MINT = (189, 252, 201)
    COOL_ICE = (176, 224, 230)
    
    # Tropical Palette
    TROPICAL_MANGO = (255, 165, 79)
    TROPICAL_LIME = (50, 205, 50)
    TROPICAL_AQUA = (0, 255, 255)
    TROPICAL_FLAMINGO = (252, 92, 101)
    
    # Vintage Palette
    VINTAGE_ROSE = (217, 175, 217)
    VINTAGE_SAGE = (157, 192, 139)
    VINTAGE_CREAM = (255, 253, 208)
    VINTAGE_DUSTY_BLUE = (156, 176, 171)
    
    # Neon Palette
    NEON_PINK = (255, 16, 240)
    NEON_GREEN = (57, 255, 20)
    NEON_BLUE = (4, 217, 255)
    NEON_YELLOW = (255, 255, 51)
    
    # Earth Palette
    EARTH_TERRACOTTA = (204, 78, 92)
    EARTH_OLIVE = (128, 128, 0)
    EARTH_SAND = (194, 178, 128)
    EARTH_CLAY = (139, 69, 19)
    
    # Pastel Palette
    PASTEL_PINK = (255, 182, 193)
    PASTEL_LAVENDER = (221, 160, 221)
    PASTEL_MINT = (152, 251, 152)
    PASTEL_PEACH = (255, 218, 185)
    
    # Deep Palette
    DEEP_EMERALD = (0, 201, 87)
    DEEP_SAPPHIRE = (15, 82, 186)
    DEEP_RUBY = (224, 17, 95)
    DEEP_AMETHYST = (153, 102, 204)
    
    # Monochrome Palette
    MONO_CHARCOAL = (54, 69, 79)
    MONO_SILVER = (192, 192, 192)
    MONO_PLATINUM = (229, 228, 226)
    MONO_PEARL = (234, 234, 234)

# Beautiful color sets for different aesthetic themes
AESTHETIC_COLOR_SETS = {
    'aurora': [Color.AURORA_MINT, Color.AURORA_PINK, Color.AURORA_GOLD],
    'sunset': [Color.SUNSET_CORAL, Color.SUNSET_YELLOW, Color.SUNSET_PURPLE],
    'ocean': [Color.OCEAN_TURQUOISE, Color.OCEAN_SKY, Color.OCEAN_PINK],
    'forest': [Color.FOREST_LIGHT_GREEN, Color.FOREST_GREEN, Color.FOREST_ORANGE],
    'cosmic': [Color.COSMIC_VIOLET, Color.COSMIC_INDIGO, Color.COSMIC_PINK],
    'warm': [Color.WARM_CORAL, Color.WARM_PEACH, Color.WARM_GOLD, Color.WARM_AMBER],
    'cool': [Color.COOL_LAVENDER, Color.COOL_PERIWINKLE, Color.COOL_MINT, Color.COOL_ICE],
    'tropical': [Color.TROPICAL_MANGO, Color.TROPICAL_LIME, Color.TROPICAL_AQUA, Color.TROPICAL_FLAMINGO],
    'vintage': [Color.VINTAGE_ROSE, Color.VINTAGE_SAGE, Color.VINTAGE_CREAM, Color.VINTAGE_DUSTY_BLUE],
    'neon': [Color.NEON_PINK, Color.NEON_GREEN, Color.NEON_BLUE, Color.NEON_YELLOW],
    'earth': [Color.EARTH_TERRACOTTA, Color.EARTH_OLIVE, Color.EARTH_SAND, Color.EARTH_CLAY],
    'pastel': [Color.PASTEL_PINK, Color.PASTEL_LAVENDER, Color.PASTEL_MINT, Color.PASTEL_PEACH],
    'deep': [Color.DEEP_EMERALD, Color.DEEP_SAPPHIRE, Color.DEEP_RUBY, Color.DEEP_AMETHYST],
    'monochrome': [Color.MONO_CHARCOAL, Color.MONO_SILVER, Color.MONO_PLATINUM, Color.MONO_PEARL]
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