from datetime import datetime
import os
import shutil
import tempfile
import pytest

from insults.data.building.dataset import (default_dataset_header,
                                           setup_dataset_file,
                                           csv_entry_to_dict,
                                           DatasetEntry)


TEST_DATASET_PATH = '/Users/jbelotti/Code/thundergolfer/Insult/tests/data/support/test_dataset.csv'


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


def test_default_dataset_header():
    assert [
        'Comment',
        'Date',
        'Insult',
        'Usage',
        'Source',
        'Score',
        'Parent Comment',
        'Grandparent Comment',
        'Status',
        'Labels',
        'Difficulty',
        'HIT ID'
    ] == default_dataset_header()


def test_setup_dataset_file():
    test_schema = ['one', 'two', 'three', 'four']
    temp_fp = 'to_delete.csv'
    setup_dataset_file(temp_fp, test_schema)

    with open(temp_fp, 'r') as temp:
        new_dataset_contents = temp.read()

    assert 'one,two,three,four\r\n' == new_dataset_contents

    os.remove(temp_fp)


def test_setup_dataset_file_which_already_exists():
    # TODO: current the function will just do nothing
    pass


def test_csv_entry_to_dict():
    test_row = ['one', 'two', 'three', 'four']
    test_csv_header = ['FIRST', 'SECOND', 'THIRD', 'FOUR']

    expected = {
        'FIRST': 'one',
        'SECOND': 'two',
        'THIRD': 'three',
        'FOUR': 'four'
    }

    assert expected == csv_entry_to_dict(test_row, test_csv_header)


def test_csv_entry_to_dict_invalid_input():
    test_row = ['one', 'two', 'three']
    test_csv_header = ['FIRST', 'SECOND', 'THIRD', 'FOUR']

    with pytest.raises(ValueError):
        csv_entry_to_dict(test_row, test_csv_header)


class TestDatasetEntry():

    entry = DatasetEntry(
        comment='This is the comment',
        datetime=datetime(2016, 9, 1, 0, 0),
        is_insult=True,
        usage=None,
        source='reddit',
        score=1000,
        parent_comment='This is the parent comment',
        grandparent_comment=None,
        status='READY',
        labels=None,
        difficulty=None
    )

    @classmethod
    def setup_class(cls):
        pass

    def test_add_to_dataset(self):
        with create_temporary_copy(TEST_DATASET_PATH) as fp:
            original_state = fp.read()
            fp.seek(0)

            self.entry.add_to_dataset(dataset_path=fp.name)

            new_state = fp.read()

        expected_state = original_state + "This is the comment,20160901000000Z,1,None,reddit,1000,This is the parent comment,,READY,,,\r\n"

        assert expected_state == new_state

    def test_csv_row(self):
        expected = [
            'This is the comment',
            '20160901000000Z',
            '1',
            'None',
            'reddit',
            '1000',
            'This is the parent comment',
            '',
            'READY',
            '',
            '',
            ''
        ]

        assert expected == self.entry.to_csv_row()
        assert all(isinstance(x, basestring) for x in self.entry.to_csv_row())

    # Testing private, but important, validation functions

    def test__validate_comment(self):
        comment = "This is a string so it is valid"
        result = self.entry._validate_comment(comment)

        assert comment == result

    def test__validate_comment_on_invalid_input(self):
        comment = 1000

        with pytest.raises(ValueError):
            result = self.entry._validate_comment(comment)

    def test__validate_source(self):
        source = "reddit"
        result = self.entry._validate_source(source)

        assert source == result

    def test__validate_source_on_invalid_input(self):
        source = "Facebook" # not in current valid sources set

        with pytest.raises(ValueError):
            result = self.entry._validate_source(source)

    def test__validate_score(self):
        source, score = 'reddit', 1000

        assert score == self.entry._validate_score(source, score)

    def test__validate_is_insult(self):
        assert 'NOT LABELLED' == self.entry._validate_is_insult(None)
        assert 1 == self.entry._validate_is_insult(True)
        assert 0 == self.entry._validate_is_insult(False)

    def test__validate_is_insult_on_invalid_input(self):
        with pytest.raises(ValueError):
            self.entry._validate_is_insult('It is an insult')

    def test__validate_a_parent_comment(self):
        assert '' == self.entry._validate_a_parent_comment(None)
        assert 'Hello my friend' == self.entry._validate_a_parent_comment('Hello my friend')

    def test__validate_a_parent_comment_on_invalid_input(self):
        with pytest.raises(ValueError):
            self.entry._validate_a_parent_comment(1000)

    def test__validate_labels(self):
        assert [] == self.entry._validate_labels(None)

    def test__validate_labels_on_invalid_input(self):
        with pytest.raises(ValueError):
            assert ['Hello', 'World'] == self.entry._validate_labels(['Hello', 'World'])
