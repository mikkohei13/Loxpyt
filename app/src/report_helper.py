
def css():
  # refer to css file above one folder level -> can update all reports with one file retroactively
  x = 1;

def audioEmbed(segment):
  html = """
  <figure>
    <figcaption>""" + segment + """</figcaption>
    <audio
        controls
        src='""" + segment + """'>
    </audio>
  </figure>
  """
  return html

def spectrogram(segment):
  html = "<img src='" + segment + "'>\n"
  return html

def saveFile(html, baseFilePath):
  filePath = baseFilePath + "_report.html"
  file = open(filePath, "w+")
  file.write(html)
  file.close()