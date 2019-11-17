

# Usage

After adding pip requirements to requirements.txt, rebuild Docker image with:

  docker-compose up --build

Terminal to container:

  docker exec -ti loxia_web bash

Handle audio file:

  cd /app/src/
  python3 audiofile_handler.py --segments 1 --file /_source_audio/noordwijk/5DB0E3A4.WAV




# Tbd

- Check what other annotated data is available, how long are the files, what format are they, what's the frequency, what kind of tags ...
- Should we adjust NFTT (+ noverlap) to have same length for each window? Yes, so that each image is same width, despite different sampling rates. 
  - Rule of thumb: 10-50 ms / window is usually good
  - My tests: c. 15 ms / window seems clearest
  - For NFTT "A power 2 is most efficient"
- Are upserts needed or allowed?
  - Needed: debugging
  - Not allowed: when segments have already been annotated, since this could break the AI training process (Todo: Set to session annotationStarted: True ?)
- How to handle when nocmig ends and morning begins? 
  - A: Manually by deciding when processing should stop, and providing that info as processing parameter (relative to file time).
- How to avoid hearing issues when sound starts/stops?
  - Option: By playing back continuously and tag with "nobirds", unless user interrupts
- Should this be refactored so that file metadata that is similar within session goes to session collection in deb? Things like recorder model and settings?
  - A: No, complicates code (at least at this point) and does not bring new functionality

# Todo

- Save all segment properties, so that segments can be reconstructed afterwards if needed 
- Parametrize segment size -> file naming based on seconds from start, prefixed with zeroes
- Refactor split and spect: var names, files in subdirs, parametrize path structure?
- Stereo to mono
- Double-check the time setting in SM4, is it UTC+3? And is the time value in metadata correct?
- Id's as hashes, in case dir names are corrected? Need still to be reproducible...
- Upsert? What can be upserted? Not segments, since replacing can harm AI training?
  - DONE: session and file upserted
- Databasing: what should be case-insensitive? Location id? Mongodb _id's? How could the case change? (typing error on terminal, dir or file name change...?)
  - DONE: location id always lowercased
- Backup of database, automatic whenever ...
- Conversion
  - Organize export files so that each session (night) is in its own dir. Do this when you know how the conversions will eventually be done (manually per night using terminal command, so that there would be no need to handle errors automatically).
  - Issues:
    - Avoid errors when typing the command manually.
    - Make it easy to change the export path during development
- Next time you change the directory structure, parametrize it
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

# Dates

- UTC is standard time without daylight saving time adjustments.
- File metadata date modified cannot be trusted, it can change when file is copied?

Audiomoth:
- Comment field has time in format "22:35:00 23/10/2019 (UTC)".
  - This seems to be *start time - 3 h* give or take few minutes. Don't use this because unclear why the difference.
- File name has time encoded as 32-bit hexadecimal unix timestamp of seconds, e.g. "5DB0D594" = ?
  - Forum says this is *start time*

SM4
- File name has *start* time, e.g. "HLO10_20191102_022600"


# Data

Session (can be 1...n nights)
- Id [string] DONE
- Directory name [string] DONE
- Location code (acts as location id) [string] DONE
- Entry datetime [datetime/string]

Source file
- Id [string] DONE
- Session id DONE
- Raw file metadata DONE
- Directory name (must not change this afterwards) [string] SAME AS SESSION_ID
- File name (must not change this afterwards) [string] DONE
- Device id [string] DONE
- Device model [string] DONE
- Device version [string] DONE
- Start datetime, normalized, from file meta, using function for each device [datetime/string]
  - Audiomoth: UTC, winter/summer?
  - SM4: Finnish summer time
- Night id (first day yyyymmdd), calculated from datetime [int]
- Length in seconds [int] DONE
- Entry datetime [datetime/string]

Segment files
- Source file uuid, dumb [string]
- Segment file uuid [string] - or just use file path convention
- Segment number [int] - or just use filename convention
- Segment size in seconds [int] - or always 10 sec
- Segment offset in seconds [int] - or just use filename convention
- Peak amplitude [int]? - not needed?

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
