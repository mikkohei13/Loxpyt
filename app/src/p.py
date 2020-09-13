
import predict_helper
import file_helper


# test_20190506-07-Ks-SM4

directory = "test_20190506-07-Ks-SM4"

print("Start")

baseFilePath = "../../_exports/" + directory + "/"
# print(baseFilePath + "\n")

segments = file_helper.getSegmentList(baseFilePath)
#print("\n".join(segments))

# Loop segments
limit = 5
i = 0

for segment in segments:
  segmentFilePath = segment + ".png"
  print(segmentFilePath)

  print(segment + " \n")
  predictionJson = predict_helper.predictAnimal(segmentFilePath, segment)
  print(predictionJson)

  i = i + 1
  if i >= limit:
    break
#  print("\n")
#  predict_helper.predict(baseFile)



