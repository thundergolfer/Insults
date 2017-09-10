#!/usr/bin/env python
import json
import logging
import sys

RESULTS_FILE = sys.argv[1]
PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(PATH_TO_HERE, '..', '..', 'new_dataset.csv')

def update_dataset(responses):
    df = pd.read_csv(DATASET_PATH, index_col=False)
    df.set_index('HIT ID', inplace=True, drop=False)

    for resp in responses:
        hit_id = resp['hit_id']
        label = resp['is_insult']
        logging.info("Updating comment '{}'' with label: {}".format(comm.encode('utf-8'),
                                                                    label))
        df.loc[hit_id, 'Insult'] = label
        df.loc[hit_id, 'Status'] = "LABELLED"

    df.to_csv(DATASET_PATH, index=False)


responses = []
with open(RESULTS_FILE, 'r') as f:
    for json_str in f.readlines():
        hit_result = json.loads(json_str)
        label = 1 if hit_result['output']['example'] else 0
        responses.append({
            'hit_id': hit_result['hit_id']
            'is_insult': label
        })
