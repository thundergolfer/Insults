import pytest
import numpy as np
from mock import patch
import random

from numpy.testing import assert_equal, assert_array_almost_equal, assert_almost_equal
from insults.core import Insults


class MockModel():
    def predict(self, comments):
        return [random.uniform(0, 1) for x in range(len(comments))]


class DeterministicMockModel():
    def __init__(self, rankings=None):
        self.rankings = rankings if rankings else [0.1, 0.33, 0.332, 0.4, 0.9, 0.87, 0.31, 0.123, 0.56, 0.04]

    def predict(self, comments):
        return self.rankings[:len(comments)]

@pytest.fixture(scope="module")
def smtp(request):
    smtp = smtplib.SMTP("smtp.gmail.com")
    yield smtp  # provide the fixture value
    print("teardown smtp")
    smtp.close()

Insults.clf = MockModel()


class TestRateComments():
    def test_rate_comment(self):
        assert isinstance(Insults.rate_comment("This is a comment"), (int, long, float))

    def test_rate_comment_binary(self):
        assert isinstance(Insults.rate_comment("This is a comment", True), int)
        assert Insults.rate_comment("This is a comment", True) in [0, 1]


class TestCheckupUser():

    @classmethod
    def setup_class(cls):
        Insults.clf = DeterministicMockModel([0.13, 0.10, 0.89, 0.50, 0.49, 0.21, 0.29])
        Insults.classifier_threshold = 0.50

    @classmethod
    def teardown_class(cls):
        Insults.clf = MockModel()
        Insults.classifier_threshold = 0.50

    test_user_comments = ["Hey, this is a first comment on Reddit!",
                          "I really like Tatum in this film. He's been solid lately ay?",
                          "Get out of here you stinky fucking facist.",
                          "I love the internet. Let's get it on niggas. Peace",
                          "Get yourself a bike and ride off. You're not wanted here bitch",
                          "911 was an inside job get the awareness out ppl this is true and real",
                          "Nooooooooooo that's the one thing we didn't want to happen."]

    def test_checkup_user_empty(self):
        percentage_insulting, insults, worst = Insults.checkup_user([])

        assert percentage_insulting is None and insults == [] and worst == []

    def test_checkup_user(self):
        percentage_insulting, insults, worst = Insults.checkup_user(self.test_user_comments)

        assert percentage_insulting == 2/7.0
        assert self.test_user_comments[2] in insults and self.test_user_comments[3] in insults
        assert_equal([self.test_user_comments[2], self.test_user_comments[3]], worst)


class TestCheckupGroup():
    @classmethod
    def setup_class(cls):
        Insults.clf = DeterministicMockModel([0.13, 0.10, 0.89, 0.50, 0.49, 0.21, 0.29])
        Insults.classifier_threshold = 0.50

    @classmethod
    def teardown_class(cls):
        Insults.clf = MockModel()
        Insults.classifier_threshold = 0.50

    def test_checkup_user_empty(self):
        percentage_insulting, insults, worst = Insults.checkup_group([])

        assert percentage_insulting is None and insults == [] and worst == []

class TestWorstComments():

    test_comments = ["This is a good comment. I love you.",
                     "This is an evil comment. Kill yourself you cuck.",
                     "I don't think we should see each other anymore. Go away.",
                     "Lyndon Johnson was an American president, I think.",
                     "Maybe he actually wasn't.",
                     "No, I'm reasonably sure he was. I remember him. The blonde, ugly one."]

    def test_worst_comments(self):
        results_default = Insults.worst_comments(self.test_comments)

        assert len(results_default) == 3

        assert len(Insults.worst_comments(self.test_comments, limit=2)) == 2

        assert isinstance(results_default[0][0], str)
        assert isinstance(results_default[0][1], (int, float, long))


    def test_worst_comments_ranking(self):
        pass


class TestFoulLanguage():
    def test_foul_language_with_context(self):
        test_strings = ["I think you're a fucking terrible person. I won't apologise for it.",
                        "Shit, this is the greatest thing ever. I luv the interwebs."]

        foul_words, context = Insults.foul_language(test_strings)
        assert_equal(foul_words, ['fucking', 'shit'])
        assert_equal(context, ["I think you're a fucking terrible person.", "Shit, this is the greatest"])

    def test_foul_language_no_context(self):
        test_string = """I think the word fuck is a foul word, as is the word cunt."""

        foul_words, _ = Insults.foul_language([test_string], context=False)

        assert_equal(foul_words, ['fuck', 'cunt'])

    def test_foul_language_clean_comment(self):
        test_string = """This is a perfectly pleasant comment. It's about sunshine and flowers."""

        foul_words, _ = Insults.foul_language([test_string], context=False)

        assert_equal(foul_words, [])

    def test_foul_language_foul_words_as_substrings(self):
        test_string = """shitake scunthorpe amassed sniggeringly"""

        foul_words, _ = Insults.foul_language([test_string], context=False)

        assert_equal(foul_words, [])

    def test_foul_language_quoted_swear_words(self):
        test_string = """You said "fuck off" to me, and I though that was unacceptable."""
        test_string_two = """I didn't say 'fuck'."""

        foul_words, _ = Insults.foul_language([test_string], context=False)
        foul_words_two, _ = Insults.foul_language([test_string_two], context=False)

        assert_equal(foul_words, [])
        assert_equal(foul_words_two, [])
