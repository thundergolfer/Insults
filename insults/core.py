from insults import classifier
from insults.word_lists.google_bad_words import badwords
from insults.word_lists.racist_words import racist_list
from insults.train import run_prediction
from insults.util import argsets
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

    def __init__(self, threshold=None):
        self.clf  = classifier.load_model()
        self.threshold = threshold if threshold else Insults.classifier_threshold
        # what else?

    def build_model(self):
        for argset in argsets['competition']:
            run_prediction(parser=parser,args_in=argset,competition=True)

    def rate_comment(self, comment, binary=False):
        prediction = self._rate_comments( comment )[0]
        if binary:
            return 1 if prediction >= self.threshold else 0
        return prediction

    def checkup_user( comments ):
        raise NotImplementedError

    def checkup_group( comments, commenters=None, scores=None):
        raise NotImplementedError

    def worst_comments( comments, limit=3):
        preds = self._rate_comments( comments )
        worst_comment_indexes = sorted(range(len(preds)), key=lambda x: preds[x])[-limit:] # highest score
        worst = []
        for i in worst_comment_indexes:
            worst.append( (comments[i], preds[i]) )
        return worst

    def racism( comments, commenters=None, scores=None):
        raise NotImplementedError

    def sexism( comments, commenters=None, scores=None):
        raise NotImplementedError

    def foul_language( comments, context=True ):
        # Quoted ('' or "") words are unlikely to be used in
        # a pejorative way
        foul_words, comment_context = [], []
        for c in comments:
            tokens = word_tokenize(c)
            for i, curr_token in enumerate(tokens):
                if i == 0:
                    prev_token = ""
                    next_token = tokens[i+1]
                elif i == len(tokens) - 1:
                    prev_token = tokens[i-1]
                    next_token = ""
                else:
                    prev_token = tokens[i-1]
                    next_token = tokens[i+1]

                quoted = False
                if curr_token.lower() in bad_words:
                    if prev_token.endswith(("'", '"')):
                        if curr_token.endswith(("'",'"')) or next_token.startswith(("'",'"')):
                            quoted = True
                    elif curr_token.startswith(("'",'"')):
                        if curr_token.endswith(("'",'"')) or next_token.startswith(("'",'"')):
                            quoted = True
                if not quoted:
                    foul_words.append(curr_token.lower())
                    if context:
                        token_i = c.index(curr_token)
                        comment_context.append(c[token_i-20:token_i+20])
        if context:
            return foul_words, comment_context
        else:
            return foul_words, None


    def _rate_comments( comments ):
        predictions = []
        for c in list(comments): # listify a single comment if needed
            predictions.append(self.clf.predict(c))
        return predictions

    def _detect_racism( comment ):
        raise NotImplementedError

    def _detect_sexism( comment ):
        raise NotImplementedError
