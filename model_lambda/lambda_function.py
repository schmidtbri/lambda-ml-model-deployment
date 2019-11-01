"""Lambda function entry point."""
from model_lambda.model_manager import ModelManager
from model_lambda.config import Config

from model_lambda.web_api.controllers import get_models, get_metadata, predict

# instantiating the model manager class
model_manager = ModelManager()

# loading the MLModel objects from configuration
model_manager.load_models(configuration=Config.models)


def lambda_handler(event, context):
    """Lambda handler function."""

    # detecting if the event came from an API Gateway
    if event.get("resource") is not None \
            and event.get("path") is not None \
            and event.get("httpMethod") is not None:

        if event["resource"] == "/api/models" and event["httpMethod"] == "GET":
            # calling the get_models controller function
            response = get_models()

        elif event["resource"] == "/api/models/{qualified_name}/metadata" and event["httpMethod"] == "GET":
            # calling the get_metadata controller function
            response = get_metadata(qualified_name=event["pathParameters"]["qualified_name"])

        elif event["resource"] == "/api/models/{qualified_name}/predict" \
            and event["httpMethod"] == "POST" \
            and event.get("pathParameters") is not None \
            and event["pathParameters"].get("qualified_name") is not None:
            # calling the predict controller function
            response = predict(qualified_name=event["pathParameters"]["qualified_name"], request_body=event["body"])

        else:
            raise ValueError("This lambda cannot handle this resource.")

        return {
            "isBase64Encoded": False,
            "statusCode": response.status,
            "headers": {"Content-Type": response.mimetype},
            "body": response.data
        }

    else:
        raise ValueError("This lambda cannot handle this event type.")
