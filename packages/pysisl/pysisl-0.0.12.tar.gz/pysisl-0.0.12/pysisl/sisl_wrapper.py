# Copyright PA Knowledge Ltd 2021
import construct
from itertools import cycle
import secrets
from binascii import unhexlify


class SislWrapper:
    def __init__(self, key_generator=None):
        self.majorVersion = 1
        self.minorVersion = 0
        self.headerLen = 48
        self.encapsulationType = 1
        self.encapsulationConfig = 3
        self.encapsulationDataLen = 8
        self.key = SislWrapper.key_generation() if key_generator is None else key_generator
        self.padding = 0
        self.cloaked_dagger = self._build_cloaked_dagger_header()
        self.chunk_count = 0

    def wraps(self, data: str):
        return self.cloaked_dagger + SislWrapper._xor_data(self.key, SislWrapper._is_bytes(data))

    @staticmethod
    def _xor_data(key, data):
        return bytes([a ^ b for (a, b) in zip(data, cycle(key))])

    @staticmethod
    def _is_bytes(data):
        if isinstance(data, (bytes, bytearray)):
            return data
        else:
            raise TypeError("Input must be bytes")

    def unwraps(self, data):
        payload = self._get_payload(data)
        unwrapped = SislWrapper._xor_data(self.key, payload)
        self.chunk_count += 1
        return unwrapped

    def _get_payload(self, data):
        if self.chunk_count == 0:
            CloakDagger.check_valid_cloaked_dagger_header(SislWrapper._is_bytes(data))
            self.key = CloakDagger.get_cloak_dagger_field_by_name(data, 'Encap_Mask')
            return SislWrapper._extract_payload_from_data(data)
        else:
            return data

    @staticmethod
    def _extract_payload_from_data(data):
        return data[CloakDagger.get_cloak_dagger_field_by_name(data, 'Length'):]

    def _build_cloaked_dagger_header(self):
        return CloakDagger.cloak_dagger_bytes().build(
            dict(Major_Version=self.majorVersion,
                 Minor_Version=self.minorVersion,
                 Length=self.headerLen,
                 Encap_Type=self.encapsulationType,
                 Encap_Config=self.encapsulationConfig,
                 Encap_Dlen=self.encapsulationDataLen,
                 Encap_Mask=self.key,
                 Padding=self.padding))

    @staticmethod
    def key_generation():
        key = unhexlify(secrets.token_hex(8))
        if b'\x00' in key:
            key = SislWrapper.key_generation()
        return key


class CloakDagger:
    @staticmethod
    def cloak_dagger_bytes():
        return construct.Struct("Magic_Number_1" / construct.Const(b'\xd1\xdf\x5f\xff'),
                                "Major_Version" / construct.Int16ub,
                                "Minor_Version" / construct.Int16ub,
                                "Length" / construct.Int32ub,
                                "Encap_Type" / construct.Int32ub,
                                "Encap_Config" / construct.Int16ub,
                                "Encap_Dlen" / construct.Int16ub,
                                "Encap_Mask" / construct.Bytes(8),
                                "RESERVED" / construct.Padding(16),
                                "Magic_Number_2" / construct.Const(b'\xff\x5f\xdf\xd1')
                                )

    @staticmethod
    def check_valid_cloaked_dagger_header(data):
        try:
            CloakDagger.cloak_dagger_bytes().parse(data)
        except construct.core.ConstructError as e:
            raise InvalidHeaderError(f"Header could not be validated: {e}")

    @staticmethod
    def get_cloak_dagger_field_by_name(data, field):
        return CloakDagger.cloak_dagger_bytes().parse(data).search(field)


class InvalidHeaderError(Exception):
    pass
