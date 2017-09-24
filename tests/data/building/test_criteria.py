# coding=utf-8
import pytest

from insults.data.building.criteria import (validate_comment,
                                            validate_parent_comments,
                                            validate_dataset_criteria_config)

TEST_CONFIG = {
  "min_comment_length": 3,
  "max_comment_length": 700,
  "allowed_languages": ["en"]
}

class TestValidateComment():

    def test_valid_comment(self):
        comment = "You are a disgusting maggot of a person"

        assert validate_comment(comment, config=TEST_CONFIG)

    def test_comment_that_is_too_long(self):
        comment = "*" * (TEST_CONFIG['max_comment_length'] + 1)

        assert not validate_comment(comment, config=TEST_CONFIG)

    def test_comment_that_is_too_short(self):
        comment = "" # no config should let this comment through

        assert not validate_comment(comment, config=TEST_CONFIG)

    def test_comment_that_is_in_invalid_language(self):
        comment = "Mieux vaut prévenir que guérir".decode('utf-8')

        assert not validate_comment(comment, config=TEST_CONFIG)


class TestValidateParentComment():

    def test_no_parents(self):
        assert validate_parent_comments(None, None)

    def test_no_parent(self):
        assert validate_parent_comments(None, "This should be fine")

    def test_no_grandparent(self):
        assert validate_parent_comments("This should be fine", None)

    def test_invalid_parent(self):
        comment = "*" * (TEST_CONFIG['max_comment_length'] + 1)
        assert not validate_parent_comments(comment, None)

    def test_invalid_grandparent(self):
        comment = "*" * (TEST_CONFIG['max_comment_length'] + 1)
        assert not validate_parent_comments(None, comment)


class TestValidateDatasetCriteriaConfig():

    def test_missing_min_comment_length(self):
        config = {
          "max_comment_length": 700,
          "allowed_languages": ["en"]
        }

        with pytest.raises(ValueError):
            validate_dataset_criteria_config(config)

    def test_missing_max_comment_length(self):
        config = {
          "min_comment_length": 7,
          "allowed_languages": ["en"]
        }

        with pytest.raises(ValueError):
            validate_dataset_criteria_config(config)

    def test_missing_allowed_lang(self):
        config = {
          "min_comment_length": 3,
          "max_comment_length": 700,
        }

        with pytest.raises(ValueError):
            validate_dataset_criteria_config(config)

    def test_langs_spec_not_list(self):
        config = {
          "min_comment_length": 3,
          "max_comment_length": 700,
          "allowed_languages": "en"
        }

        with pytest.raises(ValueError):
            validate_dataset_criteria_config(config)

    def test_valid_config(self):
        config = {
          "min_comment_length": 1,
          "max_comment_length": 1000,
          "allowed_languages": ["en", "ab", "bc"]
        }

        assert validate_dataset_criteria_config(config)
