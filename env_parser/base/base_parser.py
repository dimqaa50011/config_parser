import os.path
from pathlib import PosixPath, Path
from typing import Union, Type, Dict, Any

from dotenv import load_dotenv

from env_parser.exc import NotFoundEnvFile, NotFileError, NotFoundAttrError


class BaseParser:
    def parse(self, fields: Dict[str, Type]):
        raise NotImplementedError


class EnvironmentParser(BaseParser):
    def _get_var(self, var: str) -> str:
        res = os.environ.get(var, None)
        if res is None:
            raise NotFoundAttrError(f"Not fount attr {var}")

        return res

    def _get_variables(self, variables: Dict[str, Any]) -> Dict[str, str]:
        env_data = {}
        for key, var in variables.items():
            res = self._get_var(key)
            env_data[key] = self._cast_to_current_type(res, var)
        return env_data

    def _cast_to_current_type(self, var: str, type_var: Type):
        result = type_var(var)
        return result

    def parse(self, fields: Dict[str, Type]) -> Dict[str, Any]:
        return self._get_variables(fields)


class EnvFileParser(EnvironmentParser):
    def __init__(self, env_file: Union[str, Path]):
        self.__env_file = env_file

    def parse(self, fields: Dict[str, Type]) -> Dict[str, Any]:
        path = Path(self.__env_file)
        if not path.exists():
            raise NotFoundEnvFile(f".env file not found. Path = {self.__env_file}")
        if path.is_dir():
            raise NotFileError(f"{self.__env_file} not file!!")

        load_dotenv(path)

        return super().parse(fields)
