import unittest
import json

from model_lambda.model_manager import ModelManager
from model_lambda.web_api.schemas import ModelCollectionSchema, ModelMetadataSchema, ErrorSchema
import model_lambda.web_api.controllers as controllers


class ControllersTests(unittest.TestCase):

    def test1(self):
        """testing get_models() controller"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        result = controllers.get_models()
        schema = ModelCollectionSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 200)
        self.assertTrue(result.mimetype == "application/json")

    def test2(self):
        """testing get_metadata() controller with existing model"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        result = controllers.get_metadata(qualified_name="iris_model")
        schema = ModelMetadataSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 200)
        self.assertTrue(result.mimetype == "application/json")
        self.assertTrue(json.loads(result.data) == {'output_schema': {'additionalProperties': False, 'required': ['species'], 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'object', 'id': 'https://example.com/output_schema.json', 'properties': {'species': {'type': 'string'}}}, 'minor_version': 1, 'major_version': 0, 'qualified_name': 'iris_model', 'description': 'A machine learning model for predicting the species of a flower based on its measurements.', 'display_name': 'Iris Model', 'input_schema': {'additionalProperties': False, 'required': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], 'schema': 'http://json-schema.org/draft-07/schema#', 'type': 'object', 'id': 'https://example.com/input_schema.json', 'properties': {'sepal_length': {'type': 'number'}, 'sepal_width': {'type': 'number'}, 'petal_length': {'type': 'number'}, 'petal_width': {'type': 'number'}}}})

    def test3(self):
        """testing get_metadata() controller with non-existing model"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        result = controllers.get_metadata(qualified_name="asdf")
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 400)
        self.assertTrue(result.mimetype == "application/json")
        self.assertTrue(json.loads(result.data) == {"message": "Model not found.", "type": "ERROR"})

    def test4(self):
        """testing predict() controller with bad data"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        result = controllers.predict(qualified_name="iris_model", request_body="")
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 400)
        self.assertTrue(result.mimetype == "application/json")
        self.assertTrue(json.loads(result.data) == {"type": "DESERIALIZATION_ERROR", "message": "Expecting value: line 1 column 1 (char 0)"})

    def test5(self):
        """testing predict() controller with non-existing model"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        result = controllers.predict(qualified_name="asdf", request_body='{"petal_length": 1.0, "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}')
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 404)
        self.assertTrue(result.mimetype == "application/json")
        self.assertTrue(json.loads(result.data) == {"type": "ERROR", "message": "Model not found."})

    def test6(self):
        """testing predict() controller with good data"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        result = controllers.predict(qualified_name="iris_model", request_body='{"petal_length": 1.0, "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}')
        data = json.loads(result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 200)
        self.assertTrue(result.mimetype == "application/json")
        self.assertTrue(json.loads(result.data) == {"species": "setosa"})

    def test7(self):
        """testing predict() controller with data that does not meet the model schema"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        result = controllers.predict(qualified_name="iris_model", request_body='{"petal_length": "asdf", "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}')
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 400)
        self.assertTrue(result.mimetype == "application/json")
        self.assertTrue(json.loads(result.data) == {"message": "Failed to validate input data: Key 'petal_length' error:\n'asdf' should be instance of 'float'", "type": "SCHEMA_ERROR"})


if __name__ == '__main__':
    unittest.main()
