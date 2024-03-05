from typing import Any

import factory
from faker import Faker
from pydantic._internal._model_construction import ModelMetaclass

from easyfactory.utils import is_optional, select_generator_for_type, make_factory_class

fake = Faker()


def _select_generator[T](field_name: str, type_: type[T], model_fields):
    if field_name.endswith("_id") and field_name[:-3] in model_fields:
        return factory.SelfAttribute(f"{field_name[:-3]}.id")
    return select_generator_for_type(field_name, type_,
                                     lambda t: factory.SubFactory(PydanticFactoryGenerator.make_factory_for(t)))


class PydanticFactoryGenerator:
    generated_factories: dict[int, factory.Factory] = {}

    @classmethod
    def make_pydantic_factory(cls, model: ModelMetaclass, attributes: dict[str, Any]):
        if (key := id(model)) not in cls.generated_factories:
            model_fields = model.model_fields
            attrs = {
                field: _select_generator(field, field_info.annotation, model_fields) if not is_optional(
                    field_info.annotation) else None
                for field, field_info in model.model_fields.items() if field_info.is_required()
            }
            attrs.update(attributes)
            cls.generated_factories[key] = make_factory_class(model, attrs)
        return cls.generated_factories[key]

    @classmethod
    def make_factory_for[T](cls, model_: type[T], **attributes: Any) -> type[T]:
        return cls.make_pydantic_factory(model_, attributes)
