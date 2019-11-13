

# Usage

After adding pip requirements to requirements.txt, rebuild Docker image with:

  docker-compose up --build

Terminal to container:

  docker exec -ti loxia_web bash

Handle audio file:

  cd /app/src/
  python3 audiofile_handler.py --segments 1 --file /_source_audio/noordwijk/5DB0E3A4.WAV




# Tbd

- Should we adjust NFTT (+ noverlap) to have same length for each window? Yes, so that each image is same width, despite different sampling rates. 
  - Rule of thumb: 10-50 ms / window is usually good
  - My tests: c. 15 ms / window seems clearest
  - For NFTT "A power 2 is most efficient"


# Todo


- Backup of database, automatic whenever ...
- Conversion
  - Organize export files so that each session (night) is in its own dir. Do this when you know how the conversions will eventually be done (manually per night using terminal command, so that there would be no need to handle errors automatically).
  - Issues:
    - Avoid errors when typing the command manually.
    - Make it easy to change the export path during development

- Spectrogram
  - Instead of fitting spec to pixel dimensions, calculate size using NFTT & noverlay?
  - Fix file dimensions pixel-perfect?
  - Should not scale colors of each plot separately for AI?
  - More contrast for higher amplitudes? https://towardsdatascience.com/getting-to-know-the-mel-spectrogram-31bca3e2d9d0
  - Greyscale? https://jakevdp.github.io/PythonDataScienceHandbook/04.07-customizing-colorbars.html
- Audio
  - Limit all to same freq (~16 kHz)
  - All to mono


- Where time data: start time, day 
- Where metadata: recorded model, recorder id, original filename, original path, conversion datetime, peak amplitude

# Spectrograms

## pylab

+ some options available

## scipy

- could not get it to work properly

## pyspectrum

+ nice colors
+ seems sharp
- no options for
  - remove legend etc.
  - remove frames
  - adjust size
- slow

# Data

Session (can be 1...n nights)
- Session id, reconstructable [string]
- Directory name [string]
- Location code (acts as location id) [string]

Source file
- Source file uuid, reconstructable [string]
- Session id uuid
- Directory name & filename (must not change this afterwards) [string] DONE
- Device id [string] DONE
- Device type [string]
- Start datetime, normalized, from file meta, using function for each device [datetime/string]
  - Audiomoth: UTC, winter/summer?
  - SM4: Finnish summer time
- Night id (first day yyyymmdd), calculated from datetime [int]
- Length in seconds [int]
- File info [array]
- Conversion datetime [datetime/string]

Segment file
- Source file uuid, dumb [string]
- Segment file uuid [string]
- Segment number [int]
- Segment size in seconds [int]
- Segment offset in seconds [int]
- Peak amplitude [int]?

Segment annotation data
- Annotation uuid, dumb
- Segment file uuid, dumb [string]
- Annotation datetime [string]
- Annotator, MA id [string]
- Birds [boolean]
- Taxa [array]
  - taxon [string] (or use MX id's?)
  - individual count [int]
  - sound count [int]
  - sound type [string]

Segment AI data TBD later
- AI id uuid
- Segment file uuid
- AI run id manually
- Probability for bird | no bird



How to find the original file later, if needed?
- If path remains - use value directly
- If path changed - find the file based on datetime and other info. Often only datetime is enough?


# Logic

- Convert bunch of files to 10 sec segments
  - Save data to database (mysql/nosql?)
  - Calculate filenames, so that files can potentially be kept in same directory, and ordered reasonably
    - device id + datetime normalized + segment
  - Save wavs
  - Save spectros

- Annotate
  - List of nights, group by device id, night id
  - One night
  ...

- Train AI
  - make spectros with different settings (decrease/increase volume) and augmentation



# Links

https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html

https://stackoverflow.com/questions/33175184/the-arrays-returned-from-pylab-specgram-dont-seem-to-add-up-to-the-image-could

https://stackoverflow.com/questions/44787437/how-to-convert-a-wav-file-to-a-spectrogram-in-python3
