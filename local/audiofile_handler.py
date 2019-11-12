
import argparse
import split_and_spectro
import pyexifinfo

parser = argparse.ArgumentParser(description='Tool to create segment files and spectrograms from large audio files')
parser.add_argument("--file", help="Path to wav file (string, required)", required=True)
parser.add_argument("--segments", help="How many segments to generate (int, required)", required=True)
parser.add_argument("--deviceid", help="Id of the recording device (string, required)", required=True)

args = parser.parse_args()
file = args.file
segments = int(args.segments)
deviceId = args.deviceid

# python3 audiofile_handler.py --segments 1 --file audio/noordwijk/5DB0E3A4.WAV --deviceid TEST
# python3 audiofile_handler.py --segments 1 --file audio/ks/HLO10_20191102_022600.wav --deviceid TEST

# todo: check if file exists

metadata = pyexifinfo.parseFile(file)

split_and_spectro.parseFile(file, "exports/", segments)
