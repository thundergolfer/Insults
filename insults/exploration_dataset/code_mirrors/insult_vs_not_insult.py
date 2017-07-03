
# coding: utf-8


get_ipython().magic(u'matplotlib inline')



import os
import sys
nb_dir = os.path.split(os.getcwd())[0]
if nb_dir not in sys.path:
    sys.path.append(nb_dir)



import pandas as pd
import numpy as np

from util import data_file
import seaborn as sns
sns.set(color_codes=True)



df = pd.read_table(data_file('Inputs','train.csv'),sep=',')


# #### Do Insults disproportionately contain the word "you"?





