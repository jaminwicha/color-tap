import random
import math
from typing import List, Tuple, Dict
from config import WINDOW_WIDTH, WINDOW_HEIGHT, Color
from shape_behaviors import Circle, Square, Triangle, Rectangle
from nested_shapes import NestedShape, StaticShape, NestedShapeFactory
from shape_factory import ShapeFactory

class PrimeNumberGenerator:
    """Generates sequences based on prime numbers for organic randomness"""
    
    def __init__(self):
        self.primes = self._generate_primes(1000)
        self.fibonacci_primes = self._fibonacci_primes()
    
    def _generate_primes(self, limit: int) -> List[int]:
        """Generate prime numbers up to limit using Sieve of Eratosthenes"""
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(limit)) + 1):
            if sieve[i]:
                for j in range(i * i, limit + 1, i):
                    sieve[j] = False
        
        return [i for i in range(2, limit + 1) if sieve[i]]
    
    def _fibonacci_primes(self) -> List[int]:
        """Find primes that are also Fibonacci numbers"""
        fib_primes = []
        a, b = 1, 1
        while b < 1000:
            if b in self.primes:
                fib_primes.append(b)
            a, b = b, a + b
        return fib_primes
    
    def get_prime_position(self, zone_index: int, total_zones: int) -> Tuple[float, float]:
        """Generate position based on prime number patterns"""
        # Use twin primes for x,y coordinates
        prime_idx = zone_index % len(self.primes)
        prime = self.primes[prime_idx]
        
        # Convert prime to normalized coordinates using golden ratio
        golden_ratio = (1 + math.sqrt(5)) / 2
        x_ratio = (prime * golden_ratio) % 1.0
        y_ratio = (prime / golden_ratio) % 1.0
        
        return x_ratio, y_ratio
    
    def get_prime_size_sequence(self, length: int) -> List[int]:
        """Generate size sequence based on prime summations"""
        sequence = []
        base_size = 20
        
        for i in range(length):
            # Sum of first few primes modulo some value for variation
            prime_sum = sum(self.primes[:3 + (i % 5)]) % 50
            size = base_size + prime_sum
            sequence.append(size)
        
        return sequence

