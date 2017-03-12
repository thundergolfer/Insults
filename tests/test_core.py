import pytest
import numpy as np

from numpy.testing import assert_equal, assert_array_almost_equal, assert_almost_equal
from insults import core

insult = core.Insults()


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
