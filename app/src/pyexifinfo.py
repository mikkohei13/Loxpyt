# Dependency: exiftool

import pprint
import subprocess
from bs4 import BeautifulSoup

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

  # Nocmig device data
  if "AudioMoth" in results.get("Comment", ""):
    results["x-device-model"] = "audiomoth"
    results["x-device-id"], results["x-gain-setting"] = getAudiomothData(results.get("Comment"))
    results["x-notes"] = results.get("Comment")
    results["x-file-modified"] = results.get("File Modification Date/Time")
  else:
    results["x-device-model"] = "sm4" # Todo: fix if use other devices
    results["x-device-id"] = "HLO10" # Todo: fix if use other devices
    results["x-notes"] = "Not getting metadata from Wildlife Acoustics devices yet"
    results["x-file-modified"] = None

  # Todo: Extract metadata from Wildlife acoustics devices
  # https://github.com/riggsd/guano-py/blob/master/bin/wamd2guano.py

  results["x-duration-seconds"] = getDurationStr2Sec(results.get("Duration", "00:00:00"))

  print(results)
  pprint.pprint(results)

  return results



# audioFilePath = 'audio/noordwijk/5DB0D594.WAV'
# audioFilePath = 'audio/noordwijk/5DB0E3A4.WAV'
# audioFilePath = 'audio/ks/HLO10_20191102_022600.wav'
# audioFilePath = 'audio/noordwijk/5DB0E3A4.WAV'
# parseFile(audioFilePath)
