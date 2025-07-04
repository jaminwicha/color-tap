import pygame
import math
import time
from typing import Tuple, List, Optional
from enum import Enum

class BubbleAnimation:
    """Creates elastic, bubbly animation effects for UI elements"""
    
    def __init__(self, duration: float = 0.8):
        self.duration = duration
        self.start_time = 0.0
        self.is_active = False
        
    def start(self):
        """Start the bubble animation"""
        self.start_time = time.time()
        self.is_active = True
        
    def get_scale(self) -> float:
        """Get current scale factor (elastic bounce)"""
        if not self.is_active:
            return 1.0
            
        elapsed = time.time() - self.start_time
        if elapsed >= self.duration:
            self.is_active = False
            return 1.0
            
        # Elastic bounce animation using sine wave
        progress = elapsed / self.duration
        
        # Elastic ease-out formula
        if progress == 0 or progress == 1:
            return 1.0
        
        # Create elastic bounce effect
        amplitude = 1.0
        period = 0.3
        scale = amplitude * math.pow(2, -10 * progress) * math.sin((progress - period/4) * (2 * math.pi) / period) + 1
        
        # Scale up initially then settle to 1.0
        return max(0.5, scale * 1.2)

class RoundedRect:
    """Utility class for drawing rounded rectangles with borders"""
    
    @staticmethod
    def draw(surface: pygame.Surface, color: Tuple[int, int, int], rect: pygame.Rect, 
             border_radius: int = 15, border_color: Optional[Tuple[int, int, int]] = None, 
             border_width: int = 3):
        """Draw a rounded rectangle with optional border"""
        
        # Create a surface for the rounded rectangle
        rounded_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        
        # Draw the main rounded rectangle
        pygame.draw.rect(rounded_surf, color, (0, 0, rect.width, rect.height), border_radius=border_radius)
        
        # Draw border if specified
        if border_color and border_width > 0:
            pygame.draw.rect(rounded_surf, border_color, (0, 0, rect.width, rect.height), 
                           border_width, border_radius=border_radius)
        
        # Blit to main surface
        surface.blit(rounded_surf, rect.topleft)

class FontRenderer:
    """Enhanced font renderer that avoids unicode artifacts and creates smooth text"""
    
    def __init__(self):
        self.font_cache = {}
        self.rendered_text_cache = {}
        
    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        """Get a font with caching, using safe system fonts"""
        font_key = (size, bold)
        
        if font_key not in self.font_cache:
            # Try to use common, safe fonts that avoid unicode issues
            font_names = [
                'Arial',
                'Helvetica', 
                'DejaVu Sans',
                'Liberation Sans',
                'FreeSans',
                None  # Default fallback
            ]
            
            font = None
            for font_name in font_names:
                try:
                    if font_name:
                        font = pygame.font.SysFont(font_name, size, bold=bold)
                    else:
                        font = pygame.font.Font(None, size)
                    break
                except:
                    continue
            
            if font is None:
                font = pygame.font.Font(None, size)
                
            self.font_cache[font_key] = font
            
        return self.font_cache[font_key]
    
    def render_text(self, text: str, size: int, color: Tuple[int, int, int], 
                   bold: bool = False, antialias: bool = True) -> pygame.Surface:
        """Render text with caching and safe character handling"""
        
        # Clean text to avoid unicode artifacts
        safe_text = self._clean_text(text)
        
        cache_key = (safe_text, size, color, bold, antialias)
        
        if cache_key not in self.rendered_text_cache:
            font = self.get_font(size, bold)
            rendered = font.render(safe_text, antialias, color)
            self.rendered_text_cache[cache_key] = rendered
            
        return self.rendered_text_cache[cache_key]
    
    def _clean_text(self, text: str) -> str:
        """Clean text to remove problematic unicode characters"""
        # Replace common problematic characters with safe alternatives
        replacements = {
            '🌟': '*',
            '🎯': '*', 
            '🪆': 'o',
            '✨': '*',
            '🎉': '!',
            '🔥': '*',
            '💫': '*',
            '⭐': '*',
            '🌈': '~'
        }
        
        cleaned = text
        for unicode_char, replacement in replacements.items():
            cleaned = cleaned.replace(unicode_char, replacement)
            
        # Remove any remaining non-ASCII characters
        cleaned = ''.join(char for char in cleaned if ord(char) < 128)
        
        return cleaned

