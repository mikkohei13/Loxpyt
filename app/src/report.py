
import time
import datetime

class report():

  def __init__(self):
    self._timeStart = int(time.time())
    self._counterPositive = 0
    self._counterNegative = 0

    self._html = """<!DOCTYPE html>
  <html lang="fi" class="no-js">
  <head>
    <meta charset="UTF-8">
    <title>Loxpyt Report</title>
    <link rel='stylesheet' href='../styles.css' media='all' />
  </head>
  <body>
    """

  def addPositiveSegment(self, spectroFilename, audioFilename, score):
    score = str(score)
    self.addHtml("<div class='segment'>")
    self.addSpectro(spectroFilename)
    self.addAudio(audioFilename)
    self.addHtml("<p class='score'>score " + score + "</p>")
    self.addHtml("</div>")

    self._counterPositive = self._counterPositive + 1 # TODO: shorthand / append?


  def addAudio(self, segment):
    self._html += """
    <figure>
      <figcaption>""" + segment + """</figcaption>
      <audio
          controls
          src='""" + segment + """'>
      </audio>
    </figure>
    """

  def addSpectro(self, segment):
    self._html += "<img src='" + segment + "'>\n"


  def addHtml(self, addedHtml):
    self._html += addedHtml + "\n"


  def addNegativeSegment(self, score):
    self.addHtml(str(score) + " / ")
    self._counterNegative = self._counterNegative + 1 # TODO: shorthand / append?


  def saveFile(self, baseFilePath):
    timeEnd = int(time.time())
    timeElapsed = str(timeEnd - self._timeStart)

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    total = str(self._counterPositive + self._counterNegative)

    self._html += "<p>" + str(self._counterPositive) + " positives, " + str(self._counterNegative) + " negatives, total " + total + "</p>"
    self._html += "<p>End of report / " + date + " UTC / Elapsed " + timeElapsed + " s</p>"
    self._html += "</body></html>"

    filePath = baseFilePath + "_report.html"
    file = open(filePath, "w+")
    file.write(self._html)
    file.close()