import numpy as np
from scipy.io.wavfile import write

# ===== PARAMETRY =====
sample_rate = 96000
duration = 15  # sekundy
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)


# ===== FUNKCJE SYNTEZY =====
def sine(freq, amp=1.0):
    return amp * np.sin(2 * np.pi * freq * t)


def square(freq, amp=1.0):
    return amp * np.sign(np.sin(2 * np.pi * freq * t))


def saw(freq, amp=1.0):
    return amp * (2 * (t * freq - np.floor(0.5 + t * freq)))


def fm(carrier, mod, index, amp=1.0):
    return amp * np.sin(2 * np.pi * carrier * t + index * np.sin(2 * np.pi * mod * t))


def noise(amp=1.0):
    return amp * np.random.uniform(-1, 1, len(t))


def sweep(start, end, amp=1.0):
    freqs = np.linspace(start, end, len(t))
    return amp * np.sin(2 * np.pi * freqs * t)


def vocal_blbl(amp=0.3):
    # prosty pseudo-sygnał „blbllblbl”
    return amp * np.sign(np.sin(2 * np.pi * 150 * t) * np.sin(2 * np.pi * 5 * t))


def vocal_wrzzz(amp=0.3):
    return amp * np.sin(2 * np.pi * 800 * t) * np.sin(2 * np.pi * 4 * t)


def vocal_trrrr(amp=0.3):
    return amp * np.sign(np.sin(2 * np.pi * 300 * t) * np.sin(2 * np.pi * 15 * t))


def vocal_pwsz(amp=0.3):
    return amp * np.random.uniform(-1, 1, len(t)) * np.sin(2 * np.pi * 600 * t)


# ===== INSTRUMENTY =====
guitar = saw(220, 0.4) + fm(440, 110, 5, 0.2)
piano = sine(261.63, 0.3) + sine(329.63, 0.2)  # C4 + E4 chord

# ===== DZIWNE DŹWIĘKI =====
vocal = vocal_blbl() + vocal_wrzzz() + vocal_trrrr() + vocal_pwsz()
extra_sounds = sweep(20, 40000, 0.2) + noise(0.1) + fm(1200, 37, 15, 0.2)

# ===== STEREO =====
left = guitar + piano + vocal + extra_sounds
right = guitar * 0.8 + piano * 0.9 + vocal + sweep(40000, 20, 0.2) + noise(0.1)

# ===== NORMALIZACJA =====
stereo = np.vstack((left, right)).T
max_val = np.max(np.abs(stereo))
stereo /= max_val * 1.05

# ===== KONWERSJA NA 24-BIT =====
stereo_24bit = np.int32(stereo * (2**23 - 1))

# ===== ZAPIS WAV =====
write("audio_brain_stress_test_96kHz_24bit.wav", sample_rate, stereo_24bit)

print("✔ Wygenerowano: audio_brain_stress_test_96kHz_24bit.wav")
