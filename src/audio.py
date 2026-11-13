import pygame

class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sound(self, name, file_path):
        """Load a sound file and store it in the sounds dictionary."""
        try:
            sound = pygame.mixer.Sound(file_path)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Error loading sound {file_path}: {e}")

    def play_sound(self, name):
        """Play a loaded sound by its name."""
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Sound '{name}' not found.")

    def stop_sound(self, name):
        """Stop a playing sound by its name."""
        if name in self.sounds:
            self.sounds[name].stop()
        else:
            print(f"Sound '{name}' not found.")
 
    def set_volume(self, name, volume):
        """Set the volume for a specific sound."""
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        else:
            print(f"Sound '{name}' not found.")