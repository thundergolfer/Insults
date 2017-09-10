#!/usr/bin/env python

import csv
import json
import os
import sys


from insults.data.building.dataset import csv_entry_to_dict, default_dataset_header


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))
OUTFILE = os.path.join(PATH_TO_HERE,
                       '..',
                       'hit_inputs',
                       sys.argv[1])
DATASET_PATH = os.path.join(PATH_TO_HERE, '..', '..', 'new_dataset.csv')

LIMIT = sys.argv[2]


inputs = []
num_added = 0
with open(DATASET_PATH, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)  # skip the header
    for row in reader:
        if num_added == LIMIT:
            break

        dataset_entry = csv_entry_to_dict(row, default_dataset_header())

        if dataset_entry['Status'] == 'READY':
            input_ = {
                'comment': dataset_entry['Comment'],
                'parent': dataset_entry['Parent Comment'],
                'grandparent': dataset_entry['Grandparent Comment']
            }
            num_added += 1
            inputs.append(input_)


print("Writing new inputs to: {}".format(OUTFILE))
with open(OUTFILE, 'w') as f:
    for i in inputs:
        f.write("{}\n".format(json.dumps(i)))
