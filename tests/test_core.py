import pytest
import numpy as np
from mock import patch

from numpy.testing import assert_equal, assert_array_almost_equal, assert_almost_equal
from insults import core

insult = core.Insults()


def test_rate_comment():
    assert isinstance(insult.rate_comment("This is a comment"), (int, long, float))

def test_rate_comment_binary():
    assert isinstance(insult.rate_comment("This is a comment", True), int)
    assert insult.rate_comment("This is a comment", True) in [0, 1]

def test_worst_comments():
    test_comments = ["This is a good comment. I love you.",
                     "This is an evil comment. Kill yourself you cuck.",
                     "I don't think we should see each other anymore. Go away.",
                     "Lyndon Johnson was an American president, I think.",
                     "Maybe he actually wasn't.",
                     "No, I'm reasonably sure he was. I remember him. The blonde, ugly one."]

    results_default = insult.worst_comments(test_comments)

    assert len(results_default) == 3

    assert len(insult.worst_comments(test_comments, limit=2)) == 2

    assert isinstance(results_default[0][0], str)
    assert isinstance(results_default[0][1], (int, float, long))

def test_foul_language_no_context():
    test_string = """I think the word fuck is a foul word, as is the word cunt."""

    foul_words, _ = insult.foul_language([test_string], context=False)

    assert_equal(foul_words, ['fuck', 'cunt'])

def test_foul_language_clean_comment():
    test_string = """This is a perfectly pleasant comment. It's about sunshine and flowers."""

    foul_words, _ = insult.foul_language([test_string], context=False)

    assert_equal(foul_words, [])

def test_foul_language_foul_words_as_substrings():
    test_string = """shitake scunthorpe amassed sniggeringly"""

    foul_words, _ = insult.foul_language([test_string], context=False)

    assert_equal(foul_words, [])

def test_foul_language_quoted_swear_words():
    test_string = """You said "fuck off" to me, and I though that was unacceptable."""
    test_string_two = """I didn't say 'fuck'."""

    foul_words, _ = insult.foul_language([test_string], context=False)
    foul_words_two, _ = insult.foul_language([test_string_two], context=False)

    assert_equal(foul_words, [])
    assert_equal(foul_words_two, [])
