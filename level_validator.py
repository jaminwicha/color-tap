import math
from collections import Counter
from nested_shapes import NestedShape, StaticShape

class LevelValidator:
    """Validates level layouts for playability and aesthetic quality"""
    
    @staticmethod
    def validate_level(shapes, target_color, min_distance=20):
        """
        Comprehensive level validation
        Returns (is_valid, issues) where issues is a list of problem descriptions
        """
        issues = []
        
        # Check if level is winnable
        if not LevelValidator.is_level_winnable(shapes, target_color):
            issues.append("Level is not winnable")
        
        # Check for overlapping shapes (excluding fused shapes)
        overlapping = LevelValidator.find_overlapping_shapes(shapes, min_distance)
        if overlapping:
            issues.append(f"Found {len(overlapping)} overlapping shape pairs")
        
        # Check if shapes are too close to edges
        edge_violations = LevelValidator.check_edge_distances(shapes)
        if edge_violations:
            issues.append(f"Found {len(edge_violations)} shapes too close to edges")
        
        # Check color distribution
        color_issues = LevelValidator.validate_color_distribution(shapes)
        if color_issues:
            issues.extend(color_issues)
        
        # Check shape density
        density_issue = LevelValidator.check_shape_density(shapes)
        if density_issue:
            issues.append(density_issue)
        
        return len(issues) == 0, issues
    
    @staticmethod
    def is_level_winnable(shapes, target_color):
        """Check if level can be completed"""
        # Count shapes by color, accounting for fused shapes
        color_counts = Counter()
        
        for shape in shapes:
            if isinstance(shape, NestedShape):
                # Fused shapes count as multiple shapes of the same color
                color_counts[shape.color] += shape.get_shell_count()
            else:
                color_counts[shape.color] += 1
        
        target_count = color_counts.get(target_color, 0)
        
        if target_count < 2:
            return False
        
        # Calculate total pairs that can be formed
        total_pairs = sum(count // 2 for count in color_counts.values())
        target_pairs = target_count // 2
        
        # Level is winnable if target color can be the last pair
        return target_pairs > 0 and (total_pairs == target_pairs or target_pairs == 1)
    
    @staticmethod
    def find_overlapping_shapes(shapes, min_distance=20):
        """Find pairs of shapes that are overlapping or too close"""
        overlapping_pairs = []
        
        for i, shape1 in enumerate(shapes):
            for j, shape2 in enumerate(shapes):
                if i >= j:
                    continue
                
                # Skip if either shape is fused (fused shapes are allowed to "overlap")
                if isinstance(shape1, NestedShape) or isinstance(shape2, NestedShape):
                    continue
                
                distance = shape1.get_distance_to(shape2)
                min_safe_distance = shape1.get_collision_radius() + shape2.get_collision_radius() + min_distance
                
                if distance < min_safe_distance:
                    overlapping_pairs.append((shape1, shape2, distance))
        
        return overlapping_pairs
    
    @staticmethod
    def check_edge_distances(shapes, min_edge_distance=30):
        """Check if shapes are too close to screen edges"""
        from config import WINDOW_WIDTH, WINDOW_HEIGHT
        
        violations = []
        
        for shape in shapes:
            max_dim = shape.get_max_dimension()
            
            # Check left edge
            if shape.x - max_dim < min_edge_distance:
                violations.append((shape, "left edge"))
            
            # Check right edge  
            if shape.x + max_dim > WINDOW_WIDTH - min_edge_distance:
                violations.append((shape, "right edge"))
            
            # Check top edge
            if shape.y - max_dim < min_edge_distance:
                violations.append((shape, "top edge"))
            
            # Check bottom edge
            if shape.y + max_dim > WINDOW_HEIGHT - min_edge_distance:
                violations.append((shape, "bottom edge"))
        
        return violations
    
    @staticmethod
    def validate_color_distribution(shapes):
        """Validate that colors are reasonably distributed"""
        issues = []
        
        # Count colors
        color_counts = Counter()
        for shape in shapes:
            if isinstance(shape, NestedShape):
                color_counts[shape.color] += shape.get_shell_count()
            else:
                color_counts[shape.color] += 1
        
        # Check for colors with only one shape
        single_colors = [color for color, count in color_counts.items() if count == 1]
        if len(single_colors) > 2:
            issues.append(f"Too many colors with single shapes: {len(single_colors)}")
        
        # Check for dominant colors (more than 60% of shapes)
        total_shapes = sum(color_counts.values())
        for color, count in color_counts.items():
            if count / total_shapes > 0.6:
                issues.append(f"Color {color} dominates the level ({count}/{total_shapes} shapes)")
        
        return issues
    
    @staticmethod
    def check_shape_density(shapes, max_density=0.3):
        """Check if shapes are too densely packed"""
        from config import WINDOW_WIDTH, WINDOW_HEIGHT
        
        # Calculate total area occupied by shapes
        total_shape_area = 0
        for shape in shapes:
            if isinstance(shape, NestedShape):
                # Approximate area for fused shapes
                total_shape_area += shape.total_width * shape.total_height * 0.7  # Account for gaps
            else:
                # Approximate area for regular shapes
                if hasattr(shape, 'width'):
                    total_shape_area += shape.width * shape.height
                else:
                    total_shape_area += shape.size * shape.size * 3.14
        
        screen_area = WINDOW_WIDTH * WINDOW_HEIGHT
        density = total_shape_area / screen_area
        
        if density > max_density:
            return f"Shape density too high: {density:.1%} (max: {max_density:.1%})"
        
        return None
    
    @staticmethod
    def auto_fix_overlaps(shapes, min_distance=25):
        """Attempt to automatically fix overlapping shapes by repositioning"""
        from config import WINDOW_WIDTH, WINDOW_HEIGHT
        
        fixed_shapes = []
        
        for shape in shapes:
            if isinstance(shape, NestedShape):
                fixed_shapes.append(shape)
                continue
            
            # Try to find a valid position for this shape
            max_attempts = 50
            for attempt in range(max_attempts):
                # If this is the first attempt, keep original position
                if attempt == 0:
                    new_x, new_y = shape.x, shape.y
                else:
                    # Try random positions
                    import random
                    max_dim = shape.get_max_dimension()
                    new_x = random.randint(max_dim + 30, WINDOW_WIDTH - max_dim - 30)
                    new_y = random.randint(max_dim + 30, WINDOW_HEIGHT - max_dim - 30)
                
                # Check if this position causes overlaps
                if hasattr(shape, 'width') and hasattr(shape, 'height'):
                    # Rectangle shape
                    temp_shape = type(shape)(new_x, new_y, shape.color, shape.width, shape.height)
                else:
                    # Circle, Square, or Triangle
                    temp_shape = type(shape)(new_x, new_y, shape.color, shape.size)
                
                valid_position = True
                for existing_shape in fixed_shapes:
                    if isinstance(existing_shape, NestedShape):
                        continue
                    
                    distance = temp_shape.get_distance_to(existing_shape)
                    min_safe_distance = temp_shape.get_collision_radius() + existing_shape.get_collision_radius() + min_distance
                    
                    if distance < min_safe_distance:
                        valid_position = False
                        break
                
                if valid_position:
                    shape.x = new_x
                    shape.y = new_y
                    break
            
            fixed_shapes.append(shape)
        
        return fixed_shapes