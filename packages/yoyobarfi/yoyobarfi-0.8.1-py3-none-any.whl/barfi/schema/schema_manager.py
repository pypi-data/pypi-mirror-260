from abc import ABCMeta, abstractmethod
from typing import Dict
    
class AbsSchemaManager(metaclass=ABCMeta):
    @abstractmethod
    def load_schemas(self, user: str) -> Dict:
        pass
    
    @abstractmethod
    def save_schema(self, schema_name: str, user: str, schema_data: Dict) -> bool:
        pass
      
    @abstractmethod
    def load_schema_name(self, schema_name: str, user: str) -> Dict:
        pass
    
    @abstractmethod
    def delete_schema(self, schema_name: str, user: str) -> bool:
        pass