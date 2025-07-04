import pygame
import math
from abc import ABC, abstractmethod
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_SETTINGS

class Shape(ABC):
    def __init__(self, x, y, color, size=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.base_size = size  # Original size for pulsing
        self.velocity_x = 0
        self.velocity_y = 0
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.friction = GAME_SETTINGS['friction']
        self.pulse_scale = 1.0  # Multiplier for pulsing effect
        
        # Physics properties for realistic movement
        self.mass = size / 20.0  # Mass based on size
        self.viscosity_resistance = 0.02  # Resistance like moving through gel
        self.inertia_factor = 0.85  # How much the shape resists direction changes
        self.momentum_x = 0.0  # Accumulated momentum
        self.momentum_y = 0.0
    
    def update(self, beat_time=0.0):
        if not self.being_dragged:
            # Physics-based movement with weight, viscosity, and inertia
            
            # Apply momentum (inertia effect)
            self.momentum_x = self.momentum_x * self.inertia_factor + self.velocity_x * (1 - self.inertia_factor)
            self.momentum_y = self.momentum_y * self.inertia_factor + self.velocity_y * (1 - self.inertia_factor)
            
            # Apply viscosity resistance (like moving through gel)
            viscosity_factor = 1.0 - (self.viscosity_resistance * self.mass)
            self.momentum_x *= viscosity_factor
            self.momentum_y *= viscosity_factor
            
            # Update position with momentum
            self.x += self.momentum_x
            self.y += self.momentum_y
            
            # Enhanced friction for buttery movement (reduced for more realistic physics)
            enhanced_friction = 0.94
            self.velocity_x *= enhanced_friction
            self.velocity_y *= enhanced_friction
            
            # Apply small random perturbation for more natural movement
            if abs(self.velocity_x) > 0.1 or abs(self.velocity_y) > 0.1:
                import random
                perturbation = 0.005 / self.mass  # Heavier objects less affected by turbulence
                self.velocity_x += (random.random() - 0.5) * perturbation
                self.velocity_y += (random.random() - 0.5) * perturbation
            
            max_dimension = self.get_max_dimension()
            
            # Softer boundary bouncing with mass-based dampening
            bounce_dampening = 0.6 + (0.2 / self.mass)  # Heavier objects bounce less
            
            if self.x - max_dimension <= 0 or self.x + max_dimension >= WINDOW_WIDTH:
                self.velocity_x = -self.velocity_x * bounce_dampening
                self.momentum_x = -self.momentum_x * bounce_dampening
                self.x = max(max_dimension, min(WINDOW_WIDTH - max_dimension, self.x))
            
            if self.y - max_dimension <= 0 or self.y + max_dimension >= WINDOW_HEIGHT:
                self.velocity_y = -self.velocity_y * bounce_dampening
                self.momentum_y = -self.momentum_y * bounce_dampening
                self.y = max(max_dimension, min(WINDOW_HEIGHT - max_dimension, self.y))
        else:
            # When being dragged, reset momentum for responsive feel
            self.momentum_x = self.velocity_x
            self.momentum_y = self.velocity_y
        
        # Update pulse effect based on music beat (only for non-static shapes)
        import math
        pulse_intensity = 0.08  # Subtle pulsing effect
        self.pulse_scale = 1.0 + pulse_intensity * math.sin(beat_time * 2 * math.pi)
        self.size = int(self.base_size * self.pulse_scale)
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def contains_point(self, x, y):
        pass
    
    @abstractmethod
    def get_collision_radius(self):
        pass
    
    @abstractmethod
    def get_max_dimension(self):
        pass
    
    def get_distance_to(self, other_shape):
        dx = self.x - other_shape.x
        dy = self.y - other_shape.y
        return math.sqrt(dx * dx + dy * dy)
    
    def is_colliding_with(self, other_shape):
        return self.get_distance_to(other_shape) < (self.get_collision_radius() + other_shape.get_collision_radius())
    
    def bounce_off(self, other_shape):
        dx = self.x - other_shape.x
        dy = self.y - other_shape.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            # Normalize the collision vector
            dx /= distance
            dy /= distance
            
            # Softer, more zen-like bounce force
            zen_bounce_force = 3.5  # Reduced from harsh bouncing
            
            # Calculate relative velocities for more realistic physics
            rel_vel_x = self.velocity_x - other_shape.velocity_x
            rel_vel_y = self.velocity_y - other_shape.velocity_y
            
            # Dot product of relative velocity and collision normal
            vel_along_normal = rel_vel_x * dx + rel_vel_y * dy
            
            # Don't resolve if velocities are separating
            if vel_along_normal > 0:
                return
            
            # Apply impulse with dampening for smooth, gentle collisions
            impulse = zen_bounce_force * vel_along_normal * 0.6  # Dampening factor
            
            # Apply the impulse
            self.velocity_x -= impulse * dx * 0.5
            self.velocity_y -= impulse * dy * 0.5
            other_shape.velocity_x += impulse * dx * 0.5
            other_shape.velocity_y += impulse * dy * 0.5
            
            # Add slight separation to prevent sticking
            separation_force = 0.5
            overlap = (self.get_collision_radius() + other_shape.get_collision_radius()) - distance
            if overlap > 0:
                self.x += dx * overlap * separation_force
                self.y += dy * overlap * separation_force
                other_shape.x -= dx * overlap * separation_force
                other_shape.y -= dy * overlap * separation_force

class Circle(Shape):
    def draw(self, screen):
        # Draw with bevel/emboss effect and thicker border
        center_x, center_y = int(self.x), int(self.y)
        
        # Create subtle bevel effect with layered circles
        try:
            import pygame.gfxdraw
            
            # Shadow (darker, slightly offset)
            shadow_color = tuple(max(0, c - 40) for c in self.color)
            pygame.gfxdraw.filled_circle(screen, center_x + 2, center_y + 2, self.size, shadow_color)
            
            # Main shape
            pygame.gfxdraw.aacircle(screen, center_x, center_y, self.size, self.color)
            pygame.gfxdraw.filled_circle(screen, center_x, center_y, self.size, self.color)
            
            # Highlight (lighter, offset opposite to shadow)
            highlight_color = tuple(min(255, c + 30) for c in self.color)
            pygame.gfxdraw.filled_circle(screen, center_x - 1, center_y - 1, self.size // 3, highlight_color)
            
            # Thicker border
            border_color = tuple(max(0, c - 60) for c in self.color)
            for i in range(4):  # Multiple circles for thick border
                pygame.gfxdraw.aacircle(screen, center_x, center_y, self.size - i, border_color)
            
        except:
            # Fallback with basic effects
            # Shadow
            shadow_color = tuple(max(0, c - 40) for c in self.color)
            pygame.draw.circle(screen, shadow_color, (center_x + 2, center_y + 2), self.size)
            
            # Main shape
            pygame.draw.circle(screen, self.color, (center_x, center_y), self.size)
            
            # Highlight
            highlight_color = tuple(min(255, c + 30) for c in self.color)
            pygame.draw.circle(screen, highlight_color, (center_x - 1, center_y - 1), self.size // 3)
            
            # Thick border
            border_color = tuple(max(0, c - 60) for c in self.color)
            pygame.draw.circle(screen, border_color, (center_x, center_y), self.size, 4)
    
    def contains_point(self, x, y):
        dx = x - self.x
        dy = y - self.y
        return math.sqrt(dx * dx + dy * dy) < self.size
    
    def get_collision_radius(self):
        return self.size
    
    def get_max_dimension(self):
        return self.size

class Square(Shape):
    def draw(self, screen):
        import pygame  # Ensure pygame is available
        # Use anti-aliased rectangle for smooth edges
        rect = pygame.Rect(int(self.x - self.size), int(self.y - self.size), 
                          self.size * 2, self.size * 2)
        pygame.draw.rect(screen, self.color, rect)
        
        # Add subtle anti-aliasing border
        try:
            import pygame.gfxdraw
            pygame.gfxdraw.rectangle(screen, rect, self.color)
        except:
            pass
    
    def contains_point(self, x, y):
        return (abs(x - self.x) < self.size and abs(y - self.y) < self.size)
    
    def get_collision_radius(self):
        return self.size
    
    def get_max_dimension(self):
        return self.size

class Triangle(Shape):
    def draw(self, screen):
        points = [
            (int(self.x), int(self.y - self.size)),
            (int(self.x - self.size), int(self.y + self.size)),
            (int(self.x + self.size), int(self.y + self.size))
        ]
        
        # Use anti-aliased polygon for smooth edges
        try:
            import pygame.gfxdraw
            pygame.gfxdraw.aapolygon(screen, points, self.color)
            pygame.gfxdraw.filled_polygon(screen, points, self.color)
        except:
            # Fallback to regular polygon
            pygame.draw.polygon(screen, self.color, points)
    
    def contains_point(self, x, y):
        return math.sqrt((x - self.x)**2 + (y - self.y)**2) < self.size
    
    def get_collision_radius(self):
        return self.size
    
    def get_max_dimension(self):
        return self.size

class Rectangle(Shape):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color)
        self.width = width
        self.height = height
    
    def draw(self, screen):
        import pygame  # Ensure pygame is available
        # Use anti-aliased rectangle for smooth edges
        rect = pygame.Rect(int(self.x - self.width // 2), int(self.y - self.height // 2), 
                          self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
        
        # Add subtle anti-aliasing border
        try:
            import pygame.gfxdraw
            pygame.gfxdraw.rectangle(screen, rect, self.color)
        except:
            pass
    
    def contains_point(self, x, y):
        return (abs(x - self.x) < self.width // 2 and abs(y - self.y) < self.height // 2)
    
    def get_collision_radius(self):
        return max(self.width, self.height) // 2
    
    def get_max_dimension(self):
        return max(self.width, self.height)