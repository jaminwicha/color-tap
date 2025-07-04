import math
import random
from collections import Counter
from enum import Enum
from shapes import Shape, ShapeType
from config import WINDOW_WIDTH, WINDOW_HEIGHT, AVAILABLE_COLORS, GAME_SETTINGS

class GenerationAlgorithm(Enum):
    FRACTAL_SPIRAL = 1
    FIBONACCI_SPIRAL = 2
    ORGANIC_CLUSTERS = 3
    PERLIN_NOISE = 4
    MANDELBROT_SET = 5

class LevelGenerator:
    @staticmethod
    def generate_fractal_positions(num_shapes):
        positions = []
        
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        
        for i in range(num_shapes):
            angle = (i / num_shapes) * 2 * math.pi
            
            base_radius = GAME_SETTINGS['base_radius']
            spiral_factor = 1 + (i * GAME_SETTINGS['spiral_factor'])
            fractal_noise = math.sin(angle * 3) * 30 + math.cos(angle * 5) * 20
            
            radius = base_radius * spiral_factor + fractal_noise
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            recursive_offset = LevelGenerator.generate_recursive_offset(i, GAME_SETTINGS['fractal_depth'])
            x += recursive_offset[0]
            y += recursive_offset[1]
            
            x = max(50, min(WINDOW_WIDTH - 50, x))
            y = max(50, min(WINDOW_HEIGHT - 50, y))
            
            positions.append((x, y))
        
        return positions
    
    @staticmethod
    def generate_recursive_offset(index, depth):
        if depth == 0:
            return (0, 0)
        
        base_offset = 40 / depth
        angle = (index * 2.39996) % (2 * math.pi)
        
        x = base_offset * math.cos(angle)
        y = base_offset * math.sin(angle)
        
        child_offset = LevelGenerator.generate_recursive_offset(index * 2, depth - 1)
        
        return (x + child_offset[0], y + child_offset[1])
    
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
    def generate_fibonacci_spiral(num_shapes):
        positions = []
        golden_ratio = (1 + math.sqrt(5)) / 2
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        
        for i in range(num_shapes):
            angle = i * 2 * math.pi / golden_ratio
            radius = 15 * math.sqrt(i + 1)
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            x = max(50, min(WINDOW_WIDTH - 50, x))
            y = max(50, min(WINDOW_HEIGHT - 50, y))
            
            positions.append((x, y))
        
        return positions
    
    @staticmethod
    def generate_organic_clusters(num_shapes):
        positions = []
        num_clusters = random.randint(2, 4)
        
        cluster_centers = []
        for _ in range(num_clusters):
            center_x = random.randint(100, WINDOW_WIDTH - 100)
            center_y = random.randint(100, WINDOW_HEIGHT - 100)
            cluster_centers.append((center_x, center_y))
        
        for i in range(num_shapes):
            cluster_idx = i % num_clusters
            center_x, center_y = cluster_centers[cluster_idx]
            
            angle = random.random() * 2 * math.pi
            distance = random.gauss(0, 60)
            distance = max(0, min(120, distance))
            
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            x = max(50, min(WINDOW_WIDTH - 50, x))
            y = max(50, min(WINDOW_HEIGHT - 50, y))
            
            positions.append((x, y))
        
        return positions
    
    @staticmethod
    def generate_perlin_noise_positions(num_shapes):
        positions = []
        
        for i in range(num_shapes):
            t = i / num_shapes
            
            noise_x = (math.sin(t * 12.9898) * 43758.5453) % 1
            noise_y = (math.sin(t * 78.233) * 43758.5453) % 1
            
            smooth_x = 0.5 + 0.3 * math.sin(t * 4 * math.pi)
            smooth_y = 0.5 + 0.3 * math.cos(t * 6 * math.pi)
            
            x = (noise_x * 0.3 + smooth_x * 0.7) * (WINDOW_WIDTH - 100) + 50
            y = (noise_y * 0.3 + smooth_y * 0.7) * (WINDOW_HEIGHT - 100) + 50
            
            positions.append((x, y))
        
        return positions
    
    @staticmethod
    def generate_mandelbrot_positions(num_shapes):
        positions = []
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        
        for i in range(num_shapes):
            angle = i * 2 * math.pi / num_shapes
            
            c_real = 0.7885 * math.cos(angle)
            c_imag = 0.7885 * math.sin(angle)
            
            z_real, z_imag = 0, 0
            iterations = 0
            max_iterations = 20
            
            while iterations < max_iterations and z_real*z_real + z_imag*z_imag < 4:
                z_real, z_imag = z_real*z_real - z_imag*z_imag + c_real, 2*z_real*z_imag + c_imag
                iterations += 1
            
            radius = 100 + iterations * 5
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            x = max(50, min(WINDOW_WIDTH - 50, x))
            y = max(50, min(WINDOW_HEIGHT - 50, y))
            
            positions.append((x, y))
        
        return positions
    
    @staticmethod
    def create_shape_with_random_size(x, y, shape_type, color):
        if shape_type == ShapeType.RECTANGLE:
            width = random.randint(20, 80)
            height = random.randint(15, 60)
            return Shape(x, y, shape_type, color, width=width, height=height)
        else:
            size = random.randint(GAME_SETTINGS['min_shape_size'], GAME_SETTINGS['max_shape_size'])
            return Shape(x, y, shape_type, color, size)
    
    @staticmethod
    def create_level():
        shape_types = [ShapeType.CIRCLE, ShapeType.SQUARE, ShapeType.TRIANGLE, ShapeType.RECTANGLE]
        target_color = random.choice(AVAILABLE_COLORS)
        
        algorithm = random.choice(list(GenerationAlgorithm))
        
        max_attempts = GAME_SETTINGS['max_level_attempts']
        for _ in range(max_attempts):
            shapes = []
            
            if algorithm == GenerationAlgorithm.FRACTAL_SPIRAL:
                positions = LevelGenerator.generate_fractal_positions(GAME_SETTINGS['num_shapes'])
            elif algorithm == GenerationAlgorithm.FIBONACCI_SPIRAL:
                positions = LevelGenerator.generate_fibonacci_spiral(GAME_SETTINGS['num_shapes'])
            elif algorithm == GenerationAlgorithm.ORGANIC_CLUSTERS:
                positions = LevelGenerator.generate_organic_clusters(GAME_SETTINGS['num_shapes'])
            elif algorithm == GenerationAlgorithm.PERLIN_NOISE:
                positions = LevelGenerator.generate_perlin_noise_positions(GAME_SETTINGS['num_shapes'])
            elif algorithm == GenerationAlgorithm.MANDELBROT_SET:
                positions = LevelGenerator.generate_mandelbrot_positions(GAME_SETTINGS['num_shapes'])
            
            for pos in positions:
                shape_type = random.choice(shape_types)
                color = random.choice(AVAILABLE_COLORS)
                shapes.append(LevelGenerator.create_shape_with_random_size(pos[0], pos[1], shape_type, color))
            
            shapes.append(LevelGenerator.create_shape_with_random_size(100, 100, random.choice(shape_types), target_color))
            shapes.append(LevelGenerator.create_shape_with_random_size(200, 150, random.choice(shape_types), target_color))
            
            if LevelGenerator.is_level_winnable(shapes, target_color):
                return shapes, target_color, algorithm
        
        return None, target_color, algorithm