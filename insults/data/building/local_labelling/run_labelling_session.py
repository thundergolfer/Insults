import csv
import logging
import os
import pandas as pd
import sys
import time

from insults.data.building.dataset import csv_entry_to_dict, default_dataset_header


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(PATH_TO_HERE, '..', 'new_dataset.csv')


def gather_entries_to_label(dataset_path, limit=50):
    inputs = []
    num_added = 0
    with open(dataset_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the header

        for row in reader:
            if num_added == limit:
                print("Gathered {} examples".format(limit))
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

    return inputs


def display_entry(entry):
    header = """
    The challenge is to detect when a comment from a conversation would be considered insulting
    to another participant in the conversation. Samples could be drawn from conversation streams
    like news commenting sites, magazine comments, message boards, blogs, text messages, etc.

    The idea is to create a generalizable single-class classifier which could operate in a near real-time
    mode, scrubbing the filth of the internet away in one pass.

    ---------------------------------------------------------------------------------------------------

    NOTE: It is important that the comment must be insulting another participant in the
    conversation. For our purposes, the following are not to be classified as insults:

    * President Mugabe is an absolute idiot
    * The FCC are a bunch of dickheads

    While these comments are insulting, they are not directed at someone else in the conversation,
    but distant third-parties or non-persons.
    ----------------------------------------------------------------------------------------------------
    """

    print(header)

    print("GRANDPARENT COMMENT:\n{}\n".format(entry['grandparent']))
    print("-" * 20)
    print("PARENT COMMENT:\n{}\n".format(entry['parent']))
    print("*" * 20)
    print("COMMENT TO LABEL:\n{}\n".format(entry['comment']))
    print("*" * 20)


def get_label(entry):
    while True:
        response = raw_input("Is comment an insult? [y/n] ")

        if response not in ['y', 'n']:
            print("Invalid!")
        else:
            print("'{}' is recorded!".format(response))
            label = 1 if 'y' else 0
            return {
                'comment': entry['comment'],
                'is_insult': label
            }
            time.sleep(0.5)


def update_dataset(responses):
    df = pd.read_csv(DATASET_PATH, index_col=False)
    df.set_index('Comment', inplace=True, drop=False)

    for resp in responses:
        comm = resp['comment']
        label = resp['is_insult']
        logging.info("Updating comment '{}'' with label: {}".format(comm.encode('utf-8'),
                                                                    label))
        df.loc[comm, 'Insult'] = label
        df.loc[comm, 'HIT ID'] = 'LOCAL'
        df.loc[comm, 'Status'] = "LABELLED"

    df.to_csv(DATASET_PATH, index=False)


if __name__ == '__main__':
    LIMIT = int(sys.argv[1])

    print("Starting...")
    responses = []
    entries = gather_entries_to_label(DATASET_PATH, LIMIT)
    if not entries:
        print("Nothing available to label.. exiting")

    for entry in entries:
        display_entry(entry)
        responses.append(get_label(entry))

    print("-" * 20)
    print("Done with responses. Now will update dataset")
    print("-" * 20)

    update_dataset(responses)

    print("Update finished. Thanks for your time")
