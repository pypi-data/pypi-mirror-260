from sqlalchemy import Column
from sqlalchemy.orm import Mapper, RelationshipProperty, class_mapper, InstrumentedAttribute

from sqlgen.statement_generator.constrained import Constraint


class NoValidJoins(ValueError):
    def __init__(self, source, destination, previous_joins):
        super().__init__(source, destination, previous_joins)
        self.destination = destination
        self.source = source
        self.previous_joins = previous_joins

    def __str__(self):
        return f"No Relation between {self.source=} and {self.destination=}"


def _resolve_model_joins(
        inspected_mapper: Mapper,
        model_to_join: type,
        previous_joins: list[RelationshipProperty],
        visited_mappers: list[Mapper]
) -> list[InstrumentedAttribute | Column]:
    """
    Resolve the joins needed to access a given model from a mapper

    :param inspected_mapper: the mapper to check for relation to the model to join
    :param model_to_join: the model to join
    :param previous_joins: joins already done to access the inspected mapper
    :param visited_mappers: the mappers already visited during the recursion to avoid revisiting them again
        (and infinite loop)
    :raise ValueError: if no chain of joins links to the model_to_join
    :return: a ordered list of relation attributes to access the model to join from the inspected mapper
    """
    visited_mappers.append(inspected_mapper)
    for relation in inspected_mapper.relationships:
        if relation.entity in visited_mappers:
            continue
        if relation.entity.class_ is model_to_join:
            column = list(relation.local_columns)[0]
            return previous_joins + [column]
        try:
            return previous_joins + _resolve_model_joins(relation.entity, model_to_join, [relation.class_attribute],
                                                         visited_mappers)
        except NoValidJoins:
            continue
    raise NoValidJoins(inspected_mapper.entity, model_to_join, previous_joins)


def resolve_model_joins[S, D](model_source: type[S], model_destination: type[D]) -> Constraint:
    """
    Resolve the joins needed to access the `model_destination` from the `model_source`

    :param model_source: the source of the joins to do
    :param model_destination: the model to join
    :raise ValueError: if no chain of joins links to the model_to_join
    :return: a ordered list of relation attributes to access the `model_destination` from the `model_source`
    """
    joins = _resolve_model_joins(class_mapper(model_source), model_destination, [], [])
    return Constraint(joins=joins[:-1], joined_column=joins[-1], joined_model=model_destination)
