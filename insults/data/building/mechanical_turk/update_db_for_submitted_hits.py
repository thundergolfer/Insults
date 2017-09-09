import json
import logging
import pandas as pd
import os
import sys


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))


def link_inputs_with_hit_ids(inputs, submitted_ids):
    df = pd.read_csv(DATASET_FILE, index_col=False)
    df.set_index('Comment', inplace=True, drop=False)

    for input_, id_ in zip(inputs, submitted_ids):
        logging.info("Updating comment '{}'' with HIT ID {}".format(input_['comment'].encode('utf-8'),
                                                                    id_.encode('utf-8')))
        df.loc[input_['comment'], 'HIT ID'] = id_
        df.loc[input_['comment'], 'Status'] = "SUBMITTED"

    df.to_csv(DATASET_FILE, index=False)


DATASET_FILE = os.path.join(PATH_TO_HERE, '..', sys.argv[1])
INPUTS_FILE = sys.argv[2]
SUBMITTED_FILE = sys.argv[3]

inputs = []
with open(INPUTS_FILE, 'r') as f:
    for line in f.readlines():
        inputs.append(json.loads(line))

submitted_ids = []
with open(SUBMITTED_FILE, 'r') as f:
    for line in f.readlines():
        submitted_ids.append(line.rstrip())


if __name__ == '__main__':
    link_inputs_with_hit_ids(inputs, submitted_ids)
