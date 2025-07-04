import pygame
import math
from shape_behaviors import Shape
from config import GAME_SETTINGS

class NestedShape(Shape):
    """A shape composed of nested layers like a matryoshka doll"""
    
    def __init__(self, x, y, shells, is_static=False):
        """
        Initialize a nested shape with multiple shells
        Args:
            x, y: Position
            shells: List of (color, size) tuples representing shells from outer to inner
            is_static: Whether this shape is static (non-moving)
        """
        if not shells:
            raise ValueError("NestedShape must have at least one shell")
        
        # Use the outermost shell's properties
        outer_color, outer_size = shells[0]
        super().__init__(x, y, outer_color, outer_size)
        
        self.shells = shells  # List of (color, size) tuples
        self.is_static = is_static
        self.is_hollow = False  # Will be set for hollow static shapes
        
        # Static shapes don't move
        if self.is_static:
            self.velocity_x = 0
            self.velocity_y = 0
            self.friction = 0
    
    def get_outer_shell(self):
        """Get the outermost shell (color, size)"""
        return self.shells[0] if self.shells else None
    
    def get_shell_count(self):
        """Get the number of shells"""
        return len(self.shells)
    
    def remove_outer_shell(self):
        """Remove the outermost shell, revealing the inner shell"""
        if len(self.shells) > 1:
            self.shells.pop(0)
            # Update the shape's color and size to the new outer shell
            self.color, self.size = self.shells[0]
            return True
        elif len(self.shells) == 1:
            # Remove the last shell - shape should be eliminated
            self.shells.clear()
            return True
        return False
    
    def update(self):
        """Update nested shape physics"""
        if not self.is_static:
            super().update()
    
    def draw(self, screen):
        """Draw all shells from outer to inner with anti-aliasing"""
        if not self.shells:
            return
            
        # Draw shells from outer to inner with smooth anti-aliased circles
        for i, (shell_color, shell_size) in enumerate(self.shells):
            try:
                import pygame.gfxdraw
                if self.is_hollow and i == 0:
                    # Draw hollow outer shell with anti-aliasing
                    pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), shell_size, shell_color)
                    pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), shell_size-1, shell_color)
                    pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), shell_size-2, shell_color)
                else:
                    # Draw filled shell with anti-aliasing
                    pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), shell_size, shell_color)
                    pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), shell_size, shell_color)
            except:
                # Fallback to regular circles
                if self.is_hollow and i == 0:
                    pygame.draw.circle(screen, shell_color, (int(self.x), int(self.y)), shell_size, 3)
                else:
                    pygame.draw.circle(screen, shell_color, (int(self.x), int(self.y)), shell_size)
        
        # Draw a subtle outline to show nesting with anti-aliasing
        if len(self.shells) > 1:
            try:
                import pygame.gfxdraw
                pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), 
                                      self.shells[0][1], (255, 255, 255))
            except:
                pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 
                                 self.shells[0][1], 2)
    
    def contains_point(self, x, y):
        """Check if point is inside the outermost shell"""
        if not self.shells:
            return False
        dx = x - self.x
        dy = y - self.y
        return math.sqrt(dx * dx + dy * dy) < self.shells[0][1]
    
    def get_collision_radius(self):
        """Get the collision radius (outermost shell size)"""
        return self.shells[0][1] if self.shells else 0
    
    def get_max_dimension(self):
        """Get the maximum dimension (outermost shell size)"""
        return self.shells[0][1] if self.shells else 0
    
    def is_colliding_with(self, other_shape):
        """Check collision with another shape"""
        if isinstance(other_shape, NestedShape):
            # Check if outermost shells collide
            distance = self.get_distance_to(other_shape)
            return distance < (self.get_collision_radius() + other_shape.get_collision_radius())
        else:
            # Check collision with regular shape
            return super().is_colliding_with(other_shape)
    
    def is_empty(self):
        """Check if the nested shape has no shells left"""
        return len(self.shells) == 0