class Zone:
    """Represents a recursive zone in the level"""
    
    def __init__(self, x: int, y: int, width: int, height: int, depth: int = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.depth = depth
        self.children = []  # Sub-zones
        self.shapes = []   # Shapes in this zone
        self.zone_color = None
        self.has_static_shapes = False
        
    def add_child_zone(self, child_zone):
        """Add a child zone for recursive subdivision"""
        self.children.append(child_zone)
    
    def get_center(self) -> Tuple[int, int]:
        """Get the center point of this zone"""
        return self.x + self.width // 2, self.y + self.height // 2
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point is within this zone"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def get_random_point(self) -> Tuple[int, int]:
        """Get a random point within this zone with prime-based distribution"""
        prime_gen = PrimeNumberGenerator()
        x_ratio, y_ratio = prime_gen.get_prime_position(self.depth, 1)
        
        # Add some random variation
        x_ratio += random.uniform(-0.2, 0.2)
        y_ratio += random.uniform(-0.2, 0.2)
        x_ratio = max(0.1, min(0.9, x_ratio))
        y_ratio = max(0.1, min(0.9, y_ratio))
        
        x = int(self.x + x_ratio * self.width)
        y = int(self.y + y_ratio * self.height)
        
        return x, y

class ZoneLevelGenerator:
    """Generates levels using recursive zone-based patchwork quilt design"""
    
    def __init__(self):
        self.prime_gen = PrimeNumberGenerator()
        self.colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, 
                      Color.PURPLE, Color.ORANGE, Color.AURORA_MINT, Color.SUNSET_CORAL]
        
    def create_zone_based_level(self) -> Tuple[List, Color, str]:
        """Create a level using recursive zone subdivision"""
        # Create root zone covering the entire screen
        margin = 50
        root_zone = Zone(margin, margin, 
                        WINDOW_WIDTH - 2*margin, 
                        WINDOW_HEIGHT - 2*margin, 
                        depth=0)
        
        # Recursively subdivide zones
        self._subdivide_zone(root_zone, max_depth=3)
        
        # Generate shapes in zones (static first, then movable)
        all_shapes = []
        
        # Stage 1: Create static shapes
        static_shapes = self._create_static_shapes_in_zones(root_zone)
        all_shapes.extend(static_shapes)
        
        # Stage 2: Create movable shapes
        movable_shapes = self._create_movable_shapes_in_zones(root_zone)
        all_shapes.extend(movable_shapes)
        
        # Choose target color based on prime number selection
        target_color = self._select_target_color_with_primes(all_shapes)
        
        return all_shapes, target_color, "recursive_zone_prime"
    
    def _subdivide_zone(self, zone: Zone, max_depth: int):
        """Recursively subdivide a zone into smaller zones"""
        if zone.depth >= max_depth:
            return
        
        # Use prime numbers to determine subdivision pattern
        prime_idx = zone.depth % len(self.prime_gen.primes)
        subdivision_prime = self.prime_gen.primes[prime_idx]
        
        # Determine subdivision direction based on prime properties
        if subdivision_prime % 4 == 1:  # Primes ≡ 1 (mod 4)
            self._subdivide_horizontally(zone, max_depth)
        elif subdivision_prime % 4 == 3:  # Primes ≡ 3 (mod 4)
            self._subdivide_vertically(zone, max_depth)
        else:
            # For small primes, subdivide into quadrants
            self._subdivide_quadrants(zone, max_depth)
    
    def _subdivide_horizontally(self, zone: Zone, max_depth: int):
        """Subdivide zone horizontally"""
        # Use golden ratio for pleasing proportions
        golden_ratio = (1 + math.sqrt(5)) / 2
        split_ratio = 1.0 / golden_ratio
        
        split_y = int(zone.y + zone.height * split_ratio)
        
        # Create two child zones
        upper_zone = Zone(zone.x, zone.y, zone.width, 
                         split_y - zone.y, zone.depth + 1)
        lower_zone = Zone(zone.x, split_y, zone.width, 
                         zone.y + zone.height - split_y, zone.depth + 1)
        
        zone.add_child_zone(upper_zone)
        zone.add_child_zone(lower_zone)
        
        # Recursively subdivide children
        self._subdivide_zone(upper_zone, max_depth)
        self._subdivide_zone(lower_zone, max_depth)
    
    def _subdivide_vertically(self, zone: Zone, max_depth: int):
        """Subdivide zone vertically"""
        golden_ratio = (1 + math.sqrt(5)) / 2
        split_ratio = 1.0 / golden_ratio
        
        split_x = int(zone.x + zone.width * split_ratio)
        
        # Create two child zones
        left_zone = Zone(zone.x, zone.y, split_x - zone.x, 
                        zone.height, zone.depth + 1)
        right_zone = Zone(split_x, zone.y, zone.x + zone.width - split_x, 
                         zone.height, zone.depth + 1)
        
        zone.add_child_zone(left_zone)
        zone.add_child_zone(right_zone)
        
        # Recursively subdivide children
        self._subdivide_zone(left_zone, max_depth)
        self._subdivide_zone(right_zone, max_depth)
    
    def _subdivide_quadrants(self, zone: Zone, max_depth: int):
        """Subdivide zone into four quadrants"""
        mid_x = zone.x + zone.width // 2
        mid_y = zone.y + zone.height // 2
        
        # Create four quadrant zones
        quadrants = [
            Zone(zone.x, zone.y, mid_x - zone.x, mid_y - zone.y, zone.depth + 1),
            Zone(mid_x, zone.y, zone.x + zone.width - mid_x, mid_y - zone.y, zone.depth + 1),
            Zone(zone.x, mid_y, mid_x - zone.x, zone.y + zone.height - mid_y, zone.depth + 1),
            Zone(mid_x, mid_y, zone.x + zone.width - mid_x, zone.y + zone.height - mid_y, zone.depth + 1)
        ]
        
        for quad in quadrants:
            zone.add_child_zone(quad)
            self._subdivide_zone(quad, max_depth)
    
    def _create_static_shapes_in_zones(self, root_zone: Zone) -> List:
        """Create static shapes throughout the zone hierarchy"""
        static_shapes = []
        
        def create_static_in_zone(zone: Zone):
            # Only create static shapes in leaf zones
            if not zone.children:
                # Decide whether this zone gets static shapes based on prime distribution
                prime_idx = zone.depth % len(self.prime_gen.primes)
                if self.prime_gen.primes[prime_idx] % 7 == 0:  # Roughly 1/7 chance
                    return  # Skip this zone
                
                # Create 1-2 static shapes per leaf zone
                num_static = 1 + (self.prime_gen.primes[prime_idx] % 2)
                
                for i in range(num_static):
                    x, y = zone.get_random_point()
                    
                    # Use prime-based size
                    size_sequence = self.prime_gen.get_prime_size_sequence(1)
                    base_size = size_sequence[0]
                    
                    # Determine if hollow or solid based on prime properties
                    is_hollow = (self.prime_gen.primes[prime_idx] % 3) == 0
                    
                    # Choose attachment based on zone position
                    attachment = self._get_wall_attachment(zone, x, y)
                    
                    # Create nested static shape
                    zone_colors = self._get_zone_color_palette(zone.depth)
                    shells = [(zone_colors[i % len(zone_colors)], base_size - i*8) 
                             for i in range(2)]
                    
                    static_shape = StaticShape(x, y, shells, attachment, is_hollow)
                    static_shapes.append(static_shape)
                    zone.has_static_shapes = True
            else:
                # Recursively process child zones
                for child in zone.children:
                    create_static_in_zone(child)
        
        create_static_in_zone(root_zone)
        return static_shapes
    
    def _create_movable_shapes_in_zones(self, root_zone: Zone) -> List:
        """Create movable shapes throughout the zone hierarchy"""
        movable_shapes = []
        
        def create_movable_in_zone(zone: Zone):
            if not zone.children:
                # Create movable shapes in leaf zones
                num_movable = 2 + (zone.depth % 4)  # 2-5 shapes per zone
                
                for i in range(num_movable):
                    x, y = zone.get_random_point()
                    
                    # Use prime-based sizing
                    size_sequence = self.prime_gen.get_prime_size_sequence(1)
                    base_size = min(size_sequence[0], 35)  # Limit size
                    
                    # Decide between regular and nested shapes
                    prime_idx = (zone.depth + i) % len(self.prime_gen.primes)
                    if self.prime_gen.primes[prime_idx] % 5 == 0:
                        # Create nested shape
                        zone_colors = self._get_zone_color_palette(zone.depth)
                        num_shells = 2 + (prime_idx % 3)  # 2-4 shells
                        shells = [(zone_colors[j % len(zone_colors)], base_size - j*6) 
                                 for j in range(num_shells)]
                        shape = NestedShape(x, y, shells)
                    else:
                        # Create regular shape
                        color = self._get_zone_color_palette(zone.depth)[i % 3]
                        shape = ShapeFactory.create_random_shape(x, y, color)
                    
                    movable_shapes.append(shape)
            else:
                # Recursively process child zones
                for child in zone.children:
                    create_movable_in_zone(child)
        
        create_movable_in_zone(root_zone)
        return movable_shapes
    
    def _get_zone_color_palette(self, depth: int) -> List:
        """Get color palette for a zone based on its depth"""
        # Use different color schemes for different depths
        palettes = [
            [Color.RED, Color.ORANGE, Color.YELLOW],      # Warm colors
            [Color.BLUE, Color.AURORA_MINT, Color.PURPLE],       # Cool colors  
            [Color.GREEN, Color.FOREST_LIGHT_GREEN, Color.FOREST_GREEN], # Nature colors
            [Color.AURORA_PINK, Color.SUNSET_CORAL, Color.SUNSET_YELLOW] # Sunset colors
        ]
        return palettes[depth % len(palettes)]
    
    def _get_wall_attachment(self, zone: Zone, x: int, y: int) -> str:
        """Determine wall attachment based on position in zone"""
        margin = 30
        
        if x - zone.x < margin:
            return 'left'
        elif zone.x + zone.width - x < margin:
            return 'right'
        elif y - zone.y < margin:
            return 'top'
        elif zone.y + zone.height - y < margin:
            return 'bottom'
        else:
            return None  # Free-standing
    
    def _select_target_color_with_primes(self, shapes: List) -> Color:
        """Select target color using prime-based selection"""
        # Count available colors
        color_counts = {}
        for shape in shapes:
            if hasattr(shape, 'shells'):  # Nested shape
                for shell_color, _ in shape.shells:
                    color_counts[shell_color] = color_counts.get(shell_color, 0) + 1
            else:  # Regular shape
                color_counts[shape.color] = color_counts.get(shape.color, 0) + 1
        
        # Select color based on prime index
        available_colors = list(color_counts.keys())
        if available_colors:
            prime_idx = self.prime_gen.fibonacci_primes[0] % len(available_colors)
            return available_colors[prime_idx]
        
        return Color.RED  # Fallback