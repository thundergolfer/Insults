from sklearn import feature_extraction,linear_model, model_selection, pipeline

from insults.classifier import InsultsSGDRegressor

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


def make_pipeline(options):
    vect = ('vect', feature_extraction.text.CountVectorizer(lowercase=False,
                                                            analyzer='char',
                                                            ngram_range=(1, 5)))
    tfidf = ('tfidf', feature_extraction.text.TfidfTransformer(sublinear_tf=True, norm='l2'))
    clf = ("clf",InsultsSGDRegressor(alpha=options.sgd_alpha,
                                     penalty=options.sgd_penalty,
                                     learning_rate='constant',
                                     eta0=options.sgd_eta0,
                                     max_iter=options.sgd_max_iter,
                                     n_iter_per_step=options.sgd_n_iter_per_step))

    return InsultsPipeline([vect, tfidf, clf])
