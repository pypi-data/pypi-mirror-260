try:
    import mido
except ImportError:
    print("can not use physicsLab.music, type `pip install mido`")

from .sound import sound
from plmidi_cpp import OpenMidiFileError, plmidiInitError

__all__ = [
    "sound",
    "OpenMidiFileError", "plmidiInitError"
]