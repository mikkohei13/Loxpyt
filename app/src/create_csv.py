
import json

sourceFile = "../../_data/annotations.json"
targetFile = "../../_data/target_annotations.csv"

def leadingZeros(number):
  number = str(number)
  number = number.zfill(5)
  return number


def ignoreSegment(tagList):
  if "ignore" in tagList or "distortion2" in tagList or "faded" in tagList or "high-pass" in tagList:
    return True
  else:
    return False


def tagNormalizer(tagList):
  if "migrant" in tagList or "migrant-low" in tagList or "migrant-low" in tagList or "wander" in tagList or "local_individual" in tagList or "local_choir" in tagList or "owl" in tagList or "mystery" in tagList or "mammal" in tagList or "dog" in tagList or "other_animal" in tagList:
    return "bird-like"
  elif "bat" in tagList:
    return "bat"
  else:
    return "no-animal"


with open(sourceFile, "r") as infile, open(targetFile, "w") as outfile:
  for line in infile:
    dictData = json.loads(line)

    if ignoreSegment(dictData["tags"]):
      continue

    spectroFileName = "gs://spectro-1/" + dictData['file_id'] + "." + leadingZeros(dictData['segmentNumber']) + ".png"  # noordwijk/5DB12FD0.WAV.00344.png"
    tag = tagNormalizer(dictData["tags"])

    outfile.write(spectroFileName + "," + tag + "\n");



  # filter keywords, see readme for the plan

# export as csv


