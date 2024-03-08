from enum import Enum

from genson import SchemaBuilder
from jsonschema import ValidationError, validate


class InvalidMode(Enum):
    skip = "SKIP"
    ignore = "IGNORE"
    abort = "ABORT"


class JsonSchemaBuilder:
    _builder: SchemaBuilder
    schema: dict | None = None

    def __init__(self):
        self._builder = SchemaBuilder()

    def init_from_schema(self, schema: dict):
        self.schema = schema
        self._builder.add_schema(schema)
        self.schema = self._builder.to_schema()
        return self

    def init_from_data(self, data: dict):
        self._builder.add_schema({"type": "object", "properties": {}})
        self._builder.add_object(data)
        self.schema = self._builder.to_schema()
        return self

    def validate(self, data: dict) -> tuple[bool, ValidationError]:
        try:
            validate(instance=data, schema=self.schema)
        except ValidationError as e:
            return False, e
        return True, None
