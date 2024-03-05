import abc
from logging import getLogger
from typing import Any

from sqlgen.statement_generator.base import StatementGenerator
from sqlgen.statement_generator.factories import make_statement_generator_class_for

logger = getLogger(__name__)


def getattr_with_parent[T](attrs: dict[str, type[T] | Any], bases: tuple, attr_name: str):
    """
    get an attribute value from the dict attrs or from the first bases that possess it.

    :param attrs: a dict of parameters where the key could be
    :param bases: the list of class to search for if not found in the attrs
    :param attr_name: the key to search for
    :raise KeyError: if the attr_name is not found anywhere
    :return: the value of the first occurrence of attr_name within the child to parent hierarchy
    """
    model: type[T] = attrs.get(attr_name)
    if model is None:
        bases_cls = list(filter(lambda obj: hasattr(obj, attr_name), bases))
        if len(bases_cls) == 0:
            raise KeyError(f"{attr_name=} is not set on any model")
        elif len(bases_cls) > 1:
            logger.warning("multiple %s defined using %s", attr_name, bases_cls[0])
        # for some reason that i don't understand, we cannot use bases_cls[0][attr_name] due to it being a generic alias
        # bases_cls[0][attr_name] == ...<locals>.ProjectRelatedRepository[ForwardRef('bound_model')]
        # getattr(bases_cls[0],attr_name) == <class 'test_data.models.Project'>
        model = getattr(bases_cls[0], attr_name)
    return model


class DatabaseRepositoryMeta[T](abc.ABCMeta):

    def __new__(cls, name: str, bases: tuple, attrs: dict[str, type[T] | Any], generate: bool = True):
        if generate:
            attrs["statement_generator_factory"] = cls.get_statement_generator_factory(bases, attrs)
        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def get_statement_generator_factory[T](cls, bases: tuple, attrs: dict[str, type[T] | Any]) -> type[
        StatementGenerator[T]]:
        model: type[T] = getattr_with_parent(attrs, bases, "cls")
        return make_statement_generator_class_for(model)


class DatabaseRepository[T](abc.ABC, metaclass=DatabaseRepositoryMeta, generate=False):
    """
    Base class for DatabaseRepositories
    """
    # Metaclass provided
    statement_generator_factory: type[StatementGenerator[T]]
    # Consumer Provided
    cls: type[T]  # this must be set by the child class
    # other attr
    statement_generator: StatementGenerator[T]

    def __init__(self, *args, **kwargs):
        if self.__class__ == DatabaseRepository:
            raise ValueError("Cannot instantiate DatabaseRepository directly")
        self.statement_generator: StatementGenerator[T] = self.statement_generator_factory(*args, **kwargs)
