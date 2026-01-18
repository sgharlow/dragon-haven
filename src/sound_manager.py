"""
Sound Manager for Dragon Haven Cafe.
Procedurally generates all sound effects using synthesis.
No external audio files required.
"""

import pygame
import math
import random
import array


class SoundManager:
    """
    Manages all game audio with procedurally generated sounds.

    Usage:
        sound = get_sound_manager()
        sound.initialize()
        sound.play('ui_click')
        sound.set_volume('ui', 0.8)
    """

    # Sound categories for volume control
    CATEGORIES = ['master', 'ui', 'cooking', 'dragon', 'ambient']

    def __init__(self):
        """Initialize the sound manager (does not init pygame mixer)."""
        self._initialized = False
        self._sounds = {}
        self._volumes = {cat: 1.0 for cat in self.CATEGORIES}
        self._sound_categories = {}  # Maps sound name to category

    def initialize(self, frequency=44100, size=-16, channels=2, buffer=512):
        """
        Initialize pygame mixer and generate all sounds.

        Args:
            frequency: Sample frequency in Hz
            size: Sample size (negative for signed)
            channels: Number of channels (1=mono, 2=stereo)
            buffer: Buffer size
        """
        if self._initialized:
            return True

        try:
            pygame.mixer.init(frequency=frequency, size=size,
                            channels=channels, buffer=buffer)
            self._sample_rate = frequency
            self._generate_all_sounds()
            self._initialized = True
            return True
        except pygame.error as e:
            print(f"Warning: Sound initialization failed: {e}")
            self._initialized = False
            return False

    def _generate_all_sounds(self):
        """Generate all procedural sounds."""
        # UI sounds
        self._generate_ui_sounds()

        # Dragon sounds
        self._generate_dragon_sounds()

        # Cooking sounds
        self._generate_cooking_sounds()

        # Ambient/misc sounds
        self._generate_ambient_sounds()

    # =========================================================================
    # SOUND GENERATION HELPERS
    # =========================================================================

    def _create_sound(self, samples):
        """
        Create a pygame Sound from sample data.

        Args:
            samples: List or array of sample values (-1.0 to 1.0)

        Returns:
            pygame.mixer.Sound object
        """
        # Convert to 16-bit signed integers
        max_val = 32767
        int_samples = array.array('h',
            [int(max(min(s, 1.0), -1.0) * max_val) for s in samples])

        # Create stereo by duplicating samples
        stereo_samples = array.array('h')
        for s in int_samples:
            stereo_samples.append(s)
            stereo_samples.append(s)

        return pygame.mixer.Sound(buffer=stereo_samples)

    def _generate_sine(self, frequency, duration, volume=1.0):
        """Generate a sine wave."""
        num_samples = int(self._sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / self._sample_rate
            sample = math.sin(2 * math.pi * frequency * t) * volume
            samples.append(sample)
        return samples

    def _generate_noise(self, duration, volume=1.0):
        """Generate white noise."""
        num_samples = int(self._sample_rate * duration)
        return [random.uniform(-volume, volume) for _ in range(num_samples)]

    def _apply_envelope(self, samples, attack=0.01, decay=0.1, sustain=0.7, release=0.2):
        """Apply ADSR envelope to samples."""
        total = len(samples)
        attack_samples = int(attack * total)
        decay_samples = int(decay * total)
        release_samples = int(release * total)
        sustain_samples = total - attack_samples - decay_samples - release_samples

        result = []
        for i, sample in enumerate(samples):
            if i < attack_samples:
                # Attack phase
                env = i / max(1, attack_samples)
            elif i < attack_samples + decay_samples:
                # Decay phase
                progress = (i - attack_samples) / max(1, decay_samples)
                env = 1.0 - (1.0 - sustain) * progress
            elif i < attack_samples + decay_samples + sustain_samples:
                # Sustain phase
                env = sustain
            else:
                # Release phase
                progress = (i - attack_samples - decay_samples - sustain_samples) / max(1, release_samples)
                env = sustain * (1.0 - progress)
            result.append(sample * env)
        return result

    def _mix_samples(self, *sample_lists):
        """Mix multiple sample lists together."""
        max_len = max(len(s) for s in sample_lists)
        result = [0.0] * max_len
        for samples in sample_lists:
            for i, s in enumerate(samples):
                result[i] += s
        # Normalize
        max_val = max(abs(s) for s in result) if result else 1
        if max_val > 1.0:
            result = [s / max_val for s in result]
        return result

    def _frequency_sweep(self, start_freq, end_freq, duration, volume=1.0):
        """Generate a frequency sweep (chirp)."""
        num_samples = int(self._sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / self._sample_rate
            progress = i / num_samples
            freq = start_freq + (end_freq - start_freq) * progress
            phase = 2 * math.pi * freq * t
            sample = math.sin(phase) * volume
            samples.append(sample)
        return samples

    # =========================================================================
    # SOUND CATEGORY GENERATORS
    # =========================================================================

    def _generate_ui_sounds(self):
        """Generate UI interaction sounds."""
        # ui_click - short, soft click
        samples = self._generate_sine(800, 0.05, 0.3)
        samples = self._apply_envelope(samples, attack=0.01, decay=0.2, sustain=0.0, release=0.3)
        self._sounds['ui_click'] = self._create_sound(samples)
        self._sound_categories['ui_click'] = 'ui'

        # ui_confirm - pleasant confirmation tone (two notes)
        note1 = self._generate_sine(523, 0.1, 0.4)  # C5
        note2 = self._generate_sine(659, 0.15, 0.4)  # E5
        note1 = self._apply_envelope(note1, 0.01, 0.1, 0.5, 0.3)
        note2 = self._apply_envelope(note2, 0.01, 0.1, 0.5, 0.3)
        combined = note1 + note2
        self._sounds['ui_confirm'] = self._create_sound(combined)
        self._sound_categories['ui_confirm'] = 'ui'

        # ui_cancel - descending tone
        samples = self._frequency_sweep(400, 200, 0.15, 0.4)
        samples = self._apply_envelope(samples, 0.01, 0.2, 0.3, 0.4)
        self._sounds['ui_cancel'] = self._create_sound(samples)
        self._sound_categories['ui_cancel'] = 'ui'

        # ui_hover - very subtle high tone
        samples = self._generate_sine(1200, 0.03, 0.15)
        samples = self._apply_envelope(samples, 0.01, 0.5, 0.0, 0.4)
        self._sounds['ui_hover'] = self._create_sound(samples)
        self._sound_categories['ui_hover'] = 'ui'

    def _generate_dragon_sounds(self):
        """Generate dragon-related sounds."""
        # dragon_chirp - cute high-pitched chirp
        base = self._frequency_sweep(600, 900, 0.1, 0.5)
        vibrato = []
        for i, s in enumerate(base):
            t = i / self._sample_rate
            mod = 1.0 + 0.1 * math.sin(2 * math.pi * 30 * t)
            vibrato.append(s * mod)
        samples = self._apply_envelope(vibrato, 0.05, 0.2, 0.3, 0.4)
        self._sounds['dragon_chirp'] = self._create_sound(samples)
        self._sound_categories['dragon_chirp'] = 'dragon'

        # dragon_eat - chomping sound
        chomp = self._generate_noise(0.08, 0.3)
        tone = self._generate_sine(150, 0.08, 0.4)
        mixed = self._mix_samples(chomp, tone)
        samples = self._apply_envelope(mixed, 0.01, 0.1, 0.2, 0.5)
        self._sounds['dragon_eat'] = self._create_sound(samples)
        self._sound_categories['dragon_eat'] = 'dragon'

        # dragon_happy - ascending happy chirps
        chirp1 = self._frequency_sweep(400, 600, 0.08, 0.4)
        chirp2 = self._frequency_sweep(500, 700, 0.08, 0.4)
        chirp3 = self._frequency_sweep(600, 900, 0.12, 0.4)
        chirp1 = self._apply_envelope(chirp1, 0.01, 0.2, 0.3, 0.4)
        chirp2 = self._apply_envelope(chirp2, 0.01, 0.2, 0.3, 0.4)
        chirp3 = self._apply_envelope(chirp3, 0.01, 0.2, 0.3, 0.4)
        # Add gaps between chirps
        gap = [0.0] * int(0.05 * self._sample_rate)
        combined = chirp1 + gap + chirp2 + gap + chirp3
        self._sounds['dragon_happy'] = self._create_sound(combined)
        self._sound_categories['dragon_happy'] = 'dragon'

        # dragon_hungry - low rumble
        rumble = self._generate_sine(80, 0.3, 0.5)
        noise = self._generate_noise(0.3, 0.2)
        mixed = self._mix_samples(rumble, noise)
        samples = self._apply_envelope(mixed, 0.1, 0.2, 0.4, 0.3)
        self._sounds['dragon_hungry'] = self._create_sound(samples)
        self._sound_categories['dragon_hungry'] = 'dragon'

    def _generate_cooking_sounds(self):
        """Generate cooking-related sounds."""
        # cooking_chop - sharp cutting sound
        noise = self._generate_noise(0.05, 0.6)
        click = self._generate_sine(300, 0.02, 0.4)
        mixed = self._mix_samples(noise, click)
        samples = self._apply_envelope(mixed, 0.001, 0.1, 0.0, 0.5)
        self._sounds['cooking_chop'] = self._create_sound(samples)
        self._sound_categories['cooking_chop'] = 'cooking'

        # cooking_sizzle - continuous sizzling
        noise = self._generate_noise(0.3, 0.3)
        # Add some crackle variation
        for i in range(len(noise)):
            if random.random() < 0.02:
                noise[i] *= 2.0
        samples = self._apply_envelope(noise, 0.05, 0.1, 0.7, 0.15)
        self._sounds['cooking_sizzle'] = self._create_sound(samples)
        self._sound_categories['cooking_sizzle'] = 'cooking'

        # cooking_pour - liquid pouring
        noise = self._generate_noise(0.4, 0.25)
        # Low pass filter effect by averaging
        filtered = []
        window = 10
        for i in range(len(noise)):
            start = max(0, i - window)
            avg = sum(noise[start:i+1]) / (i - start + 1)
            filtered.append(avg * 2)  # Boost a bit
        samples = self._apply_envelope(filtered, 0.1, 0.1, 0.6, 0.2)
        self._sounds['cooking_pour'] = self._create_sound(samples)
        self._sound_categories['cooking_pour'] = 'cooking'

        # cooking_complete - pleasant ding
        note = self._generate_sine(880, 0.4, 0.4)  # A5
        overtone = self._generate_sine(1760, 0.3, 0.15)  # A6
        mixed = self._mix_samples(note, overtone)
        samples = self._apply_envelope(mixed, 0.01, 0.1, 0.3, 0.5)
        self._sounds['cooking_complete'] = self._create_sound(samples)
        self._sound_categories['cooking_complete'] = 'cooking'

    def _generate_ambient_sounds(self):
        """Generate ambient and miscellaneous sounds."""
        # coin_collect - happy coin jingle
        note1 = self._generate_sine(1047, 0.08, 0.3)  # C6
        note2 = self._generate_sine(1319, 0.12, 0.3)  # E6
        note1 = self._apply_envelope(note1, 0.01, 0.2, 0.3, 0.4)
        note2 = self._apply_envelope(note2, 0.01, 0.2, 0.3, 0.4)
        combined = note1 + note2
        self._sounds['coin_collect'] = self._create_sound(combined)
        self._sound_categories['coin_collect'] = 'ambient'

        # customer_happy - pleasant reaction
        samples = self._frequency_sweep(400, 600, 0.15, 0.35)
        samples = self._apply_envelope(samples, 0.05, 0.2, 0.3, 0.4)
        self._sounds['customer_happy'] = self._create_sound(samples)
        self._sound_categories['customer_happy'] = 'ambient'

        # customer_angry - displeased grunt
        samples = self._frequency_sweep(300, 150, 0.2, 0.4)
        noise = self._generate_noise(0.2, 0.15)
        mixed = self._mix_samples(samples, noise)
        mixed = self._apply_envelope(mixed, 0.05, 0.2, 0.4, 0.3)
        self._sounds['customer_angry'] = self._create_sound(mixed)
        self._sound_categories['customer_angry'] = 'ambient'

        # notification - gentle alert
        note = self._generate_sine(660, 0.15, 0.3)
        samples = self._apply_envelope(note, 0.02, 0.1, 0.4, 0.4)
        self._sounds['notification'] = self._create_sound(samples)
        self._sound_categories['notification'] = 'ambient'

        # door_open - creaky door
        creak = self._frequency_sweep(200, 400, 0.3, 0.3)
        noise = self._generate_noise(0.3, 0.1)
        mixed = self._mix_samples(creak, noise)
        samples = self._apply_envelope(mixed, 0.1, 0.2, 0.4, 0.3)
        self._sounds['door_open'] = self._create_sound(samples)
        self._sound_categories['door_open'] = 'ambient'

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def play(self, sound_name, volume_multiplier=1.0):
        """
        Play a sound by name.

        Args:
            sound_name: Name of the sound to play
            volume_multiplier: Additional volume multiplier (0.0-1.0)
        """
        if not self._initialized:
            return

        sound = self._sounds.get(sound_name)
        if sound is None:
            return

        # Calculate final volume
        category = self._sound_categories.get(sound_name, 'ambient')
        master_vol = self._volumes['master']
        category_vol = self._volumes.get(category, 1.0)
        final_vol = master_vol * category_vol * volume_multiplier

        sound.set_volume(final_vol)
        sound.play()

    def set_volume(self, category, level):
        """
        Set volume for a sound category.

        Args:
            category: Category name ('master', 'ui', 'cooking', 'dragon', 'ambient')
            level: Volume level (0.0 to 1.0)
        """
        if category in self._volumes:
            self._volumes[category] = max(0.0, min(1.0, level))

    def get_volume(self, category):
        """Get the current volume for a category."""
        return self._volumes.get(category, 1.0)

    def get_sound_names(self):
        """Get list of all available sound names."""
        return list(self._sounds.keys())

    def stop_all(self):
        """Stop all currently playing sounds."""
        if self._initialized:
            pygame.mixer.stop()

    def is_initialized(self):
        """Check if sound manager is properly initialized."""
        return self._initialized


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_sound_manager = None


def get_sound_manager():
    """Get the global sound manager instance."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