class BubblyPopup:
    """A popup with rounded corners, elastic animation, and clean text rendering"""
    
    def __init__(self, width: int, height: int, title: str, message: str, 
                 bg_color: Tuple[int, int, int] = (255, 255, 255),
                 border_color: Tuple[int, int, int] = (50, 50, 50),
                 text_color: Tuple[int, int, int] = (20, 20, 20)):
        
        self.width = width
        self.height = height
        self.title = title
        self.message = message
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        
        self.animation = BubbleAnimation()
        self.font_renderer = FontRenderer()
        
        self.is_visible = False
        self.x = 0
        self.y = 0
        
    def show(self, center_x: int, center_y: int):
        """Show the popup at the specified center position"""
        self.x = center_x - self.width // 2
        self.y = center_y - self.height // 2
        self.is_visible = True
        self.animation.start()
        
    def hide(self):
        """Hide the popup"""
        self.is_visible = False
        
    def draw(self, surface: pygame.Surface):
        """Draw the bubbly popup with animation"""
        if not self.is_visible:
            return
            
        # Get current animation scale
        scale = self.animation.get_scale()
        
        # Calculate scaled dimensions
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)
        
        # Calculate position to keep centered
        scaled_x = self.x + (self.width - scaled_width) // 2
        scaled_y = self.y + (self.height - scaled_height) // 2
        
        if scaled_width <= 0 or scaled_height <= 0:
            return
            
        # Create rect for the popup
        popup_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Draw rounded background with border
        RoundedRect.draw(surface, self.bg_color, popup_rect, 
                        border_radius=20, border_color=self.border_color, border_width=4)
        
        # Add subtle shadow effect
        shadow_rect = pygame.Rect(scaled_x + 5, scaled_y + 5, scaled_width, scaled_height)
        shadow_color = (0, 0, 0, 50)  # Semi-transparent black
        shadow_surf = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, shadow_color, (0, 0, scaled_width, scaled_height), border_radius=20)
        surface.blit(shadow_surf, (shadow_rect.x, shadow_rect.y))
        
        # Redraw the main popup over the shadow
        RoundedRect.draw(surface, self.bg_color, popup_rect, 
                        border_radius=20, border_color=self.border_color, border_width=4)
        
        # Draw title text
        if self.title:
            title_surface = self.font_renderer.render_text(self.title, 32, self.text_color, bold=True)
            title_rect = title_surface.get_rect(center=(popup_rect.centerx, popup_rect.y + 40))
            surface.blit(title_surface, title_rect)
        
        # Draw message text (handle multi-line)
        if self.message:
            lines = self._wrap_text(self.message, scaled_width - 60, 24)
            line_height = 30
            start_y = popup_rect.y + 80 if self.title else popup_rect.y + 40
            
            for i, line in enumerate(lines):
                line_surface = self.font_renderer.render_text(line, 24, self.text_color)
                line_rect = line_surface.get_rect(center=(popup_rect.centerx, start_y + i * line_height))
                surface.blit(line_surface, line_rect)
    
    def _wrap_text(self, text: str, max_width: int, font_size: int) -> List[str]:
        """Wrap text to fit within specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        font = self.font_renderer.get_font(font_size)
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)  # Single word too long, add anyway
        
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines

class BubblyMessage:
    """Floating message with bubble animation"""
    
    def __init__(self, text: str, x: int, y: int, duration: float = 3.0,
                 bg_color: Tuple[int, int, int] = (255, 255, 255, 200),
                 text_color: Tuple[int, int, int] = (50, 50, 50)):
        
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration
        self.bg_color = bg_color
        self.text_color = text_color
        
        self.start_time = time.time()
        self.animation = BubbleAnimation(0.5)  # Shorter animation for messages
        self.font_renderer = FontRenderer()
        
        self.animation.start()
        
    def is_alive(self) -> bool:
        """Check if message should still be displayed"""
        return time.time() - self.start_time < self.duration
        
    def draw(self, surface: pygame.Surface):
        """Draw the floating message"""
        if not self.is_alive():
            return
            
        elapsed = time.time() - self.start_time
        progress = elapsed / self.duration
        
        # Fade out near the end
        alpha = 255
        if progress > 0.8:
            fade_progress = (progress - 0.8) / 0.2
            alpha = int(255 * (1.0 - fade_progress))
        
        # Get animation scale
        scale = self.animation.get_scale()
        
        # Render text
        text_surface = self.font_renderer.render_text(self.text, 20, self.text_color)
        text_width, text_height = text_surface.get_size()
        
        # Create background
        padding = 15
        bg_width = text_width + padding * 2
        bg_height = text_height + padding * 2
        
        scaled_width = int(bg_width * scale)
        scaled_height = int(bg_height * scale)
        
        # Position
        bg_x = self.x - scaled_width // 2
        bg_y = self.y - scaled_height // 2
        
        # Create background surface with alpha
        bg_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        bg_color_with_alpha = (*self.bg_color[:3], min(alpha, self.bg_color[3] if len(self.bg_color) > 3 else 255))
        
        pygame.draw.rect(bg_surface, bg_color_with_alpha, (0, 0, scaled_width, scaled_height), border_radius=10)
        
        surface.blit(bg_surface, (bg_x, bg_y))
        
        # Draw text
        text_x = self.x - text_width // 2
        text_y = self.y - text_height // 2
        
        # Apply alpha to text
        text_with_alpha = text_surface.copy()
        text_with_alpha.set_alpha(alpha)
        surface.blit(text_with_alpha, (text_x, text_y))

class BubblyUIManager:
    """Manages all bubbly UI elements"""
    
    def __init__(self):
        self.popups: List[BubblyPopup] = []
        self.messages: List[BubblyMessage] = []
        
    def show_popup(self, title: str, message: str, center_x: int, center_y: int,
                   width: int = 400, height: int = 200) -> BubblyPopup:
        """Show a bubbly popup"""
        popup = BubblyPopup(width, height, title, message)
        popup.show(center_x, center_y)
        self.popups.append(popup)
        return popup
        
    def show_message(self, text: str, x: int, y: int, duration: float = 3.0) -> BubblyMessage:
        """Show a floating bubbly message"""
        message = BubblyMessage(text, x, y, duration)
        self.messages.append(message)
        return message
        
    def update(self):
        """Update and clean up UI elements"""
        # Remove dead messages
        self.messages = [msg for msg in self.messages if msg.is_alive()]
        
        # Remove hidden popups
        self.popups = [popup for popup in self.popups if popup.is_visible]
        
    def draw(self, surface: pygame.Surface):
        """Draw all UI elements"""
        # Draw messages first (behind popups)
        for message in self.messages:
            message.draw(surface)
            
        # Draw popups on top
        for popup in self.popups:
            popup.draw(surface)
            
    def hide_all_popups(self):
        """Hide all visible popups"""
        for popup in self.popups:
            popup.hide()