import praw

def scrape_defaults():
    for subreddit in r.subreddits.default(limit=None):
        submissions = subreddit.hot(limit=15)

        for submission in submissions:
            print submission.title
            print submission.url
            print "=" * 30
            submission.comments.replace_more()
            comments = sorted(submission.comments, key=lambda x: x.score)

            for comment in comments[0:6]:
                print comment.body
                print "score: " + str(comment.score)
                print "#" * 10
                
            print "\n" * 1


if __name__ == '__main__':
    r = praw.Reddit(user_agent='my_cool_application',
                    client_id='Zeep1Q72XFf9HA',
                    client_secret='WADOW_Pyl7nlz8oHnBFerqBTWuY')

    scrape_defaults()
