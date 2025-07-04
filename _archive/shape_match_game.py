import pygame
import sys
import math
import random
from enum import Enum
from collections import Counter

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

class ShapeType(Enum):
    CIRCLE = 1
    SQUARE = 2
    TRIANGLE = 3

class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

class Shape:
    def __init__(self, x, y, shape_type, color, size=30):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.color = color
        self.size = size
        self.velocity_x = 0
        self.velocity_y = 0
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.friction = 0.95
        
    def update(self):
        if not self.being_dragged:
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            self.velocity_x *= self.friction
            self.velocity_y *= self.friction
            
            if self.x - self.size <= 0 or self.x + self.size >= WINDOW_WIDTH:
                self.velocity_x = -self.velocity_x
                self.x = max(self.size, min(WINDOW_WIDTH - self.size, self.x))
            
            if self.y - self.size <= 0 or self.y + self.size >= WINDOW_HEIGHT:
                self.velocity_y = -self.velocity_y
                self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))
    
    def draw(self, screen):
        if self.shape_type == ShapeType.CIRCLE:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        elif self.shape_type == ShapeType.SQUARE:
            pygame.draw.rect(screen, self.color, 
                           (int(self.x - self.size), int(self.y - self.size), 
                            self.size * 2, self.size * 2))
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
        return self.get_distance_to(other_shape) < (self.size + other_shape.size)
    
    def bounce_off(self, other_shape):
        dx = self.x - other_shape.x
        dy = self.y - other_shape.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            dx /= distance
            dy /= distance
            
            bounce_force = 5
            self.velocity_x += dx * bounce_force
            self.velocity_y += dy * bounce_force
            other_shape.velocity_x -= dx * bounce_force
            other_shape.velocity_y -= dy * bounce_force
    
    def contains_point(self, x, y):
        return self.get_distance_to(Shape(x, y, ShapeType.CIRCLE, Color.WHITE, 0)) < self.size

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Shape Match Game")
        self.clock = pygame.time.Clock()
        self.background_color = Color.WHITE
        self.border_color = Color.BLACK
        self.target_color = Color.RED
        self.shapes = []
        self.dragging_shape = None
        self.last_merged_color = None
        self.level_complete = False
        self.show_impossible_popup = False
        
        self.create_level()
    
    def create_level(self):
        colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        shape_types = [ShapeType.CIRCLE, ShapeType.SQUARE, ShapeType.TRIANGLE]
        
        self.target_color = random.choice(colors)
        self.border_color = self.target_color
        
        max_attempts = 10
        for attempt in range(max_attempts):
            self.shapes = []
            positions = self.generate_fractal_positions(8)
            
            for i, pos in enumerate(positions):
                shape_type = random.choice(shape_types)
                color = random.choice(colors)
                size = random.randint(20, 40)
                self.shapes.append(Shape(pos[0], pos[1], shape_type, color, size))
            
            self.shapes.append(Shape(100, 100, random.choice(shape_types), self.target_color, 25))
            self.shapes.append(Shape(200, 150, random.choice(shape_types), self.target_color, 25))
            
            if self.is_level_winnable():
                return
        
        self.show_impossible_popup = True
    
    def generate_fractal_positions(self, num_shapes):
        positions = []
        
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        
        for i in range(num_shapes):
            angle = (i / num_shapes) * 2 * math.pi
            
            base_radius = 150
            spiral_factor = 1 + (i * 0.3)
            fractal_noise = math.sin(angle * 3) * 30 + math.cos(angle * 5) * 20
            
            radius = base_radius * spiral_factor + fractal_noise
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            recursive_offset = self.generate_recursive_offset(i, 3)
            x += recursive_offset[0]
            y += recursive_offset[1]
            
            x = max(50, min(WINDOW_WIDTH - 50, x))
            y = max(50, min(WINDOW_HEIGHT - 50, y))
            
            positions.append((x, y))
        
        return positions
    
    def generate_recursive_offset(self, index, depth):
        if depth == 0:
            return (0, 0)
        
        base_offset = 40 / depth
        angle = (index * 2.39996) % (2 * math.pi)
        
        x = base_offset * math.cos(angle)
        y = base_offset * math.sin(angle)
        
        child_offset = self.generate_recursive_offset(index * 2, depth - 1)
        
        return (x + child_offset[0], y + child_offset[1])
    
    def is_level_winnable(self):
        color_counts = Counter(shape.color for shape in self.shapes)
        
        target_count = color_counts.get(self.target_color, 0)
        
        if target_count < 2:
            return False
        
        total_pairs = sum(count // 2 for count in color_counts.values())
        target_pairs = target_count // 2
        
        return target_pairs > 0 and (total_pairs == target_pairs or target_pairs == 1)
    
    def handle_mouse_down(self, pos):
        for shape in self.shapes:
            if shape.contains_point(pos[0], pos[1]):
                self.dragging_shape = shape
                shape.being_dragged = True
                shape.drag_offset_x = pos[0] - shape.x
                shape.drag_offset_y = pos[1] - shape.y
                shape.velocity_x = 0
                shape.velocity_y = 0
                break
    
    def handle_mouse_up(self):
        if self.dragging_shape:
            self.dragging_shape.being_dragged = False
            self.dragging_shape = None
    
    def handle_mouse_motion(self, pos):
        if self.dragging_shape:
            self.dragging_shape.x = pos[0] - self.dragging_shape.drag_offset_x
            self.dragging_shape.y = pos[1] - self.dragging_shape.drag_offset_y
    
    def check_collisions(self):
        shapes_to_remove = []
        
        for i, shape1 in enumerate(self.shapes):
            for j, shape2 in enumerate(self.shapes):
                if i >= j:
                    continue
                
                if shape1.is_colliding_with(shape2):
                    if shape1.color == shape2.color:
                        self.last_merged_color = shape1.color
                        self.background_color = shape1.color
                        shapes_to_remove.extend([shape1, shape2])
                    else:
                        shape1.bounce_off(shape2)
        
        for shape in shapes_to_remove:
            if shape in self.shapes:
                self.shapes.remove(shape)
        
        if len(self.shapes) == 0 and self.last_merged_color == self.target_color:
            self.level_complete = True
    
    def draw_border(self):
        pygame.draw.rect(self.screen, self.border_color, 
                        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 5)
    
    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        
        if self.level_complete:
            win_text = font.render("Level Complete!", True, Color.GREEN)
            self.screen.blit(win_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
        
        if self.show_impossible_popup:
            self.draw_impossible_popup()
    
    def draw_impossible_popup(self):
        popup_width = 400
        popup_height = 200
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        
        pygame.draw.rect(self.screen, Color.WHITE, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, Color.BLACK, (popup_x, popup_y, popup_width, popup_height), 3)
        
        font = pygame.font.Font(None, 32)
        title_text = font.render("Level Impossible!", True, Color.RED)
        title_rect = title_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 40))
        self.screen.blit(title_text, title_rect)
        
        font_small = pygame.font.Font(None, 24)
        msg_text = font_small.render("No valid solution found.", True, Color.BLACK)
        msg_rect = msg_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 80))
        self.screen.blit(msg_text, msg_rect)
        
        restart_text = font_small.render("Press R to restart level", True, Color.BLACK)
        restart_rect = restart_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 120))
        self.screen.blit(restart_text, restart_rect)
        
        close_text = font_small.render("Press ESC to close popup", True, Color.BLACK)
        close_rect = close_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 150))
        self.screen.blit(close_text, close_rect)
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up()
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                    elif event.key == pygame.K_ESCAPE:
                        if self.show_impossible_popup:
                            self.show_impossible_popup = False
            
            for shape in self.shapes:
                shape.update()
            
            self.check_collisions()
            
            self.screen.fill(self.background_color)
            self.draw_border()
            
            for shape in self.shapes:
                shape.draw(self.screen)
            
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()