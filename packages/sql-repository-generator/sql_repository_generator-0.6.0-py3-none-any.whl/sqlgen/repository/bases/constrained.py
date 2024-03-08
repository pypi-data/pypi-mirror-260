import inspect
from logging import getLogger
from typing import Any

from sqlgen.repository.bases.base import DatabaseRepositoryMeta, getattr_with_parent
from sqlgen.statement_generator.constrained import ConstrainedStatementGenerator
from sqlgen.statement_generator.factories import make_constrained_statement_generator_class_for

logger = getLogger(__name__)


class ConstrainedRepositoryMeta[T](DatabaseRepositoryMeta):
    @classmethod
    def get_statement_generator_factory(
            cls,
            bases: tuple,
            attrs: dict[str, type[T] | Any]
    ) -> type[ConstrainedStatementGenerator[T]]:
        model: type[T] = getattr_with_parent(attrs, bases, "cls")
        bound_models = set()

        # get a set of all defined bound_model as heritage would hide them
        try:
            bound_models.add(getattr_with_parent(attrs, bases, "bound_model"))
        except KeyError:
            logger.debug("no `bound_model` defined for class")
        else:  # no need to iterate the bases if it's already not found on main
            for base in bases:
                try:
                    bound_models.add(getattr_with_parent(vars(base), inspect.getmro(base), "bound_model"))
                except KeyError:
                    logger.debug(f"no `bound_model` defined on {base=}")
        try:
            bound_models |= set(getattr_with_parent(attrs, bases, "bound_models"))
        except KeyError:
            logger.debug(f"no `bound_models` using only `bound_model` of class and parent classes: {bases}")
        return make_constrained_statement_generator_class_for(model, list(bound_models))
