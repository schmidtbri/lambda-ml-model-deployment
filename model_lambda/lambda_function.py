""""""
from model_lambda.model_manager import ModelManager
from model_lambda.config import Config


# instantiating the model manager class
model_manager = ModelManager()

# loading the MLModel objects from configuration
model_manager.load_models(configuration=Config.models)


def lambda_handler(event, context):

    return
