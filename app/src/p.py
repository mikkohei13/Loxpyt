
import predict_helper
import file_helper
import report_helper

# test_20190506-07-Ks-SM4

directory = "test_20190506-07-Ks-SM4"

# TODO: Design flow. User gives dir name as param. System creates segments to _analysis/sourcedirname_analysistime, predicts, and deletes those below threshold, and creates html report.

# TODO later: Handle only one night at a time, allow selecting which night using param

print("Start\n")
html = ""

# TODO: source dir from command line

threshold = 0.5
baseFilePath = "../../_analysis/" + directory + "/"
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
    segmentPrint = segment + " " + str(score) + "\n"
    print(segmentPrint) # debug
    html += segmentPrint
    html += report_helper.audioEmbed(segment)
    html += report_helper.spectrogram(segment)    

  # ELSE delete PNG & MP3

  i = i + 1
  if i >= limit:
    break
#  print("\n")
#  predict_helper.predict(baseFile)


report_helper.saveFile(html, baseFilePath)


print("End\n")

