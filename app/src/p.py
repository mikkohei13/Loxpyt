
import predict_helper
import file_helper


# test_20190506-07-Ks-SM4

directory = "test_20190506-07-Ks-SM4"

# TODO later: Handle only one night at a time, allow selecting which night using param

print("Start")

threshold = 0.5
baseFilePath = "../../_exports/" + directory + "/"
# print(baseFilePath + "\n")

# TODO: ordered dict in function?
segmentsDict = file_helper.getSegmentDict(baseFilePath)
#print("\n".join(segments))

# Loop segments
limit = 5
i = 0

for segment, segmentBasePath in segmentsDict.items():
  segmentPngPath = segmentBasePath + ".png"
#  print(segmentPngPath + " " + segment + " \n")

  score = predict_helper.predict(segmentPngPath, segment)
#  print(predictionDict)

  if (score >= threshold):
    print(segment + " " + str(score) + "\n")

  # ELSE TODO later: print chart of activity through the night. plane the purpose & implementation.
  # ELSE delete PNG & MP3


  i = i + 1
  if i >= limit:
    break
#  print("\n")
#  predict_helper.predict(baseFile)



