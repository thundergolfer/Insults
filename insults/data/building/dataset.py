import csv
from datetime import datetime
import os

PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))


def setup_dataset_file(fp, schema):
    if not os.path.isfile(fp):
        with open(fp, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(schema)


def default_dataset_header():
    return [
        'Comment',
        'Date',
        'Insult',
        'Usage',
        'Source',
        'Score',
        'Parent Comment',
        'Grandparent Comment',
        'Labels',
        'Difficulty'
    ]


def csv_entry_to_dict(row, csv_header):
    return dict(zip(csv_header, row))



class DatasetEntry():
    DEFAULT_DATASET = os.path.join(PATH_TO_HERE, 'new_dataset.csv')
    ALLOWED_LABLES = ['racist', 'sexist', 'sarcasm', 'ableist']
    DIFFICULTY = ['easy', 'medium', 'hard', 'impossible']

    def __init__(self,
                 comment,
                 datetime,
                 is_insult,
                 usage,
                 source,
                 score,
                 parent_comment,
                 grandparent_comment,
                 labels=None,
                 difficulty=None):
        self.comment = self._validate_comment(comment)
        self.datetime = self._validate_datetime(datetime)
        self.is_insult = self._validate_is_insult(is_insult)
        self.usage = usage
        self.source = self._validate_source(source)
        self.score = self._validate_score(source, score)
        self.parent_comment = self._validate_a_parent_comment(parent_comment)
        self.grandparent_comment = self._validate_a_parent_comment(grandparent_comment)
        self.labels = self._validate_labels(labels)
        self.difficulty = self._validate_difficulty(difficulty)
        self.added_to = []

    def add_to_dataset(self, dataset_path=DEFAULT_DATASET):
        if dataset_path in self.added_to:
            print("This entry has already been added to '{}'".format(dataset_path))
            return False

        with open(dataset_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.to_csv_row())
            self.added_to.append(dataset_path)

        return True

    def to_csv_row(self):
        return [
            self.comment.encode('utf-8'),
            self.datetime.encode('utf-8'),
            str(self.is_insult).encode('utf-8'),
            str(self.usage).encode('utf-8'),
            self.source.encode('utf-8'),
            str(self.score).encode('utf-8'),
            self.parent_comment.encode('utf-8'),
            self.grandparent_comment.encode('utf-8'),
            '+'.join(self.labels).encode('utf-8'),
            self.difficulty.encode('utf-8')
        ]

    def _validate_comment(self, comment):
        if not isinstance(comment, basestring):
            raise ValueError("'comment' is not a string")

        return comment

    def _validate_datetime(self, dt):
        if type(dt) is not datetime:
            raise ValueError("'datetime' needs to be a datetime object")

        return dt.strftime("%Y%m%d%H%M%SZ")

    def _validate_source(self, source):
        if not source in set(['reddit']):
            raise ValueError("{} is not a valid dataset source".format(source))

        return source

    def _validate_score(self, source, score):
        return score

    def _validate_is_insult(self, is_insult):
        if is_insult is None:
            return 'NOT LABELLED'

        if is_insult is not False and is_insult is not True:
            raise ValueError("'is_insult' must be a boolean")

        return 1 if True else 0

    def _validate_a_parent_comment(self, parent_comment):
        if parent_comment is None:
            parent_comment = ''

        return self._validate_comment(parent_comment)

    def _validate_labels(self, labels):
        if labels is None:
            return []

        if not all(l in self.ALLOWED_LABLES for l in labels):
            raise ValueError("invalid label in 'labels'")

        return labels

    def _validate_difficulty(self, difficulty):
        if difficulty is None:
            return ""

        if not difficulty in self.DIFFICULTY:
            raise ValueError("'{}' is not a valid difficult for an entry. Must be one of {}".format(difficulty,
                                                                                                    self.DIFFICULTY))
        return difficulty
