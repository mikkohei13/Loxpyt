
def audioEmbed(segment):
  html = """
  <figure>
    <figcaption>""" + segment + """</figcaption>
    <audio
        controls
        src='""" + segment + """.mp3'>
    </audio>
  </figure>
  """
  return html

def spectrogram(segment):
  html = "<img src='" + segment + ".png'>\n"
  return html

def saveFile(html, baseFilePath):
  filePath = baseFilePath + "_report.html"
  file = open(filePath, "w+")
  file.write(html)
  file.close()