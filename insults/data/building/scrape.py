import praw
from dataset import DatasetEntry, default_dataset_header, setup_dataset_file
from datetime import datetime
from criteria import validate_comment, validate_parent_comments
import os
import random


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATASET = os.path.join(PATH_TO_HERE, 'new_dataset.csv')

NUM_COMMENTS_TO_GRAB_PER_SUBMISSION = 10


def reservoir_sample(comments, N):
    """
    SOURCE: http://data-analytics-tools.blogspot.com.au/2009/09/reservoir-sampling-algorithm-in-perl.html
    Take N elements randomly from a comment list of unknown size.
    """
    sample = [];

    for i, comment in enumerate(comments):
        if i < N:
            sample.append(comment)
        elif (i >= N) and (random.random() < (N / float(i+1))):
            replace = random.randint(0,len(sample)-1)
            sample[replace] = comment

    for elem in sample:
        yield elem


def get_parents_of_reddit_comment(comment):
    previous_comment = comment.parent()
    if type(previous_comment) is praw.models.Submission:
        previous_comment = None
        previous_previous_comment = None
    else:
        previous_previous_comment = previous_comment.parent()
        if type(previous_previous_comment) is praw.models.Submission:
            previous_previous_comment = None

    previous_comment = previous_comment.body if previous_comment else None
    previous_previous_comment = previous_previous_comment.body if previous_previous_comment else None

    return previous_comment, previous_previous_comment


def scrape_reddit_defaults():
    setup_dataset_file(DEFAULT_DATASET, default_dataset_header())

    for subreddit in r.subreddits.default(limit=None):
        submissions = subreddit.hot(limit=15)

        for submission in submissions:
            print submission.title
            print submission.url
            print "=" * 30
            submission.comments.replace_more()
            comments = sorted(submission.comments.list(), key=lambda x: x.score)

            for comment in reservoir_sample(comments, NUM_COMMENTS_TO_GRAB_PER_SUBMISSION):
                if comment.body == '[removed]':
                    continue

                if not validate_comment(comment.body):
                    continue

                parent_comment, grandparent_comment = get_parents_of_reddit_comment(comment)

                if not validate_parent_comments(parent_comment, grandparent_comment):
                    continue

                entry = DatasetEntry(
                    comment=comment.body,
                    datetime=datetime.utcfromtimestamp(comment.created_utc),
                    is_insult=None,
                    usage=None,
                    source='reddit',
                    score=comment.score,
                    parent_comment=parent_comment,
                    grandparent_comment=grandparent_comment,
                    labels=None,
                    difficulty=None
                )
                entry.add_to_dataset()

            print "\n" * 1


if __name__ == '__main__':
    r = praw.Reddit(user_agent='my_cool_application',
                    client_id='Zeep1Q72XFf9HA',
                    client_secret='WADOW_Pyl7nlz8oHnBFerqBTWuY')

    scrape_reddit_defaults()
