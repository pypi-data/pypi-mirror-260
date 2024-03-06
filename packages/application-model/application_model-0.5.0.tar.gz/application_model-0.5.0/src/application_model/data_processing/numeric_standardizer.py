
import numpy
from sklearn.preprocessing import StandardScaler


class NumericStandardizer(object):
    """Wrapper for StandardScaler from sklearn.

        Adds the possibility of passing the pre computed means and stds for the online scenario.
    """

    def __init__(self, means=[], stds=[]):
        if means == [] and stds != [] or means != [] and stds == []:
            raise ValueError("means and stds must be set at the same time")
        self.__means = numpy.array(means)
        self.__stds = numpy.array(stds)

        if self.__means.shape != self.__stds.shape:
            raise ValueError("means and stds must have the same shape")

        self.__skscaler = StandardScaler(with_mean=True, with_std=True)

    def fit(self, X) -> None:
        self.__skscaler.fit(X)
        self.__means = self.__skscaler.mean_
        self.__stds = self.__skscaler.scale_

    def transform(self, X) -> numpy.array:
        if self.__means is []:
            raise ValueError(
                "To transform values it is necessary to fit the model first")
        if self.__stds is []:
            raise ValueError(
                "To transform values it is necessary to fit the model first")

        X = numpy.array(X)

        if X.shape[1] != self.__means.shape[0]:
            raise ValueError(
                "The dataset and the means are divergents, please check the shapes"
            )

        if X.shape[1] != self.__stds.shape[0]:
            raise ValueError(
                "The dataset and the stds are divergents, please check the shapes"
            )

        # applying z-core standardization
        X -= self.__means
        X /= self.__stds

        return X

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        if self.__means is []:
            raise ValueError(
                "To transform values it is necessary to fit the model first")
        if self.__stds is []:
            raise ValueError(
                "To transform values it is necessary to fit the model first")

        X = numpy.array(X)

        if X.shape[1] != self.__means.shape[0]:
            raise ValueError(
                "The dataset and the means are divergents, please check the shapes"
            )

        if X.shape[1] != self.__stds.shape[0]:
            raise ValueError(
                "The dataset and the stds are divergents, please check the shapes"
            )

        # removing z-core standardization
        X *= self.__stds
        X += self.__means

        return X

    def get_means(self):
        return self.__means

    def get_stds(self):
        return self.__stds
