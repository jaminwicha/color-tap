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
        self.velocity_x = 0
        self.velocity_y = 0
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.friction = GAME_SETTINGS['friction']
    
    def update(self):
        if not self.being_dragged:
            # Enhanced smooth movement with interpolation
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            # More gradual friction for buttery movement
            enhanced_friction = 0.92
            self.velocity_x *= enhanced_friction
            self.velocity_y *= enhanced_friction
            
            # Apply small random perturbation for more natural, zen-like movement
            if abs(self.velocity_x) > 0.1 or abs(self.velocity_y) > 0.1:
                import random
                self.velocity_x += (random.random() - 0.5) * 0.01
                self.velocity_y += (random.random() - 0.5) * 0.01
            
            max_dimension = self.get_max_dimension()
            
            # Softer boundary bouncing with dampening
            if self.x - max_dimension <= 0 or self.x + max_dimension >= WINDOW_WIDTH:
                self.velocity_x = -self.velocity_x * 0.7  # Dampen the bounce
                self.x = max(max_dimension, min(WINDOW_WIDTH - max_dimension, self.x))
            
            if self.y - max_dimension <= 0 or self.y + max_dimension >= WINDOW_HEIGHT:
                self.velocity_y = -self.velocity_y * 0.7  # Dampen the bounce
                self.y = max(max_dimension, min(WINDOW_HEIGHT - max_dimension, self.y))
    
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
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
    
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
        pygame.draw.rect(screen, self.color, 
                        (int(self.x - self.size), int(self.y - self.size), 
                         self.size * 2, self.size * 2))
    
    def contains_point(self, x, y):
        return (abs(x - self.x) < self.size and abs(y - self.y) < self.size)
    
    def get_collision_radius(self):
        return self.size
    
    def get_max_dimension(self):
        return self.size

class Triangle(Shape):
    def draw(self, screen):
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]
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
        pygame.draw.rect(screen, self.color, 
                        (int(self.x - self.width // 2), int(self.y - self.height // 2), 
                         self.width, self.height))
    
    def contains_point(self, x, y):
        return (abs(x - self.x) < self.width // 2 and abs(y - self.y) < self.height // 2)
    
    def get_collision_radius(self):
        return max(self.width, self.height) // 2
    
    def get_max_dimension(self):
        return max(self.width, self.height)