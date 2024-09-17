from enum import Enum, auto
import importlib
from dataclasses import dataclass, field
from pathlib import Path
import dotenv
dotenv.load_dotenv()

class Provider(Enum):
    Bitbucket = auto()
    @property
    def instance(self):
        if self._instance is None:
            self._instance = getattr(importlib.import_module(f"baloise_ai_pylib.resources.providers.{self.name}"), self.name)()
        return self._instance
    def __new__(cls, v):
        obj = object.__new__(cls)
        obj._value_ = v
        obj._instance = None
        return obj

@dataclass
class Resource:
    name: str
    org: str
    remote_path:str = Path.cwd().parts[-1]
    provider:Provider=Provider.Bitbucket
    version:str = ''
    local_path:str = field(init = False, default='')

    def __post_init__(self):
        self.provider.instance.provide(self)

class ProviderInterface:
     def provide(self, resource:Resource):
          pass

__all__ = [p.name for p in Provider]