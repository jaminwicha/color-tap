#!/usr/bin/env python3
"""
Color Tap - Main Application
A 2D puzzle game where players match colored shapes to clear levels.
"""

import pygame
import sys
from main_menu import MainMenu
from game import Game
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

class ColorTapApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Color Tap")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize menu
        self.menu = MainMenu(self.screen, self.clock)
        self.game = None
        self.current_state = "menu"  # "menu" or "game"
    
    def run(self):
        """Main application loop"""
        while self.running:
            if self.current_state == "menu":
                self.run_menu()
            elif self.current_state == "game":
                self.run_game()
        
        pygame.quit()
        sys.exit()
    
    def run_menu(self):
        """Run the main menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            action = self.menu.handle_input(event)
            if action:
                self.handle_menu_action(action)
        
        self.menu.draw()
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def handle_menu_action(self, action):
        """Handle actions from the menu"""
        action_type, data = action
        
        if action_type == "start_new_game":
            self.start_new_game(data)
        elif action_type == "load_level":
            self.load_saved_level(data)
        elif action_type == "exit_game":
            self.running = False
        elif action_type == "no_previous_levels":
            # Could show a message, for now just ignore
            pass
    
    def start_new_game(self, preview_level):
        """Start a new game with optional preview level"""
        self.game = Game(self.screen, self.clock)
        if preview_level:
            self.game.start_with_preview_level(preview_level)
        else:
            self.game.load_or_create_level()
        self.current_state = "game"
    
    def load_saved_level(self, level_data):
        """Load a saved level"""
        self.game = Game(self.screen, self.clock)
        self.game.load_level_from_data(level_data)
        self.current_state = "game"
    
    def run_game(self):
        """Run the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.game.handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.game.handle_mouse_up()
            elif event.type == pygame.MOUSEMOTION:
                self.game.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.game.level_complete:
                        self.game.reset_to_original_level()
                    else:
                        self.game.reset_to_original_level()
                elif event.key == pygame.K_n:
                    self.game.create_new_level()
                elif event.key == pygame.K_q:
                    if self.game.level_complete:
                        self.return_to_menu()
                elif event.key == pygame.K_m:
                    self.return_to_menu()
                elif event.key == pygame.K_ESCAPE:
                    if self.game.show_impossible_popup:
                        self.game.show_impossible_popup = False
        
        # Update game
        for shape in self.game.shapes:
            shape.update()
        
        self.game.check_collisions()
        
        # Check if game wants to return to menu
        if hasattr(self.game, 'return_to_menu') and self.game.return_to_menu:
            self.return_to_menu()
            return
        
        # Draw game
        self.game.screen.fill(self.game.background_color)
        self.game.draw_border()
        
        for shape in self.game.shapes:
            shape.draw(self.game.screen)
        
        self.game.draw_ui()
        
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def return_to_menu(self):
        """Return to the main menu"""
        self.current_state = "menu"
        self.game = None
        # Refresh available levels in case new ones were created
        self.menu.refresh_available_levels()
        # Generate new preview level
        self.menu.generate_preview_level()

def main():
    """Main entry point"""
    app = ColorTapApp()
    app.run()

if __name__ == "__main__":
    main()