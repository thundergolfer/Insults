from insults import classifier
from insults.word_lists.google_bad_words import bad_words
from insults.word_lists.racist_words import racist_list
from insults.train import run_prediction
from insults.util import argsets, load_model, get_parser, data_file

import pandas as pd
from nltk.tokenize import word_tokenize


# API Notes
# - is 1 comment insulting or not?
# - is a certain user/person insulting people?
#   - num insults
#   - % (percentage)
#   - average score
#   - 0-100 ratings
# - how bad is a community for insults?
# - what are the popular insults or phrases
# - worst comment from a group
# - racist comments
# - sexist comments
# - foul language

class Insults(object):
    """
    The package's API object.
    """

    classifier_threshold = 0.5
    clf = None

    @classmethod
    def load_model(cls):
        clf = load_model()

    @classmethod
    def build_model(cls):
        """
        Train the supervised classifier to prepare the Insults library for use.
        """
        parser = get_parser() # TODO
        for argset in argsets['competition']:
            run_prediction(parser=parser,args_in=argset,competition=True)

    @classmethod
    def rate_comment(cls, comment, binary=False):
        """
        Assess a comment using the Insults supervised classifier.

        Args:
            comment (string): a comment, preferably a sentence, and not a paragraph

        Returns:
            int/float: the classifier's score (0 -> not an insult, 1 -> insult)
        """

        prediction = cls._rate_comments( comment )[0]
        if binary:
            return 1 if prediction >= cls.classifier_threshold else 0
        return prediction

    @classmethod
    def checkup_user(cls, comments ):
        """
        Assesses a single user's use of insults, and identifies their comments most likely
        to be considered insulting.

        Args:
            comments (list): a collection of comments from the user

        Returns:
            tuple: % of comments that are insulting, list of insulting comments, 'worst' comments

        """

        ratings = cls._rate_comments(comments)
        rated_comments = zip(comments, ratings).sort(key=lambda x: x[1], reverse=True)

        insults = [i[0] for i in rated_comments if i[1] >= cls.classifier_threshold].sort(key=lambda x: x[1], reverse=True)
        LIMIT_WORST = 3

        return len(insults)/float(len(comments)), insults, insults[:LIMIT_WORST]

    @classmethod
    def checkup_group(cls, comments, commenters=None, scores=None):
        """
        Assesses a group's use of insulting comments, and identifies users who most
        strongly are indicated to employ insults.

        Args:
            comments (list): a collection of comments, assumedly from a cohesive group (eg. subreddit)
            commenters (list): commenter IDs associated with each commenter
            scores (list): scores/points (eg. upvotes) associated with each comment

        Returns:
            tuple: % of comments that are insulting, list of 'problem users', 'worst' comments
        """

        ratings = cls._rate_comments(comments)
        rated_comments_with_authors = zip(comments, ratings, commenters).sort(key=lambda x: x[1], reverse=True)

        rated_insults_with_authors = [i for i in rated_comments_with_authors if i[1] > cls.classifier_threshold].sort(key=lambda x: x[1], reverse=True)
        users_insults_tallied = Counter([i[2] for i in rated_insults_with_authors])
        # problem_users = sorted(list(users_tallied), key=lambda x: users_tallied[x], reverse=True)
        problem_users = [user for user in users_insults_tallied if users_insults_tallied[user] > 3] # TODO bit arbitrary

        LIMIT_WORST = 3

        return len(rated_insults_with_authors)/len(comments), problem_users, rated_insults_with_authors[:LIMIT_WORST]

    @classmethod
    def worst_comments(cls, comments, limit=3):
        """
        Finds and returns a specified subset of a comment list that have been
        ranked by the Insults supervised classifier to be most likely insulting.

        Note:   This doesn't necessarily return the 'worst' comments, it more accurately
                returns the comments which score highest by the classifier.

        Args:
            comments (list): list of comments to be assessed
            limit (int): how many 'worst' comments to return

        Returns:
            list (tuple): worst comments alongside the classifier's score for them
        """

        preds = cls._rate_comments( comments )
        worst_comment_indexes = sorted(range(len(preds)), key=lambda x: preds[x])[-limit:] # highest score
        worst = []
        for i in worst_comment_indexes:
            worst.append( (comments[i], preds[i]) )
        return worst

    @classmethod
    def racism(cls, comments, commenters=None, scores=None):
        """
        Finds racist comments using a combination of the Insults supervised
        classifier and a racist term search.

        Args:
            comments (list): list of comments to be assessed
            commenters (list): a commenter id associated with each comment
            scores (list): the score (eg. upvotes) associated with each comment

        Returns:
            list: comments which have been detected to be racist
        """
        raise NotImplementedError

    @classmethod
    def sexism(cls, comments, commenters=None, scores=None):
        """
        Finds racist comments using a combination of the Insults supervised
        classifier and a sexist term search.

        Args:
            comments (list): list of comments to be assessed
            commenters (list): a commenter id associated with each comment
            scores (list): the score (eg. upvotes) associated with each comment

        Returns:
            list: comments which have been detected to be sexist
        """
        raise NotImplementedError

    @classmethod
    def foul_language(cls, comments, context=True, target_set=None ):
        """
        Finds all *direct* use of foul language in a list of comments.

        Args:
            comments (list): list of comments to be assessed
            context (bool): whether to return context snippets
            target_set (set): collection of words to search for

        Returns:
            tuple (list, list): all foul words found, and optionally their context
        """
        # Quoted ('' or "") words are unlikely to be used in
        # a pejorative way
        target_set = target_set if target_set else bad_words

        foul_words, comment_context = [], []
        for c in comments:
            tokens = word_tokenize(c) # this doesn't handle quote chars properly
            quote_stack = []
            for i, curr_token in enumerate(tokens):
                quoted = False
                if curr_token in ["''", "'", '"', '``']:
                    if len(quote_stack) == 0:
                        quote_stack.append(curr_token)
                    elif quote_stack[-1] == curr_token:
                        del quote_stack[-1]
                    else:
                        quote_stack.append(curr_token)
                # import pdb; pdb.set_trace()
                if curr_token.lower() in target_set:
                    if len(quote_stack) == 0: # not within quotes
                        foul_words.append(curr_token.lower())
                        if context:
                            token_i = c.index(curr_token)
                            comment_context.append(c[token_i-20:token_i+20])
        if context:
            return foul_words, comment_context
        else:
            return foul_words, None


    @classmethod
    def _rate_comments(cls, comments ):
        if not isinstance(comments, list):
            comments = [comments]
        # import pdb; pdb.set_trace()
        # predictions = cls.clf.predict(pd.Series(comments, name="Comment"))
        stuff = pd.read_table(data_file('Inputs',"final.csv"),sep=',')
        predictions = cls.clf.predict(stuff.Comment.append(pd.Series(comments)))
        return predictions[-len(comments):] # Hack to get around scale_predictions()

    @classmethod
    def _detect_racism(cls, comment ):
        racist_words, context = cls.foul_language([comment], True, racist_list)

        return cls._rate_comments(comment), racist_words, context

    @classmethod
    def _detect_sexism(cls, comment ):
        sexist_words, context = cls.foul_language([comment], True, sexist_list)

        return cls._rate_comments(comment), sexist_words, context
