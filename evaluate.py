import codecs
import json
import sys
import numpy as np
import re

###################################################
# Authors - Riddhiman Dasgupta and Balaji Ganesan #
###################################################

def f1(p, r):
    if r == 0.:
        return 0.
    return 2 * p * r / float(p + r)


def strict(true_and_prediction):
    num_entities = len(true_and_prediction)
    correct_num = 0.
    for true_labels, predicted_labels in true_and_prediction:
        correct_num += set(true_labels) == set(predicted_labels)
    precision = recall = correct_num / num_entities
    return {'p': precision,
            'r': recall,
            'f1': f1(precision, recall)}


def loose_macro(true_and_prediction):
    num_entities = len(true_and_prediction)
    p = 0.
    r = 0.
    for true_labels, predicted_labels in true_and_prediction:
        if len(predicted_labels) > 0:
            p += len(set(predicted_labels).intersection(set(true_labels))) / float(len(predicted_labels))
        if len(true_labels):
            r += len(set(predicted_labels).intersection(set(true_labels))) / float(len(true_labels))
    precision = p / num_entities
    recall = r / num_entities
    return {'p': precision,
            'r': recall,
            'f1': f1(precision, recall)}


def loose_micro(true_and_prediction):
    num_predicted_labels = 0.
    num_true_labels = 0.
    num_correct_labels = 0.
    for true_labels, predicted_labels in true_and_prediction:
        num_predicted_labels += len(predicted_labels)
        num_true_labels += len(true_labels)
        num_correct_labels += len(set(predicted_labels).intersection(set(true_labels)))
    precision = num_correct_labels / num_predicted_labels
    recall = num_correct_labels / num_true_labels
    return {'p': precision,
            'r': recall,
            'f1': f1(precision, recall)}


def get_annotations(file_name):
    annotations_map = {}

    # read the file, check for correct format
    with codecs.open(file_name, 'r', 'utf-8') as f:
        json_data = None
        try:
            json_data = json.loads(f.read())
        except Exception as e:
            print("Exception - " + str(e))
        for k, v in json_data.items():
            results = v
        if (len(results) < 1):
            print("Invalid submission file.")
            sys.exit() 
             
        # now we'll read each json element
        for result in results:
            try:
                if ('text' not in result or 'entity' not in result or 'types' not in result):
                    print("Invalid result json element.")
                    print(result)
                    continue
            except Exception as e:
                print("Exception - " + str(e))
    
            anonymized_text = get_anonymized_text(result['text'], result['entity'])
            annotations_map[anonymized_text] = (result['entity'], result['types'])

        return annotations_map
      
def get_anonymized_text(text, entity=None):
    if entity is None or len(entity) < 1:
        return text
    patterns = [r'\b%s\b' % re.escape(entity), r'\bXXXX XXXX XXXX XXXX\b', r'\bXXXX XXXX XXXX\b', r'\bXXXX XXXX\b', r'\bXXXX\b', r'\bXX/XX/XXXX\b', r'\bXX/XX/\b']
    regex_patterns = '|'.join(patterns)
    try:
        mentions = re.findall(regex_patterns, text)
        if (len(mentions) == 0):
            return text
        elif (len(mentions) != 1):
            print("Error! Only one entity mention per sentence should be present.")
            print(text)
            print(mentions)
            return text
        mention = mentions[0]
        entity = 'XXXX XXXX'
        text = text.replace(mention, entity)
    except:
        return text

    return text

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " <ground_truth_file> <submission_file>")
        sys.exit()
    
    ground_truth_file = sys.argv[1]
    input_file = sys.argv[2]

    # we'll load the input files to maps
    # key is anonymized, and hence normalized text
    # values are tuples containing (entity, labels_str)
    # labels_str contain types separated by space
    ground_truths_map = get_annotations(ground_truth_file)
    submissions_map = get_annotations(input_file)

    true_and_prediction = []
    for text, gt_tuple in ground_truths_map.items():
        if text in submissions_map.keys():
            #print(text)
            # each tuple has the entity and its type
            true_labels_str = gt_tuple[1]
            true_labels = true_labels_str.split()
            #print(true_labels)
            annotation_tuple = submissions_map[text]
            predicted_labels_str = annotation_tuple[1]
            predicted_labels = predicted_labels_str.split()
            #print(predicted_labels)
            true_and_prediction.append((true_labels, predicted_labels))
    
    if len(true_and_prediction) < 1:
        print("Error: invalid prediction output")
        sys.exit()

    metrics = {
        'strict': strict(true_and_prediction),
        'macro': loose_macro(true_and_prediction),
        'micro': loose_micro(true_and_prediction),
    }
    geometricMean = (metrics['strict']['f1'] * metrics['macro']['f1'] * metrics['micro']['f1']) ** (1 / 3)
    print("        strict f1:", metrics['strict']['f1'])
    print("   loose macro f1:", metrics['macro'])
    print("   loose micro f1:", metrics['micro'])
    print("geometric mean   :", geometricMean)

