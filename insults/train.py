import pandas
from sklearn import feature_extraction,linear_model, model_selection, pipeline
import numpy as np
import os
import itertools
import logging
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import concurrent.futures

from insults.util import (data_file,
                          data_directory,
                          log_file,
                          save_folds,
                          saved_folds,
                          argsets,
                          auc,
                          score,
                          save_model)
from insults.classifier import InsultsSGDRegressor

# Dataflow
# --------
#
# training file + parameters -> folds -> chosen parameters + performance estimates
# training file + chosen parameters -> model
# labeled test file + model -> predictions -> score
# unlabeled test file + model -> predictions

class InsultsPipeline(pipeline.Pipeline):
    """
    Custom version of scikit-learn's Pipeline class, with an extra method for
    use in tuning.
    """
    def staged_auc(self, X, y):
        """
        InsultsPipeline knows about staged_auc, which
        InsultsSGDRegressor implements and uses.
        """
        Xt = X
        for name, transform in self.steps[:-1]:
            Xt = transform.transform(Xt)
        return self.steps[-1][-1].staged_auc(Xt, y)


def get_estimates():
    estimate_file = data_file('Estimates','estimates.csv')
    if os.path.exists(estimate_file):
        v = pandas.read_table(estimate_file,sep=',')
        return zip(v.submission, v.estimate)
    else:
        return []

def save_estimates(se):
    estimate_file = data_file('Estimates', 'estimates.csv')
    submissions,estimates = zip(*se)
    pandas.DataFrame(dict(submission=submissions, estimate=estimates)).to_csv(estimate_file, index=False)


def make_full_training():
    df1 = pandas.read_table(data_file('Inputs','train.csv'),sep=',')
    df2 = pandas.read_table(data_file('Inputs','test_with_solutions.csv'),sep=',')
    df = pandas.concat([df1,df2])
    df.to_csv(data_file('Inputs','fulltrain.csv'),index=False)


def make_clf(args):
    return InsultsPipeline([
                    ('vect', feature_extraction.text.CountVectorizer(
                                                                     lowercase=False,
                                                                     analyzer='char',
                                                                     ngram_range=(1,5)
                                                                    )
                    ),
                    ('tfidf', feature_extraction.text.TfidfTransformer(sublinear_tf=True, norm='l2')),
                    ("clf",InsultsSGDRegressor(alpha=args.sgd_alpha,
                                               penalty=args.sgd_penalty,
                                               learning_rate='constant',
                                               eta0=args.sgd_eta0,
                                               max_iter=args.sgd_max_iter,
                                               n_iter_per_step=args.sgd_n_iter_per_step)
                    )
                ])


def choose_n_iterations(df, show=False):
    """
    work out how many iterations to use, using data stashed during tuning.
    """
    fi = df.mean(axis=1)
    chosen = fi.argmax() # used to be fi.index[fi.argmax()]. Think this was outdated
    logging.info("chose %d iterations, projected score %f" % (chosen,fi.max()))
    return chosen, fi.max()


def tune_one_fold(i, train_i, test_i):
    """
    Tune one fold of the data.
    """
    global train
    clf = make_clf(args)
    ftrain = train[train_i]
    logging.info('fold %d' % i)
    clf.fit(ftrain.Comment, ftrain.Insult)
    ypred = clf.predict(ftrain.Comment)
    logging.info("%d train auc=%f" % (i, auc(np.array(ftrain.Insult),ypred)))
    ypred = clf.predict(train[test_i].Comment)
    # record information about the auc at each stage of training.
    xs,ys = clf.staged_auc(train[test_i].Comment, train[test_i].Insult)
    xs = np.array(xs)
    ys = np.array(ys)
    return pandas.DataFrame({ ('auc%d' % i):ys}, index=xs)



NFOLDS=15

def initialize(args):
    """
    Set up the training and test data.
    """
    train = pandas.read_table(args.trainfile,sep=',')
    leaderboard = pandas.read_table(args.testfile,sep=',')
    return train,leaderboard

def join_frames(dfs):
    df = dfs[0]
    for df2 in dfs[1:]:
        df = df.join(df2)
    return df

def tuning(args):
    """
    Train the model, while holding out folds for use in
    estimating performance.
    """
    NUM_CORES = 4 # training on quad-core Mac Pro
    logging.info("Tuning")
    kf = model_selection.KFold(NFOLDS)

    folds = kf.split(train.Insult)
    boolean_folds = []
    for f in folds:
        mask_train, mask_test = np.zeros(len(train.Insult), dtype=bool), \
                                np.zeros(len(train.Insult), dtype=bool)
        mask_train[f[0]] = True
        mask_test[f[1]] = True
        boolean_folds.append((mask_train, mask_test))

    with ProcessPoolExecutor(max_workers=NUM_CORES) as executor:
        future_to_fold = dict([
                                (executor.submit(
                                                tune_one_fold,
                                                i,
                                                train_i,
                                                test_i
                                                ), i)
                                for i,(train_i,test_i)
                                in enumerate(boolean_folds)
                              ])

        df =  join_frames([
                            future.result()
                            for future
                            in concurrent.futures.as_completed(future_to_fold)
                          ])

    logging.info('tuning complete')

    return df


