
import time
import datetime
import json

class report():

  def __init__(self, directoryPath):

    self._filePath = directoryPath + "_report.html"
    self._timeStart = int(time.time())
    self._counterPositive = 0
    self._counterNegative = 0

    html = """<!DOCTYPE html>
  <html lang="fi" class="no-js">
  <head>
    <meta charset="UTF-8">
    <title>Loxpyt Report</title>
    <link rel='stylesheet' href='../styles.css' media='all' />
  </head>
  <body>
    """

    # Create file
    f = open(self._filePath, "w+")  # open file in append mode
    f.write(html)
    f.close()


  def appendLine(self, html):
    file = open(self._filePath, "a")
    file.write(html + "\n")
    file.close()


  def addFile(self, fileData):
    print(fileData) # Debug

    html = "<h3>"
    html += fileData['fileName'] + ", start UTC " + fileData['recordDateStartUTC'].strftime("%Y-%m-%d %H:%M:%S")
    html += "</h3>"

    self.appendLine(html) # debug


  def addPositiveSegment(self, segmentMeta, score):
    score = str(score)
    scoreClass = score[0:3].replace(".", "")

    self.appendLine("<div class='segment s" + scoreClass + "'>")
    self.addSpectro(segmentMeta["spectroFilename"])
    self.addAudio(segmentMeta["finalAudioFilename"])

#    segmentStartUTCstr = segmentMeta["segmentStartUTC"].__str__()
    segmentStartUTCstr = segmentMeta["segmentStartUTC"].strftime("%H:%M:%S")

    self.appendLine("<p class='caption'><em>UTC " + segmentStartUTCstr + ",</em> <strong>score " + score + "</strong></p> \n</div>")

    self._counterPositive = self._counterPositive + 1 # TODO: shorthand / append?


  def addAudio(self, segment):
    html = """
    <figure>
      <figcaption>""" + segment + """</figcaption>
      <audio
          controls
          src='""" + segment + """'>
      </audio>
    </figure>
    """
    self.appendLine(html)


  def addSpectro(self, segment):
    html = "<img src='" + segment + "'>\n"
    self.appendLine(html)


  def addHtml(self, html):
    self.appendLine(html)


  def addNegativeSegment(self, score):
    self.appendLine(str(score) + " / ")
    self._counterNegative = self._counterNegative + 1 # TODO: shorthand / append?


  def finalize(self):
    timeEnd = int(time.time())
    timeElapsed = timeEnd - self._timeStart

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    total = self._counterPositive + self._counterNegative

    timeElapsedPerSegment = timeElapsed / total

    html = ""
    html += "<p>" + str(self._counterPositive) + " positives, " + str(self._counterNegative) + " negatives, total " + str(total) + "</p>\n"
    html += "<p>End of report / " + date + " UTC / Elapsed " + str(timeElapsed) + " s, " + str(timeElapsedPerSegment) + " s per segment</p>\n"
    html += "</body></html>"
    self.appendLine(html)

