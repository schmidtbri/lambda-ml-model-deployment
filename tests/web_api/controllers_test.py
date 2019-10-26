import unittest
import json
from model_lambda.model_manager import ModelManager
from model_lambda.web_api.schemas import ModelCollectionSchema, ModelMetadataSchema, ErrorSchema
import model_lambda.web_api.controllers as controllers


class ControllersTests(unittest.TestCase):

    def setUp(self):
        self.model_manager = ModelManager()
        self.model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

    def test1(self):
        """testing get_models() controller"""
        # arrange
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
        # act
        result = controllers.get_metadata(qualified_name="iris_model")
        schema = ModelMetadataSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 200)
        self.assertTrue(result.mimetype == "application/json")

    def test3(self):
        """testing get_metadata() controller with non-existing model"""
        # arrange
        # act
        result = controllers.get_metadata(qualified_name="asdf")
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 400)
        self.assertTrue(result.mimetype == "application/json")

    def test4(self):
        """testing predict() controller with bad data"""
        # arrange
        # act
        result = controllers.predict(qualified_name="iris_model", request_body="")
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 400)
        self.assertTrue(result.mimetype == "application/json")

    def test5(self):
        """testing predict() controller with non-existing model"""
        # arrange
        # act
        result = controllers.predict(qualified_name="asdf", request_body='{"petal_length": 1.0, "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}')
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 404)
        self.assertTrue(result.mimetype == "application/json")

    def test6(self):
        """testing predict() controller with good data"""
        # arrange
        # act
        result = controllers.predict(qualified_name="iris_model", request_body='{"petal_length": 1.0, "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}')
        data = json.loads(result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 200)
        self.assertTrue(result.mimetype == "application/json")

    def test7(self):
        """testing predict() controller with data that does not meet the model schema"""
        # arrange
        # act
        result = controllers.predict(qualified_name="iris_model", request_body='{"petal_length": "asdf", "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}')
        schema = ErrorSchema()
        data = schema.loads(json_data=result.data)

        # assert
        self.assertTrue(type(result) == controllers.Response)
        self.assertTrue(result.status == 400)
        self.assertTrue(result.mimetype == "application/json")


if __name__ == '__main__':
    unittest.main()
