from genomkit import GRegions
from collections import OrderedDict
import numpy as np
import pandas as pd


class GRegionsSet:
    """
    GRegionsSet module

    This module contains functions and classes for working with a collection of
    multiple GRegions.
    """
    def __init__(self, name: str = "", load_dict=None):
        """Initiate a GRegionsSet object which can contain multiple GRegions.

        :param name: Define the name, defaults to ""
        :type name: str, optional
        :param load_dict: Given the file paths of multiple GRegions as a
                          dictionary with names as keys and values as file
                          paths, defaults to None
        :type load_dict: dict, optional
        """
        self.collection = OrderedDict()
        if load_dict:
            for name, filename in load_dict.items():
                self.add(name=name,
                         regions=GRegions(name=name,
                                          load=filename))

    def add(self, name: str, regions):
        """Add a GRegions object into this set.

        :param name: Define the name
        :type name: str
        :param regions: Given the GRegions
        :type regions: GRegions
        """
        self.collection[name] = regions

    def __len__(self):
        """Return the number of GRegions in this set.

        :return: Number of GRegions
        :rtype: int
        """
        return len(self.collection)

    def __getattr__(self, key):
        if key in self.collection:
            return self.collection[key]
        else:
            raise AttributeError(
                f"'{self.collection.__class__.__name__}'"
                f" object has no attribute '{key}'"
                )

    def __setattr__(self, key, value):
        self.collection[key] = value

    def get_names(self):
        """Return the names of all GRegions.

        :return: Names
        :rtype: list
        """
        return list(self.collection.keys())

    def get_lengths(self):
        """Return a list of the number of regions in all GRegions

        :return: A list of region numbers
        :rtype: list
        """
        res = OrderedDict()
        for name, regions in self.collection.items():
            res[name] = len(regions)
        return res

    def count_overlaps(self, query_set, percentage: bool = False):
        """Return a pandas dataframe of the numbers of overlapping regions
        between the reference GRegionsSet (self) and the query GRegionsSet.

        :param query_set: Query GRegionsSet
        :type query_set: GRegionsSet
        :param percentage: Convert the contingency table into percentage. The
                           sum per row (reference) is 100%, defaults to False
        :type percentage: bool, optional
        :return: Matrix of numbers of overlaps
        :rtype: dataframe
        """
        res = np.zeros((len(self), len(query_set)))
        row_names = []
        col_names = []
        for i, (ref_name, ref) in enumerate(self.collection.items()):
            row_names.append(ref_name)
            for j, (query_name, query) in enumerate(query_set.items()):
                col_names.append(query_name)
                c = ref.overlap_count(target=query)
                res[i, j] = c
        df = pd.DataFrame(res,
                          index=row_names,
                          columns=col_names)
        if percentage:
            df = df.div(df.sum(axis=1), axis=0) * 100
        return df
