import random
from shape_behaviors import Circle, Square, Triangle, Rectangle
from fused_shapes import FusedShape, StackingPatterns
from config import AVAILABLE_COLORS, GAME_SETTINGS

class ShapeFactory:
    @staticmethod
    def create_random_shape(x, y, color=None):
        if color is None:
            color = random.choice(AVAILABLE_COLORS)
        
        shape_creators = [
            ShapeFactory._create_circle,
            ShapeFactory._create_square,
            ShapeFactory._create_triangle,
            ShapeFactory._create_rectangle
        ]
        
        creator = random.choice(shape_creators)
        return creator(x, y, color)
    
    @staticmethod
    def _create_circle(x, y, color):
        size = random.randint(GAME_SETTINGS['min_shape_size'], GAME_SETTINGS['max_shape_size'])
        return Circle(x, y, color, size)
    
    @staticmethod
    def _create_square(x, y, color):
        size = random.randint(GAME_SETTINGS['min_shape_size'], GAME_SETTINGS['max_shape_size'])
        return Square(x, y, color, size)
    
    @staticmethod
    def _create_triangle(x, y, color):
        size = random.randint(GAME_SETTINGS['min_shape_size'], GAME_SETTINGS['max_shape_size'])
        return Triangle(x, y, color, size)
    
    @staticmethod
    def _create_rectangle(x, y, color):
        width = random.randint(20, 80)
        height = random.randint(15, 60)
        return Rectangle(x, y, color, width, height)
    
    @staticmethod
    def create_circle(x, y, color, size=None):
        if size is None:
            size = random.randint(GAME_SETTINGS['min_shape_size'], GAME_SETTINGS['max_shape_size'])
        return Circle(x, y, color, size)
    
    @staticmethod
    def create_square(x, y, color, size=None):
        if size is None:
            size = random.randint(GAME_SETTINGS['min_shape_size'], GAME_SETTINGS['max_shape_size'])
        return Square(x, y, color, size)
    
    @staticmethod
    def create_triangle(x, y, color, size=None):
        if size is None:
            size = random.randint(GAME_SETTINGS['min_shape_size'], GAME_SETTINGS['max_shape_size'])
        return Triangle(x, y, color, size)
    
    @staticmethod
    def create_rectangle(x, y, color, width=None, height=None):
        if width is None:
            width = random.randint(20, 80)
        if height is None:
            height = random.randint(15, 60)
        return Rectangle(x, y, color, width, height)
    
    @staticmethod
    def create_fused_shape(x, y, color, component_shapes, stack_pattern="vertical"):
        """Create a fused shape from component shapes"""
        return FusedShape(x, y, color, component_shapes, stack_pattern)
    
    @staticmethod
    def create_random_fused_shape(x, y, color=None, num_components=None):
        """Create a random fused shape with random component shapes"""
        if color is None:
            color = random.choice(AVAILABLE_COLORS)
        
        if num_components is None:
            num_components = random.randint(2, 4)
        
        # Create component shapes
        component_shapes = []
        for i in range(num_components):
            # Create shapes at temporary positions (will be repositioned by FusedShape)
            temp_x = x + random.randint(-20, 20)
            temp_y = y + random.randint(-20, 20)
            component = ShapeFactory.create_random_shape(temp_x, temp_y, color)
            component_shapes.append(component)
        
        # Choose random stacking pattern
        pattern = StackingPatterns.get_random_pattern()
        
        return FusedShape(x, y, color, component_shapes, pattern)