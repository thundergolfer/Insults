from praw.models import Submission, Comment
from mock import patch
import os

from insults.data.building.scrape import (reservoir_sample,
                                          get_parents_of_reddit_comment,
                                          scrape_reddit_defaults,
                                          scrape_subreddit)


class MockReddit():
    def __init__(self):
        self.subreddits= MockSubredditsCollection()

class MockSubredditsCollection():
    def default(self, limit=None):
        return ['awww', 'funny', 'politics', 'jonathon']

class MockPrawComment():
    def __init__(self, parent_is_comment=True, grandparent_is_comment=True):
        self.body = "Has parent" if parent_is_comment else "This is it"
        self.parent_is_comment = parent_is_comment
        self.grandparent_is_comment = grandparent_is_comment

    def parent(self):
        if self.parent_is_comment and self.grandparent_is_comment:
            return MockPrawComment(parent_is_comment=True, grandparent_is_comment=False)
        if self.parent_is_comment:
            return MockPrawComment(parent_is_comment=False, grandparent_is_comment=False)
        else:
            return Submission(None, id='does not matter')

class TestReservoirSample():

    def gives_back_N_elements(self):
        test_list = [1, 2, 4, 5, 6, 7, 9, 10]
        N = 5

        result = reservoir_sample(test_list, N)
        assert 5 == len(result)

        test_list = ["Hello", "My", "Friend", "and", "confidant"]
        N = 1

        result = reservoir_sample(test_list, N)
        assert 1 == len(result)
        assert result[0] in test_list


class TestGetParentsOfRedditComment():

    def test_comment_is_parent(self):
        parent, grandparent = get_parents_of_reddit_comment(MockPrawComment(parent_is_comment=False))
        assert parent is None and grandparent is None

    def test_comment_has_parent(self):
        parent, grandparent = get_parents_of_reddit_comment(MockPrawComment(parent_is_comment=True,
                                                                            grandparent_is_comment=False))
        assert parent == "This is it"
        assert grandparent is None

    def test_comment_has_parent_and_grandparent(self):
        parent, grandparent = get_parents_of_reddit_comment(MockPrawComment(parent_is_comment=True,
                                                                            grandparent_is_comment=True))
        assert parent == "Has parent"
        assert grandparent == "This is it"


class TestScrapeRedditDefaults():
    TEST_DATASET_PATH = 'testa.csv'
    #
    # @classmethod
    # def teardown_class(cls):
    #     os.remove(cls.TEST_DATASET_PATH)

    @patch('insults.data.building.scrape.scrape_subreddit', return_value=True)
    @patch('insults.data.building.scrape.setup_dataset_file')
    def test_calls_setup_dataset_and_scrape_subreddits(self, mock, mock_scrape):
        scrape_reddit_defaults(MockReddit(), dataset_path=self.TEST_DATASET_PATH)
        mock.assert_called()
        # calls scrape_subreddit() for each sub returned by reddit.subreddits.default
        assert 4 == mock_scrape.call_count
