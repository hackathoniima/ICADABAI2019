import json
import spacy

# Author: Balaji Ganesan
# Email: balajinix@gmail.com

# we can load the dataset filename like below
dataset_filename = "./documents.json"
with open(dataset_filename, 'r') as f:
    data = json.load(f)

# this is not a complete list of patterns that you may find
patterns = [r' XXXX XXXX XXXX XXXX', r'XXXX XXXX XXXX', r'XXXX XXXX', r'XXXX', r'XX/XX/XXXX', r'XX/XX/']
regex_patterns = '|'.join(patterns)

# we'll use spacy to get the sentences from the text https://pypi.org/project/spacy/
nlp = spacy.load('en')
json_output = []
for doc in data:
    json_element = {}
    sentence = nlp(doc)
    for sent in sentence.sents:
        text = sent.text
        # sanity check
        if 'XX' not in text:
            continue
        # we don't want too short sentences
        if (len(text) < 80):
            continue
        # apostophe's create problems in tokenization, removing is fine for this hackathon
        if '\'' in text:
            continue
        # we don't want unnecessary linefeeds
        text = text.replace("\n", " ")
        text = text.strip()
        # let's see if the last character in the sentence is a period
        ch = text[-1]
        if '.' != ch:
            continue
        # let's see if the first character in the sentence is uppercase
        ch = text[0]
        if not ch.isupper():
            continue
        # atleast one of the redaction patterns above should be present in the sentence
        mentions = re.findall(regex_patterns, text)
        if (len(mentions) != 1):
                continue
        json_output.append(text)

output_filename = "./dataset.json"
with open(output_filename, "w") as f:
    json.dump(json_output, f, indent=2, separators=(',', ': '))
    f.write('\n')
