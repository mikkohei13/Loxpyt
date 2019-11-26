

import os

def getAudioFileList(directory):
  audioFileList = []
  objects = os.listdir(directory)
  print(objects)
  for name in objects:
    if name.lower().endswith(".wav"):
      audioFileList.append(directory + "/" + name)

  return tuple(audioFileList)

# -------------------------------------------------------

print("Test")
#getAudioFileList("/_source_audio/noordwijk/Data")

# fl = getAudioFileList("/_source_audio/noordwijk/Data")
# print(fl)

# -------------------------------------------------------


from PIL import Image 
  
# Opens a image in RGB mode 
# 908 x 640 px

im = Image.open(r"/_exports/test.png")
width, height = im.size

newWidth = 900
newHeight = 595 # about 93 % of original

left = 0
top = height - newHeight
right = width
bottom = height

im_cropped = im.crop((left, top, right, bottom)) 

newsize = (newWidth, newHeight) 
im_resized = im_cropped.resize(newsize) 

im_resized.save("/_exports/cropped.png") 

# "/_exports/cropped.png"
