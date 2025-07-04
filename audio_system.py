import pygame
import numpy as np
import math
import random
from typing import Dict, List, Tuple
from threading import Thread
import time

class FractalMusicGenerator:
    """Generates ambient electronic music with hip-hop rhythms using fractal algorithms"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.base_frequency = 220.0  # A3
        self.golden_ratio = (1 + math.sqrt(5)) / 2
        self.fibonacci_sequence = self._generate_fibonacci(20)
        
        # Heartbeat rhythm parameters
        self.bpm = 65  # Calm resting heartbeat tempo
        self.beat_duration = 60.0 / self.bpm  # Duration of one beat in seconds
        self.bar_duration = self.beat_duration * 4  # 4/4 time signature
        
        # Fractal rhythm patterns (using Fibonacci ratios)
        self.kick_pattern = [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]  # 16th note pattern
        self.snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0]  # Snare on 2 and 4
        self.hihat_pattern = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1]  # Hi-hat pattern
        
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
    
    def generate_kick_drum(self, duration: float = 0.1) -> np.ndarray:
        """Generate a deep kick drum sound"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Start with low frequency that drops quickly
        frequency_sweep = 60 * np.exp(-t * 50)  # Frequency drops from 60Hz
        
        # Generate the tone with frequency sweep
        wave = 0.8 * np.sin(2 * np.pi * frequency_sweep * t)
        
        # Add some noise for texture
        noise = 0.2 * np.random.normal(0, 1, samples)
        wave += noise
        
        # Sharp attack, quick decay envelope
        envelope = np.exp(-t * 25)
        
        return wave * envelope
    
    def generate_snare_drum(self, duration: float = 0.15) -> np.ndarray:
        """Generate a snappy snare drum sound"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Mix of tone and noise for snare character
        tone = 0.3 * np.sin(2 * np.pi * 200 * t)  # 200Hz tone component
        noise = 0.7 * np.random.normal(0, 1, samples)  # White noise for snare crack
        
        wave = tone + noise
        
        # Quick attack, medium decay
        envelope = np.exp(-t * 15)
        
        return wave * envelope
    
    def generate_hihat(self, duration: float = 0.05) -> np.ndarray:
        """Generate a crispy hi-hat sound"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # High-frequency noise for hi-hat
        wave = 0.4 * np.random.normal(0, 1, samples)
        
        # Apply high-pass filtering effect (emphasize high frequencies)
        for i in range(1, len(wave)):
            wave[i] = wave[i] - 0.95 * wave[i-1]
        
        # Very quick decay
        envelope = np.exp(-t * 40)
        
        return wave * envelope
    
    def generate_bass_line(self, duration: float, base_freq: float = 55.0) -> np.ndarray:
        """Generate a deep bass line using fractal patterns"""
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Create bass pattern using Fibonacci sequence
        num_notes = 8
        note_duration = duration / num_notes
        bass_wave = np.zeros(samples)
        
        for i in range(num_notes):
            start_sample = int(i * note_duration * self.sample_rate)
            end_sample = int((i + 1) * note_duration * self.sample_rate)
            note_samples = end_sample - start_sample
            
            if note_samples <= 0:
                continue
            
            # Use Fibonacci ratios for note frequencies
            fib_ratio = self.fibonacci_sequence[i % len(self.fibonacci_sequence)] / self.fibonacci_sequence[0]
            note_freq = base_freq * (1 + fib_ratio * 0.1)  # Subtle frequency variations
            
            note_t = np.linspace(0, note_duration, note_samples)
            
            # Generate bass note with harmonics
            note_wave = np.zeros(note_samples)
            note_wave += 0.6 * np.sin(2 * np.pi * note_freq * note_t)  # Fundamental
            note_wave += 0.3 * np.sin(2 * np.pi * note_freq * 2 * note_t)  # Octave
            note_wave += 0.1 * np.sin(2 * np.pi * note_freq * 3 * note_t)  # Third harmonic
            
            # Bass envelope with attack and sustain
            attack_samples = int(0.01 * self.sample_rate)  # 10ms attack
            if len(note_wave) > attack_samples:
                envelope = np.ones(note_samples)
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                # Gentle decay toward end
                decay_samples = int(0.1 * self.sample_rate)
                if len(note_wave) > decay_samples:
                    envelope[-decay_samples:] = np.linspace(1, 0.7, decay_samples)
                note_wave *= envelope
            
            bass_wave[start_sample:end_sample] += note_wave
        
        return bass_wave
    
    def create_hip_hop_track(self, total_duration: float) -> np.ndarray:
        """Create a complete hip-hop inspired track with fractal elements"""
        full_samples = int(total_duration * self.sample_rate)
        track = np.zeros(full_samples)
        
        # Calculate timing
        sixteenth_note_duration = self.beat_duration / 4
        bar_samples = int(self.bar_duration * self.sample_rate)
        
        # Generate drum samples
        kick_sample = self.generate_kick_drum()
        snare_sample = self.generate_snare_drum()
        hihat_sample = self.generate_hihat()
        
        # Loop through bars
        num_bars = int(total_duration / self.bar_duration)
        
        for bar in range(num_bars):
            bar_start = bar * bar_samples
            
            # Add bass line for this bar
            bass_duration = self.bar_duration
            bass_line = self.generate_bass_line(bass_duration)
            bass_end = min(bar_start + len(bass_line), full_samples)
            track[bar_start:bass_end] += bass_line[:bass_end - bar_start] * 0.6
            
            # Add drum patterns
            for step in range(16):  # 16 sixteenth notes per bar
                step_time = bar * self.bar_duration + step * sixteenth_note_duration
                step_sample = int(step_time * self.sample_rate)
                
                if step_sample >= full_samples:
                    break
                
                # Apply fractal variations to patterns
                pattern_variation = self.fibonacci_sequence[step % len(self.fibonacci_sequence)] % 3
                
                # Kick drum
                if self.kick_pattern[step] and (pattern_variation == 0 or step % 4 == 0):
                    end_sample = min(step_sample + len(kick_sample), full_samples)
                    track[step_sample:end_sample] += kick_sample[:end_sample - step_sample] * 0.8
                
                # Snare drum
                if self.snare_pattern[step] and (pattern_variation <= 1):
                    end_sample = min(step_sample + len(snare_sample), full_samples)
                    track[step_sample:end_sample] += snare_sample[:end_sample - step_sample] * 0.7
                
                # Hi-hat
                if self.hihat_pattern[step] and pattern_variation <= 2:
                    end_sample = min(step_sample + len(hihat_sample), full_samples)
                    track[step_sample:end_sample] += hihat_sample[:end_sample - step_sample] * 0.5
        
        # Add subtle ambient tones using original fractal method
        ambient_layer = self.create_ambient_sequence(total_duration)
        track += ambient_layer * 0.3  # Mix in ambient at lower volume
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(track))
        if max_val > 0:
            track = track / max_val * 0.8
        
        return track
    
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
            selected_freq = random.choice(base_frequencies)
            base_freq = selected_freq / (2 ** random.randint(0, 2))
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
        """Generate a water-drop like bounce sound"""
        r, g, b = color
        base_freq = 200 + (r + g + b) / 3 * 2  # Lower, more water-like frequency
        
        duration = 0.4
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Water drop sound characteristics
        # Initial impact frequency
        impact_freq = base_freq * 2
        # Secondary ripple frequency
        ripple_freq = base_freq * 0.7
        
        # Create the water drop impact
        impact_wave = 0.6 * np.sin(2 * np.pi * impact_freq * t)
        impact_envelope = np.exp(-t * 25)  # Sharp initial impact
        
        # Create the ripple effect
        ripple_wave = 0.4 * np.sin(2 * np.pi * ripple_freq * t)
        ripple_envelope = np.exp(-t * 8) * np.sin(2 * np.pi * 3 * t)**2  # Oscillating ripples
        
        # Combine impact and ripple
        wave = impact_wave * impact_envelope + ripple_wave * ripple_envelope
        
        # Add subtle liquid texture (like tiny bubbles)
        liquid_noise = 0.05 * np.random.normal(0, 1, samples) * np.exp(-t * 12)
        wave += liquid_noise
        
        # Water-like modulation (slight pitch bend down)
        pitch_bend = np.exp(-t * 2)  # Frequency drops slightly over time
        wave *= pitch_bend
        
        return wave
    
    def generate_victory_sound(self) -> np.ndarray:
        """Generate an ethereal victory sound with tubular bells and water echo"""
        duration = 3.0
        samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Tubular bell frequencies (golden ratio-based for fractal harmony)
        golden_ratio = (1 + math.sqrt(5)) / 2
        base_freq = 220  # A3
        bell_frequencies = []
        for i in range(6):
            freq = base_freq * pow(golden_ratio, i * 0.5)
            bell_frequencies.append(freq)
        
        final_wave = np.zeros(samples)
        
        # Create multiple tubular bell strikes with water-like echoes
        for i, freq in enumerate(bell_frequencies):
            strike_time = i * 0.3  # Stagger the bell strikes
            strike_samples = int(strike_time * self.sample_rate)
            
            if strike_samples < samples:
                # Generate tubular bell sound
                bell_duration = duration - strike_time
                bell_samples = samples - strike_samples
                bell_t = np.linspace(0, bell_duration, bell_samples)
                
                # Complex bell harmonic structure
                bell_wave = (
                    0.6 * np.sin(2 * np.pi * freq * bell_t) +           # Fundamental
                    0.3 * np.sin(2 * np.pi * freq * 2.76 * bell_t) +    # Bell-like harmonic
                    0.2 * np.sin(2 * np.pi * freq * 5.4 * bell_t) +     # Higher harmonic
                    0.1 * np.sin(2 * np.pi * freq * 8.2 * bell_t)       # Sparkle harmonic
                )
                
                # Water-like envelope with multiple echoes
                primary_envelope = np.exp(-bell_t * 1.5)  # Main decay
                echo1 = 0.3 * np.exp(-(bell_t - 0.4) * 2.0) * (bell_t >= 0.4)  # First echo
                echo2 = 0.15 * np.exp(-(bell_t - 0.8) * 2.5) * (bell_t >= 0.8)  # Second echo
                echo3 = 0.08 * np.exp(-(bell_t - 1.2) * 3.0) * (bell_t >= 1.2)  # Third echo
                
                envelope = primary_envelope + echo1 + echo2 + echo3
                bell_wave *= envelope
                
                # Add water-like modulation (slow oscillation like underwater)
                water_modulation = 1.0 + 0.1 * np.sin(2 * np.pi * 0.5 * bell_t)  # 0.5 Hz oscillation
                bell_wave *= water_modulation
                
                # Add to final wave
                final_wave[strike_samples:] += bell_wave * (0.8 - i * 0.1)  # Fade each bell
        
        return final_wave
    
    def generate_success_sound(self) -> np.ndarray:
        """Generate a success/completion sound - legacy method"""
        return self.generate_victory_sound()
    
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

