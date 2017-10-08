from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("../Sounds/Drums_0/sound0.wav")

# uses pyaudio if available, falls back to opening an ffplay subprocess
play(sound)