def predict(folds, args):
    """
    Train on training file, predict on test file.
    """
    logging.info("Starting predictions")

    clf = make_clf(args)
    # work out how long to train for final step.
    clf.steps[-1][-1].max_iter,estimated_score = choose_n_iterations(folds)
    clf.steps[-1][-1].reset_args()

    clf.fit(train.Comment, train.Insult) # train the classifier

    ypred = clf.predict(leaderboard.Comment) # use the trained classifier to classify comments

    submission = pandas.DataFrame(dict(Insult=ypred, Comment=leaderboard.Comment, Date=leaderboard.Date), columns=('Insult', 'Date', 'Comment'))

    if args.predictions == None:
        estimates = get_estimates()
        for x in itertools.count(1):
            filename = data_file("Submissions", "submission%d.csv" % x)
            if os.path.exists(filename):
                next
            else:
                submission.to_csv(filename,index=False)
                estimates.append((filename,estimated_score))
                save_estimates(estimates)
                logging.info('Saved %s' % filename)
                break
    else:
            submission.to_csv(args.predictions, index=False)
            logging.info('Saved %s' % args.predictions)

    save_model(clf) # Save the classifier
    logging.info("Finished predictions")


def run_prediction(parser=None,args_in=None,competition=False):
    """
    Either pick up the arguments from the command line or use the
    ones pre-packaged for the script.
    """
    global train
    global leaderboard

    if competition:
        logging.info('Running prepackaged arguments (%r)' % args_in)
        args = parser.parse_args(args_in)
    else:
        logging.info('Using arguments from command line %r' % args_in)
        args = args_in

    train,leaderboard = initialize(args)
    if args.tune:
        folds = tuning(args)
        save_folds(folds)
    else:
        folds = saved_folds()
    predict(folds,args)
    if args.score:
        score()


if __name__ == "__main__":
    competition_argsets = argsets['competition']
    tuning_argsets = argsets['tuning']


    parser = argparse.ArgumentParser(description="Generate a prediction about insults")
    parser.add_argument('--trainfile','-T',default=data_file('Inputs','train.csv'),help='file to train classifier on')
    parser.add_argument(
                            '--testfile','-t',
                            default=data_file('Inputs','test.csv'),
                            help='file to generate predictions for'
                        )
    parser.add_argument('--predictions','-p',default=None,help='destination for predictions (or None for default location)')
    parser.add_argument('--logfile','-l',
                        default=log_file('insults.log'),
                        help='name of logfile'
                        )
    parser.add_argument('--tune','-tu',
                        action='store_true',
                        help='if set, causes tuning step to occur'
                        )

    # linear classifier parameters
    parser.add_argument('--sgd_alpha','-sa',type=float,default=1e-5)
    parser.add_argument('--sgd_eta0','-se',type=float,default=0.005)
    parser.add_argument('--sgd_rho','-sr',type=float,default=0.999)
    parser.add_argument('--sgd_max_iter','-smi',type=int,default=1000)
    parser.add_argument('--sgd_n_iter_per_step','-sns',type=int,default=20)
    parser.add_argument('--sgd_penalty','-sp',default="elasticnet",help='l1 or l2 or elasticnet (default: %{default}s)')

    # other parameters.

    parser.add_argument('--competition','-c',action='store_true',help='make predictions for the final stage of the competition')
    parser.add_argument('--comptune','-ct', action='store_true',help='tuning for final stage')
    parser.add_argument('--score','-sc',action='store_true',dest='score',help='turn on print out of score at end', default=True)
    parser.add_argument('--no_score','-nsc',action='store_false',dest='score',help='turn off print out of score at end' )


    args = parser.parse_args()
    if args.competition:
        # Need to create directory
        log_dir = "Logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename=log_file('final.log'),mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        for argset in competition_argsets:
            run_prediction(parser=parser,args_in=argset,competition=True)
    elif args.comptune:
        logging.basicConfig(filename=args.logfile,mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        for argset in tuning_argsets:
            run_prediction(parser=parser,args_in=argset,competition=True)
    else:
        logging.basicConfig(filename=args.logfile,mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        run_prediction(parser=parser,args_in=args,competition=False)
