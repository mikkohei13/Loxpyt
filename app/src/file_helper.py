# Dependency: exiftool

import pprint
import subprocess
from bs4 import BeautifulSoup
import os


def getDurationStr2Sec(durationStr):
  durationList = durationStr.split(":")
  return 3600*int(durationList[0]) + 60*int(durationList[1]) + int(durationList[2])


def getAudiomothData(string):
  # Todo: log if input does not match expected, e.g. if different in new versions of the device
  words = string.split(" ")

  # deviceId
  audioMothIndex = words.index("AudioMoth")
  deviceId = words[(audioMothIndex + 1)]

  # gain setting
  settingIndex = words.index("setting")
  gainSetting = int(words[(settingIndex + 1)])

  return deviceId, gainSetting


def parseFile(audioFilePath):

  html = subprocess.check_output('exiftool -h ' + audioFilePath, shell=True)
#  print(html)
#  print(len(html))

  # Parse html to dict
  bs = BeautifulSoup(html, 'lxml')
  results = {}
  for row in bs.findAll('tr'):
    aux = row.findAll('td')
    results[aux[0].string] = aux[1].string

  # Create metadata dict
  metadata = {}

  # A) raw meta
  metadata['rawMetadata'] = results

  # B) Calculated meta
  metadata["fileName"] = results.get("File Name") # This is required for databasing
  metadata["durationSeconds"] = getDurationStr2Sec(results.get("Duration", "00:00:00"))
  metadata["dateModified"] = results.get("File Modification Date/Time")

  if "AudioMoth" in results.get("Comment", ""):
    metadata["deviceModel"] = "audiomoth"
    metadata["deviceVersion"] = "1.0"
    metadata["deviceId"], results["gainSetting"] = getAudiomothData(results.get("Comment"))

  # Expects the only other option to be WA SM4
  # Todo: fix if use other devices
  # Todo: Extract metadata from Wildlife acoustics devices
  # https://github.com/riggsd/guano-py/blob/master/bin/wamd2guano.py
  else:
    metadata["deviceModel"] = "sm4" 
    metadata["deviceVersion"] = ""
    metadata["deviceId"] = "HLO10"



  print(metadata)
  pprint.pprint(metadata)

  return metadata



# audioFilePath = 'audio/noordwijk/5DB0D594.WAV'
# audioFilePath = 'audio/noordwijk/5DB0E3A4.WAV'
# audioFilePath = 'audio/ks/HLO10_20191102_022600.wav'
# audioFilePath = 'audio/noordwijk/5DB0E3A4.WAV'
# parseFile(audioFilePath)

def getAudioFileList(directory):
  audioFileList = []
  for root, dirs, files in os.walk(directory):
    for name in files:
      if name.lower().endswith(".wav"):
        audioFileList.append(directory + "/" + name)

  return tuple(audioFileList)

