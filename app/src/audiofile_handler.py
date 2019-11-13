#
# Example usage: see readme.md
#


import argparse
import split_and_spectro
import pyexifinfo

import loxia_database

debug = True # get input from this file AND use interpreter on host Linux 

if debug:
  file = "./../../_source_audio/ks/HLO10_20191102_022600.wav"
  file = "./../../_source_audio/noordwijk/5DB0E3A4.WAV"
  segments = 1

else:
  # Get args from command line
  parser = argparse.ArgumentParser(description='Tool to create segment files and spectrograms from large audio files')
  parser.add_argument("--file", help="Path to wav file (string, required)", required=True)
  parser.add_argument("--segments", help="How many segments to generate (int, required)", required=True)
  #parser.add_argument("--deviceid", help="Id of the recording device (string, required)", required=True)

  args = parser.parse_args()
  file = args.file
  segments = int(args.segments)
  #deviceId = args.deviceid

# todo: check if file exists

# Get metadata for the file
metadata = pyexifinfo.parseFile(file)

db = loxia_database.db()

db.saveSession(metadata)


# Split into segments and generate spectrograms
#split_and_spectro.parseFile(file, "/_exports/", segments)

# Save into database
