# AmericasNLP 2022

## Data

### Downloading
The data for the competition can be found [here](https://rcweb.dartmouth.edu/homes/f00458c/americasnlp2/). Alternatively, you can use the provided download script to automatically download the data for all languages. The script takes a single argument, which is the folder in which to download the data to:
```
./download_data.sh destination_folder
```


### Data format
Each language folder contains two subfolders, each corresponding to a different training split. In each subfolder, there are multiple
audio files, and a single tsv file containing all transcriptions and translations. Audio files are split such that each file contains
a single sentence or utterance. The tsv file is structured as follows:

|Header | Content                                                                                                      |
|-------|--------------------------------------------------------------------------------------------------------------|
 |wav| The corresponding audio filename.                                                                            |
|source_processed| A processed version of the audio transcription.                                                              |
|source_raw| The original raw transcript. We ask you to use this data for training and evaluation, and to ignore the previous column. |
|target_raw| The translation of the transcription into either Spanish or Portuguese.                                      |


## Baselines

### ASR Baseline
The baseline model for the ASR task has been implemented in [espnet](https://github.com/espnet/espnet). The scripts to run the model can be found in the following [directory](https://github.com/espnet/espnet/tree/master/egs2/americasnlp22/asr1) of the espnet repository. 
