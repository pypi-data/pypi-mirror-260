import builtins
import datetime
import enum
import random
import types
import typing
import uuid
from typing import Any

import factory
from factory.base import FactoryMetaClass
from factory.declarations import BaseDeclaration
from faker import Faker

banned_prefix = ["_", "get_", "set_"]
banned_words = ["provider"]
fake = Faker()


def is_valid(word):
    return all(banned_word not in word for banned_word in banned_words) and all(
        not word.startswith(prefix) for prefix in banned_prefix)


faker_providers = [p for p in dir(fake) if is_valid(p)]


def is_optional(field):
    return typing.get_origin(field) is typing.Union and \
        type(None) in typing.get_args(field)


def _get_faker_provider_based_on_name(field_name: str) -> str:
    for provider in faker_providers:
        if field_name == provider:
            return provider
    return "word"


def select_faker_based_on_name(field_name: str) -> factory.Faker:
    return factory.Faker(_get_faker_provider_based_on_name(field_name))


def select_generator_for_type[T](
        field_name: str,
        type_: type[T],
        child_model_callback: typing.Callable[[type[T]], BaseDeclaration]
) -> BaseDeclaration | None:
    match type_:
        case builtins.bytes:
            return factory.Faker("binary")
        case builtins.str:
            return select_faker_based_on_name(field_name)
        case builtins.int:
            return factory.Faker("pyint")
        case builtins.float:
            return factory.Faker("pyfloat")
        case builtins.bool:
            return factory.Faker("pybool")
        case datetime.datetime:
            return factory.Faker("date_time")
        case uuid.UUID:
            return factory.LazyFunction(uuid.uuid4)
        case _:
            if isinstance(type_, enum.EnumType):
                return factory.LazyFunction(lambda: random.choice(list(type_)))

            args = typing.get_args(type_)
            match typing.get_origin(type_):
                case builtins.list:
                    return factory.List([select_generator_for_type(field_name, args[0], child_model_callback)])
                case builtins.dict:
                    if args[0] is str:
                        return factory.Dict({getattr(fake, _get_faker_provider_based_on_name(field_name))():
                                                 select_generator_for_type(field_name, args[1], child_model_callback)})
                    else:
                        raise NotImplementedError
                        # TODO make the code below work
                        # return factory.LazyFunction(
                        #    lambda: {select_generator_for_type(field_name, args[0], submodel_callback).
                        #             evaluate(None, None, {"locale": None}):
                        #                 select_generator_for_type(field_name, args[1], submodel_callback).
                        #             evaluate(None, None, {"locale": None})})
                case types.UnionType:
                    if types.NoneType in args:
                        return None
                    # TODO implement generation in case of Union
                    raise TypeError(type_)
                case None:
                    return child_model_callback(type_)
                case _:
                    raise TypeError(type_)


def make_factory_class[T](model_: type[T], attributes: dict[str, Any]):
    class MetaClass:
        model = model_

    attributes.update({"Meta": MetaClass})
    return FactoryMetaClass.__new__(FactoryMetaClass, model_.__name__ + "Factory", (factory.Factory,),
                                    attributes)
