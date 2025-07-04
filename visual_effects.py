import pygame
import math
import random
from typing import List, Tuple
from config import WINDOW_WIDTH, WINDOW_HEIGHT, Color

class PulseEffect:
    """Creates a growing pulse effect for background color changes"""
    
    def __init__(self, center_x: int, center_y: int, target_color: Tuple[int, int, int], duration: float = 1.0):
        self.center_x = center_x
        self.center_y = center_y
        self.target_color = target_color
        self.duration = duration
        self.current_time = 0.0
        self.max_radius = math.sqrt(WINDOW_WIDTH**2 + WINDOW_HEIGHT**2)
        self.active = True
        
    def update(self, dt: float) -> bool:
        """Update the pulse effect. Returns True if still active"""
        if not self.active:
            return False
            
        self.current_time += dt
        if self.current_time >= self.duration:
            self.active = False
            return False
            
        return True
    
    def get_progress(self) -> float:
        """Get the progress of the pulse (0.0 to 1.0)"""
        return min(self.current_time / self.duration, 1.0)
    
    def get_radius(self) -> float:
        """Get the current radius of the pulse"""
        progress = self.get_progress()
        # Use easing function for smooth animation
        eased_progress = self._ease_out_cubic(progress)
        return eased_progress * self.max_radius
    
    def get_alpha(self) -> int:
        """Get the current alpha value for the pulse"""
        progress = self.get_progress()
        # Fade out as it expands
        return int(255 * (1.0 - progress))
    
    def _ease_out_cubic(self, t: float) -> float:
        """Cubic easing out function for smooth animation"""
        return 1 - pow(1 - t, 3)
    
    def draw(self, screen: pygame.Surface, background_color: Tuple[int, int, int]):
        """Draw the pulse effect"""
        if not self.active:
            return
            
        radius = self.get_radius()
        alpha = self.get_alpha()
        
        if radius > 0 and alpha > 0:
            # Create a surface for the pulse with alpha
            pulse_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            
            # Draw concentric circles for a more sophisticated effect
            for i in range(3):
                inner_radius = max(0, radius - 20 * (i + 1))
                circle_alpha = alpha // (i + 1)
                
                if inner_radius > 0:
                    color_with_alpha = (*self.target_color, circle_alpha)
                    pygame.draw.circle(pulse_surface, color_with_alpha, 
                                     (self.center_x, self.center_y), int(inner_radius))
            
            screen.blit(pulse_surface, (0, 0))

class ParticleEffect:
    """Individual particle for various effects"""
    
    def __init__(self, x: float, y: float, vel_x: float, vel_y: float, 
                 color: Tuple[int, int, int], life: float, size: float):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = 50.0
        
    def update(self, dt: float) -> bool:
        """Update particle. Returns True if still alive"""
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.vel_y += self.gravity * dt
        self.life -= dt
        
        return self.life > 0
    
    def draw(self, screen: pygame.Surface):
        """Draw the particle"""
        if self.life <= 0:
            return
            
        # Calculate alpha based on remaining life
        alpha = int(255 * (self.life / self.max_life))
        color_with_alpha = (*self.color, alpha)
        
        # Create a small surface for the particle
        particle_size = int(self.size * (self.life / self.max_life))
        if particle_size > 0:
            particle_surface = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color_with_alpha, 
                             (particle_size, particle_size), particle_size)
            screen.blit(particle_surface, (int(self.x - particle_size), int(self.y - particle_size)))

class ParticleSystem:
    """Manages multiple particles for various effects"""
    
    def __init__(self):
        self.particles: List[ParticleEffect] = []
    
    def add_merge_burst(self, x: float, y: float, color: Tuple[int, int, int]):
        """Add a burst of particles for shape merging"""
        num_particles = 15
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 200)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed - 100  # Bias upward
            
            particle = ParticleEffect(
                x, y, vel_x, vel_y, color, 
                random.uniform(0.5, 1.0), 
                random.uniform(3, 6)
            )
            self.particles.append(particle)
    
    def add_bounce_sparks(self, x: float, y: float, color: Tuple[int, int, int]):
        """Add sparks for shape bouncing"""
        num_particles = 8
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 120)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = ParticleEffect(
                x, y, vel_x, vel_y, color, 
                random.uniform(0.3, 0.6), 
                random.uniform(2, 4)
            )
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, screen: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)

