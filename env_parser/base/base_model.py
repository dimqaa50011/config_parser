import abc
from typing import Dict, Any


class AbstractBaseModel(abc.ABC):
    @classmethod
    def get_fields(cls):
        raise NotImplementedError


class BaseModel(AbstractBaseModel):
    _is_root_model: bool = ...

    @classmethod
    def get_fields(cls) -> Dict[str, Any]:
        return {k: v for k, v in cls.__annotations__.items()}

    @classmethod
    def create(cls, data: Dict):
        _fields = cls.get_fields()
        obj = cls.__new__(cls)
        for k, v in data.items():
            if k in _fields.keys():
                obj.__setattr__(k, v)

        return obj

    @classmethod
    def is_root(cls):
        return cls._is_root_model

    def to_dict(self):
        res = {k: v for k, v in self.__dict__.items() if not (k.startswith("__") and k.endswith("__"))}
        return res

    def __str__(self):
        _fields = ", ".join([f"{item[0]}={item[1]}" for item in self.to_dict().items()])
        return f"{self.__class__.__name__}({_fields})"


class BaseAppSettings(BaseModel):
    _is_root_model = True


class BaseSubModel(BaseModel):
    _is_root_model = False
