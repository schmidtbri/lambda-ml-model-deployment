import os
import unittest
import json

from model_lambda.web_api.controllers import Response


class LambdaFunctionTests(unittest.TestCase):

    def test1(self):
        """test for handling unknown event type in the lambda_function.lambda_handler function"""
        # arrange
        from model_lambda.lambda_function import lambda_handler

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "sns_event.json")
        with open(path) as json_file:
            event = json.load(json_file)

        # act
        exception_thrown = False
        exception_message = None
        try:
            result = lambda_handler(event=event, context=None)
        except Exception as e:
            exception_thrown = True
            exception_message = str(e)

        # assert
        self.assertTrue(exception_thrown)
        self.assertTrue((exception_message == "This lambda cannot handle this event type."))

    def test2(self):
        """test model manager is loaded with configuration when the lambda_function module is initiated"""
        # arrange, act
        from model_lambda.lambda_function import lambda_handler
        from model_lambda.model_manager import ModelManager
        model_manager = ModelManager()

        # assert
        self.assertTrue(model_manager.get_models() == [{'display_name': 'Iris Model', 'qualified_name': 'iris_model', 'description': 'A machine learning model for predicting the species of a flower based on its measurements.', 'major_version': 0, 'minor_version': 1}])

    def test3(self):
        """test for handling GET /models endpoint request in lambda_function.lambda_handler"""
        # arrange
        from model_lambda.lambda_function import lambda_handler

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "api_gateway_list_models_event.json")
        with open(path) as json_file:
            event = json.load(json_file)

        # act
        exception_thrown = False
        exception_message = None
        try:
            result = lambda_handler(event=event, context=None)
        except Exception as e:
            exception_thrown = True
            exception_message = str(e)

        # assert
        self.assertFalse(exception_thrown)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result["statusCode"] == 200)
        self.assertTrue(result["headers"] == {'Content-Type': 'application/json'})
        self.assertTrue(json.loads(result["body"]) == {'models': [{'qualified_name': 'iris_model', 'description': 'A machine learning model for predicting the species of a flower based on its measurements.', 'minor_version': 1, 'major_version': 0, 'display_name': 'Iris Model'}]})

    def test4(self):
        """test for handling GET /api/models/{qualified_name}/metadata endpoint request in lambda_function.lambda_handler"""
        # arrange
        from model_lambda.lambda_function import lambda_handler

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "api_gateway_get_metadata_event.json")
        with open(path) as json_file:
            event = json.load(json_file)

        # act
        exception_thrown = False
        exception_message = None
        try:
            result = lambda_handler(event=event, context=None)
        except Exception as e:
            exception_thrown = True
            exception_message = str(e)

        # assert
        self.assertFalse(exception_thrown)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result["statusCode"] == 200)
        self.assertTrue(result["headers"] == {'Content-Type': 'application/json'})
        self.assertTrue(json.loads(result["body"]) == {"description": "A machine learning model for predicting the species of a flower based on its measurements.", "input_schema": {"id": "https://example.com/input_schema.json", "additionalProperties": False, "properties": {"sepal_length": {"type": "number"}, "sepal_width": {"type": "number"}, "petal_length": {"type": "number"}, "petal_width": {"type": "number"}}, "schema": "http://json-schema.org/draft-07/schema#", "type": "object", "required": ["sepal_length", "sepal_width", "petal_length", "petal_width"]}, "major_version": 0, "qualified_name": "iris_model", "minor_version": 1, "output_schema": {"id": "https://example.com/output_schema.json", "additionalProperties": False, "properties": {"species": {"type": "string"}}, "schema": "http://json-schema.org/draft-07/schema#", "type": "object", "required": ["species"]}, "display_name": "Iris Model"})

    def test5(self):
        """test for handling POST /api/models/{qualified_name}/predict endpoint request in lambda_function.lambda_handler"""
        # arrange
        from model_lambda.lambda_function import lambda_handler

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "api_gateway_predict_event.json")
        with open(path) as json_file:
            event = json.load(json_file)

        # act
        exception_thrown = False
        exception_message = None
        try:
            result = lambda_handler(event=event, context=None)
        except Exception as e:
            exception_thrown = True
            exception_message = str(e)

        # assert
        self.assertFalse(exception_thrown)
        self.assertTrue(type(result) == dict)
        self.assertTrue(result["statusCode"] == 200)
        self.assertTrue(result["headers"] == {'Content-Type': 'application/json'})
        self.assertTrue(json.loads(result["body"]) == {"species": "setosa"})

    def test6(self):
        """test for handling unknown http api resource in the lambda_function.lambda_handler function"""
        # arrange
        from model_lambda.lambda_function import lambda_handler

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "api_gateway_unknown_event.json")
        with open(path) as json_file:
            event = json.load(json_file)

        # act
        exception_thrown = False
        exception_message = None
        try:
            result = lambda_handler(event=event, context=None)
        except Exception as e:
            exception_thrown = True
            exception_message = str(e)

        # assert
        self.assertTrue(exception_thrown)
        self.assertTrue((exception_message == "This lambda cannot handle this resource."))


if __name__ == '__main__':
    unittest.main()
