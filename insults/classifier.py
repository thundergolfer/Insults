import os
import numpy as np
import logging
from sklearn.externals import joblib
from sklearn import linear_model

from insults import util

class InsultsSGDRegressor(linear_model.SGDRegressor):
    """
    A customized SGD regressor that
    a) transforms the output into 0..1
    b) fits in stages so you can see the effect of number of iterations.
    """
    def __init__(self,n_iter_per_step=50,max_iter=500,alpha=0.001,penalty='l2',**kwargs):
        self.max_iter=max_iter
        self.kwargs = kwargs
        self.n_iter_per_step = n_iter_per_step
        self.alpha = alpha
        self.penalty = penalty
        self.reset_args()

    def reset_args(self):
        """
        """
        assert self.max_iter % self.n_iter_per_step == 0
        linear_model.SGDRegressor.__init__(self,
                                            alpha=self.alpha,
                                            penalty=self.penalty,
                                            n_iter=self.n_iter_per_step,
                                            **self.kwargs)
    def fit(self,X,y):
        self.coef_ = None
        self.intercept_ = None
        self.stages_ = []
        for i in range(0,self.max_iter,self.n_iter):

            if self.coef_ is not None:
                assert(self.intercept_ is not None)
                linear_model.SGDRegressor.fit(self,X,y,coef_init=self.coef_,intercept_init=self.intercept_)
            else:
                linear_model.SGDRegressor.fit(self,X,y)
            # record coefs and intercept for later
            self.stages_.append((i+self.n_iter,self.coef_.copy(),self.intercept_.copy()))
            logging.info('done %d/%d steps' % (i+self.n_iter,self.max_iter))
            logging.info('training set auc %f' % self.auc(X,y))

    def auc(self,X,y):
        yhat = self.predict(X)
        return util.auc(np.array(y),yhat)

    def staged_predict(self,X):
        """
        Predict after each of the stages.
        """
        return [(n_iter_,self.predict(X,coef=coef_,intercept=intercept_)) for (n_iter_,coef_,intercept_) in self.stages_]

    def staged_auc(self,X,y):
        """
        calculate the AUC after each of the stages.

        returns: ns   -- list of iteration numbers
                 aucs -- list of corresponding areas under the curve.
        """
        y = np.array(y)
        results = [ (n, util.auc(y,p)) for n,p in self.staged_predict(X)]

        return zip(*results) # Python idiom unzips list into two parallel ones.

    def predict(self,X,coef=None,intercept=None):
        """
        a) do the prediction based on given coefs and intercept, if provided.
        b) Scale the predictions so that they are in 0..1.

        """
        if coef is not None:
            assert intercept is not None
            self.intercept_ = intercept
            self.coef_ = coef

        return scale_predictions(linear_model.SGDRegressor.predict(self,X))

def scale_predictions(ypred):
    """
    normalize range of predictions to 0-1.
    """
    yrange = ypred.max() - ypred.min()
    ypred -= ypred.min()
    ypred /= yrange

    # protection against rounding, ENSURE nothing out of range.
    ypred[ypred > 1] = 1
    ypred[ypred < 0] = 0
    return ypred
