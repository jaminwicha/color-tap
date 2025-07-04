import random
from collections import Counter
from generation_strategies import GenerationStrategyFactory
from shape_factory import ShapeFactory
from config import AVAILABLE_COLORS, GAME_SETTINGS
from level_validator import LevelValidator
from fused_shapes import StackingPatterns

class LevelGenerator:
    @staticmethod
    def is_level_winnable(shapes, target_color):
        """Use the enhanced validator for winnability checking"""
        return LevelValidator.is_level_winnable(shapes, target_color)
    
    @staticmethod
    def create_level():
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
            
            # Add some fused shapes for aesthetic appeal (20% chance)
            if random.random() < 0.2:
                shapes = LevelGenerator.add_fused_shapes(shapes)
            
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
        
        return None, target_color, strategy.name
    
    @staticmethod
    def add_fused_shapes(shapes):
        """Add some aesthetically pleasing fused shapes to the level"""
        if len(shapes) < 4:
            return shapes
        
        # Find shapes that could be fused (same color, reasonably close)
        fusion_candidates = LevelGenerator.find_fusion_candidates(shapes)
        
        if not fusion_candidates:
            return shapes
        
        # Pick one group to fuse
        group_to_fuse = random.choice(fusion_candidates)
        if len(group_to_fuse) < 2:
            return shapes
        
        # Remove original shapes
        remaining_shapes = [s for s in shapes if s not in group_to_fuse]
        
        # Create fused shape
        center_x = sum(s.x for s in group_to_fuse) / len(group_to_fuse)
        center_y = sum(s.y for s in group_to_fuse) / len(group_to_fuse)
        
        pattern = StackingPatterns.get_random_pattern()
        
        if pattern == "vertical":
            fused_shape = StackingPatterns.create_vertical_stack(group_to_fuse, center_x, center_y)
        elif pattern == "horizontal":
            fused_shape = StackingPatterns.create_horizontal_stack(group_to_fuse, center_x, center_y)
        elif pattern == "pyramid":
            fused_shape = StackingPatterns.create_pyramid_stack(group_to_fuse, center_x, center_y)
        else:  # circle
            fused_shape = StackingPatterns.create_circle_stack(group_to_fuse, center_x, center_y)
        
        if fused_shape:
            remaining_shapes.append(fused_shape)
        
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