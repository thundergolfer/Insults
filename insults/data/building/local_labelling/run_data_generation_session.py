#
# How to Run:
# from the thundergolfer/Insults project root run
# `python -m insults.data.building.local_labelling.run_data_generation_session`
#

from datetime import datetime

from insults.data.building.dataset import DatasetEntry

SESSION_LENGTH = 2


def elicit_dataset_entry():
    def display_confirmation(data):
        print("You entered: '{}'".format(grandparent))

    print("Enter 'Grandparent Comment', or hit ENTER to skip:")
    grandparent = raw_input()
    if grandparent:
        display_confirmation(grandparent)

    print("Enter 'Parent Comment', or hit ENTER to skip:")
    parent = raw_input()
    if parent:
        display_confirmation(parent)

    while True:
        print("Enter 'Comment':")
        comment = raw_input()
        if not comment:
            print("Error: must enter a comment. cannot be blank")
        else:
            display_confirmation(comment)
            break

    while True:
        print("Is the comment an insult? (Y/N):")
        is_insult = raw_input()
        if is_insult.lower() not in ['y', 'n']:
            print("Error: must enter 'y' (Yes) or 'n' (No)")
        else:
            is_insult = True if is_insult.lower() == 'y' else False
            break

    while True:
        print("What's the difficulty of this example? [easy, medium, hard, impossible]:")
        diff = raw_input()
        if diff.lower() not in DatasetEntry.DIFFICULTY:
            print("Error: must be one of the options shown. You entered: {}".format(diff))
        else:
            break

    while True:
        print("Should this comment get a label? [racist, sexist, sarcasm, ableist]:")
        print("Press ENTER for no")
        label = raw_input()
        if label and label.lower() not in DatasetEntry.ALLOWED_LABELS:
            print("Error: invalid label")
        else:
            break

    entry = DatasetEntry(
        comment=comment,
        datetime=datetime.now(),
        is_insult=is_insult,
        usage=None,  # this is a weird field that just stays None
        source='SYNTHETIC',
        score=None,
        parent_comment=parent,
        grandparent_comment=grandparent,
        status='READY',
        labels=[label] if label else [],
        difficulty=diff
    )

    entry.add_to_dataset()


for i in range(SESSION_LENGTH):
    print("{} of {}".format(i + 1, SESSION_LENGTH))
    elicit_dataset_entry()
