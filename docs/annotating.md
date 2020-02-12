# Annotating & AI Training

## Annotation guidelines & notes

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

## Todo

- Check what other annotated data is available, how long are the files, what format are they, what's the frequency, what kind of tags ...
  - https://zenodo.org/record/1298604
  - https://zenodo.org/record/1208080
- Nocmig literature, e.g. Poland/Pamula

- Re-annotate high-pass filtered sounds, re-upload them to cloud
- Kannattaako augmentaatiota käyttää
- Kannattaako distorted/filtered -tiedostoja käyttää? http://localhost/segment?file_id=XC-Set-1/XC459718_-_Eurasian_Coot_-_Fulica_atra-ss5vol07.wav#11

- XC:
  - Owls
  - Anthus, Phoen...
  - emberiza
  - buntings
  - flycathers

- Omat
  - Mössenkärr
  - Morning chorus with buzzing sound 
  - Clahye
  - Noorwijk: birds
  - Suvisaaristo: wind
  - Aamukuoro
  - Wind + aamukuoro



## Annotating Xeno-Canto Sounds

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

- Annotate problem recordings

  - **distortion2** when spectrogram is malformed
  - **fade**
  - **high-pass**



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

- Crop images
    EXAMPLE: chop 50 pixels from top

    ../_portable/magick example.png -gravity North -chop 0x50 result.png


## Biases etc.

- no birds when loud vehicles (training data from winter, difficulties hearing)
- most birds from noordwijk, with seashore wave sounds
- many birds during good migration -> multiple calls in each segment


## Old notes

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

## Misc

25.1.2020:
4376 annotations
647 migrant's (14,8 %)
578 migrant-low's (13,2 %)

31.1.2020:
5587 annotations
694 migrant's (15,9 %)
725 migrant-low's (13,0 %)
