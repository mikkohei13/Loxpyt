# Dependency: exiftool

import subprocess
from bs4 import BeautifulSoup
import os
import datetime

from wamd import wamd


### HELPERS #########################################################

def getDurationStr2Sec(durationStr):
  # Xeno-Canto duration string, e.g. "24.02 s"
  if durationStr.find(" s") > -1:
    return -1
  elif "00:00:00" == durationStr:
    raise ValueError("File has zero or missing duration")
  else:
    durationList = durationStr.split(":")
    return 3600*int(durationList[0]) + 60*int(durationList[1]) + int(durationList[2])


def getAudioFileList(directory):
  audioFileList = []
  objects = os.listdir(directory)
  print(objects) # debug
  for name in objects:
    # Todo: from mp3
    if name.lower().endswith(".wav"):
      audioFileList.append(directory + "/" + name)

  return tuple(audioFileList)


def getSegmentList(directory):
  segmentList = []
  objects = os.listdir(directory)
#  print(objects) # debug
  for name in objects:
    if name.lower().endswith(".png"):
      segment = name.replace(".png", "")
      segmentList.append(directory + "/" + segment)

  return tuple(segmentList)



### AUDIOMOTH PARSER #########################################################

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


def getAudiomothTimes(filename, timespanSeconds):
  hexTimestamp = int(filename.replace(".WAV", ""), 16)
  dateStartUTC = datetime.datetime.utcfromtimestamp(hexTimestamp)
  dateEndUTC = dateStartUTC + datetime.timedelta(0, timespanSeconds)

  return dateStartUTC, dateEndUTC


### SM4 PARSER #########################################################

def getSM4Times(timestamp, timespanSeconds):
  timestamp = timestamp.decode("utf-8")

  # Crude way to convert from time zone +3 to UTC: just calculate the time manually 
  # Todo: Prepare for other time zones also, using some module
  timestampList = timestamp.split("+")
  dateStartUTC = datetime.datetime.strptime(timestampList[0], '%Y-%m-%d %H:%M:%S')
  if ("03:00" == timestampList[1]):
    dateStartUTC = dateStartUTC + datetime.timedelta(0, -(3*60*60))  
  else:
    raise NotImplementedError("This time zone not yet supported: " + timestampList[1])

#  print(dateStartUTC)
  # Todo: adjust to UTC

  dateEndUTC = dateStartUTC + datetime.timedelta(0, timespanSeconds)

  return dateStartUTC, dateEndUTC


### MAIN PARSER #########################################################

def parseFile(audioFilePath):

  # Check if filename contains spaces
  if audioFilePath.find(" ") > -1:
    exit("Spaces not allowed in filename: " + audioFilePath)
  else:
    print("Filename ok: " + audioFilePath)

  html = subprocess.check_output("exiftool -h '" + audioFilePath + "'", shell=True)
#  print(html) # debug
#  print(len(html))

  # Parse html to dict
  bs = BeautifulSoup(html, 'lxml')
  results = {}
  for row in bs.findAll('tr'):
    aux = row.findAll('td')
    results[aux[0].string] = aux[1].string

  # Create metadata dict
  metadata = {}

  # A) Raw exif metadata
  metadata['fileRawMetadata'] = results

  # B) Calculated metadata
  metadata["fileName"] = results.get("File Name")
  metadata["recordDurationSeconds"] = getDurationStr2Sec(results.get("Duration", "00:00:00"))
  metadata["fileDateModified"] = results.get("File Modification Date/Time") # Todo: Convert to datetime object?

  # C) Device model -specific metadata

  # AUDIOMOTH
  if "AudioMoth" in results.get("Comment", ""):
    metadata["deviceModel"] = "audiomoth 1.0"
    metadata["deviceFirmwareVersion"] = ""
    metadata["deviceId"] = "biomi.org.1" # Ad hoc id
    metadata["deviceSerial"], results["deviceGainSetting"] = getAudiomothData(results.get("Comment")) # Todo: Refactor: divide into two 
    
    metadata["recordDateStartUTC"], metadata["recordDateEndUTC"] = getAudiomothTimes(results.get("File Name"), metadata["recordDurationSeconds"])

  # XENO-CANTO
  elif results.get("Product") == "xeno-canto":
    metadata["deviceModel"] = "xeno-canto"
    metadata["recordDateStartUTC"] = datetime.datetime.utcfromtimestamp(0); # Fake time, since real time is not known for xeno-canto files

  # WILDLIFE ACOUSTICS SM4
  # Expects the only other option to be SM4
  # Todo: Handle identifying SM4 better than from file name 
  elif audioFilePath.find("HLO10") > -1:

    wamdMetadata = wamd(audioFilePath)
    metadata['fileRawMetadata'].update(wamdMetadata)

    metadata["deviceModel"] = wamdMetadata['model']
    metadata["deviceFirmwareVersion"] = wamdMetadata['firmware']
    metadata["deviceSerial"] = wamdMetadata['serial']
    metadata["deviceId"] = wamdMetadata['prefix']
    metadata["deviceSensitivitySetting"] = wamdMetadata['sensitivity']

    metadata["recordDateStartUTC"], metadata["recordDateEndUTC"] = getSM4Times(wamdMetadata['timestamp'], metadata["recordDurationSeconds"])

    """
    metadata["deviceModel"] = "sm4" 
    metadata["deviceVersion"] = ""
    metadata["deviceId"] = "HLO10"
    """

  else:
    metadata["deviceModel"] = "training"
    metadata["recordDateStartUTC"] = datetime.datetime.utcfromtimestamp(0); # Fake time, since real time is not known for xeno-canto files
#    return False

  # Todo: Night id

#  print(metadata)

  return metadata

