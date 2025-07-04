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
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            self.velocity_x *= self.friction
            self.velocity_y *= self.friction
            
            max_dimension = self.get_max_dimension()
            
            if self.x - max_dimension <= 0 or self.x + max_dimension >= WINDOW_WIDTH:
                self.velocity_x = -self.velocity_x
                self.x = max(max_dimension, min(WINDOW_WIDTH - max_dimension, self.x))
            
            if self.y - max_dimension <= 0 or self.y + max_dimension >= WINDOW_HEIGHT:
                self.velocity_y = -self.velocity_y
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
            dx /= distance
            dy /= distance
            
            bounce_force = GAME_SETTINGS['bounce_force']
            self.velocity_x += dx * bounce_force
            self.velocity_y += dy * bounce_force
            other_shape.velocity_x -= dx * bounce_force
            other_shape.velocity_y -= dy * bounce_force

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