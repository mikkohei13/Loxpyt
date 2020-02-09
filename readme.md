

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

# Google Cloud AI

Searching files with regex/wildcard in mongodb:

  { file_id: { $in: [ /^noordwijk*/ ] } }


Create bucket:

  gsutil mb -l europe-north1 gs://spectro-us/


Copy single file:

  gsutil cp *.png gs://spectro-us/


Copies files from current dir to bucket, but does not create folder structure:

  gsutil cp -r $(find . -name "*.png") gs://spectro-us/


Rsync all subdirs, excluding mp3-files:

  gsutil -m rsync -r -x ".*.mp3$" . gs://spectro-us


Move bucket ...

  gsutil mb -l us-central1 gs://spectro-us/
  gsutil cp -r gs://spectro-1/ gs://spectro-us/


Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-2/XC501499_-_Whimbrel_-_Numenius_phaeopus.wav.00013.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC465612_-_Greater_White-fronted_Goose_-_Anser_albifrons.wav.00001.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC468592_-_Barnacle_Goose_-_Branta_leucopsis.wav.00003.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC450496_-_Barnacle_Goose_-_Branta_leucopsis.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC467572_-_European_Robin_-_Erithacus_rubecula.wav.00001.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC429361_-_Northern_Shoveler_-_Spatula_clypeata.wav.00001.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-2/XC489824_-_Eurasian_Curlew_-_Numenius_arquata.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC465567_-_Little_Owl_-_Athene_noctua.wav.00005.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC481741_-_Black-crowned_Night_Heron_-_Nycticorax_nycticorax.wav.00004.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/20190926-1002-Ks-SM4/HLO10_20190929_010500.wav.00354.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC467243_-_Black-crowned_Night_Heron_-_Nycticorax_nycticorax.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC503221_-_Little_Grebe_-_Tachybaptus_ruficollis.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC433197_-_Black-crowned_Night_Heron_-_Nycticorax_nycticorax.wav.00003.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-1/XC400521_-_Eurasian_Coot_-_Fulica_atra_atra.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC500213_-_Little_Grebe_-_Tachybaptus_ruficollis_ruficollis.wav.00006.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC432922_-_Grey_Heron_-_Ardea_cinerea.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC500659_-_Barnacle_Goose_-_Branta_leucopsis.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-2/XC461226_-_European_Golden_Plover_-_Pluvialis_apricaria.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-2/XC487134_-_Eurasian_Dotterel_-_Charadrius_morinellus.wav.00004.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC441695_-_Brant_Goose_-_Branta_bernicla.wav.00004.png.




Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC447974_-_Snow_Bunting_-_Plectrophenax_nivalis.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/20190926-1002-Ks-SM4/HLO10_20190929_010500.wav.00354.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/Noise-training-data/HLO10_20200103_173712.wav.00360.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC423405_-_Barnacle_Goose_-_Branta_leucopsis.wav.00001.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC481741_-_Black-crowned_Night_Heron_-_Nycticorax_nycticorax.wav.00004.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC500376_-_Taiga_Bean_Goose_-_Anser_fabalis.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-2/XC500492_-_Eurasian_Dotterel_-_Charadrius_morinellus.wav.00003.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC501687_-_Barnacle_Goose_-_Branta_leucopsis.wav.00004.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC507966_-_Black-crowned_Night_Heron_-_Nycticorax_nycticorax.wav.00005.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/20190427-28-Hanikka/5CC4A6B0.WAV.00360.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC493877_-_Common_Snipe_-_Gallinago_gallinago.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-2/XC501501_-_Whimbrel_-_Numenius_phaeopus.wav.00012.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC493356_-_Little_Bittern_-_Ixobrychus_minutus.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC468906_-_Eurasian_Oystercatcher_-_Haematopus_ostralegus.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-3/XC473159_-_Little_Grebe_-_Tachybaptus_ruficollis.wav.00001.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-6/XC501519_-_Brambling_-_Fringilla_montifringilla.wav.00002.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC465603_-_Common_Blackbird_-_Turdus_merula.wav.00001.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/XC-Set-4/XC465573_-_Song_Thrush_-_Turdus_philomelos.wav.00001.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/20200126-27-Ks-häiriöjasade/5E2E6040.WAV.00360.png.
Error: Cannot find the specified file: gs://spectro-us/spectro-1/20190512-15-Söderskoginmetsä-jyrkänne/5CD9DAD2.WAV.00360.png.



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

## Update data in MongoDB

How to increment values in db:

  mongo --username root --password
  use loxia
  db.segments.updateMany({}, { $inc: { segmentNumber: 1 } })
  db.segments.updateMany({}, { $inc: { segmentStartSeconds: -10 } })
  db.segments.updateMany({}, { $inc: { segmentEndSeconds: -10 } })

**Documents have not been updated**, since should also update segment _id, which is string


Cloud hosted / Host your model on Google Cloud for online predictions
Edge / Download your model for offline/mobile use
- optimize for higher accuracy / 360ms latency for Google Pixel 2 ... Best trade-off / 150 ms latency ... Faster predictions / 56 ms latency




# Todo

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
- Preload next spectro & audio

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
