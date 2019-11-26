

# Usage

## Setup (not tested)

- Install Docker
- Clone this repository
- Create directories for audio files:
  - _exports
  - _source_audio
- Place audio (.wav) files to _source_audio/{DIRECTORY_NAME}/Data
- Start containers:
  - `docker-compose up --build`
- Terminal to container:
  - `docker exec -ti loxia_web bash`
- Handle audio file inside the container:
  - `cd /app/src/`
  - `python3 audiofile_handler.py --dir DIRECTORY_NAME --location LOCATION_ID`
- Annotate at localhost
- TODO...


# Tbd

- Check what other annotated data is available, how long are the files, what format are they, what's the frequency, what kind of tags ...
  - https://zenodo.org/record/1298604
  - https://zenodo.org/record/1208080
- Are upserts needed or allowed?
  - Needed: debugging
  - Allowed: production for most entities
  - Not allowed: when segments have already been annotated, since this could break the AI training process
- How to handle when nocmig ends and morning begins? 
  - A: Manually by deciding when processing should stop, and providing that info as processing parameter (relative to file time).
- How to avoid hearing issues when sound starts/stops?
  - Option: By playing back continuously and tag with "nobirds", unless user interrupts
- Should this be refactored so that file metadata that is similar within session goes to session collection in deb? Things like recorder model and settings?
  - A: No, complicates code (at least at this point) and does not bring new functionality
- Should we use segment number or segment start time in segment_id?
  - A: Segment number. Using segment start time would not allow having segments with different lengths in the same system, as there would be id collisions anyway. If segment lenght is changed, a fresh database and _exports directory are needed.

# Todo

- Todo's in the files
- Why spectro creation is slo slow?
- UI:
  - List of sessions and files to annotate
  - All buttons -> keywords
  - Warning if anotation already exists?
  - Preload next spectro & audio
- CHECK Are all spectrograms same size, despite of source bitrate?
- Backup mongodb, when? docker-compose down?
- CHECK Refactor split and spect: var names, files in subdirs, parametrize path structure?
- CHECK Double-check the time setting in SM4, is it UTC+3? And is the time value in metadata correct?
- Databasing: what should be case-insensitive? Location id? Mongodb _id's? How could the case change? (typing error on terminal, dir or file name change...?)
  - DONE: location id always lowercased
- Conversion
- Spectrogram
  - Should not scale colors of each plot separately for AI? Can this be prevented in pylab?
  - More contrast for higher amplitudes? How?
  - Greyscale? https://jakevdp.github.io/PythonDataScienceHandbook/04.07-customizing-colorbars.html
- Audio

- Where time data: start time, day 
- Where metadata: recorded model, recorder id, original filename, original path, conversion datetime, peak amplitude

# Spectrograms

- Calculating NFTT so that the spectro is close to the desired size seems to produce clearest results, despite pylab's instruction to have "A power 2 is most efficient" for the NFTT. This avoids blurring due to image resizing.
  - With 32 KhZ recording and 450 px wide 10 sec segments this means 22 ms segments and NFTT of ~1400 
- MR: Rule of thumb: 10-50 ms / window is usually good
- Youtube: "standard" is 25 ms window size and 10 ms step (= 15 ms noverlap)


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
- Id [string]: directory DONE
- Directory name [string] DONE
- Location code (acts as location id) [string] DONE
- Entry datetime [datetime/string] DONE

Source file
- Id [string]: directory/sourceFilename DONE 
- Session id DONE
- Raw file metadata DONE
- Directory name (must not change this afterwards) [string] SAME AS SESSION_ID
- File name (must not change this afterwards) [string] DONE
- Device id [string] DONE
- Device model [string] DONE
- Device version [string] DONE
- Start datetime, normalized, from file meta, using function for each device [datetime/string] DONE
- Night id (first day yyyymmdd), calculated from datetime [int] --TODO--
- Length in seconds [int] DONE
- Entry datetime [datetime/string] DONE

Segment
- Id [string]: directory/sourceFilename/baseAudioFilename DONE
- Segment number [int] DONE
- Segment size in seconds [int] DONE
- Segment offset in seconds [int] DONE
- Peak amplitude [int]? - not needed? --TODO--
- Entry datetime [datetime/string] DONE

Annotation
- Id [string]: directory/sourceFilename/baseAudioFilename --TODO--
- Tags [array of strings] --TODO--
- Observations --TODO--
- Entry datetime [datetime/string] 


Segment AI data TBD later
- AI id uuid
- Segment file uuid
- AI run id manually
- Probability for bird | no bird



How to find the original file later, if needed?
- If path remains - use value directly
- If path changed - find the file based on datetime and other info. Often only datetime is enough?


# Logic

Annotate

- Sessions
- Files / Segments
- Get data of single segment
- Open
  - spectro
  - audio
  - next spectro in the background, async
  - next audio in the background, async
- Display player & scale to spectro width?
- Autoplay audio
- Display
  - file & segment info
  - buttons
  - fields for observations (taxon, calls x3-4)
  - notes
- Parse field data to json
- POST json to API
- API
  - Get POST
  - Sanitize
  - Save to db, appending to existing
  - Respond with code
- When ok response code
  - Open new data

Batch annotate?
- Command line tool to add data to range of annotations

Train AI

- Make spectros with different settings (decrease/increase volume) and augmentation


# AI

## How to annotate the files

Primary
- no species TRAIN NEGATIVE
- uncertain, skip (= leave out from training)

Birds:
- nocmig, one (Single or few sounds passes by - nfc's) TRAIN
- nocmig, many (Multiple similar sounds passes by - Melnig, Clahye, Braleu...) TRAIN
- wandering, one (Single or few sounds passes by, but not interpreted as nocmig - Scorus) TRAIN
- wandering, many (rare case?) MAYBE TRAIN
- stationary, one (Few distincg sounds - Turpil, Turmer, first singer...) - TRAIN
- stationary, many (Continuous sounds - morning chorus) MAYBE TRAIN
- owl MAYBE TRAIN

Mammals:
- bat NO TRAIN
- mammal MAYBE TRAIN
- mystery animal MAYBE TRAIN

Other, specify in notes

Disturbance
- single sound (drops, cracks, etc.)
- rain
- wind
- rustle
- human
- plane
- vehicle

Observations
- Species
- NFC count
- Individual count estimate
- Flock count estimate
- Notes

Notes


# Links

https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html

https://stackoverflow.com/questions/33175184/the-arrays-returned-from-pylab-specgram-dont-seem-to-add-up-to-the-image-could

https://stackoverflow.com/questions/44787437/how-to-convert-a-wav-file-to-a-spectrogram-in-python3
