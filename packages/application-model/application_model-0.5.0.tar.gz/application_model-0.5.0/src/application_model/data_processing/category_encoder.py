
import numpy
import pandas
from sklearn.preprocessing import LabelEncoder


class CategoryEncoder:
    """Wrapper of LabelEncoder from sklearn.
    
    Adds the possibility of passing a proportion threshold or a number max of classes it must
    encodes the data. The number max of classes sort the values by its frequency and gets the
    first max classes and group the others in a single class.
    """

    def __init__(self,
                 generic_label="UNLABELED",
                 class_prefix="CLASS_",
                 threshold=None,
                 max_classes=None):

        if threshold is not None and max_classes is not None:
            raise AttributeError(
                "threshold and max_classes can not be set at the same time")

        if threshold is not None and (threshold > 1.0 or threshold < 0.0):
            raise ValueError("threshold must be a value between 0 and 1")

        if max_classes is not None and (not isinstance(max_classes, int)
                                        or max_classes <= 0):
            raise ValueError("max_classes must an integer greater than 0")

        self.threshold = threshold
        self.max_classes = max_classes
        self.class_prefix = class_prefix

        # these values are going to be used to grouped classes excluded by the threshold or
        # max classes filtering, and for unknown values
        self.generic_label = generic_label
        self.__generic_class = self.class_prefix + generic_label
        self.is_loaded = False

        self.__skencoder = LabelEncoder()
        self.__class_value_map = None
        self.__value_class_map = None

    def fit(self, data) -> None:
        if not isinstance(data, pandas.Series):
            data = pandas.Series(data)

        if len(data.shape) != 1:
            raise ValueError(
                "Please provide an 1D list, array or pandas.Series")

        if self.threshold is not None:
            # replace all values having its frequency below the threshold by some generic label
            data = self.__transform_data_by_frequency(data)
        elif self.max_classes is not None:
            # keep values of the most frequent classes and replace othes by generic data
            data = self.__transform_data_by_max_classes(data)

        # generating the labels for each class
        self.__skencoder.fit(data)
        self.__build_maps(self.__skencoder.classes_)

    def transform(self, data) -> numpy.array:
        if self.__value_class_map is None:
            raise ValueError('Please fit/load the encoder before to transform')

        if not isinstance(data, pandas.Series):
            data = pandas.Series(data)

        a = []
        for d in data.values:
            # the class is unknown we return the generic label
            if d not in self.__value_class_map:
                a.append(self.__generic_class)
            else:
                a.append(self.__value_class_map[d])

        return numpy.array(a)

    def fit_transform(self, data) -> numpy.array:
        self.fit(data)
        return self.transform(data)

    def inverse_transform(self, data) -> numpy.array:
        if self.__class_value_map is None:
            raise ValueError('Please fit/load the encoder before to transform')

        if not isinstance(data, pandas.Series):
            data = pandas.Series(data)

        a = []

        for d in data.values:
            # the values is unknown we return the generic value
            if d not in self.__class_value_map:
                a.append(self.generic_label)
            else:
                a.append(self.__class_value_map[d])

        return numpy.array(a)

    def load(self, class_value_map) -> None:
        self.__value_class_map = {}
        self.__class_value_map = {}

        for c in class_value_map:
            self.__class_value_map[c] = class_value_map[c]
            self.__value_class_map[class_value_map[c]] = c

        self.is_loaded = True

    def get_mapping(self) -> dict:
        return self.__class_value_map

    def get_generic_class(self) -> str:
        return self.__generic_class

    def __transform_data_by_frequency(self, data) -> pandas.Series:

        # getting the descending frequency of the unique values in the dataset
        # it returns a series having the index being the value and the value being the frequency
        frequencies = data.value_counts(sort=True, ascending=False)

        # getting total of instances of the dataset
        total = frequencies.sum()

        # getting the proportion of all classes in the dataset according to its frequency
        proportions = frequencies.apply(lambda x: x / float(total)
                                        if total > 0.0 else 0.0)

        # replacing the value of the data having frequency less than the threshold
        # by some generic class
        data = data.apply(lambda x: self.generic_label
                          if proportions[x] < self.threshold else x)

        return data

    def __transform_data_by_max_classes(self, data) -> pandas.Series:

        # getting the descending frequency of the unique values in the dataset
        # it returns a series having the index being the value and the value being the frequency
        frequencies = data.value_counts(sort=True, ascending=False)

        # there is no need to make any modification in the dataset
        if self.max_classes >= frequencies.size:
            return data

        # getting only the number of classes we want to consider based on frequency
        classes = frequencies[:self.max_classes]

        # replacing values that are not part of the most frequent classes by some generic class
        data = data.apply(lambda x: self.generic_label
                          if x not in classes.index.values else x)

        return data

    def __build_maps(self, values):

        self.__class_value_map = {}
        self.__value_class_map = {}

        n = 1
        for v in values:
            # generic label does not need to be mapped. It is going to have a standard value
            if v == self.generic_label:
                continue

            self.__class_value_map[self.class_prefix + str(n)] = v
            self.__value_class_map[v] = self.class_prefix + str(n)
            n += 1

        self.is_loaded = True
