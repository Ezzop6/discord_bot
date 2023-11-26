import simpleaudio as sa
import sounddevice as sd
import numpy as np
from scipy.io import wavfile


def nahrat_zvuk(sekundy, vzorkovaci_frekvence=44100):
    """
    Nahrává zvuk z mikrofonu po dobu zadaných sekund.

    :param sekundy: Délka nahrávání v sekundách.
    :param vzorkovaci_frekvence: Vzorkovací frekvence zvuku.
    :return: Nahrávka jako NumPy pole.
    """
    nahravka = sd.rec(int(sekundy * vzorkovaci_frekvence), samplerate=vzorkovaci_frekvence, channels=2)
    sd.wait()  # Čeká na dokončení nahrávání
    return nahravka


def prehrat_zvuk(nahravka, vzorkovaci_frekvence=44100):
    """
    Přehrává nahrávku.

    :param nahravka: Nahrávka jako NumPy pole.
    :param vzorkovaci_frekvence: Vzorkovací frekvence zvuku.
    """
    # Převod nahrávky na byty
    audio = np.int16(nahravka * 32767).tobytes()

    # Přehrávání zvuku
    play_obj = sa.play_buffer(audio, 2, 2, vzorkovaci_frekvence)
    play_obj.wait_done()  # Čeká na dokončení přehrávání


# Nahrát 5 sekund zvuku
zvuk = nahrat_zvuk(5)
zvuk_int16 = np.int16(zvuk * 32767)
wavfile.write('zvuk.wav', 44100, zvuk_int16)
