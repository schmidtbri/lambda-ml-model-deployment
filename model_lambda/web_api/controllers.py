"""Module for the controller functions."""
import json
import collections
from ml_model_abc import MLModelSchemaValidationException

from model_lambda.model_manager import ModelManager
from model_lambda.web_api.schemas import ModelCollectionSchema, ModelMetadataSchema, ErrorSchema


# creating a named tuple to hold a response that will be returned to the lambda function
Response = collections.namedtuple('Response', ["data", "status", "mimetype"])

# instantiating the marshmallow schema objects here so we can reuse them below
model_collection_schema = ModelCollectionSchema()
model_metadata_schema = ModelMetadataSchema()
error_schema = ErrorSchema()


# @app.route("/models", methods=['GET'])
def get_models():
    """List of models available.

    ---
    get:
      responses:
        200:
          description: List of model available
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ModelCollection'
    """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    models = model_manager.get_models()
    response_data = model_collection_schema.dumps(dict(models=models))
    return Response(data=response_data, status=200, mimetype="application/json")


# @app.route("/models/<qualified_name>/metadata", methods=['GET'])
def get_metadata(qualified_name):
    """Metadata about one model.

    ---
    get:
      parameters:
        - in: path
          name: qualified_name
          schema:
            type: string
          required: true
          description: The qualified name of the model for which metadata is being requested.
      responses:
        200:
          description: Metadata about one model
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ModelMetadata'
        404:
          description: Model not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
    """
    model_manager = ModelManager()
    metadata = model_manager.get_model_metadata(qualified_name=qualified_name)
    if metadata is not None:
        response_data = model_metadata_schema.dumps(metadata)
        return Response(response_data, status=200, mimetype='application/json')
    else:
        response = dict(type="ERROR", message="Model not found.")
        response_data = error_schema.dumps(response)
        return Response(data=response_data, status=400, mimetype='application/json')


# @app.route("/models/<qualified_name>/predict", methods=['POST'])
def predict(qualified_name, request_body):
    """Endpoint that uses a model to make a prediction.

    ---
    post:
      parameters:
        - in: path
          name: qualified_name
          schema:
            type: string
          required: true
          description: The qualified name of the model being used for prediction.
      responses:
        200:
          description: Prediction is succesful. The schema of the body of the response is described by the model's
            output schema.
        400:
          description: Input is not valid JSON or does not meet the model's input schema.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        404:
          description: Model not found.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        500:
          description: Server error.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
    """
    # attempting to deserialize JSON in body of request
    try:
        data = json.loads(request_body)
    except json.decoder.JSONDecodeError as e:
        response = dict(type="DESERIALIZATION_ERROR", message=str(e))
        response_data = error_schema.dumps(response)
        return Response(data=response_data, status=400, mimetype='application/json')

    # getting the model object from the Model Manager
    model_manager = ModelManager()
    model_object = model_manager.get_model(qualified_name=qualified_name)

    # returning a 404 if model is not found
    if model_object is None:
        response = dict(type="ERROR", message="Model not found.")
        response_data = error_schema.dumps(response)
        return Response(data=response_data, status=404, mimetype='application/json')

    try:
        prediction = model_object.predict(data)
        return Response(data=json.dumps(prediction), status=200, mimetype="application/json")
    except MLModelSchemaValidationException as e:
        # responding with a 400 if the schema does not meet the model's input schema
        response = dict(type="SCHEMA_ERROR", message=str(e))
        response_data = error_schema.dumps(response)
        return Response(data=response_data, status=400, mimetype='application/json')
    except Exception as e:
        response = dict(type="ERROR", message="Could not make a prediction.")
        response_data = error_schema.dumps(response)
        return Response(data=response_data, status=500, mimetype='application/json')
