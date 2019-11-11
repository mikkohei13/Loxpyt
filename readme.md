
# Tbd

- Should we adjust NFTT (+ noverlap) to have same length for each window? Yes, so that each image is same width, despite different sampling rates. 
  - Rule of thumb: 10-50 ms / window is usually good
  - My tests: c. 15 ms / window seems clearest
  - For NFTT "A power 2 is most efficient"


# Todo

- Git
- Pip in Docker
- Spectrogram
  - Should not scale colors of each plot separately for AI?
  - More contrast for higher amplitudes? https://towardsdatascience.com/getting-to-know-the-mel-spectrogram-31bca3e2d9d0
  - Greyscale? https://jakevdp.github.io/PythonDataScienceHandbook/04.07-customizing-colorbars.html
- limit all to same freq (~16 kHz)
- all to mono
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

# Logic

- Convert bunch of files to 10 sec segments
  - Save data to database (mysql/nosql?)
    - uuid
    - source device id
    - source filename
    - segment number
    - location name from dir name
    - datetime normalized from file meta (filename, with a functions for SM4 and Audiomoth, handling also timezone) and segment number
      - Audiomoth: UTC, winter/summer?
      - SM4: Finnish summer time
    - Night id (first day yyyymmdd)
    - conversion datetime
    - file info?
  - Calculate filenames, so that files can be kept in same directory
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
