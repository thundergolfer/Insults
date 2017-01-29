# Insults
`Code for Kaggle and Impermium's insult detection competition`

##### TODO:

1. Refactor code to move to a recent version of scikit-learn. Currently using 0.13.1
2. Implement model persistence to avoid training over and over
3. package up for use in [mAIcroft](https://github.com/thundergolfer/mAIcroft). Should a package be used?
4. Refactor and document the code. It's not super clear at the moment
5. Work out how to auto-download this: nltk.download('punkt')

### How to run


Thanks to Abhay Deshmukh <abhay_2685@yahoo.com> for showing me that the original instructions needed to be improved.

The code lives in the Insults directory next to this readme. You need the Anaconda Python distribution to run it in the way that I recommend. I use Linux and MacOSX, which have all the necessary command-line tools. If you are on Windows, you will have to adapt the instructions to make sense for your environment.

`cd insults`

### Dependencies

`Python 2.7.3` + `scikit-learn 0.13-git` + `ml_metrics 0.1.1` + `pandas 0.8.1` + `futures 2.2.0` + `matplotlib 1.2.1` (for plotting)

### Setup

##### 1 Create a conda env with everything except ml-metrics

```
conda create -n insults pandas scikit-learn=0.18.1 matplotlib futures
source activate insults
```

##### 2 Update `Pyside`

Without updating `Pyside` I got the following error when trying to run `Insults.py`.

```
from PySide import QtCore, QtGui, __version__, __version_info__
ImportError: libshiboken-python2.7.so.1.1: cannot open shared object file: No such file or directory
```

Running the following command to update `Pyside` allowed everything to work.

`conda update pyside`

##### 3 Run the training

Run the code

```
python insults.py --competition
```

##### 4 Monitor the training process

Open a separate shell

```
cd $INSULTS_DIR
tail -f Logs/final.log  (Ctrl-C to quit when python finishes)
```

#### General approach

Character n-grams plus carefully tuned SGD using elastic net. Character n-grams because
regular linguistic processing is compromised by weird spelling and grammar. SGD because
it works well with sparse features and can be tuned to give good results.

#### Data files

Place the .csv file that you want to have results for in Data/Inputs/final.csv.

Data/Inputs/fulltrain.csv is the concatenation of the two labeled files that
Kaggle provided.

#### The code

insults.py is a single Python file running the whole process.

What this does is to train on "fulltrain.csv" and test on "final.csv". It uses a range of values for
SGD's alpha parameter

show.py is a utility for seeing the learning curve that I used to select a training regime.
score.py spits out some stats for the various submissions.




Submission plan
---------------

Will generate 21 (7 for each penalty type) models using the commands above, then select the five having the highest cross-validation scores.
