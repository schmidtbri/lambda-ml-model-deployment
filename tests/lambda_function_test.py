import unittest


class ModelManagerTests(unittest.TestCase):

    def test1(self):
        """ testing the lambda_function module startup code """
        # arrange
        import model_lambda.lambda_function

        # act
        models = model_lambda.lambda_function.model_manager.get_models()
        model = model_lambda.lambda_function.model_manager.get_model("iris_model")
        metadata = model_lambda.lambda_function.model_manager.get_model_metadata("iris_model")

        # assert
        self.assertTrue(len(models) == 1)
        self.assertTrue(models == [{'display_name': 'Iris Model', 'qualified_name': 'iris_model', 'description': 'A machine learning model for predicting the species of a flower based on its measurements.', 'major_version': 0, 'minor_version': 1}])
        self.assertTrue(str(type(model)) == "<class 'iris_model.iris_predict.IrisModel'>")
        self.assertTrue(metadata == {'display_name': 'Iris Model', 'qualified_name': 'iris_model', 'description': 'A machine learning model for predicting the species of a flower based on its measurements.', 'major_version': 0, 'minor_version': 1, 'input_schema': {'type': 'object', 'properties': {'sepal_length': {'type': 'number'}, 'sepal_width': {'type': 'number'}, 'petal_length': {'type': 'number'}, 'petal_width': {'type': 'number'}}, 'required': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], 'additionalProperties': False, 'id': 'https://example.com/input_schema.json', '$schema': 'http://json-schema.org/draft-07/schema#'}, 'output_schema': {'type': 'object', 'properties': {'species': {'type': 'string'}}, 'required': ['species'], 'additionalProperties': False, 'id': 'https://example.com/output_schema.json', '$schema': 'http://json-schema.org/draft-07/schema#'}})


if __name__ == '__main__':
    unittest.main()
