from pydub import AudioSegment
import wave
import pylab
import os
from PIL import Image, ImageChops
import math

import time # debug
startTime = time.time()

def prof(position, startTime):
  now = time.time()
  elapsed = now - startTime
  print("PROFILER: " + position + " " + str(elapsed));


### HELPER FUNCTIONS #########################################################

def createDir(dirPath):
  if not os.path.exists(dirPath):
    os.makedirs(dirPath)
  return True


### AUDIO HANDLING FUNCTIONS #########################################################

# Cropper
# Crop whitespace around the image, based on colour of top right (?) pixel, and save to disk
def trim(im):
  bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
  diff = ImageChops.difference(im, bg)
  diff = ImageChops.add(diff, diff, 2.0, -100)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)


# Spectro
# Creates a spectrogram and saves to disk
# https://github.com/cgoldberg/audiotools/blob/master/visualization/spectrogram_matplotlib.py
def graph_spectrogram(wavFilename, spectroFilename, maxFrequency = 16000):
  prof("graphSpectrogram start", startTime)
  sound_info, frame_rate = get_wav_info(wavFilename)

  prof("sound_info", startTime)
  # Spectrogram settings for 900 px wide spectrograms:
  #  pylab.figure(num=None, figsize=(10, 7)) # Size in inches, 1. version
  # Cleaner, less contrast, visually good noverlap value: 512 / 2
  # Noisier, sharper, more contrast: 1024 / 8
  #  NFTT = 512

  # Noordwijk audio files, 32 kHz
  # target: 10 sec = 450px
  # noverlap 50 %
  # NFTT = 32000 * 10 / 450 * 2 
  # = 1422

  segmentLengthSeconds = 10
  spectroWidth = 450 # If this is changed, also change figsize below
  noverlapRatio = 2
  NFTT = math.floor( frame_rate * segmentLengthSeconds / spectroWidth * noverlapRatio )

  noverlap = NFTT / noverlapRatio
  cmap = "gray" # jet | viridis | RdBu | cubehelix | gray
  prof("settings", startTime)

  # Size of the spectrogram, adjusted for margings added by pylab
  pylab.figure(num=None, figsize=(45.8, 32.6)) 
  prof("figure", startTime)
  pylab.specgram(sound_info, Fs=frame_rate, NFFT=NFTT, noverlap=noverlap, scale_by_freq=False, cmap=cmap)
  prof("specgram", startTime)

  # Remove chart axis etc.
  pylab.tight_layout() # Todo: Will this work in new versions of pylab? 
  pylab.axis('off')

  pylab.axis(ymin = 0, ymax = maxFrequency)
  prof("layout", startTime)

  # Saves temp version - todo: send the image directly to trimmer?
  pylab.savefig(spectroFilename, dpi = 10)
  prof("save temp image", startTime)
  pylab.cla() # Without this, looping figures will get really slow.
  prof("cla temp image", startTime)
  pylab.close()
  prof("close temp image", startTime)

  # Remove whitespace  
  im = Image.open(spectroFilename)
  im = trim(im)
  im.save(spectroFilename)
  im.close()
  prof("final", startTime)


# Info
# Returns audio data and info
def get_wav_info(wavFilename):
  wav = wave.open(wavFilename, 'r')
  frames = wav.readframes(-1)
  sound_info = pylab.fromstring(frames, 'int16')
  frame_rate = wav.getframerate()
  wav.close()
  print("Frame rate: " + str(frame_rate))
  return sound_info, frame_rate


### MAIN PARSER GENERATOR #########################################################

# Parse single audio file
def parseFile(sourceAudioFilePath, exportDir, sessionDir, sourceAudioFileName, segments = 1, segmentLengthSeconds = 10):
  prof("parseFile start", startTime)

  # Todo: More elegant way to do this?
  if 0 == segments:
    segments = 10000

  # Todo: from mp3
  newAudio = AudioSegment.from_wav(sourceAudioFilePath)
  prof("newAudio", startTime)

  exportDirPath = exportDir + "/" + sessionDir + "/"
  segmentStartSeconds = 0
  segmentEndSeconds = segmentStartSeconds + segmentLengthSeconds
  segmentNumber = 0

  createDir(exportDirPath)

  while (segmentNumber < segments):
    prof("while", startTime)

    # Create names
    segmentNumberLeadingZeroes = str("{:05d}".format(segmentNumber))

#    baseAudioFilename = segmentNumberLeadingZeroes + "_" + str(segmentStartSeconds) + "-" + str(segmentEndSeconds)
    baseAudioFilename = sourceAudioFileName + "." + segmentNumberLeadingZeroes
    tempAudioFilename = baseAudioFilename +  ".wav"
    spectroFilename = baseAudioFilename + ".png"
    finalAudioFilename = baseAudioFilename + ".mp3"

    # Create wav segment
    segment = newAudio[(segmentStartSeconds * 1000):(segmentEndSeconds * 1000)]
    prof("segment", startTime)

    # Break if no more full segments
    if segment.duration_seconds < (segmentLengthSeconds / 1000):
      print("Reached the end")
      break

      # Save wav file
    segment.export(exportDirPath + tempAudioFilename, format="wav")
    prof("wav export", startTime)

    # Create spectrogram
    # Saves the spectro image to disk
    graph_spectrogram(exportDirPath + tempAudioFilename, exportDirPath + spectroFilename)
    prof("spectro", startTime)

    # Save mp3 file to disk and remove wav
    # Todo: exclude wav file extension from mp3 & spectro
    segment.export(exportDirPath + finalAudioFilename, format="mp3")
    os.remove(exportDirPath + tempAudioFilename)
    prof("mp3 export", startTime)

    # Finish this loop
    segmentStartSeconds = segmentEndSeconds
    segmentEndSeconds = segmentEndSeconds + segmentLengthSeconds
    segmentNumber = segmentNumber + 1

    # Create metadata to be returned
    # Todo: parametrize file names
    segmentMetadata = {}
    segmentMetadata['baseAudioFilename'] = baseAudioFilename
    segmentMetadata['finalAudioFilename'] = finalAudioFilename
    segmentMetadata['spectroFilename'] = spectroFilename
    segmentMetadata['segmentNumber'] = segmentNumber
    segmentMetadata['segmentStartSeconds'] = segmentStartSeconds
    segmentMetadata['segmentEndSeconds'] = segmentEndSeconds
    segmentMetadata['segmentLengthSeconds'] = segmentLengthSeconds
    
    print("Segment " + str(segmentNumber) + " done")
    prof("meta", startTime)

    yield segmentMetadata

  # End while

  # Todo: return something useful?
#  return True

# End function