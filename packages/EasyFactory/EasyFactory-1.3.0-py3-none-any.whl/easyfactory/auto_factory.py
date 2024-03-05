import typing
from logging import getLogger

import pydantic._internal._model_construction as pydantic_model
from sqlalchemy.orm import decl_api

from easyfactory.pydantic import PydanticFactoryGenerator
from easyfactory.sqlalchemy import SQLAlchemyFactoryGenerator

logger = getLogger(__name__)


def make_factory_for[T](model: type[T], **attributes: typing.Any) -> type[T]:
    if isinstance(model, pydantic_model.ModelMetaclass):
        return PydanticFactoryGenerator.make_pydantic_factory(model, attributes)
    elif isinstance(model, decl_api.DeclarativeAttributeIntercept):
        return SQLAlchemyFactoryGenerator.make_sqlalchemy_factory(model, attributes)
    raise TypeError(model)


class AutoFactoryMeta(type):
    def __new__[T](cls, name, bases, attributes: dict[str, type[T] | typing.Any]) -> T:
        x = super().__new__(cls, name, bases, attributes)
        if name == "AutoFactory":
            return x
        if (meta := attributes.get("Meta", None)) is not None:
            if (model := getattr(meta, "model", None)) is not None:
                logger.debug("model found generating Factory for `%s`", model)
                return make_factory_for(model, **attributes)
            else:
                logger.warning("Meta class found but no model inside it")
        raise TypeError(name)


class AutoFactory(metaclass=AutoFactoryMeta):
    ...
