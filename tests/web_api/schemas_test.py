import unittest
from model_lambda.web_api.schemas import ModelCollectionSchema, ModelMetadataSchema, ErrorSchema


class SchemaTests(unittest.TestCase):

    def test1(self):
        """testing ModelCollectionSchema"""
        # arrange
        schema = ModelCollectionSchema()

        # act
        exception_thrown = False
        try:
            result = schema.loads(json_data='{"models":[{"display_name":"asdf", "qualified_name":"asdf", "description":"asdf", "major_version":1, "minor_version":1}]}')
        except Exception as e:
            exception_thrown = True

        # assert
        self.assertFalse(exception_thrown)

    def test2(self):
        """testing ModelMetadataSchema"""
        # arrange
        schema = ModelMetadataSchema()

        # act
        exception_thrown = False
        try:
            result = schema.loads(json_data='{ "description": "string", "display_name": "string", "input_schema": { "additionalProperties": true, "id": "string", "properties": { "additionalProp1": { "description": "string", "type": "string" }, "additionalProp2": { "description": "string", "type": "string" }, "additionalProp3": { "description": "string", "type": "string" } }, "required": [ "string" ], "schema": "string", "title": "string", "type": "string" }, "major_version": 0, "minor_version": 0, "output_schema": { "additionalProperties": true, "id": "string", "properties": { "additionalProp1": { "description": "string", "type": "string" }, "additionalProp2": { "description": "string", "type": "string" }, "additionalProp3": { "description": "string", "type": "string" } }, "required": [ "string" ], "schema": "string", "title": "string", "type": "string" }, "qualified_name": "string" }')
        except Exception as e:
            print(e)
            exception_thrown = True

        # assert
        self.assertFalse(exception_thrown)

    def test3(self):
        """testing ErrorSchema"""
        # arrange
        schema = ErrorSchema()

        # act
        exception_thrown = False
        try:
            result = schema.loads(json_data='{ "message": "string", "type": "string"}')
        except Exception as e:
            print(e)
            exception_thrown = True

        # assert
        self.assertFalse(exception_thrown)


if __name__ == '__main__':
    unittest.main()
