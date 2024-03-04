"""
Provide some common classes for work with configurations
"""

import typing

import yaml
import pydantic

class Singletone(type):
    """
    Singletone metaclass for making singletones
    """

    __instances: dict[type, typing.Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)

        return cls.__instances[cls]


class ConstModel: # pylint: disable=too-few-public-methods
    """
    Make model unchangeable
    """

    def __setattr__(self, _: str, __: typing.Any) -> None:
        """
        Override the default __setattr__ method to make the object readonly.

        Args:
            _: Ignored parameter.
            __: Ignored parameter.

        Raises:
            AttributeError: If any attempt is made to modify the object.
        """

        raise AttributeError("Object is readonly")


class ConfigModel(pydantic.BaseModel):
    """
    This model should be inherited and the type of config
    should be relaced with the real one. ConfigModel child
    than may be passed in YamlConfig to correctly
    validate yaml file content
    """

    cfg: typing.Type[pydantic.BaseModel]


class ConstModelWrapper(metaclass=Singletone):
    """
    If you make model wrapper based on
    these class it will be const and singletone
    """

    _model: typing.Optional[pydantic.BaseModel] = None

    def __getattr__(self, name: str) -> typing.Any:
        return getattr(self._model, name)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        try:
            self.__getattribute__(name)
            super().__setattr__(name, value)
        except AttributeError as attr_err:
            raise AttributeError("Object is readonly") from attr_err


class YamlConfig(ConstModelWrapper): # pylint: disable=too-few-public-methods
    """
    Universal Yaml config class
    """

    def __init__(self,
        config_file_path: str,
    ) -> None:
        with open(config_file_path, mode="r", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)

        model_types = typing.get_type_hints(self)["_model"]
        model_type = typing.get_args(model_types)[0]

        self._model = model_type(cfg=config)
