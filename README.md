# ICADABAI 2019 IIM Ahmedabad, April 6-7, 2019

https://conference.iima.ac.in/icadabai/2019/ 

# Dataset Generation Hackathon, Jan 29-Feb 28, 2019

https://sites.google.com/iimahd.ernet.in/hackathon-icadabai2019/home 

As described in the problem statement of the hackathon, the task is to impute Personal Data Entities wherever we find them redacted (marked as XXXX) in the dataset provided in this git repo.

### Files

types.json - these are the types of the Personal Data Entities that need to be imputed in the dataset. You can impute other types if you wish, but they'll not be considered for evaluation. 


dataset.json - these are the 30916 sentences, which need to be annotated by the participating teams. 

create_submission.py - this python code can be used to read the input file and create the submission file.

### Additional Data

In the directory additional_data, we're providing more data if you wish to use them. The 30916 sentences in the dataset.json come from the text in documents.json. If looking at the whole document, helps understand the context of the sentences, you can use these documents. For example, for manual annotations and depency parsing the whole document can be useful. 

all_pde_types.json has additional types if you choose to annotate more types.

Please note that your submissions should only contain the 30916 sentences and the imputed values. And only the 20 types in types.json are mandatory. Other types are optional and will not be used for evaluation.

### Questions?

Please join the below mailing group, to ask questions, and discuss with organisers and other contestants. 

https://groups.google.com/forum/#!forum/iima-hackathon-2019
