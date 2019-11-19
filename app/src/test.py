
"""
import datetime

date_time_str = '2018-06-29 08:15:27.243860'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)

Audiomoth 
lengthSeconds = 60*60
dateModifiedText = "2019:10:23 19:34:50+00:00"
dateModifiedObject = datetime.datetime.strptime(dateModifiedText, '%Y:%m:%d %H:%M:%S')

filename = "5DB0D594.WAV"

def getAudiomothTimes(filename, timespanSeconds):
  hexTimestamp = int(filename.replace(".WAV", ""), 16)
  dateStartUTC = datetime.datetime.utcfromtimestamp(hexTimestamp)
  dateEndUTC = dateStartUTC + datetime.timedelta(0, timespanSeconds)

  return dateStartUTC, dateEndUTC

dateStartUTC, dateEndUTC = getAudiomothTimes(filename, lengthSeconds)

print(dateStartUTC)
print(dateEndUTC)

dateModifiedObjectUTC 
dateBeginObjectUTC

import datetime

print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
"""

"""
# Split audio file

from pydub import AudioSegment

audioFilePath = ""
wavFilename = "export.wav"
minutes = 5
seconds = minutes * 60

newAudio = AudioSegment.from_wav(audioFilePath)

segment = newAudio[0:(seconds * 1000)]

segment.export(wavFilename, format="wav")
"""

import os

def getAudioFileList(directory):
  audioFileList = []
  objects = os.listdir(directory)
  print(objects)
  for name in objects:
    if name.lower().endswith(".wav"):
      audioFileList.append(directory + "/" + name)

  return tuple(audioFileList)

  """
  for root, dirs, files in os.walk(directory):
    print(files)
    for name in files:
      if name.lower().endswith(".wav"):
        audioFileList.append(directory + "/" + name)

  return tuple(audioFileList)
  """

print("Test")
#getAudioFileList("/_source_audio/noordwijk/Data")

fl = getAudioFileList("/_source_audio/noordwijk/Data")
print(fl)