class ReverbProcessor:
    """Adds reverb effects to audio"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        
    def apply_reverb(self, audio: np.ndarray, reverb_amount: float = 0.3, 
                    decay_time: float = 1.5) -> np.ndarray:
        """Apply reverb effect to audio"""
        if len(audio) == 0:
            return audio
            
        # Simple reverb using multiple delayed copies
        reverb_delays = [0.05, 0.1, 0.15, 0.25, 0.35, 0.5, 0.75, 1.0]  # Delay times in seconds
        reverb_gains = [0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.08, 0.05]  # Corresponding gains
        
        output = audio.copy()
        
        for delay, gain in zip(reverb_delays, reverb_gains):
            if delay > decay_time:
                break
                
            delay_samples = int(delay * self.sample_rate)
            if delay_samples < len(audio):
                # Create delayed version
                delayed = np.zeros_like(audio)
                delayed[delay_samples:] = audio[:-delay_samples] * gain * reverb_amount
                
                # Add to output
                output += delayed
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(output))
        if max_val > 1.0:
            output = output / max_val * 0.95
            
        return output

class AudioManager:
    """Manages all audio in the game"""
    
    def __init__(self):
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        self.sample_rate = 44100
        self.music_generator = FractalMusicGenerator(self.sample_rate)
        self.sfx_generator = SoundEffectGenerator(self.sample_rate)
        self.reverb_processor = ReverbProcessor(self.sample_rate)
        
        self.music_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
        
        self.music_volume = 0.4  # Heartbeat music volume
        self.sfx_volume = 0.7
        
        # Track transition system
        self.current_track = None
        self.next_track = None
        self.music_started = False
        self.track_start_time = 0
        self.track_transition_duration = 120.0  # 2 minutes in seconds
        self.is_transitioning = False
        self.transition_progress = 0.0
        
        # Generate initial heartbeat track
        self.generate_new_heartbeat_track()
        
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
    
    def generate_new_heartbeat_track(self):
        """Generate new heartbeat-paced music track"""
        def generate_async():
            # Generate a longer heartbeat track (150 seconds to allow smooth transitions)
            heartbeat_track = self.music_generator.create_hip_hop_track(150.0)
            
            if self.current_track is None:
                self.current_track = self.numpy_to_pygame_sound(heartbeat_track)
            else:
                self.next_track = self.numpy_to_pygame_sound(heartbeat_track)
        
        # Generate in background thread to avoid blocking
        Thread(target=generate_async, daemon=True).start()
    
    def start_background_music(self):
        """Start playing background heartbeat music - call this from title screen"""
        if not self.music_started and self.current_track:
            self.music_channel.play(self.current_track, loops=-1)
            self.music_channel.set_volume(self.music_volume)
            self.music_started = True
            self.track_start_time = time.time()
            
            # Start generating next track in advance
            self.generate_new_heartbeat_track()
    
    def play_ambient_music(self):
        """Legacy method - now starts hip-hop background music"""
        self.start_background_music()
    
    def play_merge_sound(self, color: Tuple[int, int, int]):
        """Play merge sound effect with reverb"""
        wave = self.sfx_generator.generate_merge_sound(color)
        wave_with_reverb = self.reverb_processor.apply_reverb(wave, 0.4, 1.2)
        sound = self.numpy_to_pygame_sound(wave_with_reverb)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume)
    
    def play_bounce_sound(self, color: Tuple[int, int, int]):
        """Play bounce sound effect with reverb"""
        wave = self.sfx_generator.generate_bounce_sound(color)
        wave_with_reverb = self.reverb_processor.apply_reverb(wave, 0.2, 0.8)
        sound = self.numpy_to_pygame_sound(wave_with_reverb)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume)
    
    def play_victory_sound(self):
        """Play ethereal victory sound with deep reverb"""
        wave = self.sfx_generator.generate_victory_sound()
        wave_with_reverb = self.reverb_processor.apply_reverb(wave, 0.6, 2.5)  # Deep, long reverb
        sound = self.numpy_to_pygame_sound(wave_with_reverb)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume)
    
    def play_success_sound(self):
        """Play success sound - legacy method, now uses victory sound"""
        self.play_victory_sound()
    
    def play_ui_sound(self, sound_type: str):
        """Play UI sound"""
        wave = self.sfx_generator.generate_ui_sound(sound_type)
        sound = self.numpy_to_pygame_sound(wave)
        self.sfx_channel.play(sound)
        self.sfx_channel.set_volume(self.sfx_volume * 0.5)
    
    def set_music_volume(self, volume: float):
        """Set background music volume"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music_channel.get_busy():
            self.music_channel.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def stop_all(self):
        """Stop all audio"""
        pygame.mixer.stop()
    
    def update(self):
        """Update audio system - handles smooth track transitions"""
        # Start music if not already started and track is ready
        if not self.music_started and self.current_track:
            self.start_background_music()
        
        # Handle track transitions every 2 minutes
        if self.music_started:
            current_time = time.time()
            elapsed_time = current_time - self.track_start_time
            
            # Check if it's time to transition to next track
            if elapsed_time >= self.track_transition_duration and self.next_track and not self.is_transitioning:
                self.start_track_transition()
            
            # Handle smooth transition
            if self.is_transitioning:
                self.update_track_transition()
    
    def start_track_transition(self):
        """Start smooth transition to next track"""
        if self.next_track:
            self.is_transitioning = True
            self.transition_progress = 0.0
            
            # Start playing next track at low volume
            self.music_channel.play(self.next_track, loops=-1)
            self.music_channel.set_volume(0.0)
    
    def update_track_transition(self):
        """Update smooth track transition"""
        transition_speed = 0.02  # How fast to transition (2% per frame)
        self.transition_progress += transition_speed
        
        if self.transition_progress >= 1.0:
            # Transition complete
            self.current_track = self.next_track
            self.next_track = None
            self.is_transitioning = False
            self.track_start_time = time.time()
            self.music_channel.set_volume(self.music_volume)
            
            # Generate next track in advance
            self.generate_new_heartbeat_track()
        else:
            # Smoothly fade between tracks
            # Current track fades out, next track fades in
            fade_volume = self.music_volume * (1.0 - self.transition_progress)
            self.music_channel.set_volume(fade_volume)
    
    def get_current_beat_time(self):
        """Get current beat timing for pulse effects"""
        if not self.music_started:
            return 0.0
        
        current_time = time.time()
        elapsed_time = (current_time - self.track_start_time) % self.music_generator.beat_duration
        return elapsed_time / self.music_generator.beat_duration  # 0.0 to 1.0