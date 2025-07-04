import random
from collections import Counter
from generation_strategies import GenerationStrategyFactory
from shape_factory import ShapeFactory
from config import AVAILABLE_COLORS, GAME_SETTINGS
from level_validator import LevelValidator
from nested_shapes import NestedShapeFactory
from zone_level_generator import ZoneLevelGenerator

class LevelGenerator:
    @staticmethod
    def is_level_winnable(shapes, target_color):
        """Use the enhanced validator for winnability checking"""
        return LevelValidator.is_level_winnable(shapes, target_color)
    
    @staticmethod
    def create_level():
        # Use zone-based generation 70% of the time, legacy generation 30% of the time
        use_zone_generation = random.random() < 0.7
        
        if use_zone_generation:
            # Use the new recursive zone-based patchwork quilt generation
            zone_generator = ZoneLevelGenerator()
            try:
                return zone_generator.create_zone_based_level()
            except Exception as e:
                # Fallback to legacy generation if zone generation fails
                print(f"Zone generation failed: {e}, falling back to legacy")
                use_zone_generation = False
        
        if not use_zone_generation:
            # Legacy generation system
            target_color = random.choice(AVAILABLE_COLORS)
            strategy = GenerationStrategyFactory.get_random_strategy()
            
            max_attempts = GAME_SETTINGS['max_level_attempts']
            for attempt in range(max_attempts):
                shapes = []
                positions = strategy.generate_positions(GAME_SETTINGS['num_shapes'])
                
                # Create regular shapes
                for pos in positions:
                    color = random.choice(AVAILABLE_COLORS)
                    shape = ShapeFactory.create_random_shape(pos[0], pos[1], color)
                    shapes.append(shape)
            
                # Add target shapes
                target_shape1 = ShapeFactory.create_random_shape(100, 100, target_color)
                target_shape2 = ShapeFactory.create_random_shape(200, 150, target_color)
                shapes.extend([target_shape1, target_shape2])
                
                # Add some nested shapes for aesthetic appeal (20% chance)
                if random.random() < 0.2:
                    shapes = LevelGenerator.add_nested_shapes(shapes)
                
                # Validate the level thoroughly
                is_valid, issues = LevelValidator.validate_level(shapes, target_color)
                
                if is_valid:
                    return shapes, target_color, strategy.name
                elif attempt == max_attempts - 1:
                    # On final attempt, try to auto-fix issues
                    shapes = LevelValidator.auto_fix_overlaps(shapes)
                    is_valid, _ = LevelValidator.validate_level(shapes, target_color)
                    if is_valid:
                        return shapes, target_color, strategy.name
            
            return None, target_color, "legacy_generation"
    
    @staticmethod
    def add_nested_shapes(shapes):
        """Add some aesthetically pleasing nested shapes to the level"""
        if len(shapes) < 2:
            return shapes
        
        # Create some nested shapes by converting existing shapes
        nested_candidates = [s for s in shapes if hasattr(s, 'color')]
        
        if len(nested_candidates) < 2:
            return shapes
        
        # Pick 1-2 shapes to convert to nested shapes
        num_to_convert = min(2, len(nested_candidates) // 3)
        shapes_to_convert = random.sample(nested_candidates, num_to_convert)
        
        remaining_shapes = [s for s in shapes if s not in shapes_to_convert]
        
        # Create nested shapes
        for original_shape in shapes_to_convert:
            # Create shells with different colors
            from config import AESTHETIC_COLOR_SETS
            color_set = random.choice(list(AESTHETIC_COLOR_SETS.values()))
            
            num_shells = random.randint(2, 4)
            shells = []
            base_size = getattr(original_shape, 'size', 30)
            
            for i in range(num_shells):
                shell_color = color_set[i % len(color_set)]
                shell_size = base_size - (i * 6)
                if shell_size > 5:  # Minimum shell size
                    shells.append((shell_color, shell_size))
            
            if shells:
                nested_shape = NestedShapeFactory.create_nested_shape(
                    original_shape.x, original_shape.y, 
                    num_shells=len(shells), 
                    base_size=base_size,
                    color_sequence=[shell[0] for shell in shells]
                )
                remaining_shapes.append(nested_shape)
        
        return remaining_shapes
    
    @staticmethod
    def find_fusion_candidates(shapes, max_distance=80):
        """Find groups of same-colored shapes that could be fused"""
        from collections import defaultdict
        
        # Group shapes by color
        color_groups = defaultdict(list)
        for shape in shapes:
            color_groups[shape.color].append(shape)
        
        candidates = []
        
        for color, group in color_groups.items():
            if len(group) < 2:
                continue
            
            # Find close groups within this color
            close_groups = []
            remaining = group[:]
            
            while len(remaining) >= 2:
                cluster = [remaining.pop(0)]
                
                # Find shapes close to this cluster
                for i in range(len(remaining) - 1, -1, -1):
                    shape = remaining[i]
                    
                    # Check if shape is close to any shape in current cluster
                    for cluster_shape in cluster:
                        distance = shape.get_distance_to(cluster_shape)
                        if distance < max_distance:
                            cluster.append(remaining.pop(i))
                            break
                
                if len(cluster) >= 2:
                    close_groups.append(cluster)
            
            candidates.extend(close_groups)
        
        return candidates