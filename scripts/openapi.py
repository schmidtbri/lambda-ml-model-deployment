import os
import sys
from apispec import APISpec
from apispec import BasePlugin
from apispec.yaml_utils import load_operations_from_docstring
from apispec.ext.marshmallow import MarshmallowPlugin

if os.path.abspath(os.path.dirname(os.path.dirname(__file__))) not in sys.path:
    sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from model_lambda import __doc__, __version__
from model_lambda.web_api.schemas import *
from model_lambda.web_api.controllers import get_models, get_metadata, predict


class DocPlugin(BasePlugin):
    def init_spec(self, spec):
        super(DocPlugin, self).init_spec(spec)
        self.openapi_major_version = spec.openapi_version.major

    def operation_helper(self, operations, func, **kwargs):
        """Operation helper that parses docstrings for operations. Adds a ``func`` parameter to `apispec.APISpec.path`.
        """
        doc_operations = load_operations_from_docstring(func.__doc__)
        operations.update(doc_operations)


spec = APISpec(
    openapi_version="3.0.2",
    title='Model Lambda Web API',
    version=__version__,
    info=dict(description=__doc__),
    plugins=[MarshmallowPlugin(), DocPlugin()],
)

# adding schemas to OpenAPI spec from marshmallow schema classes
spec.components.schema("Model", schema=ModelSchema)
spec.components.schema("ModelCollection", schema=ModelCollectionSchema)
spec.components.schema("JsonSchemaProperty", schema=JsonSchemaProperty)
spec.components.schema("JSONSchema", schema=JSONSchema)
spec.components.schema("ModelMetadata", schema=ModelMetadataSchema)
spec.components.schema("Error", schema=ErrorSchema)

# adding paths to OpenAPI spec from controller docstrings
spec.path(path="/api/models", func=get_models)
spec.path(path="/api/models/{qualified_name}/metadata", func=get_metadata)
spec.path(path="/api/models/{qualified_name}/predict", func=predict)


with open('openapi_specification.yaml', 'w') as f:
    f.write(spec.to_yaml())
