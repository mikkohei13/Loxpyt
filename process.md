
Training the AI

- Annotate audio segments
  - System creates 10-second audio segments and spectrograms
  - User annotates segments using web UI
- Train the AI using
  - Audio segment spectrograms
  - Annotation data on database
- Test the AI

Using the AI

- User uploads recordings
- System creates audio segments automatically
- AI handles each segment 
- AI saves predictions to db
- Systems shows migration activity index for the night
- User listens and views segments with predicted NFC's
  - Identifies species
  - Records these as observations to the system
- System sends observations to FinBIF Notebook via API
- Eventually AI is retrained with the new material


