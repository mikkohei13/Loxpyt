

import os
import librosa 

# filepath = "/_source_audio/ks/Data/"
# filename = "HLO10_20191102_022600.wav" # mono, 32 kHz
# filename = "HLO10_20190914_005100.wav" # stereo, 48 kHz

# tempFile = filepath + "mono.wav"
# resultFile = filepath + "32khz-mono.wav"

# fullPath = filepath + filename

from pydub import AudioSegment

def mono(filePath):
  print("Loading file " + filePath + " to pydub")
  sound = AudioSegment.from_wav(filePath)
  if sound.channels > 1:
    print("Converting to mono")
    sound = sound.set_channels(1)

    tempFilePath = "/_exports/temp/normalized.wav"
    sound.export(tempFilePath, format="wav")
    return True, tempFilePath

  else:
    print("Source file is mono")
    return False, filePath



def normalize(filePath):
  # Todo: check if mono & 32 kHz already

  print("Loading file " + filePath + " to librosa")
  y, sr = librosa.load(filePath, sr=32000)
  
  print("Converting to mono")
  y_mono = librosa.to_mono(y)
  
  print("Saving with new sample rate")
  tempFilePath = "/_exports/temp/normalized.wav"
  librosa.output.write_wav(tempFilePath, y_mono, sr)
  return tempFilePath


def deleteTempFile(tempFilePath):
  os.remove(tempFilePath)
  return True

