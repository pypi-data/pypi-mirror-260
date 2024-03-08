# Copyright PA Knowledge Ltd 2021

from pysisl.deep_merger import ListTuple


class Anon:
    def __init__(self, value):
        self.value = value


class SislEncoder:

    @classmethod
    def dumps(cls, decoded_sisl):
        return "{" + cls._concatenate_sisl_triple(decoded_sisl) + "}"

    @classmethod
    def _concatenate_sisl_triple(cls, decoded_sisl):
        return ', '.join(cls._sisl_triple_list(cls.construct_dict_for_anonymous_data(decoded_sisl)))

    @classmethod
    def construct_dict_for_anonymous_data(cls, decoded_sisl):
        if type(decoded_sisl) != dict:
            return {"_": Anon(decoded_sisl)}
        else:
            return decoded_sisl

    @classmethod
    def _sisl_triple_list(cls, dict_to_encode):
        return [cls._construct_sisl_triple(k, v) for k, v in dict_to_encode.items()]

    @classmethod
    def _construct_sisl_triple(cls, key, value):
        return f"{key}: {cls._select_type_and_value(value)}"

    @classmethod
    def _select_type_and_value(cls, value):
        if type(value) == Anon:
            return f"!_{cls.sisl_string_from_type(value.value)}"
        else:
            return f"!{cls.sisl_string_from_type(value)}"

    @classmethod
    def sisl_string_from_type(cls, value):
        try:
            return {
                int: lambda val: f"int \"{value}\"",
                float: lambda val: f"float \"{value}\"",
                str: lambda val: f"str \"{cls._escape(value)}\"",
                bool: lambda val: f"bool \"{str(value).lower()}\"",
                list: lambda val: f"list {{{cls._construct_sisl_for_list_object(value)}}}",
                dict: lambda val: f"obj {cls.dumps(value)}",
                None.__class__: lambda val: f"null \"\""
            }[type(value)](value)
        except KeyError as err:
            raise TypeValidationError(err)

    @classmethod
    def _escape(cls, value: str):
        return value.encode('unicode_escape').decode().replace(r'"', r'\"')

    @classmethod
    def _construct_sisl_for_list_object(cls, value):
        return ', '.join([cls._construct_sisl_triple(*cls._check_if_list_tuple(i, item)) for i, item in enumerate(value)])

    @classmethod
    def _check_if_list_tuple(cls, index, list_item):
        if type(list_item) is ListTuple:
            return f"_{list_item.position}", list_item.value

        return f"_{index}", list_item


class TypeValidationError(Exception):
    pass
