from pydub import AudioSegment
import wave
import pylab
import os
from PIL import Image, ImageChops


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
  pylab.tight_layout() # Todo: Will this work in new versions of pylab? 
  pylab.axis('off')

  # Saves temp version - todo: send the image directly to trimmer?
  pylab.savefig(spectroFilename)

  # Remove whitespace  
  im = Image.open(spectroFilename)
  im = trim(im)
  im.save(spectroFilename)

# Info
# Returns audio data and info
def get_wav_info(wavFilename):
  wav = wave.open(wavFilename, 'r')
  frames = wav.readframes(-1)
  sound_info = pylab.fromstring(frames, 'int16')
  frame_rate = wav.getframerate()
  wav.close()
  return sound_info, frame_rate


### MAIN PARSER GENERATOR #########################################################

# Parse single audio file
def parseFile(audioFilePath, exportDir, directory, segments = 1, segmentLengthSeconds = 10):

  newAudio = AudioSegment.from_wav(audioFilePath)

  exportDirPath = exportDir + "/" + directory + "/"
  segmentStartSeconds = 0
  segmentEndSeconds = segmentStartSeconds + segmentLengthSeconds
  segmentNumber = 0

  while (segmentNumber < segments):

    # Create names
    segmentNumberLeadingZeroes = str("{:05d}".format(segmentNumber))

    baseAudioFilename = segmentNumberLeadingZeroes + "_" + str(segmentStartSeconds) + "-" + str(segmentEndSeconds) + ".wav"
    tempAudioFilename = baseAudioFilename +  ".wav"
    spectroFilename = tempAudioFilename + ".png"
    finalAudioFilename = baseAudioFilename + ".mp3"

    # Todo ABBA tempAudioFilename is not a path, needs exportDirPath

    # Create wav segment
    segment = newAudio[(segmentStartSeconds * 1000):(segmentEndSeconds * 1000)]

    # Break if no more full segments
    if segment.duration_seconds < (segmentLengthSeconds / 1000):
      print("Reached the end")
      break

      # Save wav file
    segment.export(exportDirPath + tempAudioFilename, format="wav")

    # Create spectrogram
    # NOTE: PRESUMES MONO
    # Todo: stereo to mono

    # Saves the spectro image to disk
    graph_spectrogram(exportDirPath + tempAudioFilename, exportDirPath + spectroFilename)

    # Save mp3 file to disk and remove wav
    # Todo: exclude wav file extension from mp3 & spectro
    segment.export(exportDirPath + tempAudioFilename + ".mp3", format="mp3")
    os.remove(exportDirPath + tempAudioFilename)

    # Finish this loop
    segmentStartSeconds = segmentEndSeconds
    segmentEndSeconds = segmentEndSeconds + segmentLengthSeconds
    segmentNumber = segmentNumber + 1

    # Create metadata to be returned
    # Todo: parametrize file names
    segmentMetadata = {}
    segmentMetadata['finalAudioFilename'] = finalAudioFilename
    segmentMetadata['spectroFilename'] = spectroFilename
    segmentMetadata['segmentNumber'] = segmentNumber
    segmentMetadata['segmentStartSeconds'] = segmentStartSeconds
    segmentMetadata['segmentEndSeconds'] = segmentEndSeconds
    segmentMetadata['segmentLengthSeconds'] = segmentLengthSeconds
    segmentMetadata['segmentId'] = directory
    
    print("Segment " + str(segmentNumber) + " done")

    yield segmentMetadata

  # End while

  # Todo: return something useful?
#  return True

# End function