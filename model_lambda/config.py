"""Configuration settings for the lambda application."""


class Config(object):
    """Configuration for all environments."""

    models = [
        {
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }
    ]


class ProdConfig(Config):
    """Configuration for the prod environment."""

    pass


class BetaConfig(Config):
    """Configuration for the beta environment."""

    pass


class TestConfig(Config):
    """Configuration for the test environment."""

    pass


class DevConfig(Config):
    """Configuration for the dev environment."""

    pass
