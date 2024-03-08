# Copyright PA Knowledge Ltd 2021

from pysisl.deep_merger import DeepMerger, ListTuple


class ExplodeStructure:
    @classmethod
    def explode_structure(cls, structure):
        """
        Expands input structure to list, from first item adding successive items as new lists
        """
        return cls._merge_paths(cls.enumerate_paths(structure))

    @classmethod
    def _merge_paths(cls, leaves):
        output_list = [[next(leaves)][0]]
        for each_element in leaves:
            output_list.append(DeepMerger.merge(output_list, each_element))
        return output_list

    @classmethod
    def enumerate_paths(cls, p):
        if type(p) is list:
            yield from cls._enumerate_list(p)
        elif type(p) is dict:
            yield from cls._enumerate_dict(p)
        elif type(p) is ListTuple:
            yield from cls._enumerate_list_tuple(p)
        else:
            yield p

    @classmethod
    def _enumerate_list(cls, p):
        """
        Expands list to nested list, from first element adding successive elements as ListTuples
        [1, 2, 3]
        -> [[ListTuple(1, 0)], [ListTuple(1, 0), ListTuple(2, 1)], [ListTuple(1, 0), ListTuple(2, 1), ListTuple(3, 2)]]
        """
        for index, list_item in enumerate(p):
            for item in cls.enumerate_paths(list_item):
                if type(item) == ListTuple:
                    yield [item]
                else:
                    yield [ListTuple(item, index)]

    @classmethod
    def _enumerate_dict(cls, p):
        """
        Expands dictionary to list, from first {key, value} pair adding successive {key, value} pairs
        {"key": 1, "key2": 2, "key3": 3}
        -> [{key1: 1}, {"key": 1, "key2": 2}, {"key": 1, "key2": 2, "key3": 3}]
        """
        for key, value in p.items():
            for path in cls.enumerate_paths(value):
                yield {key: path}

    @classmethod
    def _enumerate_list_tuple(cls, p):
        """
        Expands ListTuples to list, from first element adding successive elements
        [ListTuple(1, 0), ListTuple(2, 1), ListTuple(3, 1)]
        -> [[ListTuple(1, 0)], [ListTuple(1, 0), ListTuple(2, 1)], [ListTuple(1, 0), ListTuple(2, 1), ListTuple(3, 2)]]
        """
        if isinstance(p.value, (dict, list)):
            for value in cls.enumerate_paths(p.value):
                yield ListTuple(value, p.position)
        else:
            yield p

