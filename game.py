import pygame
import sys
import uuid
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, Color, GAME_SETTINGS
from level_generator import LevelGenerator
from level_data import LevelData, LevelPersistence

class Game:
    def __init__(self, screen=None, clock=None):
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Color Tap")
            self.clock = pygame.time.Clock()
            self.owns_display = True
        else:
            self.screen = screen
            self.clock = clock
            self.owns_display = False
        
        self.background_color = Color.WHITE
        self.border_color = Color.BLACK
        self.target_color = Color.RED
        self.shapes = []
        self.dragging_shape = None
        self.last_merged_color = None
        self.level_complete = False
        self.show_impossible_popup = False
        self.level_persistence = LevelPersistence()
        self.current_level_data = None
        self.return_to_menu = False
    
    def load_or_create_level(self):
        saved_level = self.level_persistence.load_current_level()
        if saved_level:
            self.load_level_from_data(saved_level)
        else:
            self.create_new_level()
    
    def start_with_preview_level(self, preview_level):
        """Start game with a previewed level from menu"""
        if preview_level:
            level_id = str(uuid.uuid4())[:8]
            self.current_level_data = LevelData(level_id, preview_level['shapes'], 
                                              preview_level['target_color'], 
                                              preview_level['algorithm'])
            self.level_persistence.save_level(self.current_level_data)
            self.level_persistence.save_current_level(self.current_level_data)
            self.load_level_from_data(self.current_level_data)
        else:
            self.create_new_level()
    
    def create_new_level(self):
        result = LevelGenerator.create_level()
        if result[0] is not None:
            shapes, target_color, algorithm = result
            level_id = str(uuid.uuid4())[:8]
            self.current_level_data = LevelData(level_id, shapes, target_color, algorithm)
            self.level_persistence.save_level(self.current_level_data)
            self.level_persistence.save_current_level(self.current_level_data)
            self.load_level_from_data(self.current_level_data)
        else:
            self.show_impossible_popup = True
    
    def load_level_from_data(self, level_data):
        self.current_level_data = level_data
        self.shapes = level_data.get_fresh_shapes()
        self.target_color = level_data.target_color
        self.border_color = self.target_color
        self.show_impossible_popup = False
        self.level_complete = False
        self.last_merged_color = None
        self.background_color = Color.WHITE
    
    def reset_to_original_level(self):
        if self.current_level_data:
            self.load_level_from_data(self.current_level_data)
    
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
        
        if shapes_to_remove:
            self.check_level_possibility()
        
        if len(self.shapes) == 0 and self.last_merged_color == self.target_color:
            self.level_complete = True
    
    def check_level_possibility(self):
        if len(self.shapes) > 0 and not LevelGenerator.is_level_winnable(self.shapes, self.target_color):
            self.show_impossible_popup = True
    
    def draw_border(self):
        pygame.draw.rect(self.screen, self.border_color, 
                        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), GAME_SETTINGS['border_width'])
    
    def draw_ui(self):
        if self.level_complete:
            self.draw_completion_menu()
        elif self.show_impossible_popup:
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
        restart_rect = restart_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 110))
        self.screen.blit(restart_text, restart_rect)
        
        new_text = font_small.render("Press N for new level", True, Color.BLACK)
        new_rect = new_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 135))
        self.screen.blit(new_text, new_rect)
        
        close_text = font_small.render("Press ESC to close popup", True, Color.BLACK)
        close_rect = close_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 160))
        self.screen.blit(close_text, close_rect)
        
        menu_text = font_small.render("Press M for main menu", True, Color.BLACK)
        menu_rect = menu_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 185))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_completion_menu(self):
        popup_width = 450
        popup_height = 250
        popup_x = (WINDOW_WIDTH - popup_width) // 2
        popup_y = (WINDOW_HEIGHT - popup_height) // 2
        
        pygame.draw.rect(self.screen, Color.WHITE, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, Color.GREEN, (popup_x, popup_y, popup_width, popup_height), 4)
        
        font_large = pygame.font.Font(None, 48)
        title_text = font_large.render("Level Complete!", True, Color.GREEN)
        title_rect = title_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 50))
        self.screen.blit(title_text, title_rect)
        
        font_medium = pygame.font.Font(None, 28)
        
        option1_text = font_medium.render("Press R - Play Again (Same Level)", True, Color.BLACK)
        option1_rect = option1_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 120))
        self.screen.blit(option1_text, option1_rect)
        
        option2_text = font_medium.render("Press N - Play Next Level", True, Color.BLACK)
        option2_rect = option2_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 150))
        self.screen.blit(option2_text, option2_rect)
        
        option3_text = font_medium.render("Press Q - Back to Menu", True, Color.BLACK)
        option3_rect = option3_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 180))
        self.screen.blit(option3_text, option3_rect)
    
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
                        if self.level_complete:
                            self.reset_to_original_level()
                        else:
                            self.reset_to_original_level()
                    elif event.key == pygame.K_n:
                        self.create_new_level()
                    elif event.key == pygame.K_q:
                        if self.level_complete:
                            self.return_to_menu = True
                            running = False
                    elif event.key == pygame.K_m:
                        self.return_to_menu = True
                        running = False
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
        
        if self.owns_display:
            pygame.quit()
            sys.exit()