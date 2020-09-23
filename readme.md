
# See also

* [Annotation notes](docs/annotating.md)
* [Google AI & models](docs/google-ai.md)


# Usage


## Setup

- Install Docker & Docker-Compose
- Clone this repository
- Create directories for audio files:
  - _exports
  - _source_audio
- Place audio (.wav) files to _source_audio/{RECORDING SESSION NAME}/Data
- Start containers:
  - `docker-compose up --build; docker-compose down`
  - To rebuild images, if they are modified `docker-compose up --build; docker-compose down`


## Process files

- Terminal to container:
  - `docker exec -ti loxia_web bash`
- Handle audio file inside the container:
  - `cd /app/src/`
  - `python3 audiofile_handler.py --dir DIRECTORY_NAME --location LOCATION_ID`
- Make predictions
  - TODO: parameters
  - `python3 predict.py`


## Annotate

- Annotate at http://localhost/files
- See & manage data at http://localhost:8081/ 

- [More annotation notes](docs/annotating.md)


## Export annotations

- Export annotations using Mongo express. This creates a file of annotations with JSON document on each row.
- Remove those annotations that you dont need (if you are training an existing model)
- Save the file to _data/annotations.json
- Adjust settings in create_csv.py
- Run `create_csv.py` on your machine (not in Docker)
  - If this fails, remove any empty lines in the annotations.json file (end of the file)




# System design & Specs

- All data except annotations are upserted, so that there won't be duplicates.-
- Annotations are not upserted, because this might lose work and/or break the AI training process
- How to handle when nocmig ends and morning begins? The system should recognize alo local birds. Then user decides which segments they want to handle.
  - Due to this, cannot easily create a migration index for the night?
- File metadata (such as recorder device info) will be duplicated for each file, due to simplicity.
- All times are UTC.
- Segments are identified by an incremented integer. 
- Due to this, if segment length changes, this requires fresh database and _exports directory.


## Files

### Annotator

- ROOT app/
- main.py - Annotator Flask routers
  - src/data_helper.py - Handle segment & file data from database 

### Audio file handler

- ROOT app/src/
- audiofile_handler.py - Handles large audio files, saves data into db
  - split_and_spectro.py - Splits large files to segments, creates spectrograms
  - file_helper.py - Functions to parse audio files, e.g. getting recoding device metadata
    - wamd.py - Third-party functions to parse Wildlife Acoustics sound files
  - file_normalizer.py - Functions to normalize audio files, converts stereo to mono
  - loxia_database.py - Class to access database

### Misc

- ROOT app/src/
- create_csv.py - Converts MongoDB json files to CSV files for Google AutoML Vision 
- predict.py - Makes predictions using AI model
- api.py - TEST?


## Spectrograms

- Calculating NFTT so that the spectro is close to the desired size seems to produce clearest results, despite pylab's instruction to have "A power 2 is most efficient" for the NFTT. This avoids blurring due to image resizing.
  - With 32 KhZ recording and 450 px wide 10 sec segments this means 22 ms segments and NFTT of ~1400 
- MR: Rule of thumb: 10-50 ms / window is usually good
- Youtube: "standard" is 25 ms window size and 10 ms step (= 15 ms noverlap)


## Dates

- UTC is standard time without daylight saving time adjustments.
- File metadata date modified cannot be trusted, it can change when file is copied?

Audiomoth:
- Comment field has time in format "22:35:00 23/10/2019 (UTC)".
  - This seems to be *start time - 3 h* give or take few minutes. Don't use this because unclear why the difference.
- File name has time encoded as 32-bit hexadecimal unix timestamp of seconds, e.g. "5DB0D594" = ?
  - Forum says this is *start time*

SM4
- File name has *start* time, e.g. "HLO10_20191102_022600"


## Data model

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


### Data notes

Segment AI data TBD later
- AI id uuid
- Segment file uuid
- AI run id manually
- Probability for bird | no bird

How to find the original file later, if needed?
- If path remains - use value directly
- If path changed - find the file based on datetime and other info. Often only datetime is enough?


## Logic

### Annotation

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

Train AI
- Make spectros with different settings (decrease/increase volume) and augmentation




# Todo


N) To automate processing of one night, without keeping all segments to train AI
* must be able to handle spring nights, with lot of bird sounds
* sound analysis is repeatable, so no need to store to db permanently
- Report
  - show start date in report and folder name
  - show when new file starts
  - sort Audiomoth files by date
  - class with threshold, js to display only some thresholds
  - styles
  - warn of 10 consecutive bird segments?
- Split into reports at 12.00 midday
- Find out if splitting can be done faster


- BACKUP DATABASE
- Start from command line, not debug
- Two modes: training segments, sound analysis
- a) train mode: as currently, don't predict
- b) sound analysis mode: 
  - output mp3 & files to different folder
  - don't save to database (or save elsewhere?)
  - predict whole folder (make copy of predict.py)
    - if below threshold, delete spectro & mp3
    - if above threshold, add entry to file string
  - output file string with
    - file info (needed to retrain AI)
    - visual cue
    - embedded spectro
    - embedded mp3? or link to mp3?




1) Audiofile handling:
- Validate that file names dont have spaces
- Adjust volume to create augmented training data

2) UI
- highlight keyword field when contains something
- Shortcuts toggle
- add keys
  - insect
  - rain (r) vs loud_rain (loud = cannot listen/hear birds -> just give up)
  - wind (w) vs loud_wind
- Add buttons to move prev / next
- Preload next spectro & audio, https://stackoverflow.com/questions/37642224/can-html-link-tag-be-used-to-prefetch-audio-files

3) Misc
- Todo's in the files
- Try better mongodb admin tool (CRUD, easier to fix tags and move to next segement)
- UI:
- CHECK Are all spectrograms same size, despite of source bitrate?
- Backup mongodb, when? docker-compose down?
- CHECK Refactor split and spect: var names, files in subdirs, parametrize path structure?
- CHECK Double-check the time setting in SM4, is it UTC+3? And is the time value in metadata correct?
- Databasing: what should be case-insensitive? Location id? Mongodb _id's? How could the case change? (typing error on terminal, dir or file name change...?)
  - DONE: location id always lowercased
- Spectrogram
  - Should not scale colors of each plot separately for AI? Can this be prevented in pylab?
  - More contrast? How?
- Where time data: start time, day 
- Where metadata: recorded model, recorder id, original filename, original path, conversion datetime, peak amplitude


## Recording

- Sijoita äänitin niin ettei sade osu suoraan mikrofonin edessä olevaan muoviin, muuten tulee paljon häiriöääntä.




# Notes


## MongoDB

How to increment values in db:

  mongo --username root --password
  use loxia
  db.segments.updateMany({}, { $inc: { segmentNumber: 1 } })
  db.segments.updateMany({}, { $inc: { segmentStartSeconds: -10 } })
  db.segments.updateMany({}, { $inc: { segmentEndSeconds: -10 } })

Fing partial string:

  {"file_id": /XC469422/}


**Documents have not been updated**, since should also update segment _id, which is string


## Links

https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html

https://stackoverflow.com/questions/33175184/the-arrays-returned-from-pylab-specgram-dont-seem-to-add-up-to-the-image-could

https://stackoverflow.com/questions/44787437/how-to-convert-a-wav-file-to-a-spectrogram-in-python3
