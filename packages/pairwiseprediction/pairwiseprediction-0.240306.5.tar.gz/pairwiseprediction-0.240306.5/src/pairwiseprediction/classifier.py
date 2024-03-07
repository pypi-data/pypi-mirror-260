import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.utils.validation import check_is_fitted

from pairwiseprediction.combination import pairwise_diff, pairwise_hstack
from pairwiseprediction.interpolation import interpolate_for_classification


class PairwiseClassifier(BaseEstimator, ClassifierMixin):
    r"""

    :param algorithm: Class of algorithm to predict pairs internally.
    :param pairwise: Type of combination: "difference" or "concatenation".
    :param threshold: How much difference between target values should be considered as relevant within a pair?
    :param proportion: Is the threshold an absolute value (difference) or relative value (proportion)?
    :param center: Default value is the mean of the training sample.
    :param only_relevant_pairs_on_prediction: Whether to keep only relevant differences during interpolation.
    :param n_jobs: Number of processess in parallel
    :param kwargs: Arguments for user-provided `algorithm`.

    >>> import numpy as np
    >>> from sklearn.datasets import load_diabetes
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> a, b = load_diabetes(return_X_y=True)
    >>> me = np.mean(b)
    >>> # noinspection PyUnresolvedReferences
    >>> y = (b > me).astype(int)
    >>> alg = RandomForestClassifier(n_estimators=3, random_state=0, n_jobs=-1)
    >>> np.mean(cross_val_score(alg, a, y, cv=StratifiedKFold(n_splits=2)))  # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
    0.6...
    >>> c = b.reshape(len(b), 1)
    >>> X = np.hstack([a, c])
    >>> alg = PairwiseClassifier(n_estimators=3, threshold=20, only_relevant_pairs_on_prediction=False, random_state=0, n_jobs=-1)
    >>> np.mean(cross_val_score(alg, X, y, cv=StratifiedKFold(n_splits=2)))  # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
    0.7...
    >>> alg = alg.fit(X[:80])
    >>> alg.predict(X[:2])
    array([1, 0])
    >>> alg.predict(X[:6], paired_rows=True)
    array([1, 0, 0, 1, 1, 0])
    >>> p1 = alg.predict(X[80::2])
    >>> p2 = alg.predict(X[80:], paired_rows=True)[::2]
    >>> a = X[80::2,-1]
    >>> b = X[81::2,-1]
    >>> np.sum(p1 == y[80::2]) / len(p1)  # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
    0.7...
    >>> np.sum(p2 == (a>b)) / len(p2)  # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
    0.6...
    """

    def __init__(self, algorithm=RandomForestClassifier, pairwise="concatenation", threshold=0, proportion=False, center=None, only_relevant_pairs_on_prediction=False, **kwargs):
        self.algorithm = algorithm
        self.kwargs = kwargs
        self.pairwise = pairwise
        self.threshold = threshold
        self.proportion = proportion
        self.center = center
        self.only_relevant_pairs_on_prediction = only_relevant_pairs_on_prediction
        self._estimator = None

    # def get_params(self, deep=False):
    #     return {}  # "n_estimators": self.n_estimators, "n_jobs": self.n_jobs, "random_state": self.random_state, "diff": self.diff}

    def fit(self, X, y=None):
        """
        WARNING: y is ignored; permutation test wont work
        TODO: see if permutation test accept pandas; use index to fix warning above

        :param X:   Last column is the continuous target.
        :param y:   Ignored.

        :return:
        """
        self.Xw = X if isinstance(X, np.ndarray) else np.array(X)
        X = y = None

        if self.center is None:
            self.center = np.mean(self.Xw[:, -1])

        handle_last_as_y = "%" if self.proportion else True
        filter = lambda tmp: (tmp[:, -1] < -self.threshold) | (tmp[:, -1] >= self.threshold)
        pairwise = True
        if self.pairwise == "difference":
            pairs = lambda a, b: pairwise_diff(a, b, pct=handle_last_as_y == "%")
        elif self.pairwise == "concatenation":
            pairs = lambda a, b: pairwise_hstack(a, b, handle_last_as_y=handle_last_as_y)
        elif self.pairwise == "none":
            if self.proportion:
                raise Exception(f"Just use delta=9 instead of pct,delta=0.1  (assuming you are looking for 20% increase")
            boo = self.Xw[(self.Xw[:, -1] < self.center - self.threshold) | (self.Xw[:, -1] >= self.center + self.threshold)]
            self.Xw = self.Xw[boo]
            pairwise = False
            pairs = None
        else:
            raise Exception(f"Not implemented for {self.pairwise=}")
        # self.classes_ = unique_labels(y)

        # sort
        self.idxs = np.argsort(self.Xw[:, -1].flatten(), kind="stable").flatten()
        self.Xw = self.Xw[self.idxs]

        if pairwise:  # pairwise transformation
            tmp = pairs(self.Xw, self.Xw)
            pairs_Xy_tr = tmp[filter(tmp)]
            Xtr = pairs_Xy_tr[:, :-1]
            ytr = (pairs_Xy_tr[:, -1] >= 0).astype(int)
        else:
            Xtr = self.Xw[:, :-1]
            w = self.Xw[:, -1]
            # noinspection PyUnresolvedReferences
            ytr = (w >= self.center).astype(int)

        self._estimator = self.algorithm(**self.kwargs).fit(Xtr, ytr)
        self.Xtr, self.ytr = Xtr, ytr
        self.Xw_tr = self.Xw[abs(self.Xw[:, -1] - self.center) >= self.threshold] if self.only_relevant_pairs_on_prediction else self.Xw
        return self

    def predict_proba(self, X, paired_rows=False):
        """

        :param X:               Last column is discarded.
        :param paired_rows:
        :return:

        >>> import numpy as np
        >>> from sklearn.datasets import load_diabetes
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> a, b = load_diabetes(return_X_y=True)
        >>> me = np.mean(b)
        >>> # noinspection PyUnresolvedReferences
        >>> y = (b > me).astype(int)
        >>> alg = RandomForestClassifier(n_estimators=10, random_state=0, n_jobs=-1)
        >>> alg = alg.fit(a, y)
        >>> y[:5], b[:5], me  # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
        (array([0, 0, 0, 1, 0]), array([151.,  75., 141., 206., 135.]), 152...)
        >>> np.round(alg.predict_proba(a[:5]), 2)  # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
        array([[0.7, 0.3],
               [1. , 0. ],
               [0.9, 0.1],
               [0. , 1. ],
               [1. , 0. ]])
        >>> c = b.reshape(len(b), 1)
        >>> X = np.hstack([a, c])
        >>> alg = PairwiseClassifier(n_estimators=30, threshold=20, only_relevant_pairs_on_prediction=False, random_state=0, n_jobs=-1)
        >>> alg = alg.fit(X)
        >>> np.round(alg.predict_proba(X[:5]), 2)  # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
        array([[0.9 , 0.1 ],
               [0.41, 0.59],
               [0.96, 0.04],
               [0.76, 0.24],
               [0.74, 0.26]])
        >>> b[:6]
        array([151.,  75., 141., 206., 135.,  97.])
        >>> # 151 > 75  →  label=1
        >>> alg.predict(X[:6], paired_rows=True)[::2]
        array([1, 0, 1])
        >>> alg.predict_proba(X[:6], paired_rows=True)[::2]
        array([[0. , 1. ],
               [1. , 0. ],
               [0.1, 0.9]])
        """
        return self.predict(X, paired_rows, predict_proba=True)

    def predict(self, X, paired_rows=False, predict_proba=False):
        """

        :param X:               Last column is discarded.
        :param paired_rows:
        :param predict_proba:
        :return:
        """
        check_is_fitted(self._estimator)
        Xw_ts = X if isinstance(X, np.ndarray) else np.array(X)
        X = Xw_ts[:, :-1]  # discard label to avoid data leakage

        pairwise = True
        if self.pairwise == "difference":
            pairs = lambda a, b: pairwise_diff(a, b)
        elif self.pairwise == "concatenation":
            pairs = lambda a, b: pairwise_hstack(a, b)
        elif self.pairwise == "none":
            if self.proportion:
                raise Exception(f"For no pairwise, just use delta=9 instead of pct,delta=0.1  (assuming you are looking for 20% increase")
            pairwise = False
            pairs = None
        else:
            raise Exception(f"Not implemented for {self.pairwise=}")

        if pairwise:
            targets = self.Xw_tr[:, -1]
            pos_ampl, neg_ampl = (np.max(targets) - self.center, self.center - np.min(targets)) if predict_proba else (None, None)
            l = []
            loop = range(0, X.shape[0], 2) if paired_rows else range(X.shape[0])
            for i in loop:
                x = X[i : i + 1, :]
                if paired_rows:
                    Xts = pairs(x, X[i + 1 : i + 2, :])
                    if predict_proba:
                        predicted = self._estimator.predict_proba(Xts)[0]
                    else:
                        predicted = int(self._estimator.predict(Xts)[0])
                    l.append(predicted)
                    l.append(1 - predicted)
                else:
                    Xts = pairs(x, self.Xw_tr[:, :-1])
                    zts = self._estimator.predict(Xts)
                    # interpolation
                    conditions = 2 * zts - 1
                    z = interpolate_for_classification(targets, conditions)
                    if predict_proba:
                        d = float(z - self.center)
                        p = (d / pos_ampl) if d > 0 else (-d / neg_ampl)
                        predicted = [1 - p, p]
                    else:
                        predicted = int(z >= self.center)
                    l.append(predicted)
            return np.array(l)
        return self._estimator.predict(X)

    def shap(self, xa, xb, columns, seed=0, **kwargs):
        """
        Return an indexed dict {variable: (value, SHAP)} for the given pair of instances

        A, B: last column is discarded.

        :param xa:      Test instance A.
        :param xb:      Test instance B.
        :param columns: Column names for a single instance.
        :param seed:
        :return:

        >>> import numpy as np
        >>> from pandas import DataFrame
        >>> from sklearn.datasets import load_diabetes
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> a, b = load_diabetes(return_X_y=True)
        >>> a = a[:, :3]
        >>> c = b.reshape(len(b), 1)
        >>> X = np.hstack([a, c])
        >>> alg = PairwiseClassifier(n_estimators=3, threshold=20, only_relevant_pairs_on_prediction=False, random_state=0, n_jobs=-1)
        >>> alg = alg.fit(X[:80])
        >>> d = alg.shap(X[0], X[1], columns=list("abc"))
        >>> d.sort()
        >>> d # doctest:+ELLIPSIS +NORMALIZE_WHITESPACE
        IndexedOrderedDict([('a_a', (0.038..., 0.078...)), ('a_b', (0.050..., -0.007...)), ('a_c', (0.061..., 0.079...)), ('b_a', (-0.001..., 0.085...)), ('b_b', (-0.044..., 0.025...)), ('b_c', (-0.051..., 0.237...))])
        """
        check_is_fitted(self._estimator)
        import dalex as dx
        from indexed import Dict
        from pandas import DataFrame

        f = lambda i: [f"{i}_{col}" for col in columns]
        columns = f("a") + f("b")
        self._estimator.feature_names_in_ = columns
        if self.pairwise == "difference":
            x = pairwise_diff(xa[:-1].reshape(1, -1), xb[:-1].reshape(1, -1))
        elif self.pairwise == "concatenation":
            x = pairwise_hstack(xa[:-1].reshape(1, -1), xb[:-1].reshape(1, -1))
        else:
            raise Exception(f"Not implemented for {self.pairwise=}")
        x = DataFrame(x, columns=columns)
        Xtr = DataFrame(self.Xtr, columns=columns)
        explainer = dx.Explainer(model=self._estimator, data=Xtr, y=self.ytr, verbose=False)
        predictparts = dx.Explainer.predict_parts(explainer, new_observation=x, type="shap", random_state=seed, **kwargs)
        zz = zip(predictparts.result["variable"], predictparts.result["contribution"])
        var__val_shap = Dict((name_val.split(" = ")[0], (float(name_val.split(" = ")[1:][0]), co)) for name_val, co in zz)
        return var__val_shap

    def __sklearn_is_fitted__(self):
        return check_is_fitted(self._estimator)

    def __repr__(self, **kwargs):
        return "PW" + repr(self.algorithm)

    # def __sklearn_clone__(self):
    #     return PairwiseClassifier(self.n_estimators, self.n_jobs, self.random_state, self.diff)
