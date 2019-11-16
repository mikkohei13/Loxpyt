#
# Example usage: see readme.md
#

import argparse

import split_and_spectro
import file_helper
import loxia_database

### INPUT #########################################################

segments = 0
segmentsLimit = 100

debug = True # get input from this file AND use interpreter on host Linux 

if debug:
  directory = "noordwijk"
  directory = "ks"

  location = "Kaskisavu"
  segments = 10

else:
  # Get args from command line
  parser = argparse.ArgumentParser(description='Tool to create segment files and spectrograms from large audio files')
  parser.add_argument("--dir", help="Name of directory to parse audio files from, relative to _source_audio. (string, required)", required=True)
  parser.add_argument("--segments", help="How many segments to generate for debugging. Limited to " + segmentsLimit + ". Set to 0 or leave out to create as many as needeed. (int, required)")
  parser.add_argument("--location", help="Unique location name, used as a location id. (string, required)", required=True)

  args = parser.parse_args()
  directory = args.dir
  segments = int(args.segments)
  location = args.location

# Validate input
# Todo: tbd: Check that dir name contains locality? To avoid errors.
# Todo: check if directory/data (case-sensitivity?) exists and contains wav files, or raise error

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

### SESSION
# Todo: tbd: What to do if same directory handled twice?
sessionId = directory
sessionData = { "_id": sessionId, "directory": directory, "location": location }
db.saveSession(sessionData)

### FILES
for filePath in audioFileList:

  # Todo: tbd: What to do if save file handled twice?
  # Save file
  fileData = file_helper.parseFile(filePath)
  # File name is not necessarily unique, e.g. when multiple recorders start at the same time. Therefore need to include session to the id.
  fileId =directory + "/" + fileData.get("fileName")
  fileData["_id"] = fileId
  fileData["session_id"] = sessionId

  db.saveFile(fileData)

  ### SEGMENTS
  # Create and loop segments

  # Split into segments and generate spectrograms
  exportDirPath = "/_exports/" + directory

  """
  Todo:
  Save segments to database
  a) yield
  b) db as dependency injection
  """
  segmentMetaGenerator = split_and_spectro.parseFile(filePath, exportDirPath, segments)

  for segmentMeta in segmentMetaGenerator:
    print(segmentMeta)

  # If segments defined for debugging, break processing
  if segments > 0:
    break;

