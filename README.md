# Dataset Generation Hackathon at ICADABAI 2019

## IIM Ahmedabad, April 6-7, 2019

As described in the problem statement, the task is to impute Personal Data Entities wherever we find them redacted (marked as XXXX) in the dataset provided in this git repo.

### Files

types.json - these are the types of the Personal Data Entities that need to be imputed in the dataset. You can impute other types if you wish, but they'll not be considered for evaluation.
dataset.json - these are the 30000 sentences, which need to be annotated by the participating teams.

### Additional Data

In the directory additional_data, we're providing more data if you wish to use them for training a neural model etc. Please note that your submissions should only contain the 30000 sentences and the imputed values.
