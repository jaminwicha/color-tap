import math
import random
from abc import ABC, abstractmethod
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_SETTINGS

class GenerationStrategy(ABC):
    @abstractmethod
    def generate_positions(self, num_shapes):
        pass
    
    @property
    @abstractmethod
    def name(self):
        pass

class FractalSpiralStrategy(GenerationStrategy):
    @property
    def name(self):
        return "FRACTAL_SPIRAL"
    
    def generate_positions(self, num_shapes):
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
            
            recursive_offset = self._generate_recursive_offset(i, GAME_SETTINGS['fractal_depth'])
            x += recursive_offset[0]
            y += recursive_offset[1]
            
            x = max(50, min(WINDOW_WIDTH - 50, x))
            y = max(50, min(WINDOW_HEIGHT - 50, y))
            
            positions.append((x, y))
        
        return positions
    
    def _generate_recursive_offset(self, index, depth):
        if depth == 0:
            return (0, 0)
        
        base_offset = 40 / depth
        angle = (index * 2.39996) % (2 * math.pi)
        
        x = base_offset * math.cos(angle)
        y = base_offset * math.sin(angle)
        
        child_offset = self._generate_recursive_offset(index * 2, depth - 1)
        
        return (x + child_offset[0], y + child_offset[1])

class FibonacciSpiralStrategy(GenerationStrategy):
    @property
    def name(self):
        return "FIBONACCI_SPIRAL"
    
    def generate_positions(self, num_shapes):
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

class OrganicClustersStrategy(GenerationStrategy):
    @property
    def name(self):
        return "ORGANIC_CLUSTERS"
    
    def generate_positions(self, num_shapes):
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

class PerlinNoiseStrategy(GenerationStrategy):
    @property
    def name(self):
        return "PERLIN_NOISE"
    
    def generate_positions(self, num_shapes):
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

class MandelbrotStrategy(GenerationStrategy):
    @property
    def name(self):
        return "MANDELBROT_SET"
    
    def generate_positions(self, num_shapes):
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

class GenerationStrategyFactory:
    _strategies = {
        "FRACTAL_SPIRAL": FractalSpiralStrategy(),
        "FIBONACCI_SPIRAL": FibonacciSpiralStrategy(),
        "ORGANIC_CLUSTERS": OrganicClustersStrategy(),
        "PERLIN_NOISE": PerlinNoiseStrategy(),
        "MANDELBROT_SET": MandelbrotStrategy()
    }
    
    @classmethod
    def get_strategy(cls, strategy_name):
        return cls._strategies.get(strategy_name)
    
    @classmethod
    def get_random_strategy(cls):
        return random.choice(list(cls._strategies.values()))
    
    @classmethod
    def get_all_strategies(cls):
        return list(cls._strategies.values())