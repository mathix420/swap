from re import compile
from os import path
import yaml

variables = compile(r'\s(\$[A-Z_]+)\s')


def get_config(config_path):
    if not path.exists(config_path):
        return None
    with open(config_path) as fp:
        config = yaml.load(fp, yaml.SafeLoader)
    return config


def save_config(config, config_path):
    with open(config_path, 'w+') as fp:
        yaml.dump(config, fp, default_flow_style=False, indent=2)
