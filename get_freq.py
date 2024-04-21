"""
Arjun Chandra
"""
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import aubio

def record_and_save_audio(filename):
    """
    This function records and digitizes audio from the microphone through the Pyaudio binding
    and writes the audio data as a wav file under the filename argument. Credit to Joska de
    Langen for the original code.
    """
    chunk = 1024
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100
    seconds = 3

    p = pyaudio.PyAudio()

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def get_frequency(filename):
    """
    This function takes a filename for an input and then uses the Aubio.pitch command line tool
    to find the average frequency and print it to the console. Credit to Lukasz Tracewski for the
    original code.
    >>> filename = '440Hz_44100Hz_16bit_05sec.wav'
    >>> get_frequency(filename)
    Average frequency = 437.80374 Hz
    >>> filename = 'silence.wav'
    >>> get_frequency(filename)
    No audio detected
    >>> filename = 'low_e_youtube.wav'
    >>> get_frequency(filename)
    Average frequency = 83.00123 Hz
    """
    # Setting default arguments for aubio.pitch tool
    buff_size = 2048
    hop_size = 256
    Unit = "Hz"
    tolerance = 0.8
    sample_rate = 44100

    #Reading file with aubio source tool
    file_read = aubio.source(filename, sample_rate, hop_size)

    # aubio.pitch only takes 4 arguments max, lines 35 and 36 set other 2
    get_pitch = aubio.pitch("mcomb", buff_size, hop_size, sample_rate)
    get_pitch.set_unit(Unit)
    get_pitch.set_tolerance(tolerance)

    pitches = []


    while True:
        samples, read = file_read()         #https://aubio.org/manual/latest/py_io.html
        pitch = get_pitch(samples)[0]
        #filters all silent noise from pitches array
        if pitch > 30:
            pitches += [pitch]
        #Break loop if reading less samples than hop_size, not enough samples left
        if read < hop_size:
            break
    if len(pitches) == 0:
        print('No audio detected')
    else:
        print(f"Average frequency = {str(np.array(pitches).mean())} Hz")
   


def get_info(filename):
    audio = wave.open(filename, 'rb')
    print('Audio info: \n')
    print('Audio channels:', audio.getnchannels())
    print('Frame rate:', audio.getframerate())
    print('Number of frames', audio.getnframes())
    print('Sample width:', audio.getsampwidth())
    audio.close()

def print_frequencies():  #modify later to print user frequencies next to them
    print('E: 329.63 Hz')
    print('B: 246.94 Hz')
    print('G: 196 Hz')
    print('D: 146.83 Hz')
    print('A: 110 Hz')
    print('E: 82.31 Hz')

"""
get_info('test2.wav')
song_test = AudioSegment.from_wav("test2.wav")
song_test_edited = song_test.reverse()     #song_test is immutable, have to modify with new object
song_test_edited.export("pleasework.wav", format="wav")

array = np.arange(15).reshape(3, 5)
print(array)
"""

def main():
    record_and_save_audio('fulltest.wav')
    get_frequency('fulltest.wav')



if __name__ == "__main__":
    main()
