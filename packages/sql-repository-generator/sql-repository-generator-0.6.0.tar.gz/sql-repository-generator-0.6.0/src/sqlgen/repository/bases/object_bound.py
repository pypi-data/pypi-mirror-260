from typing import Any

from sqlgen.repository.bases.base import DatabaseRepositoryMeta, DatabaseRepository, getattr_with_parent
from sqlgen.statement_generator.factories import make_object_bound_statement_generator_class_for
from sqlgen.statement_generator.object_bound import ObjectBoundStatementGenerator


class ObjectBoundRepositoryMeta[T, D](DatabaseRepositoryMeta):
    @classmethod
    def get_statement_generator_factory(
            cls,
            bases: tuple,
            attrs: dict[str, type[T] | type[D] | Any]
    ) -> type[ObjectBoundStatementGenerator[T, D]]:
        """
        get an ObjectBoundStatementGenerator class/type for the repository class generated

        :param bases: the bases of the created repository class
        :param attrs: the class parameters of the created repository class (expected "cls", and "bound_model")
        :return: an ObjectBoundStatementGenerator class/type for the model and bound_model specified in class attributes
        """
        model: type[T] = getattr_with_parent(attrs, bases, "cls")
        bound_model: type[D] = getattr_with_parent(attrs, bases, "bound_model")
        return make_object_bound_statement_generator_class_for(model, bound_model)


class ObjectBoundRepository[T, D](DatabaseRepository, metaclass=ObjectBoundRepositoryMeta, generate=False):
    bound_model: type[D]
    statement_generator: ObjectBoundStatementGenerator[T, D]

    def __init__(self, bound_object_id, *args, **kwargs):
        if self.__class__ == ObjectBoundRepository:
            raise ValueError("Cannot instantiate ObjectBoundRepository directly")
        super().__init__(*args, bound_object_id=bound_object_id, **kwargs)
