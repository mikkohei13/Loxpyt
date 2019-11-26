import os
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


def deleteTempFile(tempFilePath):
  os.remove(tempFilePath)
  return True

