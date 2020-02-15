
# Google Cloud

## Project Settings

* Project birdmig
* Region us-central1


## DATASET: birdmig1_animals_1000

10.2.2020
Single-label classification
1000 random images from the full c. 5900 image set.

Labels:
- ignore: "ignore" in tagList or "distortion2" in tagList or "faded" in tagList or "high-pass" in tagList
- animal (376 images): "migrant" in tagList or "migrant-low" in tagList or "migrant-low" in tagList or "wander" in tagList or "local_individual" in tagList or "local_choir" in tagList or "owl" in tagList or "mystery" in tagList or "mammal" in tagList or "dog" in tagList or "other_animal" in tagList or "bat" in tagList:
- no-animal (624 images): the rest

### MODEL: birdmig1_animals_1000_20200210

Edge
High-precision
max 10 node hours, c. 2,5 hours used


## DATASET: 

11.2.2020

### MODEL: birdmig1_animals_full_20200212

Edge
High-precision
max 20 node hours, c. 2,5 hours used

  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 4076: The label is already a ground truth.
  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 5802: The label is already a ground truth.
  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 4875: The label is already a ground truth.
  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 4937: The label is already a ground truth.
  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 3005: The label is already a ground truth.
  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 4719: The label is already a ground truth.
  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 5825: The label is already a ground truth.
  Error: gs://spectro-us/spectro-1/_data/target_annotations_animals_full.csv line 2921: The label is already a ground truth.

AUC c. 0.96
Precison & recall: 92.57 %
Animals: c. 91.8 %


Problem cases:
- Clahye's
- Faint migrants
- Some local fieldfares


## Possible datasets & models

Check what kind of sounds are problematic and add those
- grasshoppers

Heavy rain and/or wind separately -> give up on those?

Multi-classification, with heavy rain & heavy wind as separate classes -> System can give up and not report them.

Test with Juha Saari's recording

Train with Xeno-Canto, test with own recordings, or vice versa. Balance bird/non bird 50/50%.

Multi-label classification
- bird
- bird chorus
- bat
- rain & heavy rain
- wind & heavy wind


## Notes

Cloud hosted / Host your model on Google Cloud for online predictions
Edge / Download your model for offline/mobile use
- optimize for higher accuracy / 360ms latency for Google Pixel 2 ... Best trade-off / 150 ms latency ... Faster predictions / 56 ms latency


Specify your own TRAIN, TEST, VALIDATION split. The tool randomly assigns images, but near-duplicates may end up in TRAIN and VALIDATION which could lead to overfitting and then poor performance on the TEST set.

rule of thumb - the label with the lowest number of examples should have at least 10% of the examples as the label with the highest number of examples.

Using a somewhat novel dataset to fine-tune model structure means your model will generalize better


## CSV formats

Single-label classification:

[set,]image_path[,label]
TRAIN,gs://My_Bucket/sample1.jpg,cat
TEST,gs://My_Bucket/sample2.jpg,dog

Multi:

[set,]image_path[,label1][,label2][,labelN]


### Commands

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



