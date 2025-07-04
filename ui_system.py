import pygame
import math
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    ENCOURAGEMENT = "encouragement"
    CELEBRATION = "celebration"

@dataclass
class ColorPalette:
    """Aesthetic color palette for the game"""
    primary: Tuple[int, int, int]
    secondary: Tuple[int, int, int]
    accent: Tuple[int, int, int]
    background: Tuple[int, int, int]
    text: Tuple[int, int, int]
    success: Tuple[int, int, int]
    warning: Tuple[int, int, int]
    error: Tuple[int, int, int]
    
    @property
    def as_dict(self) -> Dict[str, Tuple[int, int, int]]:
        return {
            'primary': self.primary,
            'secondary': self.secondary,
            'accent': self.accent,
            'background': self.background,
            'text': self.text,
            'success': self.success,
            'warning': self.warning,
            'error': self.error
        }

class AestheticPalettes:
    """Collection of beautiful color palettes"""
    
    AURORA = ColorPalette(
        primary=(71, 225, 166),      # Mint green
        secondary=(255, 121, 198),   # Pink
        accent=(255, 195, 0),        # Golden yellow
        background=(13, 17, 23),     # Dark blue-black
        text=(248, 248, 242),        # Off-white
        success=(80, 250, 123),      # Bright green
        warning=(255, 184, 108),     # Orange
        error=(255, 85, 85)          # Red
    )
    
    SUNSET = ColorPalette(
        primary=(255, 158, 128),     # Coral
        secondary=(255, 206, 84),    # Warm yellow
        accent=(108, 92, 231),       # Purple
        background=(26, 24, 38),     # Dark purple
        text=(255, 255, 255),        # White
        success=(129, 236, 159),     # Mint
        warning=(255, 206, 84),      # Yellow
        error=(255, 107, 107)        # Light red
    )
    
    OCEAN = ColorPalette(
        primary=(64, 224, 208),      # Turquoise
        secondary=(135, 206, 235),   # Sky blue
        accent=(255, 182, 193),      # Light pink
        background=(25, 25, 112),    # Midnight blue
        text=(240, 248, 255),        # Alice blue
        success=(127, 255, 212),     # Aquamarine
        warning=(255, 215, 0),       # Gold
        error=(255, 99, 71)          # Tomato
    )
    
    FOREST = ColorPalette(
        primary=(144, 238, 144),     # Light green
        secondary=(34, 139, 34),     # Forest green
        accent=(255, 140, 0),        # Orange
        background=(47, 79, 79),     # Dark slate gray
        text=(245, 245, 220),        # Beige
        success=(50, 205, 50),       # Lime green
        warning=(255, 165, 0),       # Orange
        error=(220, 20, 60)          # Crimson
    )
    
    COSMIC = ColorPalette(
        primary=(138, 43, 226),      # Blue violet
        secondary=(75, 0, 130),      # Indigo
        accent=(255, 20, 147),       # Deep pink
        background=(25, 25, 25),     # Very dark gray
        text=(230, 230, 250),        # Lavender
        success=(124, 252, 0),       # Lawn green
        warning=(255, 215, 0),       # Gold
        error=(255, 69, 0)           # Red orange
    )
    
    @classmethod
    def get_all_palettes(cls) -> List[ColorPalette]:
        return [cls.AURORA, cls.SUNSET, cls.OCEAN, cls.FOREST, cls.COSMIC]
    
    @classmethod
    def get_random_palette(cls) -> ColorPalette:
        import random
        return random.choice(cls.get_all_palettes())

class FriendlyMessages:
    """Collection of friendly and encouraging messages"""
    
    WELCOME_MESSAGES = [
        "Welcome to Color Tap! ✨",
        "Ready to paint the world with color? 🎨",
        "Time for some colorful fun! 🌈",
        "Let's create something beautiful together! 💫"
    ]
    
    LEVEL_START_MESSAGES = [
        "Here we go! Match the colors to win! 🎯",
        "New adventure awaits! 🚀",
        "Time to show your color-matching skills! 🎪",
        "Let's make some magic happen! ✨"
    ]
    
    SUCCESSFUL_MERGE_MESSAGES = [
        "Beautiful match! 🌟",
        "Perfect harmony! 🎵",
        "Colors united! 💕",
        "Wonderful! 🎉",
        "Fantastic pairing! ✨",
        "Color magic! 🪄"
    ]
    
    BOUNCE_ENCOURAGEMENT = [
        "Keep trying! 💪",
        "Almost there! 🎯",
        "You've got this! 🌟",
        "Try a different approach! 🔄",
        "Keep experimenting! 🧪",
        "Every attempt teaches us something! 💡"
    ]
    
    LEVEL_COMPLETE_MESSAGES = [
        "🎉 Magnificent! You've mastered this level! 🎉",
        "🌟 Outstanding work! Level completed! 🌟",
        "✨ Brilliant! You're a color wizard! ✨",
        "🎊 Amazing! Another level conquered! 🎊",
        "🏆 Exceptional! You've done it! 🏆",
        "🌈 Wonderful! Colors perfectly matched! 🌈"
    ]
    
    GAME_OVER_MESSAGES = [
        "Great effort! Ready to try again? 🔄",
        "You're getting better! Another round? 🎯",
        "Almost had it! One more try? 💪",
        "Practice makes perfect! Let's go again! 🌟"
    ]
    
    LOADING_MESSAGES = [
        "Preparing your colorful adventure... 🎨",
        "Mixing beautiful colors... 🌈",
        "Creating something special... ✨",
        "Setting up the magic... 🪄"
    ]
    
    MENU_HINTS = [
        "💡 Tip: Same colors merge, different colors bounce!",
        "🎯 Goal: Match all shapes to the border color!",
        "🌟 Pro tip: Plan your moves carefully!",
        "✨ Remember: Every level is solvable!"
    ]
    
    @classmethod
    def get_random_message(cls, message_type: str) -> str:
        import random
        messages = getattr(cls, f"{message_type.upper()}_MESSAGES", [])
        return random.choice(messages) if messages else "Keep going! 🌟"

