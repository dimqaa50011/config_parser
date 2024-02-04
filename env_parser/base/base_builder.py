import abc
from typing import Optional, Type

from env_parser.base.base_model import BaseAppSettings, BaseModel
from env_parser.base.base_parser import BaseParser
from env_parser.exc import NotValidModel, NotValidParser


class AbstractBaseBuilder(abc.ABC):
    def build(self, *args, **kwargs):
        raise NotImplementedError


class BaseBuilder(AbstractBaseBuilder):
    def __init__(
            self, *args,
            root_model: BaseAppSettings,
            parser: BaseParser
    ):
        self._root_model = root_model
        self._parser = parser

    def build(self, *args, **kwargs) -> BaseAppSettings:
        if not isinstance(self._root_model, BaseAppSettings):
            raise NotValidModel(f"model must be BaseAppSettings. type = {type(self._root_model)}")
        if not isinstance(self._parser, BaseParser):
            raise NotValidParser(f"parser must be BaseParser. type = {type(self._parser)}")

        return self._run_build(*args, **kwargs)

    def _run_build(self, *args, **kwargs):
        raise NotImplementedError


class DefaultBuilder(BaseBuilder):

    def _get_values(self, model: Type[BaseModel]):
        fields_model = model.get_fields()
        if model.is_root():
            return {f: self.__build_model(v) for f, v in fields_model.items()}
        return self._parser.parse(fields_model)

    def __build_model(self, model: Type[BaseModel]):
        values = self._get_values(model)
        return model.create(values)

    def _run_build(self, *args, **kwargs):
        return self.__build_model(self._root_model)
