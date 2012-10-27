import scipy
import numpy as np
import scipy.signal as signal

# References:
# Bello, Daudet, Abdallah, Duxbury, Davies, Sandler: A Tutorial on Onset Detection in Music Signals

def detect_onsets(sig, fftwin = 512):
    spectrogram = generate_spectrogram(sig, fftwin)
    hfcs = np.array(map(get_hfc, spectrogram))
    hfcs /= max(hfcs)
    hfcs = filter_hfcs(hfcs)
    peak_indices = np.array([i for i, x in enumerate(hfcs) if x > 0]) * fftwin
    return peak_indices

def get_hfc(spectrum):
    hfc = np.sum(np.power(spectrum, 2) * np.arange(1, len(spectrum) + 1))
    return hfc

def generate_spectrogram(audio, window_size):
    spectrogram = [None] * (1 + (len(audio) / window_size))
    for t in xrange(0, len(audio), window_size):
        actual_window_size = min(window_size, len(audio) - t)
        windowed_signal = audio[t:(t + window_size)] * np.hanning(actual_window_size)
        spectrum = abs(scipy.fft(windowed_signal))
        spectrum = spectrum[0:len(spectrum) / 2]
        spectrogram[int(t / window_size)] = spectrum

    return spectrogram

def filter_hfcs(hfcs):
    fir = signal.firwin(11, 1.0 / 8, window = "hamming")
    filtered = np.convolve(hfcs, fir, mode="same")
    filtered = climb_hills(filtered)
    return filtered

def climb_hills(vector):
    moving_points = range(len(vector))
    stable_points = []

    while len(moving_points) > 0:
        for (i, x) in reversed(list(enumerate(moving_points))):

            def stable():
                stable_points.append(x)
                del moving_points[i]

            if x > 0 and x < len(vector) - 1:
                if vector[x] >= vector[x - 1] and vector[x] >= vector[x + 1]:
                    stable()
                elif vector[x] < vector[x - 1]:
                    moving_points[i] -= 1
                else:
                    moving_points[i] += 1

            elif x == 0:
                if vector[x] >= vector[x + 1]:
                    stable()
                else:
                    moving_points[i] += 1

            else:
                if vector[x] >= vector[x - 1]:
                    stable()
                else:
                    moving_points[i] -= 1

    filtered = [0] * len(vector)
    for x in set(stable_points):
        filtered[x] = vector[x]

    return filtered

