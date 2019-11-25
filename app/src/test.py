

import os

def getAudioFileList(directory):
  audioFileList = []
  objects = os.listdir(directory)
  print(objects)
  for name in objects:
    if name.lower().endswith(".wav"):
      audioFileList.append(directory + "/" + name)

  return tuple(audioFileList)

# -------------------------------------------------------

print("Test")
#getAudioFileList("/_source_audio/noordwijk/Data")

# fl = getAudioFileList("/_source_audio/noordwijk/Data")
# print(fl)

# -------------------------------------------------------

from pydub import AudioSegment

filepath = "/_source_audio/20190506-07-Ks-SM4/Data/"
filename = "HLO10_20190506_220000.wav" # stereo, 48 kHz

fullPath = filepath + filename

sound = AudioSegment.from_wav(fullPath)
sound = sound.set_channels(1)
sound.export("/_temp/" + filename, format="wav")
