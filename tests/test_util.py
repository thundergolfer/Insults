import pytest
import numpy as np

from numpy.testing import assert_equal, assert_array_almost_equal, assert_almost_equal
from insults import util


def test_data_file():
    path = util.data_file("test_category")
    path_two = util.data_file("test_category", name="test_name")

    assert path.endswith('insults/data/test_category')
    assert path_two.endswith('insults/data/test_category/test_name')

def test_data_directory():
    path = util.data_file("test_category")

    assert path.endswith('insults/data/test_category')

def test_log_file():
    log_f = util.log_file("test_name")

    assert log_f.endswith('insults/logs/test_name')
