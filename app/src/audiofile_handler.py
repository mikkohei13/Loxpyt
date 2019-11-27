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

### INPUT #########################################################

segments = 0
segmentsLimit = 100
exportDir = "/_exports"

debug = True # get input from this file

if debug:
  directory = "ks"
  directory = "20190422-26-Harmaakallio"
  directory = "noordwijk"

  location = "Noordwijk"
  segments = 0

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

# Validate input
# Todo: tbd: Check that dir name contains locality string? To avoid errors.
# Todo: check if directory/data (case-sensitivity?) exists and contains wav files, or raise error. What happens now?

if segments > segmentsLimit:
  segments = segmentsLimit

location = location.lower()

# Todo: good place to define path structure?
path = "/_source_audio/" + directory + "/Data"


### HANDLING DATA #########################################################

audioFileList = file_helper.getAudioFileList(path)

# Get metadata for the file
# Todo: move this to last, so that error will prevent it from running

db = loxia_database.db()

### SESSION ###
# Todo: tbd: What to do if same directory handled twice?
sessionId = directory
sessionData = { "_id": sessionId, "directory": directory, "location": location }
db.saveSession(sessionData)

### FILES ###
for audioFilePath in audioFileList:
  # Todo: tbd: What to do if save file handled twice?

  # File metadata
  fileData = file_helper.parseFile(audioFilePath)

  # File name is not necessarily unique, e.g. when multiple recorders start at the same time. Therefore need to include session to the id.
  fileId = sessionId + "/" + fileData.get("fileName")
  fileData["_id"] = fileId
  fileData["session_id"] = sessionId

  db.saveFile(fileData)

  # File to mono
  deleteMonoFile, monoFilePath = file_normalizer.mono(audioFilePath)

  ### SEGMENTS ###
  # Split into segments and generate spectrograms
  segmentMetaGenerator = split_and_spectro.parseFile(monoFilePath, exportDir, directory, fileData["fileName"], segments, 10)

  for segmentMeta in segmentMetaGenerator:
    segmentId = fileId + "/" + str(segmentMeta["segmentNumber"])

    # Additional data
    segmentMeta["_id"] = segmentId
    segmentMeta["file_id"] = fileId
    segmentMeta["fileDirectory"] = directory

    segmentMeta["segmentStartUTC"] = fileData["recordDateStartUTC"] + datetime.timedelta(0, segmentMeta["segmentStartSeconds"])

    db.saveSegment(segmentMeta)

  # Remove temp file
  if deleteMonoFile:
    file_normalizer.deleteTempFile(monoFilePath)

  # If segments defined for debugging, break processing before going to next file
  if segments > 0:
    break;

