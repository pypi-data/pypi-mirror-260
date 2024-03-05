import pickle
from typing import Dict
from barfi.schema.schema_manager import AbsSchemaManager

# Schema Manager
class LocalSchemaManager(AbsSchemaManager):
    def __init__(self, schema_path = None) -> None:
        if schema_path is None:
            schema_path = 'schemas.barfi'
        self.schema_path = schema_path
        
    
    def get_schema_name(self, schema_name: str, user: str) -> str:
        if user == '' or user is None:
            return schema_name
        return f'{schema_name}@{user}'
    
    
    def get_user(self, schema_name: str) -> str:
        if '@' in schema_name:
            return schema_name.split('@')[1]
        return ''
    
    def get_prefix_name(self, schema_name: str) -> str:
        if '@' in schema_name:
            return schema_name.split('@')[0]
        return schema_name
    
    def load_schemas(self, user: str) -> Dict:
        try:
            with open('schemas.barfi', 'rb') as handle_read:
                schemas = pickle.load(handle_read)
        except FileNotFoundError:
            schemas = {}

        schema_names = list(schemas.keys())
        
        if (len(schemas) == 0):
            return {'schema_names': schema_names, 'schemas': schemas}
        # Dict 按名称过滤
        name = self.get_schema_name('', user)
        if (name != '' and name is not None):
            _filtered = {key: value for key, value in schemas.items() if key.endswith(name)}
        else:
            _filtered = schemas
        keys = list(_filtered.keys())
        show_names = [self.get_prefix_name(key) for key in keys]
        return {'schema_names': show_names, 'schemas': _filtered}


    def save_schema(self, schema_name: str, user: str, schema_data: Dict) -> bool:
        try:
            with open('schemas.barfi', 'rb') as handle_read:
                schemas = pickle.load(handle_read)
        except FileNotFoundError:
            schemas = {}

        name = self.get_schema_name(schema_name, user)
        with open('schemas.barfi', 'wb') as handle_write:
            schemas[name] = schema_data
            pickle.dump(schemas, handle_write, protocol=pickle.HIGHEST_PROTOCOL)
        return True


    def load_schema_name(self, schema_name: str, user: str) -> Dict:
        schemas_barfi = self.load_schemas(user)
        name = self.get_schema_name(schema_name, user)
        if schema_name in schemas_barfi['schema_names']:
            return schemas_barfi['schemas'][name]
        else:
            raise ValueError(
                f'Schema :{schema_name}: not found in the saved schemas')


    def delete_schema(self, schema_name: str, user: str) -> Dict:
        try:
            with open('schemas.barfi', 'rb') as handle_read:
                schemas = pickle.load(handle_read)
        except FileNotFoundError:
            schemas = {}
        temp = {}
        del_schema_name = self.get_schema_name(schema_name, user)
        if del_schema_name in schemas:
            temp = schemas[del_schema_name]
            del schemas[del_schema_name]
        else:
            raise ValueError(
                f'Schema :{del_schema_name}: not found in the saved schemas')
        
        with open('schemas.barfi', 'wb') as handle_write:
            pickle.dump(schemas, handle_write, protocol=pickle.HIGHEST_PROTOCOL)
        return temp
    