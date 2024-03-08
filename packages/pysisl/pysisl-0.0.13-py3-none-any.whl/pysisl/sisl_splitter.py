# Copyright PA Knowledge Ltd 2021

from pysisl.sisl_encoder import SislEncoder
from pysisl.explode_structure import ExplodeStructure
from pysisl.remove_data import RemoveData


class SplitSisl:
    def __init__(self, max_length=1000000):
        self.max_length = max_length
        self.exploded_input = None

    def split_sisl(self, decoded_sisl_input):
        sisl_file = []
        self.exploded_input = self._convert_to_list_tuple(decoded_sisl_input)
        sisl_file.append(self._generate_sisl_file())
        while self._check_for_next_file_to_generate():
            sisl_file.append(self._generate_sisl_file())
        return sisl_file

    @staticmethod
    def _convert_to_list_tuple(decoded_sisl_input):
        return ExplodeStructure.explode_structure(decoded_sisl_input)[-1]

    def _generate_sisl_file(self):
        potential_sisl_file_candidates = ExplodeStructure.explode_structure(self.exploded_input)
        encoded_sisl, successful_struct = self._split_to_encoded_sisl(potential_sisl_file_candidates, self.max_length)
        self.exploded_input = RemoveData.subtract_data_from_input(self.exploded_input, successful_struct)
        return encoded_sisl

    def _check_for_next_file_to_generate(self):
        return not (self.exploded_input == {} or self.exploded_input == [])

    def _split_to_encoded_sisl(self, decoded_sisl_candidates, max_bytes):
        sisl = SislEncoder.dumps(decoded_sisl_candidates[0])
        self._check_sisl_length(max_bytes, sisl)
        decoded_sisl = decoded_sisl_candidates[0]

        for file in decoded_sisl_candidates:
            test_sisl = SislEncoder.dumps(file)
            if len(test_sisl.encode('utf-8')) > max_bytes:
                return sisl, decoded_sisl
            else:
                sisl = test_sisl
                decoded_sisl = file

        return sisl, decoded_sisl_candidates[-1]

    @staticmethod
    def _check_sisl_length(max_bytes, sisl):
        if len(sisl) > max_bytes:
            raise Exception(f"Unable to split input. {sisl} is greater than max size. ")
