from contextlib import contextmanager
from mock import patch
import pandas as pd
import os
import shutil
import tempfile

from insults.data.building.local_labelling.run_labelling_session import (gather_entries_to_label,
                                                                         get_label,
                                                                         update_dataset)


TEST_DATASET_PATH = '/Users/jbelotti/Code/thundergolfer/Insult/tests/data/support/test_dataset.csv'


@contextmanager
def mockRawInput(mock):
    original_raw_input = __builtins__.raw_input
    __builtins__.raw_input = lambda _: mock
    yield
    __builtins__.raw_input = original_raw_input


def create_temporary_copy(src):
  # create the temporary file in read/write mode (r+)
  tf = tempfile.NamedTemporaryFile(mode='r+b', prefix='__', suffix='.tmp')

  # on windows, we can't open the the file again, either manually
  # or indirectly via shutil.copy2, but we *can* copy
  # the file directly using file-like objects, which is what
  # TemporaryFile returns to us.
  # Use `with open` here to automatically close the source file
  with open(src,'r+b') as f:
    shutil.copyfileobj(f,tf)

  # rewind the temporary file, otherwise things will go tragically wrong on Windows
  tf.seek(0)
  return tf


class TestGatherEntriesToLabel():

    def test_only_gathers_READY_entries(self):
        entries_to_label = gather_entries_to_label(TEST_DATASET_PATH)
        expected = [
        {'comment': 'Comment 1',
         'grandparent': 'Grandparent 1',
         'parent': 'Parent 1'
         },
        {'comment': 'Comment 2',
         'grandparent': '',
         'parent': 'Parent 2'}
        ]

        assert expected == entries_to_label

    def test_can_limit_number_of_returned_entries(self):
        entries_to_label = gather_entries_to_label(TEST_DATASET_PATH, limit=1)
        expected = [
        {'comment': 'Comment 1',
         'grandparent': 'Grandparent 1',
         'parent': 'Parent 1'
         }
        ]

        assert expected == entries_to_label


class TestGetLabel():

    def test_handles_good_input_positive_label(self):
        entry = {
            'comment': 'This is a comment'
        }

        with patch('__builtin__.raw_input', return_value='y') as _raw_input:
            result = get_label(entry)

        expected = {
            'comment': 'This is a comment',
            'is_insult': 1
        }
        assert expected == result

    def test_handles_good_input_negative_label(self):
        entry = {
            'comment': 'This is another comment'
        }

        with patch('__builtin__.raw_input', return_value='n') as _raw_input:
            result = get_label(entry)

        expected = {
            'comment': 'This is another comment',
            'is_insult': 0
        }
        assert expected == result


class TestUpdateDataset():

    def test_update_dataset_with_no_responses(self):
        with open(TEST_DATASET_PATH, 'r') as d:
            original_state = d.read()

        with create_temporary_copy(TEST_DATASET_PATH) as temp:
            update_dataset(temp.name, [])
            new_dataset = temp.read()

            assert original_state == new_dataset

    def test_update_dataset_with_one_response(self):
        responses = [
            {'comment': 'Comment 1', 'is_insult': 1}
        ]

        original_dataset = pd.read_csv(TEST_DATASET_PATH)
        expected = original_dataset
        expected.loc[expected['Comment'] == responses[0]['comment'], 'Insult'] = '1'
        expected.loc[expected['Comment'] == responses[0]['comment'], 'Status'] = 'LABELLED'
        expected.loc[expected['Comment'] == responses[0]['comment'], 'HIT ID'] = 'LOCAL'

        with create_temporary_copy(TEST_DATASET_PATH) as temp:
            update_dataset(temp.name, responses)
            new_dataset = pd.read_csv(temp.name)

            assert new_dataset.equals(expected)

    def test_update_dataset_with_multiple_responses(self):
        responses = [
            {'comment': 'Comment 1', 'is_insult': 0},
            {'comment': 'Comment 2', 'is_insult': 1}
        ]

        original_dataset = pd.read_csv(TEST_DATASET_PATH)
        expected = original_dataset
        expected.loc[expected['Comment'] == responses[0]['comment'], 'Insult'] = '0'
        expected.loc[expected['Comment'] == responses[1]['comment'], 'Insult'] = '1'
        expected.loc[expected['Comment'] == responses[1]['comment'], 'Status'] = 'LABELLED'
        expected.loc[expected['Comment'] == responses[1]['comment'], 'HIT ID'] = 'LOCAL'
        expected.loc[expected['Comment'] == responses[0]['comment'], 'Status'] = 'LABELLED'
        expected.loc[expected['Comment'] == responses[0]['comment'], 'HIT ID'] = 'LOCAL'

        with create_temporary_copy(TEST_DATASET_PATH) as temp:
            update_dataset(temp.name, responses)
            new_dataset = pd.read_csv(temp.name)

            assert new_dataset.equals(expected)
