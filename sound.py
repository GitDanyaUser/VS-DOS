import pygame
import numpy as np

def play_beep(frequency=440, duration=100, volume=0.3): # Added volume parameter
    sample_rate = 44100
    n_samples = int(sample_rate * (duration / 1000.0))
    
    t = np.linspace(0, duration / 1000.0, n_samples, False)
    wave = np.sin(frequency * t * 2 * np.pi)
    
    # Lower the multiplier to decrease volume
    # Max is 32767, so 32767 * 0.3 is about 9830 (much quieter)
    amplitude = int(32767 * volume)
    audiobuffer = (wave * amplitude).astype(np.int16)
    
    # Convert Mono to Stereo for the mixer
    stereo_buffer = np.repeat(audiobuffer.reshape(-1, 1), 2, axis=1)
    
    beep_sound = pygame.sndarray.make_sound(stereo_buffer)
    beep_sound.play()