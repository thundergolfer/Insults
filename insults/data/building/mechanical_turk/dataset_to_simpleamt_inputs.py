import csv
import json
import os


from insults.data.building.dataset import csv_entry_to_dict, default_dataset_header


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))
OUTFILE = os.path.join(PATH_TO_HERE, 'hit_inputs', 'inputs.txt')
DATASET_PATH = os.path.join(PATH_TO_HERE, '..', 'new_dataset.csv')

inputs = []

with open(DATASET_PATH, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)  # skip the headers
    for row in spamreader:
        dataset_entry = csv_entry_to_dict(row, default_dataset_header())
        input_ = {
            'comment': dataset_entry['Comment'],
            'parent': dataset_entry['Parent Comment'],
            'grandparent': dataset_entry['Grandparent Comment']
        }
        inputs.append(input_)

with open(OUTFILE, 'w') as f:
    for i in inputs:
        f.write("{}\n".format(json.dumps(i)))

print(inputs)
