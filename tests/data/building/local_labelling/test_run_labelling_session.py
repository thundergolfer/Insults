from contextlib import contextmanager
from mock import patch

from insults.data.building.local_labelling.run_labelling_session import gather_entries_to_label, get_label

TEST_DATASET_PATH = '/Users/jbelotti/Code/thundergolfer/Insult/tests/data/support/test_dataset.csv'


@contextmanager
def mockRawInput(mock):
    original_raw_input = __builtins__.raw_input
    __builtins__.raw_input = lambda _: mock
    yield
    __builtins__.raw_input = original_raw_input


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

    def test_correctly_handles_good_input(self):
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
