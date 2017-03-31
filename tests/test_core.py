import pytest
import numpy as np
from mock import patch
import random

from numpy.testing import assert_equal, assert_array_almost_equal, assert_almost_equal
from insults.core import Insults


# class mockModel():
#     def predict(self, comments):
#         return [random.uniform(0, 1) for x in range(len(comments))]
#
# Insults.clf = mockModel()
#
# def test_rate_comment():
#     assert isinstance(Insults.rate_comment("This is a comment"), (int, long, float))
#
#
# def test_rate_comment_binary():
#     assert isinstance(Insults.rate_comment("This is a comment", True), int)
#     assert Insults.rate_comment("This is a comment", True) in [0, 1]
#
# class TestWorstComments():
#
#     test_comments = ["This is a good comment. I love you.",
#                      "This is an evil comment. Kill yourself you cuck.",
#                      "I don't think we should see each other anymore. Go away.",
#                      "Lyndon Johnson was an American president, I think.",
#                      "Maybe he actually wasn't.",
#                      "No, I'm reasonably sure he was. I remember him. The blonde, ugly one."]
#
#     def test_worst_comments(self):
#         results_default = Insults.worst_comments(self.test_comments)
#
#         assert len(results_default) == 3
#
#         assert len(Insults.worst_comments(self.test_comments, limit=2)) == 2
#
#         assert isinstance(results_default[0][0], str)
#         assert isinstance(results_default[0][1], (int, float, long))
#
#
#     def test_worst_comments_ranking(self):
#         class DeterministicMockModel():
#             def predict(self, comments):
#                 rankings = [0.1, 0.33, 0.332, 0.4, 0.9, 0.87, 0.31, 0.123, 0.56, 0.04]
#                 return rankings[:len(comments)]
#         pass
#
#
# def test_foul_language_no_context():
#     test_string = """I think the word fuck is a foul word, as is the word cunt."""
#
#     foul_words, _ = Insults.foul_language([test_string], context=False)
#
#     assert_equal(foul_words, ['fuck', 'cunt'])
#
# def test_foul_language_clean_comment():
#     test_string = """This is a perfectly pleasant comment. It's about sunshine and flowers."""
#
#     foul_words, _ = Insults.foul_language([test_string], context=False)
#
#     assert_equal(foul_words, [])
#
# def test_foul_language_foul_words_as_substrings():
#     test_string = """shitake scunthorpe amassed sniggeringly"""
#
#     foul_words, _ = Insults.foul_language([test_string], context=False)
#
#     assert_equal(foul_words, [])
#
# def test_foul_language_quoted_swear_words():
#     test_string = """You said "fuck off" to me, and I though that was unacceptable."""
#     test_string_two = """I didn't say 'fuck'."""
#
#     foul_words, _ = Insults.foul_language([test_string], context=False)
#     foul_words_two, _ = Insults.foul_language([test_string_two], context=False)
#
#     assert_equal(foul_words, [])
#     assert_equal(foul_words_two, [])
