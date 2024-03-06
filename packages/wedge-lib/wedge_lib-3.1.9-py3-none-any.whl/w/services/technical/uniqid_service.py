import inspect
from abc import ABC, abstractmethod
from hashlib import sha256
from typing import Type
from uuid import uuid4

from w.services.abstract_service import AbstractService


class AbstractUniqIdGenerator(ABC):
    @classmethod
    @abstractmethod
    def next_id(cls) -> str:
        ...  # pragma: no cover


class FakeGenerator(AbstractUniqIdGenerator):
    start = "000000000000000000000000"
    referrer_last_uuid = {}

    @classmethod
    def next_id(cls) -> str:
        referrer = cls._get_referrer_name()
        if referrer not in cls.referrer_last_uuid:
            cls.referrer_last_uuid[referrer] = cls.start

        cls.referrer_last_uuid[referrer] = cls._increment_id(
            cls.referrer_last_uuid[referrer]
        )
        return cls.referrer_last_uuid[referrer]

    @classmethod
    def reset(cls, last_id=None):
        cls.start = last_id or "000000000000000000000000"
        cls.referrer_last_uuid = {}

    @classmethod
    def _get_referrer_name(cls) -> str:
        context = inspect.stack()[3]
        key = f"{context.filename}{context.lineno}".encode()
        return sha256(key).hexdigest()

    @staticmethod
    def _increment_id(str_id):
        str_id = str(int(str_id) + 1)
        return "0" * (24 - len(str_id)) + str_id


class UuidGenerator(AbstractUniqIdGenerator):
    @classmethod
    def next_id(cls) -> str:
        return str(uuid4())


class UniqIdService(AbstractService):
    _generator: Type[AbstractUniqIdGenerator] = UuidGenerator

    @classmethod
    def get(cls):
        return cls._generator.next_id()

    @classmethod
    def set_fake_generator(cls):
        FakeGenerator.reset()
        cls._generator = FakeGenerator

    @classmethod
    def clear(cls):
        cls._generator = UuidGenerator
