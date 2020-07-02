from typing import Tuple, List, Any
from enum import Enum


class TupleEnumMixin:
    @classmethod
    def get_tuple(cls) -> Tuple[Any, str]:
        return tuple((tag.value, tag.to_string()) for tag in cls)

    @classmethod
    def get_dict(cls) -> Tuple[Any, str]:
        return {tag.value: tag.to_string() for tag in cls}

    @classmethod
    def has_value(cls, value: Any) -> bool:
        return value in cls.__members__.values()

    @classmethod
    def get_values(cls) -> List[Any]:
        return [e.value for e in cls]

    def to_string(self) -> str:
        raise NotImplementedError()


class Status(int, TupleEnumMixin, Enum):

    TODO = 0
    IN_PROGRESS = 1
    DONE = 2

    def to_string(self):
        mapping = {
            Status.TODO: 'TODO',
            Status.IN_PROGRESS: 'In Progress',
            Status.DONE: 'Done',
        }
        return mapping.get(self)
