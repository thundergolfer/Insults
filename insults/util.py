import argparse
import errno
import pandas
import os
import numpy as np
from sklearn.externals import joblib
import sys

def make_sure_path_exists(path):
    """
    Create directories if they don't exist already.
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def data_file(category, name=None):
    """
    Create a filename within Data
    """
    if name == None:
        return os.path.join(os.path.dirname(__file__), 'data', category)
    else:
        return os.path.join(os.path.dirname(__file__), 'data', category, name)


def data_directory(category):
    """
    Create a directory within Data
    """
    return os.path.join(os.path.dirname(__file__), 'data', category)


def log_file(name):
    """
    Create a log file.
    """
    return os.path.join(os.path.dirname(__file__), 'logs', name)


def save_folds(folds):
    """
    Stash the fold information.
    """
    folds.to_csv(data_file('folds.csv'),index=True,index_label='iterations')


def saved_folds():
    """
    Get the fold information back.
    """
    return pandas.read_table(data_file('folds.csv'), sep=',', index_col='iterations')


SAVEFILE_LOCATION = "models/"
MODEL_FILENAME = "insult_classifier.joblib.pkl"

def save_model( clf, location=SAVEFILE_LOCATION ):
    save_path = os.path.join(os.path.dirname(__file__), SAVEFILE_LOCATION)
    make_sure_path_exists(save_path)
    save_path = os.path.join(save_path, MODEL_FILENAME)
    with open(save_path, 'w') as fh:
        _ = joblib.dump(clf, fh, compress=9)


def load_model( location=SAVEFILE_LOCATION, model_filename=MODEL_FILENAME):
    load_path = os.path.join(os.path.dirname(__file__), location, model_filename)
    try:
        with open(load_path, 'rb') as fh:
            clf = joblib.load(fh)
    except IOError:
        print("Model failed to load. Run Insults.build_modeL().")
        return None
    return clf


argsets = {}
argsets['production'] = (
        [
        "--tune",
        "--sgd_alpha","1e-4",
        "--sgd_penalty","elasticnet" ,
        "--trainfile",data_file('Inputs',"fulltrain.csv"),
        "--testfile",data_file('Inputs',"final.csv"),
        '--predictions',data_file('Final','final1.csv'),
        '--no_score'],
        [
        "--tune",
        "--sgd_alpha","3e-5",
        "--sgd_penalty","elasticnet" ,
        "--trainfile",data_file('Inputs',"fulltrain.csv"),
        "--testfile",data_file('Inputs',"final.csv"),
        '--predictions',data_file('Final','final2.csv'),
        '--no_score'],
        [
        "--tune",
        "--sgd_alpha","1e-4",
        "--sgd_penalty","l2",
        "--trainfile",data_file('Inputs',"fulltrain.csv"),
        "--testfile",data_file('Inputs',"final.csv"),
        '--predictions',data_file('Final','final8.csv'),
        '--no_score'],
        [
        "--tune",
        "--sgd_alpha","3e-5",
        "--sgd_penalty","l2",
        "--trainfile",data_file('Inputs',"fulltrain.csv"),
        "--testfile",data_file('Inputs',"final.csv"),
        '--predictions',data_file('Final','final9.csv'),
        '--no_score'],
        [
        "--tune",
        "--sgd_alpha","1e-5",
        "--sgd_penalty","l2",
        "--trainfile",data_file('Inputs',"fulltrain.csv"),
        "--testfile",data_file('Inputs',"final.csv"),
        '--predictions',data_file('Final','final10.csv'),
        '--no_score'],
        )

argsets['tuning'] = (
        ["--tune","--sgd_alpha","1e-4","--sgd_penalty","elasticnet"],
        ["--tune","--sgd_alpha","3e-5","--sgd_penalty","elasticnet"],
        ["--tune","--sgd_alpha","1e-5","--sgd_penalty","elasticnet"],
        ["--tune","--sgd_alpha","3e-6","--sgd_penalty","elasticnet"],
        ["--tune","--sgd_alpha","1e-6","--sgd_penalty","elasticnet"],
        ["--tune","--sgd_alpha","3e-7","--sgd_penalty","elasticnet"],
        ["--tune","--sgd_alpha","1e-7","--sgd_penalty","elasticnet"],
        ["--tune","--sgd_alpha","1e-4","--sgd_penalty","l2"],
        ["--tune","--sgd_alpha","3e-5","--sgd_penalty","l2"],
        ["--tune","--sgd_alpha","1e-5","--sgd_penalty","l2"],
        ["--tune","--sgd_alpha","3e-6","--sgd_penalty","l2"],
        ["--tune","--sgd_alpha","1e-6","--sgd_penalty","l2"],
        ["--tune","--sgd_alpha","3e-7","--sgd_penalty","l2"],
        ["--tune","--sgd_alpha","1e-7","--sgd_penalty","l2"],
        ["--tune","--sgd_alpha","1e-4","--sgd_penalty","l1"],
        ["--tune","--sgd_alpha","3e-5","--sgd_penalty","l1"],
        ["--tune","--sgd_alpha","1e-5","--sgd_penalty","l1"],
        ["--tune","--sgd_alpha","3e-6","--sgd_penalty","l1"],
        ["--tune","--sgd_alpha","1e-6","--sgd_penalty","l1"],
        ["--tune","--sgd_alpha","3e-7","--sgd_penalty","l1"],
        ["--tune","--sgd_alpha","1e-7","--sgd_penalty","l1"],
        )


def get_parser():
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

    parser.add_argument('--production','-c',action='store_true',help='make predictions for the final stage of the production')
    parser.add_argument('--comptune','-ct', action='store_true',help='tuning for final stage')
    parser.add_argument('--score','-sc',action='store_true',dest='score',help='turn on print out of score at end', default=True)
    parser.add_argument('--no_score','-nsc',action='store_false',dest='score',help='turn off print out of score at end' )

    return parser


def tied_rank(x):
    """
    Credit To: https://github.com/LostProperty/ml-metrics-patched/blob/master/ml_metrics/auc.py

    Computes the tied rank of elements in x.
    This function computes the tied rank of elements in x.
    Parameters
    ----------
    x : list of numbers, numpy array
    Returns
    -------
    score : list of numbers
            The tied rank f each element in x
    """
    sorted_x = sorted(zip(x, range(len(x))))
    r = [0 for k in x]
    cur_val = sorted_x[0][0]
    last_rank = 0
    for i in range(len(sorted_x)):
        if cur_val != sorted_x[i][0]:
            cur_val = sorted_x[i][0]
            for j in range(last_rank, i):
                r[sorted_x[j][1]] = float(last_rank+1+i)/2.0
            last_rank = i
        if i==len(sorted_x)-1:
            for j in range(last_rank, i+1):
                r[sorted_x[j][1]] = float(last_rank+i+2)/2.0
    return r


def auc(actual, posterior):
    """
    Credit To: https://github.com/LostProperty/ml-metrics-patched/blob/master/ml_metrics/auc.py

    Computes the area under the receiver-operater characteristic (AUC)
    This function computes the AUC error metric for binary classification.
    Parameters
    ----------
    actual : list of binary numbers, numpy array
             The ground truth value
    posterior : same type as actual
                Defines a ranking on the binary numbers, from most likely to
                be positive to least likely to be positive.
    Returns
    -------
    score : double
            The mean squared error between actual and posterior
    """
    r = tied_rank(posterior)
    num_positive = len([0 for x in actual if x==1])
    num_negative = len(actual)-num_positive
    sum_positive = sum([r[i] for i in range(len(r)) if actual[i]==1])
    auc = ((sum_positive - num_positive*(num_positive+1)/2.0) /
           (num_negative*num_positive))
    return auc


def score():
    """ Track performance. """

    gold = pandas.read_table(data_file('Inputs','test_with_solutions.csv'), sep=',')
    private = gold[gold.Usage=='PrivateTest'].Insult
    public = gold[gold.Usage=='PublicTest'].Insult
    data = []
    for fn in os.listdir(data_directory('Submissions')):
            if fn[-4:] == ".csv":
                guess = pandas.read_table(data_file('Submissions', fn), sep=',')
                pub_guess = guess.Insult[public.index]
                priv_guess = guess.Insult[private.index]
                data.append({"fn": fn[:-4],
                                    "score" : auc(gold.Insult, guess.Insult),
                                    "public": auc(np.array(public), np.array(pub_guess)),
                                    "private": auc(np.array(private), np.array(priv_guess)),
                                    })
    print pandas.DataFrame(data, columns=("fn", "score", "public", "private")).sort('score')