class StaticShape(NestedShape):
    """A static shape that doesn't move and can be attached to walls"""
    
    def __init__(self, x, y, shells, attachment_side=None, is_hollow=False):
        """
        Initialize a static shape
        Args:
            x, y: Position
            shells: List of (color, size) tuples
            attachment_side: 'left', 'right', 'top', 'bottom' or None for free-standing
            is_hollow: Whether the shape is hollow (allows other shapes inside)
        """
        super().__init__(x, y, shells, is_static=True)
        self.attachment_side = attachment_side
        self.is_hollow = is_hollow
        
        # Adjust position based on wall attachment
        if attachment_side:
            self._adjust_position_for_attachment()
    
    def _adjust_position_for_attachment(self):
        """Adjust position to attach to specified wall"""
        from config import WINDOW_WIDTH, WINDOW_HEIGHT
        
        outer_size = self.shells[0][1]
        
        if self.attachment_side == 'left':
            self.x = outer_size
        elif self.attachment_side == 'right':
            self.x = WINDOW_WIDTH - outer_size
        elif self.attachment_side == 'top':
            self.y = outer_size
        elif self.attachment_side == 'bottom':
            self.y = WINDOW_HEIGHT - outer_size
    
    def update(self):
        """Static shapes don't move"""
        pass
    
    def can_contain_shape(self, other_shape):
        """Check if this hollow static shape can contain another shape"""
        if not self.is_hollow:
            return False
        
        # Check if the other shape fits inside and has different color
        if hasattr(other_shape, 'color') and other_shape.color == self.color:
            return False  # Same color would be confusing
        
        # Check if it fits inside
        distance = self.get_distance_to(other_shape)
        inner_radius = self.get_collision_radius() - 10  # Leave some margin
        return distance < inner_radius and other_shape.get_collision_radius() < inner_radius
    
    def draw(self, screen):
        """Draw static shape with special styling"""
        if not self.shells:
            return
        
        # Draw shells with static shape styling
        for i, (shell_color, shell_size) in enumerate(self.shells):
            if self.is_hollow and i == 0:
                # Draw hollow outer shell with thicker border
                pygame.draw.circle(screen, shell_color, (int(self.x), int(self.y)), shell_size, 5)
            else:
                # Draw filled shell
                pygame.draw.circle(screen, shell_color, (int(self.x), int(self.y)), shell_size)
        
        # Draw attachment indicator if attached to wall
        if self.attachment_side:
            attachment_color = (128, 128, 128)
            outer_size = self.shells[0][1]
            
            if self.attachment_side == 'left':
                pygame.draw.line(screen, attachment_color, 
                               (0, int(self.y)), (int(self.x - outer_size), int(self.y)), 3)
            elif self.attachment_side == 'right':
                pygame.draw.line(screen, attachment_color, 
                               (int(self.x + outer_size), int(self.y)), 
                               (screen.get_width(), int(self.y)), 3)
            elif self.attachment_side == 'top':
                pygame.draw.line(screen, attachment_color, 
                               (int(self.x), 0), (int(self.x), int(self.y - outer_size)), 3)
            elif self.attachment_side == 'bottom':
                pygame.draw.line(screen, attachment_color, 
                               (int(self.x), int(self.y + outer_size)), 
                               (int(self.x), screen.get_height()), 3)


class NestedShapeFactory:
    """Factory for creating nested shapes with various configurations"""
    
    @staticmethod
    def create_nested_shape(x, y, num_shells=3, base_size=40, color_sequence=None):
        """Create a nested shape with specified number of shells"""
        if color_sequence is None:
            from config import Color
            colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE]
            color_sequence = colors[:num_shells]
        
        shells = []
        for i in range(num_shells):
            shell_size = base_size - (i * 8)  # Each shell is 8 pixels smaller
            shell_color = color_sequence[i % len(color_sequence)]
            shells.append((shell_color, shell_size))
        
        return NestedShape(x, y, shells)
    
    @staticmethod
    def create_static_shape(x, y, num_shells=2, base_size=60, attachment_side=None, 
                           is_hollow=False, color_sequence=None):
        """Create a static nested shape"""
        if color_sequence is None:
            from config import Color
            colors = [Color.ORANGE, Color.CYAN, Color.MAGENTA, Color.LIME]
            color_sequence = colors[:num_shells]
        
        shells = []
        for i in range(num_shells):
            shell_size = base_size - (i * 10)  # Each shell is 10 pixels smaller
            shell_color = color_sequence[i % len(color_sequence)]
            shells.append((shell_color, shell_size))
        
        return StaticShape(x, y, shells, attachment_side, is_hollow)
    
    @staticmethod
    def create_hollow_container(x, y, container_color, container_size=80):
        """Create a hollow static shape that can contain other shapes"""
        from config import Color
        # Only one shell for hollow containers
        shells = [(container_color, container_size)]
        return StaticShape(x, y, shells, attachment_side=None, is_hollow=True)