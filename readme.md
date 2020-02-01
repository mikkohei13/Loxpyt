

# Usage

## Setup (not tested)

- Install Docker
- Clone this repository
- Create directories for audio files:
  - _exports
  - _source_audio
- Place audio (.wav) files to _source_audio/{RECORDING SESSION NAME}/Data
- Start containers:
  - `docker-compose up --build`
- Terminal to container:
  - `docker exec -ti loxia_web bash`
- Handle audio file inside the container:
  - `cd /app/src/`
  - `python3 audiofile_handler.py --dir DIRECTORY_NAME --location LOCATION_ID`

## Annotating

- Annotate at http://localhost/files
- See & manage data at http://localhost:8081/


### Annotation guidelines & notes

- Use distortion2 for real distortions, not filters or fading.
  - The old term distortion is used for both distortion and filters.
- Use high-pass and fade for filtered segments.
  - Note that sometimes it's not clear if filters have applied, e.g. http://localhost/segment?file_id=XC-Set-2/XC501502_-_Whimbrel_-_Numenius_phaeopus.wav#4
- Use vechile, wind, rain, human tags only if especially loud, when it might be better to check these segments manually.
- Tag silence only if no other tags. In practice, I have used this also with other sounds except animals.
- Faint and strong have not been used systematically. They can be considered as good examples of faint and strong sounds.
- Some dogs have been tagged as mammals.
- Local_choir / individual and migrants can be tagged in same annotation.
- Annotations are often lacking dogs etc, if there are only birds. So cannot be used for learning absence of dogs.

??

- Kannattaako augmentaatiota käyttää
- Kannattaako distorted/filtered -tiedostoja käyttää? http://localhost/segment?file_id=XC-Set-1/XC459718_-_Eurasian_Coot_-_Fulica_atra-ss5vol07.wav#11


# Some design principles:

- All data except annotations are upserted, so that there won't be duplicates.-
- Annotations are not upserted, because this might lose work and/or break the AI training process
- How to handle when nocmig ends and morning begins? The system should recognize alo local birds. Then user decides which segments they want to handle.
  - Due to this, cannot easily create a migration index for the night?
- File metadata (such as recorder device info) will be duplicated for each file, due to simplicity.
- All times are UTC.
- Segments are identified by an incremented integer. 
- Due to this, if segment length changes, this requires fresh database and _exports directory.


# Todo

## Background

- Check what other annotated data is available, how long are the files, what format are they, what's the frequency, what kind of tags ...
  - https://zenodo.org/record/1298604
  - https://zenodo.org/record/1208080
- Nocmig literature, e.g. Poland/Pamula


## Sounds

- Use Low-pass filter for silent clips
- MAYBE: Use fade in for silent clips. Long and short, e.g. http://localhost/segment?file_id=XC-Set-2/XC461226_-_European_Golden_Plover_-_Pluvialis_apricaria.wav#1

- XC:
  - owls
  - Anthus, Phoen...
  - emberiza
  - chahia, chadub, tringa, calidris

- Omat
  - Morning chorus with buzzing sound 
  - Clahye
  - Noorwijk: birds
  - Suvisaaristo: wind
  - Aamukuoro


## AI Training

- Classification
  - remove: ignore, distortion2, faded, (high-pass?)
  - animal: migrant, migrant-low, wander, local_individual, local_choir, owl, bat, mammal, dog, other_animal, mystery
  - no-animal: the rest

- TBD
  - Clip top 15% away? -> faster handling, high-freq noise does not bother. Might affect negatively in recognizing spikes?
  - Remove most bats? Or learn to give positives on bats also?
  - include dog, mammal & other animal as positives?
  - remove faints that also have bats, noise or loud things?

- don't use loud vehicles (at least from ks training recording), expect that recorded is not near roads. But use loud planes.


# Misc

25.1.2020:
4376 annotations
647 migrant's (14,8 %)
578 migrant-low's (13,2 %)

31.1.2020:
5587 annotations
694 migrant's (15,9 %)
725 migrant-low's (13,0 %)




BIASES
- no birds when loud vehicles (training data from winter)
- most birds from noordwijk, with seashore wave sounds
- many birds during good migration -> multiple calls in each segment

DOWNLOAD
- common sandpiper
- green sandpiper
- tringa's
- charadrius'
- geese
- gulls
- thrushes
- buntings
- flycathers
- robin

Tips
- Sijoita äänitin niin ettei sade osu suoraan mikrofonin edesäs olevaan muoviin -> paljon häiriöääntä

XC Sounds
- ALWAYS DO
  - Replace spaces with underscores in filenames
      rename 's/ /_/g' *
  - Create nonmodified wav's
      for i in *.mp3; do ffmpeg -i "$i" "${i%.*}.wav"; done

- MAYBE DO
  - Basic augmentation sets:
    - Skip 2 sec, volume 1.3
        for i in *.mp3; do ffmpeg -ss 2 -i "$i" -filter:a "volume=1.3" "${i%.*}-ss2vol13.wav"; done
    - Skip 5 sec, volume 0.7
        for i in *.mp3; do ffmpeg -ss 5 -i "$i" -filter:a "volume=0.7" "${i%.*}-ss5vol07.wav"; done

- Annotate
  - Ignore those with malformed spectrogram
  - Ignore faade in & fade out recordings

- Crop images
    EXAMPLE: chop 50 pixels from top
    ../_portable/magick example.png -gravity North -chop 0x50 result.png


# Todo

- Validate that file names dont have spaces
- highlight keyword field when contains something
- Shortcuts toggle
- add keys
  - insect
  - rain (r) vs loud_rain (loud = cannot listen/hear birds -> just give up)
  - wind (w) vs loud_wind
- Adjust volume to create augmented training data
- Handle also mp3 files -> can use xeno-canto data. Options:
  - Handle mp3 same way as wav (See Todo: from mp3)
  - PRAGMATIC? Convert mp3 first to wav, using a separate tool
- Highlight keyword field if contains something
- Disable submitting the form normally when pressing enter on keywords field
- Preload?
- Add buttons to move prev / next
- Try put better mongodb admin tool (easier to fix tags and move to next segement)
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
