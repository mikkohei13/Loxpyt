#
# Example usage: see readme.md
#

import argparse

import split_and_spectro
import file_helper
import loxia_database


debug = True # get input from this file AND use interpreter on host Linux 

if debug:
  directory = "ks"
  directory = "noordwijk"
  location = "Noordwijk"
  segments = 1

else:
  # Get args from command line
  parser = argparse.ArgumentParser(description='Tool to create segment files and spectrograms from large audio files')
  parser.add_argument("--dir", help="Name of directory to parse audio files from, relative to _source_audio. (string, required)", required=True)
  parser.add_argument("--segments", help="How many segments to generate. Give 0 to parse all. (int, required)", required=True)
  parser.add_argument("--location", help="Unique location name, used as a location id. (string, required)", required=True)

  args = parser.parse_args()
  directory = args.dir
  segments = int(args.segments)
  location = args.location

# Todo: tbd: Check that dir name contains locality? To avoid errors.

# Todo: check if directory/data (case-sensitivity?) exists and contains wav files, or raise error

# Todo: good place to define path structure?
path = "/_source_audio/" + directory + "/Data"

audioFileList = file_helper.getAudioFileList(path)

# Get metadata for the file
# Todo: move this to last, so that error will prevent it from running

db = loxia_database.db()

# SESSION
# Todo: tbd: What to do if save directory handled twice?
sessionData = { "_id": directory, "directory": directory, "location": location }
db.saveSession(sessionData)

# FILES
for filePath in audioFileList:

  # Todo: tbd: What to do if save file handled twice?
  # Save file
  fileData = file_helper.parseFile(filePath)
  # File name is not necessarily unique, e.g. when multiple recorders start at the same time. Therefore need to include session to the id.
  fileData["_id"] = directory + "__" + fileData.get("fileName")

  db.saveFile(fileData)

  # SEGMENTS
  # Create and loop segments

  # Split into segments and generate spectrograms
  #split_and_spectro.parseFile(file, "/_exports/", segments)

