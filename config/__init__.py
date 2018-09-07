import os
import yaml


def init_config():
    """Initializes configuration for the application, obtaining values from a config.yaml file

    :return: A dictionary containing configuration directives
    :rtype: dict
    """
    with open('config/config.yaml') as f:
        config_data = yaml.load(f.read())

    return config_data


def apply_environment_updates(config_data):
    """Overrides config items with environment-specific values

    :param config_data: Dictionary containing currently configured set of config options
    :type config_data: dict
    """
    for key in config_data:
        override = os.getenv(key)
        if override:
            config_data[key] = override


config = init_config()
apply_environment_updates(config)
