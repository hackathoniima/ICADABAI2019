import json
import random
import re

# Author: Balaji Ganesan
# Email: balajinix@gmail.com

# we can load the dataset filename like below
dataset_filename = "./dataset.json"
with open(dataset_filename, 'r') as f:
    data = json.load(f)

# we call the entities that we are interested in as personal data entities (PDE)
# in this task, we are interested in about 20 PDE types (PDETs), but you are welcome to
# type more than these 20 too. See additional_data/all_pde_types.json
pde_types_filename = "./types.json"
pde_types_list = []
with open(pde_types_filename, "r") as f:
    pde_types = json.load(f)
    pde_types_list = pde_types['pde_types']

# this is not a complete list of patterns that you may find in original data (see ./additional_data)
# but we have chosen only these in the dataset for the hackathon
patterns = [r' XXXX XXXX XXXX XXXX', r'XXXX XXXX XXXX', r'XXXX XXXX', r'XXXX', r'XX/XX/XXXX', r'XX/XX/']
regex_patterns = '|'.join(patterns)

json_output = []
i = 1
for text in data:
    json_element = {}

    # we're using a simple regex pattern to find the redacted mentions
    mentions = re.findall(regex_patterns, text)
    if (len(mentions) != 1):
        print("Error! Only one entity mention per sentence should be present.")
        print(mentions)
        continue
    mention = mentions[0]

    ######### ENTITIES FOR DEMO - REPLACE THIS ##########
    entity = "entity_" + str(i)
    ######### ENTITIES FOR DEMO - REPLACE THIS ##########

    json_element['text'] = text.replace(mention, entity)
    json_element["entity"] = entity

    ######### TYPES FOR DEMO - REPLACE THIS ##########
    # this are just some fake types that we are creating, you should remove all this
    rand_int = random.randint(0, len(pde_types_list)) - 1
    types = pde_types_list[rand_int]
    # typically parents of the types also apply to the entity, hence adding here
    if rand_int > 5:
       for pdet in pde_types:
          if pdet in types:
             types += " " + pdet
    # sometimes types from different branches in the hierarchy can apply to an entity
    if rand_int > 15:
        rand_int = random.randint(0, len(pde_types_list)) - 1
        another_type = pde_types_list[rand_int]
        if another_type not in types:
            types += " " + another_type
    ######### TYPES FOR DEMO - REPLACE THIS ##########

    json_element["types"] = types
    json_output.append(json_element)
    i += 1

submission = {}
submission["your_team_name"] = json_output
output_filename = "sample_submission_file.json"
with open(output_filename, "w") as f:
    json.dump(submission, f, indent=2, separators=(',', ': '))
    f.write('\n')
