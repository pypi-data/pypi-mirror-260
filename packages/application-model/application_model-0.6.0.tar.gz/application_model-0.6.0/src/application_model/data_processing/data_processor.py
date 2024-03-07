
import logging
import pickle

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

from .category_encoder import CategoryEncoder
from .numeric_standardizer import NumericStandardizer

UNKNOWN_LABEL = "DESCONHECIDO"


class DataProcessor(BaseEstimator):
    """
    Extract the metadata from train dataset.
    """
    
    def __init__(self):
        self.__categorical_map = None
        self.__numeric_map = None
        self.__bool_map = None
        self.__original_cols_dtype = None
        

    def fit(self, data, categorical_limit=12) -> None:
        """This function generates the attribute maps according to the data, this maps
        are used to transform the dataframe.

        Parameters
        ----------
        data : pandas.DataFrame
            This is the data used to generate the maps, the maps will use the information
            in this dataframe to generate the attribute maps

        categorical_limits : dict, optional
            if you want to use limits in the categorical data fitting you can pass a dict having
            the column and the limits used to fit the data, these limits are related
            to the categorical encoder we use (CategoryEncoder),
            and can be max_classes or threshold,
            by default is {}, but you can pass a dict like this:
            {
                "column_1": {
                    "max_classes":10
                },
                "column_2": {
                    "threshold":0.1
                }
            }
        """

        self.__numeric_map = {}
        self.__categorical_map = {}
        self.__bool_map = {}
        self.__original_cols_dtype = {}

        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
            
        for c in data.columns:
            if "float" in str(data[c].dtype) or "int" in str(data[c].dtype):
                self.__numeric_map[c] = {
                    "max": float(data[c].max()),
                    "min": float(data[c].min()),
                    "mean": float(data[c].mean()),
                    "std": float(data[c].std()),
                }
            elif "bool" in str(data[c].dtype):
                data[c] = data[c].fillna(False).copy()
                self.__bool_map[c] = data[c].mode().values[0]
                
            elif "object" in str(data[c].dtype):
                data[c] = data[c].fillna(UNKNOWN_LABEL).copy()
                e = CategoryEncoder(max_classes=categorical_limit)
                try:
                    e.fit(data[c])
                    self.__categorical_map[c] = e.get_mapping()
                except:
                    raise ValueError('Something wrong with ' + c + ' column.')

        
        cols = data.columns.to_series().groupby(data.dtypes).groups
        dtypes_columns = {k.name: v.values for k, v in cols.items()}

        # getting the columns by types to process according its type
        attrs = {}
        for dtype in dtypes_columns.keys():
            attrs[dtype] = data.select_dtypes(dtype).columns.values
        self.__original_cols_dtype = {
            col: dtype for dtype, cols in attrs.items() for col in cols
        }
        
        return self
        
        
    def transform(self,
                  data,
                  clip_outliers=True,
                  replace_nan=True,
                  one_hot=True) -> pd.DataFrame:
        """This function receive a raw dataframe and returns a transformed dataframe.
        It will use the attribute maps previously loaded or fitted.

        Parameters
        ----------
        data : pandas.DataFrame
            The dataframe to be transformed
        clip_outliers : bool, optional
            when transforming numeric data we can clip values above or below
            the max and min found in the fitting, by default True
        replace_nan : bool, optional
            when transforming numeric data we can replace all nan by 0.0 after
            the z-score normalization, by default True
        one_hot : bool, optional
            when transforming categorical data we can transform it to one
            hot encoded, by default True

        Returns
        -------
        pandas.DataFrame
            Transformed dataframe, having all columns found in the maps and
            without all columns not found in the maps

        Raises
        ------
        ValueError
            Error when try to transform without numeric map loaded or fitted
        ValueError
            Error when try to transform without categorical map loaded or fitted
        ValueError
            Error when try to transform without bool map loaded or fitted
        """

        if self.__numeric_map is None:
            raise ValueError(
                'Please fit/load the maps before transforming! Missing numeric map'
            )

        if self.__categorical_map is None:
            raise ValueError(
                'Please fit/load the maps before transforming! Missing categorical map'
            )

        if self.__bool_map is None:
            raise ValueError(
                'Please fit/load the maps before transforming! Missing bool columns list'
            )

        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        data = data.copy(deep=True)
        data = self.__remove_unknown_attributes(data)
        data = self.__convert_to_original_dtypes(data)
        data = self.__insert_missing_attributes(data)
        data = self.__transform_numeric_data(data, clip_outliers, replace_nan)
        data = self.__transform_bool_data(data)
        data = self.__transform_categorical_data(data, one_hot)

        return data
        
        
    def fit_transform(self, data) -> pd.DataFrame:
        """This funciton applies the fit to generate the maps and after transform 
        the data and returns the transformed data.

        Parameters
        ----------
        data : pandas.DataFrame
            The dataframe used to find the attribute maps and to be transformed.
            The same dataframe will be used to perform the actions of fitting and transforming

        Returns
        -------
        pandas.DataFrame
            Transformed dataframe
        """
        self.fit(data)
        return self.transform(data)
        
        
    def load_maps(self, numeric_map, categorical_map, bool_map) -> None:
        """Load pre fitted attribute maps. If you load the maps you do not need to fit.

        Parameters
        ----------
        numeric_map : dict
            the numeric map
        categorical_map : dict
            the categorical map
        bool_map : dict
            the bool map (obs: this map have the columns and the mode)
        """
        self.__numeric_map = numeric_map
        self.__categorical_map = categorical_map
        self.__bool_map = bool_map
        
        
    def get_numeric_mapping(self) -> dict:
        """Get the numeric map filtered or loaded.

        Returns
        -------
        dict
            the numeric map fitted or loaded
        """
        return self.__numeric_map
        
        
    def get_categorical_mapping(self) -> dict:
        """Get the categorical map fitted or loaded

        Returns
        -------
        dict
            the categorical map fitted or loaded
        """
        return self.__categorical_map
        
        
    def get_bool_mapping(self) -> dict:
        """Get the bool map fitted or loaded

        Returns
        -------
        dict
            the bool map fitted or loaded
        """
        return self.__bool_map
        
        
    def __transform_numeric_data(self, data, clip_outliers, replace_nan) -> pd.DataFrame:
        """Norm numeric data and extract metadata.
        """
        means = []
        stds = []
        for c in self.__numeric_map:
            means.append(self.__numeric_map[c]["mean"])
            stds.append(self.__numeric_map[c]["std"])
            if clip_outliers:
                # clipping outliers in the data
                data.loc[data[c] > self.__numeric_map[c]["max"],
                         c] = self.__numeric_map[c]["max"]
                data.loc[data[c] < self.__numeric_map[c]["min"],
                         c] = self.__numeric_map[c]["min"]

        # loading means and stds
        ns = NumericStandardizer(means=means, stds=stds)
        # transforming numeric data
        data[list(self.__numeric_map.keys())] = ns.transform(data[list(
            self.__numeric_map.keys())])

        # after applying z-score, if enabled, all nan become 0.0
        if replace_nan:
            for c in self.__numeric_map.keys():
                data.loc[data[c].isnull(), c] = 0.0

        return data
        
        
    def __transform_bool_data(self, data) -> pd.DataFrame:
        """Transform bool data to int.
        """
        # binaryzing bool columns
        for c in self.__bool_map.keys():
            data[c].fillna(False, inplace=True)
            data[c] = data[c].astype(int)
            
        return data
        
        
    def __transform_categorical_data(self, data, one_hot) -> pd.DataFrame:
        """Transform categorical data in standadize way like one hot.
        """

        # transforming categorical data
        for c in self.__categorical_map:
            # ensure that even nan values will be filled to avoid problems
            data[c].fillna(UNKNOWN_LABEL, inplace=True)
            e = CategoryEncoder()
            e.load(self.__categorical_map[c])
            data[c] = e.transform(data[c])

            if one_hot:
                one_hot_df = pd.get_dummies(data[c], prefix=c)
                one_hot_df = one_hot_df.astype('int64')
                
                # ensure all classes in the encoder has a column in the one hoted
                for a in e.get_mapping():
                    if c + '_' + a not in one_hot_df.columns:
                        one_hot_df[c + '_' + a] = 0
                        
                # ensure that all hot vector will have the generic class label
                if c + '_' + e.get_generic_class() not in one_hot_df.columns:
                    one_hot_df[c + '_' + e.get_generic_class()] = 0

                columns_order = [c + '_' + a for a in e.get_mapping().keys()]
                columns_order.append(c + '_' + e.get_generic_class())

                one_hot_df = one_hot_df.reindex(columns_order, axis=1)
                one_hot_df = one_hot_df.astype('int64')
                
                # join to the dataframe
                data = data.join(one_hot_df)

                # drop the category column
                data.drop(columns=[c], inplace=True)
        return data
        
        
    def __remove_unknown_attributes(self, data) -> pd.DataFrame:
        """Remove unknown columns generate for unknown values and are not in metadata.
        """
        # removing unknown attributes
        for c in data.columns:
            if (c not in self.__numeric_map and c not in self.__categorical_map
                    and c not in self.__bool_map):
                data.drop(columns=[c], inplace=True)

        return data
        
        
    def __insert_missing_attributes(self, data) -> pd.DataFrame:
        """Insert default missing values in attributes.
        """
        for c in self.__numeric_map:
            if c not in data.columns:
                data[c] = float('NaN')

        for c in self.__categorical_map:
            if c not in data.columns:
                data[c] = UNKNOWN_LABEL

        for c in self.__bool_map:
            if c not in data.columns:
                data[c] = pd.Series(self.__bool_map[c].astype(int))

        return data
        
        
    def convert_to_bool(self, val):
        """Tries to convert val to bool.

        For most values this will simply apply bool(val). For str will check if its a numerical 
        string or 'False', or any variation. If numerical will return as if its a regular 
        numerical value and its boolean value. If str as all string values passed to bool
        function will evaluate to True, checks if its a str value that could be
        evaluated to False, as 'false', 'False', 'FALSE'.

        Parameters
        ----------
        val : any Value to be converted to bool.

        Returns
        -------
        out : bool
        """
        if isinstance(val, str):
            return val.strip().lower().replace(
                '0', '') not in ['false', 'f', '', '.']

        return bool(val)
        
        
    def __convert_to_original_dtypes(self, data: pd.DataFrame) -> pd.DataFrame:
        """Converts columns to original dtype attempting to convert its value.

        This is a safeguard to prevent known and expected columns to have
        unexpected dtypes, e.g., if fit function was called with column 'a'
        with dtype float and transform function receives said column with dtype
        str the function will break, because it will try to use float
        operations on str values. This function tries to convert any column with dtypes 
        different from their original dtype, used during fitting. If it can't it sets the
        column to the empty value of the original type:

        - bool: False
        - float: 0.0
        - int: 0
        - str: ''
        - object: ''

        Parameters
        ----------
        data : pd.DataFrame Dataframe holding columns and values that may be
            converted.

        Returns
        -------
        out: pd.DataFrame
        """
        if self.__original_cols_dtype is None:
            return data

        for col in data.columns:
            if col in self.__original_cols_dtype and data[
                    col].dtype != self.__original_cols_dtype[col]:

                try:
                    if self.__original_cols_dtype[col] == np.dtype('bool'):
                        data.loc[:, col] = data[col].map(self.convert_to_bool)

                    else:
                        data.loc[:, col] = data[col].astype(
                            self.__original_cols_dtype[col])

                except ValueError:
                    logging.warning(
                        'Unable to cast to original value, column %s', col)

                    if self.__original_cols_dtype[col] in ['str', 'object']:
                        data.loc[:, col] = ''

                    elif self.__original_cols_dtype[col] in ['bool']:
                        data.loc[:, col] = False

                    elif self.__original_cols_dtype[col] in ['int', 'float']:
                        data.loc[:, col] = 0

        return data
        
        
    def get_metadata(self) -> dict:
        """Returns expected features and respective dtypes for each one.
        """
        if self.__original_cols_dtype is not None:
            return {
                feature: dtype
                for feature, dtype in self.__original_cols_dtype.items()
            }
        return None
        
        
    def save(self, path='data_processor.pkl'):
        """Serializes this object to a file.
        """
        with open(path, 'wb') as fout:
            pickle.dump(self, fout)
        