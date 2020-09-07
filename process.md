
Training the AI

- Run script NN to split large audio files into segments. See YY for insturctions for working with e.g. Xenp-Canto -files.
  - System creates 10-second audio segments and spectrograms
- Annotate audio segments
  - User annotates segments using web UI
- Train the AI using
  - Audio segment spectrograms
  - Annotation data on database
- Test the AI

Using the AI

- User places audio files from one night into a folder (later: more nights)
- User starts the process
- System creates audio segments automatically
- AI handles each segment 
- System saves predictions to a file, with links to those segments that are above thresholds. (Later: to database, like manual annotations, so that can retrain the AI)
- System deletes audio files of below-threshold segments, to save space. (Maybe also spectrograms?)
(- Systems shows migration activity index for the night)
- User listens and views segments with predicted NFC's
  - Identifies species
  - Records these as observations / no-birds to the system, which creates annotations to the db.
- System sends observations to FinBIF Notebook via API

- Eventually AI is retrained with the new material in the db.


