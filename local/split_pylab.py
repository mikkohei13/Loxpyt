from pydub import AudioSegment
import wave
import pylab

from PIL import Image, ImageChops

# -------------------------------------------------------------------------------------------
# Audio functions

# Crop whitespace around the image, based on colour of top right (?) pixel
def trim(im):
  bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
  diff = ImageChops.difference(im, bg)
  diff = ImageChops.add(diff, diff, 2.0, -100)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)


# https://github.com/cgoldberg/audiotools/blob/master/visualization/spectrogram_matplotlib.py
def graph_spectrogram(wavFilename, spectroFilename):
  sound_info, frame_rate = get_wav_info(wavFilename)
  pylab.figure(num=None, figsize=(10, 7))

  # Spectrogram settings
  # Cleaner, less contrast, visually good noverlap value: 512 / 2
  # Noisier, sharper, more contrast: 1024 / 8

  NFTT = 512
  noverlap = NFTT / 2
  cmap = "viridis" # jet | viridis | RdBu | cubehelix

  pylab.specgram(sound_info, Fs=frame_rate, NFFT=NFTT, noverlap=noverlap, scale_by_freq=False, cmap=cmap)

  # Remove chart axis etc.
  pylab.tight_layout() # Or possibly in new versions use: 
  pylab.axis('off')

  # Saves temp version - todo: send the image directly to trimmer?
  pylab.savefig(spectroFilename)

  # Remove whitespace  
  im = Image.open(spectroFilename)
  im = trim(im)
  im.save(spectroFilename)


def get_wav_info(wavFilename):
  wav = wave.open(wavFilename, 'r')
  frames = wav.readframes(-1)
  sound_info = pylab.fromstring(frames, 'int16')
  frame_rate = wav.getframerate()
  wav.close()
  return sound_info, frame_rate

# -------------------------------------------------------------------------------------------
# Main

audioDir = "audio/noordwijk/"
audioFilename = "5DB0E3A4.WAV"

# audioDir = "audio/ks/"
# audioFilename = "HLO10_20191102_022600.wav"

audioFullPath = audioDir + audioFilename

newAudio = AudioSegment.from_wav(audioFullPath)

# Slicing settings
exportDir = "exports/"
limit = 360
length = 10 # sec

limit = 1 #DEBUG

t1 = 0
t2 = t1 + length
i = 0

while (i < limit):

  # Create wav segment
  iZeros = str("{:05d}".format(i))
  wavFilename = exportDir + "segment" + iZeros + "_" + str(t1) + "-" + str(t2) + ".wav"
  spectroFilename = wavFilename + ".png"

  segment = newAudio[(t1 * 1000):(t2 * 1000)]

  # Break if no more full segments
  if segment.duration_seconds < (length / 1000):
    print("Reached the end")
    break

    # Save wav file
  segment.export(wavFilename, format="wav")

  # Create spectrogram
  # NOTE: PRESUMES MONO

  # Saves the spectro image to disk
  graph_spectrogram(wavFilename, spectroFilename)

  # Finish this loop
  t1 = t2
  t2 = t2 + length
  i = i + 1

  print("Segment " + str(i) + " done")  

# End while

print("Finished")
