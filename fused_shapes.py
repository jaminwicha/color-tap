import pygame
import math
from shape_behaviors import Shape
from config import GAME_SETTINGS

class FusedShape(Shape):
    """A shape composed of multiple fused shapes stacked together"""
    
    def __init__(self, x, y, color, component_shapes, stack_pattern="vertical"):
        # Use the average size of component shapes
        avg_size = sum(shape.size for shape in component_shapes) // len(component_shapes)
        super().__init__(x, y, color, avg_size)
        
        self.component_shapes = component_shapes
        self.stack_pattern = stack_pattern
        self.total_width = self._calculate_total_width()
        self.total_height = self._calculate_total_height()
        
        # Update component positions relative to the fused shape center
        self._update_component_positions()
    
    def _calculate_total_width(self):
        """Calculate the total width of the fused shape"""
        if self.stack_pattern == "horizontal":
            return sum(getattr(shape, 'width', shape.size * 2) for shape in self.component_shapes)
        else:
            return max(getattr(shape, 'width', shape.size * 2) for shape in self.component_shapes)
    
    def _calculate_total_height(self):
        """Calculate the total height of the fused shape"""
        if self.stack_pattern == "vertical":
            return sum(getattr(shape, 'height', shape.size * 2) for shape in self.component_shapes)
        else:
            return max(getattr(shape, 'height', shape.size * 2) for shape in self.component_shapes)
    
    def _update_component_positions(self):
        """Update positions of component shapes relative to fused shape center"""
        if self.stack_pattern == "vertical":
            current_y = self.y - self.total_height // 2
            for shape in self.component_shapes:
                shape_height = getattr(shape, 'height', shape.size * 2)
                shape.x = self.x
                shape.y = current_y + shape_height // 2
                current_y += shape_height
        elif self.stack_pattern == "horizontal":
            current_x = self.x - self.total_width // 2
            for shape in self.component_shapes:
                shape_width = getattr(shape, 'width', shape.size * 2)
                shape.x = current_x + shape_width // 2
                shape.y = self.y
                current_x += shape_width
        elif self.stack_pattern == "pyramid":
            # Stack in pyramid formation
            self._arrange_pyramid()
        elif self.stack_pattern == "circle":
            # Arrange in circular pattern
            self._arrange_circle()
    
    def _arrange_pyramid(self):
        """Arrange shapes in a pyramid pattern"""
        num_shapes = len(self.component_shapes)
        if num_shapes <= 1:
            self.component_shapes[0].x = self.x
            self.component_shapes[0].y = self.y
            return
        
        # Bottom row has more shapes, top has fewer
        rows = int(math.sqrt(num_shapes)) + 1
        shape_index = 0
        
        for row in range(rows):
            if shape_index >= num_shapes:
                break
            
            shapes_in_row = max(1, num_shapes - shape_index) if row == rows - 1 else min(rows - row, num_shapes - shape_index)
            row_y = self.y + (row - rows // 2) * 40
            
            for col in range(shapes_in_row):
                if shape_index >= num_shapes:
                    break
                
                shape = self.component_shapes[shape_index]
                shape.x = self.x + (col - shapes_in_row // 2) * 45
                shape.y = row_y
                shape_index += 1
    
    def _arrange_circle(self):
        """Arrange shapes in a circular pattern"""
        num_shapes = len(self.component_shapes)
        radius = max(30, num_shapes * 8)
        
        for i, shape in enumerate(self.component_shapes):
            angle = (i / num_shapes) * 2 * math.pi
            shape.x = self.x + radius * math.cos(angle)
            shape.y = self.y + radius * math.sin(angle)
    
    def update(self):
        """Update fused shape physics"""
        super().update()
        # Update all component shapes to follow the fused shape
        self._update_component_positions()
    
    def draw(self, screen):
        """Draw all component shapes"""
        for shape in self.component_shapes:
            shape.draw(screen)
        
        # Optional: Draw connection lines or outline
        if len(self.component_shapes) > 1:
            self._draw_fusion_indicator(screen)
    
    def _draw_fusion_indicator(self, screen):
        """Draw subtle indicators showing shapes are fused"""
        # Draw thin connecting lines between component shapes
        for i in range(len(self.component_shapes) - 1):
            shape1 = self.component_shapes[i]
            shape2 = self.component_shapes[i + 1]
            
            # Draw a thin line
            pygame.draw.line(screen, (128, 128, 128), 
                           (int(shape1.x), int(shape1.y)), 
                           (int(shape2.x), int(shape2.y)), 2)
    
    def contains_point(self, x, y):
        """Check if point is inside any component shape"""
        return any(shape.contains_point(x, y) for shape in self.component_shapes)
    
    def get_collision_radius(self):
        """Get the collision radius for the entire fused shape"""
        return max(self.total_width, self.total_height) // 2
    
    def get_max_dimension(self):
        """Get the maximum dimension of the fused shape"""
        return max(self.total_width, self.total_height)
    
    def is_colliding_with(self, other_shape):
        """Check collision with any component of this fused shape"""
        if isinstance(other_shape, FusedShape):
            # Check if any component of this shape collides with any component of other
            for my_component in self.component_shapes:
                for other_component in other_shape.component_shapes:
                    if my_component.is_colliding_with(other_component):
                        return True
            return False
        else:
            # Check if any component collides with the single shape
            return any(component.is_colliding_with(other_shape) for component in self.component_shapes)
    
    def get_component_count(self):
        """Get the number of shapes in this fused shape"""
        return len(self.component_shapes)
    
    def remove_component(self):
        """Remove one component from the fused shape"""
        if len(self.component_shapes) > 0:
            self.component_shapes.pop()
            # Recalculate dimensions
            self.total_width = self._calculate_total_width()
            self.total_height = self._calculate_total_height()
            # Update positions
            self._update_component_positions()
            return True
        return False

class StackingPatterns:
    """Factory for creating different stacking patterns"""
    
    @staticmethod
    def create_vertical_stack(shapes, x, y):
        """Create a vertical stack of shapes"""
        if not shapes:
            return None
        
        # All shapes in stack should have same color
        color = shapes[0].color
        return FusedShape(x, y, color, shapes, "vertical")
    
    @staticmethod
    def create_horizontal_stack(shapes, x, y):
        """Create a horizontal stack of shapes"""
        if not shapes:
            return None
        
        color = shapes[0].color
        return FusedShape(x, y, color, shapes, "horizontal")
    
    @staticmethod
    def create_pyramid_stack(shapes, x, y):
        """Create a pyramid arrangement of shapes"""
        if not shapes:
            return None
        
        color = shapes[0].color
        return FusedShape(x, y, color, shapes, "pyramid")
    
    @staticmethod
    def create_circle_stack(shapes, x, y):
        """Create a circular arrangement of shapes"""
        if not shapes:
            return None
        
        color = shapes[0].color
        return FusedShape(x, y, color, shapes, "circle")
    
    @staticmethod
    def get_random_pattern():
        """Get a random stacking pattern"""
        import random
        patterns = ["vertical", "horizontal", "pyramid", "circle"]
        return random.choice(patterns)