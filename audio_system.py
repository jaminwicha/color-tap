import pygame
import numpy as np
import math
import random
from typing import Dict, List, Tuple
from threading import Thread
import time

class FractalMusicGenerator:
    """Generates ambient electronic music using fractal algorithms"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.base_frequency = 220.0  # A3
        self.golden_ratio = (1 + math.sqrt(5)) / 2
        self.fibonacci_sequence = self._generate_fibonacci(20)
        
    def _generate_fibonacci(self, n: int) -> List[int]:
        """Generate Fibonacci sequence"""
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
    
    def _mandelbrot_frequency(self, c: complex, max_iter: int = 50) -> float:
        """Generate frequency based on Mandelbrot set"""
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n / max_iter
            z = z*z + c
        return 1.0
    
    def generate_fractal_tone(self, duration: float, base_freq: float, 
                            pattern: str = "fibonacci") -> np.ndarray:
        """Generate a fractal-based tone"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        if pattern == "fibonacci":
            # Use Fibonacci ratios for harmonics
            wave = np.zeros(samples)
            for i, fib in enumerate(self.fibonacci_sequence[:6]):
                harmonic_freq = base_freq * fib / self.fibonacci_sequence[0]
                amplitude = 1.0 / (i + 1)  # Decreasing amplitude
                wave += amplitude * np.sin(2 * np.pi * harmonic_freq * t)
                
        elif pattern == "golden_ratio":
            # Use golden ratio for frequency relationships
            wave = np.zeros(samples)
            for i in range(5):
                harmonic_freq = base_freq * (self.golden_ratio ** i)
                amplitude = 1.0 / (i + 1)
                wave += amplitude * np.sin(2 * np.pi * harmonic_freq * t)
                
        elif pattern == "mandelbrot":
            # Use Mandelbrot set for complex harmonics
            wave = np.zeros(samples)
            for i in range(8):
                c = complex(-0.7 + i * 0.1, 0.3)
                freq_mult = self._mandelbrot_frequency(c)
                harmonic_freq = base_freq * (1 + freq_mult)
                amplitude = 0.3 / (i + 1)
                wave += amplitude * np.sin(2 * np.pi * harmonic_freq * t)
        
        # Apply envelope for smooth attack and decay
        envelope = np.ones(samples)
        attack_samples = int(0.1 * samples)
        decay_samples = int(0.2 * samples)
        
        # Attack
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        # Decay
        envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
        
        return wave * envelope
    
    def create_ambient_sequence(self, total_duration: float) -> np.ndarray:
        """Create a complete ambient music sequence"""
        # Generate multiple overlapping tones
        full_samples = int(total_duration * self.sample_rate)
        ambient_track = np.zeros(full_samples)
        
        # Base frequencies based on pentatonic scale
        base_frequencies = [220.0, 247.0, 277.0, 330.0, 370.0]  # A, B, C#, E, F#
        patterns = ["fibonacci", "golden_ratio", "mandelbrot"]
        
        num_layers = 6
        for layer in range(num_layers):
            # Randomize timing and frequency for each layer
            start_time = random.uniform(0, total_duration * 0.3)
            tone_duration = random.uniform(8, 15)
            base_freq = random.choice(base_frequencies) / (2 ** random.randint(0, 2))
            pattern = random.choice(patterns)
            
            # Generate the tone
            tone = self.generate_fractal_tone(tone_duration, base_freq, pattern)
            
            # Position in the full track
            start_sample = int(start_time * self.sample_rate)
            end_sample = min(start_sample + len(tone), full_samples)
            tone_samples = end_sample - start_sample
            
            # Mix the tone into the ambient track
            ambient_track[start_sample:end_sample] += tone[:tone_samples] * 0.3
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(ambient_track))
        if max_val > 0:
            ambient_track = ambient_track / max_val * 0.7
        
        return ambient_track

