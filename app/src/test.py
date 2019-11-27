
import split_and_spectro
import profile

monoFilePath = "/_source_audio/noordwijk/Data/5DB0D594.WAV"
exportDir = "_exports/test"
directory = "noordwijk"
tempFileName = "5DB0D594.WAV"
segments = 1;

segmentMetaGenerator = split_and_spectro.parseFile(monoFilePath, exportDir, directory, tempFileName, segments, 10)

# profile.run('split_and_spectro.parseFile(monoFilePath, exportDir, directory, tempFileName, segments, 10)')
