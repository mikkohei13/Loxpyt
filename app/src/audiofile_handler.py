#
# Example usage: see readme.md
#

import argparse
import datetime
import os

import split_and_spectro
import file_helper
import file_normalizer
import loxia_database
import predict_helper
import report_helper


### INPUT #########################################################

segments = 0
segmentsLimit = 100

debug = True # get input from this file
onlyAnalyse = True;

threshold = 0.8

html = "" # refactor into class


if onlyAnalyse:
  now = datetime.datetime.now() # OR datetime.datetime ??
  timestampSuffix = "_" + now.strftime("%Y%m%d_%H%M%S") # timestamp because analysis can be repeated later with a btter model
  exportDir = "/_analysis"

else:
  exportDir = "/_exports"
  timestampSuffix = "" # No timestamp because should be created only once



if debug:
  directory = "ks"
  directory = "20190422-26-Harmaakallio"
  directory = "20190512-15-Söderskoginmetsä-jyrkänne"
  directory = "20190505-11-Nötkärrinkallio-N"
  directory = "noordwijk"
  directory = "20190421-22-Nötkärrinkallio"
  directory = "20190926-1002-Ks-SM4"
  directory = "Noise-training-data"
  directory = "20190427-28-Hanikka"
  directory = "XC-Set-1"
  directory = "xctest"
  directory = "20200126-27-Ks-häiriöjasade"
  directory = "20190506-07-Ks-SM4"
  directory = "Noise-training-data"
  directory = "20200201-07-Lilla-Bodö"
  directory = "20190831-0901-Hässelholmen-SM4"
  directory = "XC-Set-8"
  directory = "20190505-11-Nötkärrinkallio-N"
  directory = "20190522-27-Harmaakallio"
  directory = "20190522-27-Harmaakallio-test"
  directory = "test_20190506-07-Ks-SM4"
  
  location =  "xctest"
  location =  "training"
  location =  "xeno-canto"
  location =  "nötkärrinkallio-n"
  location =  "harmaakallio"
  location =  "kaskisavu"
  location =  "test"

  segments = 0    # zero for unlimited

else:
  # Get args from command line
  parser = argparse.ArgumentParser(description='Tool to create segment files and spectrograms from large audio files')
  parser.add_argument("--dir", help="Name of directory to parse audio files from, relative to _source_audio. (string, required)", required=True)
  parser.add_argument("--segments", help="How many segments to generate for debugging. Limited to " + segmentsLimit + ". Set to 0 or leave out to create as many as needed. (int, required)")
  parser.add_argument("--location", help="Unique location name, used as a location id. (string, required)", required=True)

  args = parser.parse_args()
  directory = args.dir
  segments = int(args.segments)
  location = args.location


# TODO: Think up a good place to define path structure?
path = "/_source_audio/" + directory + "/Data"
directory = directory + timestampSuffix

# Validate input
# Todo: tbd: Check that dir name contains locality string? To avoid errors.
# Todo: check if directory/data (case-sensitivity?) exists and contains wav files, or raise error. What happens now?

if segments > segmentsLimit:
  segments = segmentsLimit

location = location.lower()


### HANDLING DATA #########################################################

audioFileList = file_helper.getAudioFileList(path)

# Get metadata for the file
# Todo: move this to last, so that error will prevent it from running

db = loxia_database.db()

### SESSION ###
# Todo: tbd: What to do if same directory handled twice? Exit the process with warning.

sessionId = directory
sessionData = { "_id": sessionId, "directory": directory, "location": location }
db.saveSession(sessionData)

### FILES ###
for audioFilePath in audioFileList:
  # TODO: tbd: What to do if same file handled twice? Exit the process with warning.

  # File to mono
  # TODO later: log
  try:
    deleteMonoFile, monoFilePath = file_normalizer.mono(audioFilePath)
  except:
    print("   WARNING: Skipping due to normalization problem " + audioFilePath)
    continue

  # Create file metadata
  fileData = file_helper.parseFile(audioFilePath)
  if False == fileData:
    # Todo: log
    print("   WARNING: Skipping file with unknown origin " + audioFilePath)
    continue

  # File name is not necessarily unique, e.g. when multiple recorders start at the same time. Therefore need to include session to the id.
  fileId = sessionId + "/" + fileData.get("fileName")
  fileData["_id"] = fileId
  fileData["session_id"] = sessionId

  # If analyzing, skip saving to database. Start saving into file/string instead.
  if not onlyAnalyse:
    db.saveFile(fileData)
  
  # Split file into segments and generate spectrograms, return metadata about them
  segmentMetaGenerator = split_and_spectro.parseFile(monoFilePath, exportDir, directory, fileData["fileName"], segments, 10)


  ### SEGMENTS ###
  # Create segment metadata
  for segmentMeta in segmentMetaGenerator:
    segmentId = fileId + "/" + str(segmentMeta["segmentNumber"])

    # Additional data
    segmentMeta["_id"] = segmentId
    segmentMeta["file_id"] = fileId
    segmentMeta["fileDirectory"] = directory

    segmentMeta["segmentStartUTC"] = fileData["recordDateStartUTC"] + datetime.timedelta(0, segmentMeta["segmentStartSeconds"])

    if onlyAnalyse:
      # ABBA: predict, delete, report
      print("HERE: ") # debug
      print(segmentMeta) # debug

      spectroFilePath = "../.." + exportDir + "/" + segmentMeta["fileDirectory"] + "/" + segmentMeta["spectroFilename"]

      print(", PATH: " + spectroFilePath) # debug

      score = predict_helper.predict(spectroFilePath, segmentMeta["spectroFilename"])

      if score >= threshold:
        print("above threshold " + str(score) + "\n")
#        html += "\n\n" + segmentMeta["baseAudioFilename"] + "\n"
        html += report_helper.spectrogram(segmentMeta["spectroFilename"])
        html += "<p>score " + str(score) + "</p>\n"
        html += report_helper.audioEmbed(segmentMeta["finalAudioFilename"])

      else:
        print("below threshold " + str(score) + "\n")
        html += "<p>below threshold score " + str(score) + "</p>\n"
        mp3FilePath = "../.." + exportDir + "/" + segmentMeta["fileDirectory"] + "/" + segmentMeta["finalAudioFilename"]
        os.remove(mp3FilePath)
        os.remove(spectroFilePath)


    # If analyzing, skip saving to database.
    else:
      db.saveSegment(segmentMeta)


  # Remove temp mono file
  if deleteMonoFile:
    file_normalizer.deleteTempFile(monoFilePath)


  # If segments defined for debugging, break processing before going to next file
  if segments > 0:
    break;

# Save report
report_helper.saveFile(html, ("../.." + exportDir + "/" + segmentMeta["fileDirectory"] + "/")) # TODO: simplify dir management