class SoundEffectGenerator:
    """Generates ethereal sound effects for game interactions"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
    def generate_merge_sound(self, color: Tuple[int, int, int]) -> np.ndarray:
        """Generate a pleasant merge sound based on color"""
        # Map color to frequency
        r, g, b = color
        base_freq = 300 + (r + g + b) / 3 * 2  # 300-800 Hz range
        
        duration = 0.8
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Create a chord with multiple harmonics
        wave = np.zeros(samples)
        harmonics = [1, 1.5, 2, 3]  # Perfect fourth, octave, perfect fifth
        
        for i, harmonic in enumerate(harmonics):
            freq = base_freq * harmonic
            amplitude = 0.4 / (i + 1)
            wave += amplitude * np.sin(2 * np.pi * freq * t)
        
        # Add some ethereal modulation
        modulation = 0.1 * np.sin(2 * np.pi * 5 * t)  # 5 Hz modulation
        wave *= (1 + modulation)
        
        # Apply envelope
        envelope = np.exp(-t * 2)  # Exponential decay
        wave *= envelope
        
        return wave
    
    def generate_bounce_sound(self, color: Tuple[int, int, int]) -> np.ndarray:
        """Generate a sharp bounce sound"""
        r, g, b = color
        base_freq = 400 + (r + g + b) / 3 * 3  # Higher frequency for bounce
        
        duration = 0.2
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Sharp attack, quick decay
        wave = 0.5 * np.sin(2 * np.pi * base_freq * t)
        
        # Add some noise for texture
        noise = np.random.normal(0, 0.1, samples)
        wave += noise
        
        # Sharp envelope
        envelope = np.exp(-t * 15)
        wave *= envelope
        
        return wave
    
    def generate_success_sound(self) -> np.ndarray:
        """Generate a success/completion sound"""
        duration = 1.5
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Ascending arpeggio
        frequencies = [523, 659, 784, 1047]  # C5, E5, G5, C6
        wave = np.zeros(samples)
        
        for i, freq in enumerate(frequencies):
            start_time = i * 0.2
            note_duration = 0.5
            start_sample = int(start_time * self.sample_rate)
            end_sample = min(start_sample + int(note_duration * self.sample_rate), samples)
            
            note_samples = end_sample - start_sample
            note_t = np.linspace(0, note_duration, note_samples)
            
            # Generate note
            note = 0.3 * np.sin(2 * np.pi * freq * note_t)
            envelope = np.exp(-note_t * 2)
            note *= envelope
            
            wave[start_sample:end_sample] += note
        
        return wave
    
    def generate_ui_sound(self, sound_type: str) -> np.ndarray:
        """Generate UI interaction sounds"""
        if sound_type == "select":
            # Soft selection sound
            duration = 0.1
            samples = int(duration * self.sample_rate)
            t = np.linspace(0, duration, samples)
            wave = 0.2 * np.sin(2 * np.pi * 800 * t)
            envelope = np.exp(-t * 10)
            return wave * envelope
            
        elif sound_type == "confirm":
            # Confirmation sound
            duration = 0.3
            samples = int(duration * self.sample_rate)
            t = np.linspace(0, duration, samples)
            wave = 0.3 * np.sin(2 * np.pi * 600 * t)
            envelope = np.exp(-t * 5)
            return wave * envelope
            
        elif sound_type == "error":
            # Error sound
            duration = 0.2
            samples = int(duration * self.sample_rate)
            t = np.linspace(0, duration, samples)
            wave = 0.2 * np.sin(2 * np.pi * 200 * t)
            envelope = np.exp(-t * 8)
            return wave * envelope
        
        return np.zeros(1024)

class AudioManager:
    """Manages all audio in the game"""
    
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        self.sample_rate = 44100
        self.music_generator = FractalMusicGenerator(self.sample_rate)
        self.sfx_generator = SoundEffectGenerator(self.sample_rate)
        
        self.ambient_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
        
        self.ambient_volume = 0.3
        self.sfx_volume = 0.7
        
        # Generate initial ambient music
        self.current_ambient = None
        self.generate_new_ambient_music()
        
    def numpy_to_pygame_sound(self, wave: np.ndarray) -> pygame.mixer.Sound:
        """Convert numpy array to pygame Sound object"""
        # Convert to 16-bit integers
        wave_int = (wave * 32767).astype(np.int16)
        
        # Create stereo sound
        if len(wave_int.shape) == 1:
            stereo_wave = np.column_stack((wave_int, wave_int))
        else:
            stereo_wave = wave_int
            
        return pygame.mixer.Sound(stereo_wave)
    
    def generate_new_ambient_music(self):
        """Generate new ambient music"""
        def generate_async():
            ambient_sequence = self.music_generator.create_ambient_sequence(30.0)  # 30 seconds
            self.current_ambient = self.numpy_to_pygame_sound(ambient_sequence)
        
        # Generate in background thread to avoid blocking
        Thread(target=generate_async, daemon=True).start()
    
    def play_ambient_music(self):
        """Start playing ambient music"""
        if self.current_ambient and not self.ambient_channel.get_busy():
            self.ambient_channel.play(self.current_ambient, loops=-1)
            self.ambient_channel.set_volume(self.ambient_volume)
    
    def play_merge_sound(self, color: Tuple[int, int, int]):
        """Play merge sound effect"""
        wave = self.sfx_generator.generate_merge_sound(color)
        sound = self.numpy_to_pygame_sound(wave)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume)
    
    def play_bounce_sound(self, color: Tuple[int, int, int]):
        """Play bounce sound effect"""
        wave = self.sfx_generator.generate_bounce_sound(color)
        sound = self.numpy_to_pygame_sound(wave)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume)
    
    def play_success_sound(self):
        """Play success sound"""
        wave = self.sfx_generator.generate_success_sound()
        sound = self.numpy_to_pygame_sound(wave)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume)
    
    def play_ui_sound(self, sound_type: str):
        """Play UI sound"""
        wave = self.sfx_generator.generate_ui_sound(sound_type)
        sound = self.numpy_to_pygame_sound(wave)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume * 0.5)
    
    def set_ambient_volume(self, volume: float):
        """Set ambient music volume"""
        self.ambient_volume = max(0.0, min(1.0, volume))
        if self.ambient_channel.get_busy():
            self.ambient_channel.set_volume(self.ambient_volume)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def stop_all(self):
        """Stop all audio"""
        pygame.mixer.stop()
    
    def update(self):
        """Update audio system"""
        # Check if we need to generate new ambient music
        if not self.ambient_channel.get_busy() and self.current_ambient:
            self.play_ambient_music()
        
        # Occasionally generate new ambient music for variety
        if random.random() < 0.001:  # Low probability per frame
            self.generate_new_ambient_music()