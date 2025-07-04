import pygame
import sys
from enum import Enum
from config import WINDOW_WIDTH, WINDOW_HEIGHT, Color
from level_data import LevelPersistence
from level_generator import LevelGenerator

class MenuState(Enum):
    MAIN_MENU = 1
    LEVEL_SELECT = 2

class MainMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.state = MenuState.MAIN_MENU
        self.selected_option = 0
        self.level_persistence = LevelPersistence()
        self.available_levels = self.level_persistence.list_levels()
        self.selected_level = 0
        self.preview_level = None
        self.generate_preview_level()
    
    def generate_preview_level(self):
        """Generate a preview of the next random level with validation"""
        from level_validator import LevelValidator
        
        max_attempts = 5
        for _ in range(max_attempts):
            result = LevelGenerator.create_level()
            if result[0] is not None:
                shapes, target_color, algorithm = result
                
                # Double-check validation before offering as preview
                is_valid, issues = LevelValidator.validate_level(shapes, target_color)
                
                if is_valid:
                    self.preview_level = {
                        'shapes': shapes,
                        'target_color': target_color,
                        'algorithm': algorithm
                    }
                    return
        
        # If we couldn't generate a valid level, clear preview
        self.preview_level = None
    
    def handle_input(self, event):
        """Handle menu input and return action"""
        if event.type == pygame.KEYDOWN:
            if self.state == MenuState.MAIN_MENU:
                return self.handle_main_menu_input(event)
            elif self.state == MenuState.LEVEL_SELECT:
                return self.handle_level_select_input(event)
        return None
    
    def handle_main_menu_input(self, event):
        """Handle main menu navigation"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % 3
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % 3
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.selected_option == 0:  # Start New Game
                return ("start_new_game", self.preview_level)
            elif self.selected_option == 1:  # Previous Levels
                if self.available_levels:
                    self.state = MenuState.LEVEL_SELECT
                    self.selected_level = 0
                else:
                    return ("no_previous_levels", None)
            elif self.selected_option == 2:  # Exit
                return ("exit_game", None)
        elif event.key == pygame.K_ESCAPE:
            return ("exit_game", None)
        return None
    
    def handle_level_select_input(self, event):
        """Handle level selection menu navigation"""
        if event.key == pygame.K_UP:
            self.selected_level = (self.selected_level - 1) % len(self.available_levels)
        elif event.key == pygame.K_DOWN:
            self.selected_level = (self.selected_level + 1) % len(self.available_levels)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            level_id = self.available_levels[self.selected_level]
            level_data = self.level_persistence.load_level(level_id)
            if level_data:
                return ("load_level", level_data)
        elif event.key == pygame.K_ESCAPE:
            self.state = MenuState.MAIN_MENU
        return None
    
    def refresh_available_levels(self):
        """Refresh the list of available levels"""
        self.available_levels = self.level_persistence.list_levels()
    
    def draw(self):
        """Draw the current menu state"""
        self.screen.fill(Color.WHITE)
        
        if self.state == MenuState.MAIN_MENU:
            self.draw_main_menu()
        elif self.state == MenuState.LEVEL_SELECT:
            self.draw_level_select()
    
    def draw_main_menu(self):
        """Draw the main menu"""
        # Title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("COLOR TAP", True, Color.BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Match colors to win!", True, Color.BLACK)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 170))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        option_font = pygame.font.Font(None, 48)
        options = ["Start New Game", "Previous Levels", "Exit Game"]
        colors = [Color.BLUE, Color.GREEN, Color.RED]
        
        start_y = 250
        for i, (option, color) in enumerate(zip(options, colors)):
            # Highlight selected option
            text_color = color if i == self.selected_option else Color.BLACK
            bg_color = Color.YELLOW if i == self.selected_option else None
            
            text = option_font.render(option, True, text_color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * 60))
            
            # Draw background for selected option
            if bg_color:
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, bg_color, bg_rect)
                pygame.draw.rect(self.screen, Color.BLACK, bg_rect, 2)
            
            self.screen.blit(text, text_rect)
        
        # Draw preview if available
        if self.preview_level and self.selected_option == 0:
            self.draw_level_preview()
        
        # Controls
        control_font = pygame.font.Font(None, 24)
        controls_text = control_font.render("↑↓ Navigate  ENTER/SPACE Select  ESC Exit", True, Color.BLACK)
        controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(controls_text, controls_rect)
    
    def draw_level_select(self):
        """Draw the level selection menu"""
        # Title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Select Previous Level", True, Color.BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        if not self.available_levels:
            # No levels available
            no_levels_font = pygame.font.Font(None, 36)
            no_levels_text = no_levels_font.render("No previous levels found", True, Color.RED)
            no_levels_rect = no_levels_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(no_levels_text, no_levels_rect)
        else:
            # Level list
            level_font = pygame.font.Font(None, 32)
            start_y = 150
            visible_levels = 8
            
            # Calculate scroll offset
            if len(self.available_levels) > visible_levels:
                scroll_offset = max(0, self.selected_level - visible_levels // 2)
                scroll_offset = min(scroll_offset, len(self.available_levels) - visible_levels)
            else:
                scroll_offset = 0
            
            for i in range(min(visible_levels, len(self.available_levels))):
                level_index = i + scroll_offset
                if level_index >= len(self.available_levels):
                    break
                
                level_id = self.available_levels[level_index]
                
                # Highlight selected level
                if level_index == self.selected_level:
                    bg_rect = pygame.Rect(100, start_y + i * 40 - 5, WINDOW_WIDTH - 200, 35)
                    pygame.draw.rect(self.screen, Color.YELLOW, bg_rect)
                    pygame.draw.rect(self.screen, Color.BLACK, bg_rect, 2)
                
                level_text = level_font.render(f"Level {level_id}", True, Color.BLACK)
                self.screen.blit(level_text, (120, start_y + i * 40))
        
        # Controls
        control_font = pygame.font.Font(None, 24)
        controls_text = control_font.render("↑↓ Navigate  ENTER/SPACE Select  ESC Back", True, Color.BLACK)
        controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(controls_text, controls_rect)
    
    def draw_level_preview(self):
        """Draw a small preview of the next level"""
        if not self.preview_level:
            return
        
        preview_x = 50
        preview_y = 400
        preview_width = 200
        preview_height = 150
        
        # Preview background
        preview_rect = pygame.Rect(preview_x, preview_y, preview_width, preview_height)
        pygame.draw.rect(self.screen, Color.WHITE, preview_rect)
        pygame.draw.rect(self.screen, self.preview_level['target_color'], preview_rect, 3)
        
        # Preview title
        preview_font = pygame.font.Font(None, 24)
        preview_title = preview_font.render("Next Level Preview:", True, Color.BLACK)
        self.screen.blit(preview_title, (preview_x, preview_y - 25))
        
        # Draw mini shapes
        if self.preview_level['shapes']:
            scale = 0.3
            offset_x = preview_x + preview_width // 2
            offset_y = preview_y + preview_height // 2
            
            for shape in self.preview_level['shapes'][:6]:  # Show first 6 shapes
                mini_x = offset_x + (shape.x - WINDOW_WIDTH // 2) * scale
                mini_y = offset_y + (shape.y - WINDOW_HEIGHT // 2) * scale
                mini_size = max(3, int(shape.size * scale))
                
                if hasattr(shape, 'width'):  # Rectangle
                    mini_width = max(3, int(shape.width * scale))
                    mini_height = max(3, int(shape.height * scale))
                    pygame.draw.rect(self.screen, shape.color,
                                   (int(mini_x - mini_width // 2), int(mini_y - mini_height // 2),
                                    mini_width, mini_height))
                else:  # Circle, Square, Triangle
                    pygame.draw.circle(self.screen, shape.color, (int(mini_x), int(mini_y)), mini_size)
        
        # Algorithm info
        algo_text = preview_font.render(f"Pattern: {self.preview_level['algorithm']}", True, Color.BLACK)
        self.screen.blit(algo_text, (preview_x, preview_y + preview_height + 5))