import os
import pygame
import numpy as np
import constants

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

def play_sound(filename, volume=1.0):
    """
    Plays a sound file relative to the VFS virtual hard drive (STORAGE_PATH).
    Example: play_sound("dos/beep.wav") or play_sound("beep.wav")
    """
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # Resolve target file path inside the VFS storage directory
    vfs_path = os.path.abspath(os.path.join(constants.STORAGE_PATH, filename))
    vfs_root = os.path.abspath(constants.STORAGE_PATH)

    # VFS Jail check
    if not vfs_path.startswith(vfs_root):
        return "Access denied: File outside VFS storage."

    if not os.path.exists(vfs_path) or not os.path.isfile(vfs_path):
        return f"File not found in VFS: {filename}"

    try:
        sound = pygame.mixer.Sound(vfs_path)
        sound.set_volume(volume)
        sound.play()
        return None
    except Exception as e:
        return f"Sound playback error: {e}"

def play_root_sound(filename, volume=1.0):
    """
    Plays a sound file relative to the project root directory (BASE_DIR).
    Example: play_root_sound("assets/boot.wav")
    """
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # Resolve path relative to host project root directory
    root_path = os.path.abspath(os.path.join(constants.BASE_DIR, filename))

    if not os.path.exists(root_path) or not os.path.isfile(root_path):
        return f"File not found in project root: {filename}"

    try:
        sound = pygame.mixer.Sound(root_path)
        sound.set_volume(volume)
        sound.play()
        return None
    except Exception as e:
        return f"Sound playback error: {e}"