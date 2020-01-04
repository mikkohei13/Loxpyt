
def combineLists(segments, annotations):
  segmentsArr = {}
  for item in segments:
    segmentsArr[item["_id"]] = item["count"]

  annotationsArr = {}
  for item in annotations:
    annotationsArr[item["_id"]] = item["count"]

  combinedArr = {}
  
  for key, value in segmentsArr.items():
    combinedArr[key] = {}
    combinedArr[key]["segments"] = value
    if key in annotationsArr:
      combinedArr[key]["annotations"] = annotationsArr[key]

  return combinedArr

