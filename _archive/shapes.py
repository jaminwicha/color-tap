import pygame
import math
from enum import Enum
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_SETTINGS, Color

class ShapeType(Enum):
    CIRCLE = 1
    SQUARE = 2
    TRIANGLE = 3
    RECTANGLE = 4

class Shape:
    def __init__(self, x, y, shape_type, color, size=30, width=None, height=None):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.color = color
        self.size = size
        self.width = width if width is not None else size
        self.height = height if height is not None else size
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
            
            max_dimension = max(self.width, self.height) if self.shape_type == ShapeType.RECTANGLE else self.size
            
            if self.x - max_dimension <= 0 or self.x + max_dimension >= WINDOW_WIDTH:
                self.velocity_x = -self.velocity_x
                self.x = max(max_dimension, min(WINDOW_WIDTH - max_dimension, self.x))
            
            if self.y - max_dimension <= 0 or self.y + max_dimension >= WINDOW_HEIGHT:
                self.velocity_y = -self.velocity_y
                self.y = max(max_dimension, min(WINDOW_HEIGHT - max_dimension, self.y))
    
    def draw(self, screen):
        if self.shape_type == ShapeType.CIRCLE:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        elif self.shape_type == ShapeType.SQUARE:
            pygame.draw.rect(screen, self.color, 
                           (int(self.x - self.size), int(self.y - self.size), 
                            self.size * 2, self.size * 2))
        elif self.shape_type == ShapeType.RECTANGLE:
            pygame.draw.rect(screen, self.color, 
                           (int(self.x - self.width // 2), int(self.y - self.height // 2), 
                            self.width, self.height))
        elif self.shape_type == ShapeType.TRIANGLE:
            points = [
                (self.x, self.y - self.size),
                (self.x - self.size, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ]
            pygame.draw.polygon(screen, self.color, points)
    
    def get_distance_to(self, other_shape):
        dx = self.x - other_shape.x
        dy = self.y - other_shape.y
        return math.sqrt(dx * dx + dy * dy)
    
    def is_colliding_with(self, other_shape):
        self_radius = max(self.width, self.height) // 2 if self.shape_type == ShapeType.RECTANGLE else self.size
        other_radius = max(other_shape.width, other_shape.height) // 2 if other_shape.shape_type == ShapeType.RECTANGLE else other_shape.size
        return self.get_distance_to(other_shape) < (self_radius + other_radius)
    
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
    
    def contains_point(self, x, y):
        if self.shape_type == ShapeType.RECTANGLE:
            return (abs(x - self.x) < self.width // 2 and abs(y - self.y) < self.height // 2)
        else:
            return self.get_distance_to(Shape(x, y, ShapeType.CIRCLE, Color.WHITE, 0)) < self.size