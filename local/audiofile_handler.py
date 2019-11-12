
import argparse
import split_and_spectro

parser = argparse.ArgumentParser(description='Tool to create segment files and spectrograms from large audio files')
parser.add_argument("--file")
parser.add_argument("--segments")

args = parser.parse_args()
audioFullPath = args.file
segments = int(args.segments)

# --segments 1 --file audio/noordwijk/5DB0E3A4.WAV
# --segments 1 --file audio/ks/HLO10_20191102_022600.wav

split_and_spectro.parseFile(audioFullPath, "exports/", segments)