class AnimationManager:
    """Manages all visual effects and animations"""
    
    def __init__(self):
        self.pulse_effects: List[PulseEffect] = []
        self.particle_system = ParticleSystem()
        self.shape_animations = {}
        
    def add_background_pulse(self, x: int, y: int, target_color: Tuple[int, int, int]):
        """Add a pulse effect for background color changes"""
        pulse = PulseEffect(x, y, target_color, 1.2)
        self.pulse_effects.append(pulse)
    
    def add_merge_effect(self, x: float, y: float, color: Tuple[int, int, int]):
        """Add visual effects for shape merging"""
        self.particle_system.add_merge_burst(x, y, color)
    
    def add_bounce_effect(self, x: float, y: float, color: Tuple[int, int, int]):
        """Add visual effects for shape bouncing"""
        self.particle_system.add_bounce_sparks(x, y, color)
    
    def add_shape_animation(self, shape_id: str, animation_type: str, duration: float):
        """Add animation for a specific shape"""
        self.shape_animations[shape_id] = {
            'type': animation_type,
            'duration': duration,
            'current_time': 0.0
        }
    
    def update(self, dt: float):
        """Update all animations"""
        # Update pulse effects
        self.pulse_effects = [p for p in self.pulse_effects if p.update(dt)]
        
        # Update particle system
        self.particle_system.update(dt)
        
        # Update shape animations
        for shape_id, anim in list(self.shape_animations.items()):
            anim['current_time'] += dt
            if anim['current_time'] >= anim['duration']:
                del self.shape_animations[shape_id]
    
    def draw_background_effects(self, screen: pygame.Surface, background_color: Tuple[int, int, int]):
        """Draw background effects like pulses"""
        for pulse in self.pulse_effects:
            pulse.draw(screen, background_color)
    
    def draw_particle_effects(self, screen: pygame.Surface):
        """Draw particle effects"""
        self.particle_system.draw(screen)
    
    def get_shape_animation_scale(self, shape_id: str) -> float:
        """Get the current scale for a shape animation"""
        if shape_id not in self.shape_animations:
            return 1.0
            
        anim = self.shape_animations[shape_id]
        if anim['type'] == 'bounce':
            progress = anim['current_time'] / anim['duration']
            # Bounce scale effect
            return 1.0 + 0.3 * math.sin(progress * math.pi)
        elif anim['type'] == 'merge':
            progress = anim['current_time'] / anim['duration']
            # Shrink and fade effect
            return 1.0 - progress * 0.5
            
        return 1.0

class HighResolutionRenderer:
    """Handles high-resolution rendering with anti-aliasing"""
    
    def __init__(self, scale_factor: float = 2.0):
        self.scale_factor = scale_factor
        self.high_res_surface = pygame.Surface(
            (int(WINDOW_WIDTH * scale_factor), int(WINDOW_HEIGHT * scale_factor)), 
            pygame.SRCALPHA
        )
    
    def draw_smooth_circle(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                          center: Tuple[int, int], radius: int, width: int = 0):
        """Draw a smooth anti-aliased circle"""
        # Use gfxdraw for better anti-aliasing
        try:
            pygame.gfxdraw.aacircle(surface, center[0], center[1], radius, color)
            if width == 0:
                pygame.gfxdraw.filled_circle(surface, center[0], center[1], radius, color)
        except:
            # Fallback to regular circle if gfxdraw not available
            pygame.draw.circle(surface, color, center, radius, width)
    
    def draw_smooth_polygon(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                           points: List[Tuple[int, int]], width: int = 0):
        """Draw a smooth anti-aliased polygon"""
        try:
            pygame.gfxdraw.aapolygon(surface, points, color)
            if width == 0:
                pygame.gfxdraw.filled_polygon(surface, points, color)
        except:
            # Fallback to regular polygon if gfxdraw not available
            pygame.draw.polygon(surface, color, points, width)
    
    def begin_high_res_render(self):
        """Begin high-resolution rendering"""
        self.high_res_surface.fill((0, 0, 0, 0))
        return self.high_res_surface
    
    def end_high_res_render(self, target_surface: pygame.Surface):
        """End high-resolution rendering and scale down"""
        # Scale down the high-resolution surface
        scaled_surface = pygame.transform.smoothscale(
            self.high_res_surface, 
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        target_surface.blit(scaled_surface, (0, 0))