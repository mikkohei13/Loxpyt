
import split_and_spectro

audioDir = "audio/noordwijk/"
audioFilename = "5DB0E3A4.WAV"

# audioDir = "audio/ks/"
# audioFilename = "HLO10_20191102_022600.wav"

audioFullPath = audioDir + audioFilename

split_and_spectro.parseFile(audioFullPath, "exports/", 101)