class IconRenderer:
    """Renders beautiful icons for UI elements"""
    
    def __init__(self):
        self.icon_cache = {}
    
    def draw_heart_icon(self, surface: pygame.Surface, pos: Tuple[int, int], 
                       size: int, color: Tuple[int, int, int]):
        """Draw a heart icon"""
        x, y = pos
        # Create heart shape using circles and a triangle
        heart_points = []
        
        # Left curve
        for angle in range(0, 180, 5):
            rad = math.radians(angle)
            px = x + int(size * 0.3 * math.cos(rad)) - size // 4
            py = y + int(size * 0.3 * math.sin(rad)) - size // 4
            heart_points.append((px, py))
        
        # Right curve
        for angle in range(0, 180, 5):
            rad = math.radians(angle)
            px = x + int(size * 0.3 * math.cos(rad)) + size // 4
            py = y + int(size * 0.3 * math.sin(rad)) - size // 4
            heart_points.append((px, py))
        
        # Bottom point
        heart_points.append((x, y + size // 2))
        
        if len(heart_points) > 2:
            pygame.draw.polygon(surface, color, heart_points)
    
    def draw_star_icon(self, surface: pygame.Surface, pos: Tuple[int, int], 
                      size: int, color: Tuple[int, int, int]):
        """Draw a star icon"""
        x, y = pos
        points = []
        
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                radius = size // 2
            else:
                radius = size // 4
            
            px = x + int(radius * math.cos(angle - math.pi / 2))
            py = y + int(radius * math.sin(angle - math.pi / 2))
            points.append((px, py))
        
        pygame.draw.polygon(surface, color, points)
    
    def draw_play_icon(self, surface: pygame.Surface, pos: Tuple[int, int], 
                      size: int, color: Tuple[int, int, int]):
        """Draw a play triangle icon"""
        x, y = pos
        points = [
            (x - size // 3, y - size // 2),
            (x - size // 3, y + size // 2),
            (x + size // 2, y)
        ]
        pygame.draw.polygon(surface, color, points)
    
    def draw_pause_icon(self, surface: pygame.Surface, pos: Tuple[int, int], 
                       size: int, color: Tuple[int, int, int]):
        """Draw a pause icon"""
        x, y = pos
        bar_width = size // 4
        bar_height = size
        
        # Left bar
        pygame.draw.rect(surface, color, 
                        (x - bar_width - 2, y - bar_height // 2, 
                         bar_width, bar_height))
        # Right bar
        pygame.draw.rect(surface, color, 
                        (x + 2, y - bar_height // 2, 
                         bar_width, bar_height))
    
    def draw_settings_icon(self, surface: pygame.Surface, pos: Tuple[int, int], 
                          size: int, color: Tuple[int, int, int]):
        """Draw a settings gear icon"""
        x, y = pos
        
        # Draw gear teeth
        for i in range(8):
            angle = math.pi * i / 4
            inner_x = x + int(size * 0.3 * math.cos(angle))
            inner_y = y + int(size * 0.3 * math.sin(angle))
            outer_x = x + int(size * 0.5 * math.cos(angle))
            outer_y = y + int(size * 0.5 * math.sin(angle))
            
            pygame.draw.line(surface, color, (inner_x, inner_y), (outer_x, outer_y), 3)
        
        # Draw center circle
        pygame.draw.circle(surface, color, (x, y), size // 6)
    
    def draw_home_icon(self, surface: pygame.Surface, pos: Tuple[int, int], 
                      size: int, color: Tuple[int, int, int]):
        """Draw a home icon"""
        x, y = pos
        
        # House shape
        points = [
            (x, y - size // 2),  # Top
            (x - size // 2, y),  # Left
            (x - size // 3, y),  # Left wall
            (x - size // 3, y + size // 2),  # Bottom left
            (x + size // 3, y + size // 2),  # Bottom right
            (x + size // 3, y),  # Right wall
            (x + size // 2, y)   # Right
        ]
        pygame.draw.polygon(surface, color, points)
        
        # Door
        door_rect = pygame.Rect(x - size // 8, y + size // 6, size // 4, size // 3)
        pygame.draw.rect(surface, color, door_rect)

class StylishFont:
    """Manages consistent, stylish fonts for the game"""
    
    def __init__(self):
        self.fonts = {}
        self.default_font_name = "Arial"  # Fallback
        self.preferred_fonts = [
            "Helvetica Neue",
            "Arial",
            "Segoe UI",
            "San Francisco",
            "Roboto"
        ]
        
        # Try to find the best available font
        self.font_name = self._find_best_font()
        
        # Initialize font sizes
        self.load_fonts()
    
    def _find_best_font(self) -> str:
        """Find the best available font from preferences"""
        available_fonts = pygame.font.get_fonts()
        
        for preferred in self.preferred_fonts:
            # Check exact match first
            if preferred.lower().replace(" ", "") in available_fonts:
                return preferred
            
            # Check partial matches
            for available in available_fonts:
                if preferred.lower().replace(" ", "") in available:
                    return available
        
        return self.default_font_name
    
    def load_fonts(self):
        """Load all font sizes"""
        sizes = {
            'title': 72,
            'subtitle': 48,
            'heading': 36,
            'body': 24,
            'small': 18,
            'tiny': 14
        }
        
        for size_name, size in sizes.items():
            try:
                # Ensure pygame font is initialized
                if not pygame.font.get_init():
                    pygame.font.init()
                self.fonts[size_name] = pygame.font.SysFont(self.font_name, size)
            except:
                # Fallback to default font
                try:
                    if not pygame.font.get_init():
                        pygame.font.init()
                    self.fonts[size_name] = pygame.font.Font(None, size)
                except:
                    # Final fallback - create a dummy font for testing
                    self.fonts[size_name] = None
    
    def get_font(self, size_name: str) -> pygame.font.Font:
        """Get font by size name"""
        return self.fonts.get(size_name, self.fonts.get('body'))
    
    def render_text(self, text: str, size_name: str, color: Tuple[int, int, int], 
                   antialias: bool = True) -> pygame.Surface:
        """Render text with the stylish font"""
        font = self.get_font(size_name)
        if font is None:
            # Return a dummy surface for testing
            return pygame.Surface((100, 20))
        return font.render(text, antialias, color)
    
    def get_text_size(self, text: str, size_name: str) -> Tuple[int, int]:
        """Get the size of text when rendered"""
        font = self.get_font(size_name)
        if font is None:
            # Return dummy size for testing
            return (100, 20)
        return font.size(text)

class MessageDisplay:
    """Displays friendly messages with animations"""
    
    def __init__(self, font_system: StylishFont):
        self.font_system = font_system
        self.current_message = ""
        self.message_type = MessageType.INFO
        self.message_timer = 0.0
        self.message_duration = 3.0
        self.fade_alpha = 255
        self.bounce_offset = 0.0
        
    def show_message(self, message: str, message_type: MessageType = MessageType.INFO, 
                    duration: float = 3.0):
        """Display a new message"""
        self.current_message = message
        self.message_type = message_type
        self.message_timer = 0.0
        self.message_duration = duration
        self.fade_alpha = 255
        self.bounce_offset = 0.0
    
    def update(self, dt: float):
        """Update message display"""
        if self.current_message:
            self.message_timer += dt
            
            # Bounce animation
            self.bounce_offset = math.sin(self.message_timer * 4) * 3
            
            # Fade out near the end
            if self.message_timer > self.message_duration - 1.0:
                fade_progress = (self.message_timer - (self.message_duration - 1.0)) / 1.0
                self.fade_alpha = int(255 * (1.0 - fade_progress))
            
            # Clear message when time is up
            if self.message_timer >= self.message_duration:
                self.current_message = ""
    
    def draw(self, surface: pygame.Surface, pos: Tuple[int, int], palette: ColorPalette):
        """Draw the current message"""
        if not self.current_message:
            return
        
        # Choose color based on message type
        if self.message_type == MessageType.SUCCESS:
            color = palette.success
        elif self.message_type == MessageType.WARNING:
            color = palette.warning
        elif self.message_type == MessageType.ERROR:
            color = palette.error
        else:
            color = palette.text
        
        # Apply fade alpha
        if self.fade_alpha < 255:
            color = (*color, self.fade_alpha)
        
        # Render text
        text_surface = self.font_system.render_text(
            self.current_message, 'body', color
        )
        
        # Position with bounce
        x, y = pos
        y += int(self.bounce_offset)
        
        # Center the text
        text_rect = text_surface.get_rect(center=(x, y))
        
        # Draw with shadow for better visibility
        shadow_surface = self.font_system.render_text(
            self.current_message, 'body', (0, 0, 0)
        )
        shadow_rect = shadow_surface.get_rect(center=(x + 2, y + 2))
        
        surface.blit(shadow_surface, shadow_rect)
        surface.blit(text_surface, text_rect)