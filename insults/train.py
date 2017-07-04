import pandas
from sklearn import model_selection
import numpy as np
import os
import itertools
import logging
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import concurrent.futures

from insults.util import (data_file,
                          data_directory,
                          log_file,
                          save_folds,
                          saved_folds,
                          argsets,
                          auc,
                          score,
                          save_model,
                          get_parser)
from insults.pipeline import make_pipeline

# Dataflow
# --------
#
# training file + parameters -> folds -> chosen parameters + performance estimates
# training file + chosen parameters -> model
# labeled test file + model -> predictions -> score
# unlabeled test file + model -> predictions



NFOLDS=15


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


def choose_n_iterations(df, show=False):
    """
    work out how many iterations to use, using data stashed during tuning.
    """
    fi = df.mean(axis=1)
    chosen = fi.argmax() # used to be fi.index[fi.argmax()]. Think this was outdated
    logging.info("chose %d iterations, projected score %f" % (chosen,fi.max()))
    return chosen, fi.max()


def tune_one_fold(options, i, train_i, test_i):
    """
    Tune one fold of the data.
    """
    global train
    clf = make_pipeline(options)
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


def initialize(arguments):
    """
    Set up the training and test data.
    """
    train = pandas.read_table(arguments.trainfile,sep=',')
    test_examples = pandas.read_table(arguments.testfile,sep=',')
    return train, test_examples


def join_frames(dfs):
    df = dfs[0]
    for df2 in dfs[1:]:
        df = df.join(df2)
    return df


def tuning(arguments):
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
                                                arguments,
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


def predict(folds, arguments):
    """
    Train on training file, predict on test file.
    """
    logging.info("Starting predictions")

    clf = make_pipeline(arguments)
    # work out how long to train for final step.
    clf.steps[-1][-1].max_iter,estimated_score = choose_n_iterations(folds)
    clf.steps[-1][-1].reset_args()
    clf.fit(train.Comment, train.Insult) # train the classifier
    ypred = clf.predict(test_examples.Comment) # use the trained classifier to classify comments

    submission = pandas.DataFrame(dict(Insult=ypred, Comment=test_examples.Comment, Date=test_examples.Date), columns=('Insult', 'Date', 'Comment'))

    if arguments.predictions == None:
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
            submission.to_csv(arguments.predictions, index=False)
            logging.info('Saved %s' % arguments.predictions)

    save_model(clf) # Save the classifier
    logging.info("Finished predictions")


def run_prediction(parser=None,args_in=None,competition=False):
    """
    Either pick up the arguments from the command line or use the
    ones pre-packaged for the script.
    """
    global train
    global test_examples

    if competition:
        logging.info('Running prepackaged arguments (%r)' % args_in)
        arguments = parser.parse_args(args_in)
    else:
        logging.info('Using arguments from command line %r' % args_in)
        arguments = args_in

    train,test_examples = initialize(arguments)
    if arguments.tune:
        folds = tuning(arguments)
        save_folds(folds)
    else:
        folds = saved_folds()
    predict(folds,arguments)
    if arguments.score:
        score()


if __name__ == "__main__":
    competition_argsets = argsets['competition']
    tuning_argsets = argsets['tuning']

    parser = get_parser()
    arguments = parser.parse_args()

    if arguments.competition:
        # Need to create directory
        log_dir = "Logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename=log_file('final.log'),mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        for argset in competition_argsets:
            run_prediction(parser=parser,args_in=argset,competition=True)
    elif arguments.comptune:
        logging.basicConfig(filename=arguments.logfile,mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        for argset in tuning_argsets:
            run_prediction(parser=parser,args_in=argset,competition=True)
    else:
        logging.basicConfig(filename=arguments.logfile,mode='w',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        run_prediction(parser=parser,args_in=args,competition=False)
