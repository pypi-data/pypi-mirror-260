from enum import Enum, auto
import json

class RequestType(Enum):
    INPUT = auto()
    OUTPUT = auto()
    TRAINING = auto()
    BASE = auto()

class ModelOption:
    def __init__(self, request_type, price):
        self.request_type = RequestType[request_type.upper()]
        self.price = price

class Model:
    def __init__(self, name, options):
        self.name = name
        self.options = {option['type']: ModelOption(option['type'], option['price']) for option in options}

class ModelRegistry:
    def __init__(self):
        self.models = {}

    def add_model(self, model_data):
        model = Model(model_data['name'], model_data['options'])
        self.models[model.name] = model

    def get_model(self, model_name):
        return self.models.get(model_name)

    def load_models(self, config_file='models_config.json'):
        with open(config_file, 'r') as file:
            models_data = json.load(file)
            for model_data in models_data:
                self.add_model(model_data)

# Instantiate the model registry and load models from a configuration file
model_registry = ModelRegistry()
model_registry.load_models()
