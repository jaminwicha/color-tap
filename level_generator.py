import random
from collections import Counter
from generation_strategies import GenerationStrategyFactory
from shape_factory import ShapeFactory
from config import AVAILABLE_COLORS, GAME_SETTINGS

class LevelGenerator:
    @staticmethod
    def is_level_winnable(shapes, target_color):
        color_counts = Counter(shape.color for shape in shapes)
        
        target_count = color_counts.get(target_color, 0)
        
        if target_count < 2:
            return False
        
        total_pairs = sum(count // 2 for count in color_counts.values())
        target_pairs = target_count // 2
        
        return target_pairs > 0 and (total_pairs == target_pairs or target_pairs == 1)
    
    @staticmethod
    def create_level():
        target_color = random.choice(AVAILABLE_COLORS)
        strategy = GenerationStrategyFactory.get_random_strategy()
        
        max_attempts = GAME_SETTINGS['max_level_attempts']
        for _ in range(max_attempts):
            shapes = []
            positions = strategy.generate_positions(GAME_SETTINGS['num_shapes'])
            
            for pos in positions:
                color = random.choice(AVAILABLE_COLORS)
                shape = ShapeFactory.create_random_shape(pos[0], pos[1], color)
                shapes.append(shape)
            
            target_shape1 = ShapeFactory.create_random_shape(100, 100, target_color)
            target_shape2 = ShapeFactory.create_random_shape(200, 150, target_color)
            shapes.extend([target_shape1, target_shape2])
            
            if LevelGenerator.is_level_winnable(shapes, target_color):
                return shapes, target_color, strategy.name
        
        return None, target_color, strategy.name