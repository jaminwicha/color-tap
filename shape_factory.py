import random
from shape_behaviors import Circle, Square, Triangle, Rectangle
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