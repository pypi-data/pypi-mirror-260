from abc import ABC, abstractmethod
from typing import Any, Type, Union, Annotated, get_origin, get_args, List
from uuid import UUID as _UUID

from bson import Binary
from bson import ObjectId as _ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


def is_optional(field):
    return get_origin(field) is Union and \
           type(None) in get_args(field)


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> _ObjectId:
        if isinstance(v, _ObjectId):
            return v

        s = handler(v)
        if _ObjectId.is_valid(s):
            return _ObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is _ObjectId or (is_optional(source_type) and _ObjectId in get_args(source_type))
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


ObjectId = Annotated[_ObjectId, ObjectIdPydanticAnnotation]


class Uuid(_UUID):
    @classmethod
    def validate_uuid(cls, v: Any) -> _UUID:
        if isinstance(v, _UUID): return v
        if isinstance(v, str): return _UUID(v)

    def to_binary(self):
        return Binary.from_uuid(self)

    @classmethod
    def from_uuid(cls, payload):
        return Binary.from_uuid(payload)

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate_uuid,
            core_schema.uuid_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                function=cls.from_uuid
            ),
        )


MaybeUuid = Union[Uuid, _UUID, Binary]


def to_binary_uuid(uuid_: Union[MaybeUuid, List[MaybeUuid]]):
    if isinstance(uuid_, list): return [to_binary_uuid(u) for u in uuid_]
    if isinstance(uuid_, Binary): return uuid_
    return Binary.from_uuid(uuid_)

def serialize_object_ids_in_dict(mey_be_dict: Any):
    if not isinstance(mey_be_dict, dict): return
    for key, val in mey_be_dict.items():
        if isinstance(val, _ObjectId):
            mey_be_dict[key] = str(val)
        elif isinstance(val, dict):
            serialize_object_ids_in_dict(val)
        elif isinstance(val, list):
            for item in val:
                serialize_object_ids_in_dict(item)


class DbSettingsABC(ABC):

    @property
    @abstractmethod
    def qdrant_host(self) -> str: ...

    @property
    @abstractmethod
    def qdrant_port(self) -> int: ...

    @property
    @abstractmethod
    def mongo_db_uri(self) -> str: ...

    @property
    @abstractmethod
    def redis_uri(self) -> str: ...

    @property
    @abstractmethod
    def sql_write_uri(self) -> str: ...

    @property
    @abstractmethod
    def sql_read_uri(self) -> str: ...

    @property
    @abstractmethod
    def sql_uri(self) -> str: ...
