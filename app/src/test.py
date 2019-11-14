
import os

directory = "./../../_source_audio/noordwijk"
for root, dirs, files in os.walk(directory):
  for name in files:
    if name.lower().endswith(".wav"):
      print(directory + "/" + name)

