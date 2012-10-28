Onset Detector
==============

Simple onset detector. Detects onsets by finding peaks in high frequency content,
and filtering said peaks using hill climbing.

Example usage
-------------

    import scipy.io.wavfile
    import onsetdetection
    sr, audio = scipy.io.wavfile.read('audio.wav')
    audio = audio[:,0] # make it mono
    onsets = onsetdetection.detect_onsets(audio)

Returns a numpy array of offsets, in samples.

References
----------

Bello, Daudet, Abdallah, Duxbury, Davies, Sandler: A Tutorial on Onset Detection in Music Signals, 2005
