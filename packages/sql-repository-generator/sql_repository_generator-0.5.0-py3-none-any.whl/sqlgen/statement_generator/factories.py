from sqlalchemy import Column
from sqlalchemy.orm import RelationshipProperty, class_mapper

from sqlgen.joins import resolve_model_joins
from sqlgen.statement_generator.base import StatementGenerator
from sqlgen.statement_generator.object_bound import ObjectBoundStatementGenerator


def make_statement_generator_class_for[T](cls: type[T]) -> type[StatementGenerator[T]]:
    """
    Generate a StatementGenerator class for the given model

    :param cls: the model to use for the StatementGenerator class
    :return: a child class of StatementGenerator with `cls` set
    """
    return type(f"{cls.__name__}StatementGenerator", (StatementGenerator,), {"cls": cls})


def make_object_bound_statement_generator_class_for[S, D](
        cls: type[S],
        model_to_join: type[D]
) -> type[ObjectBoundStatementGenerator[S, D]]:
    """
    Generate a ObjectBoundStatementGenerator class for the given model `cls` with filters for bounding to
    `model_to_join`

    bound model == query will be filtered to only match objects that have a relation with the instance of
    the model specified at class init (this function generate a class but does not instantiate it)

    :param cls: the model to use for the return of ObjectBoundStatementGenerator
    :param model_to_join: the model to bound for the requests
    :return: a child class of ObjectBoundStatementGenerator with `cls` set and joins to `model_to_join`
    """
    joins: list[RelationshipProperty | Column] = resolve_model_joins(cls, model_to_join)
    return type(f"{model_to_join.__name__}Bound{cls.__name__}StatementGenerator", (ObjectBoundStatementGenerator,),
                {"cls": cls, "joins": joins})
