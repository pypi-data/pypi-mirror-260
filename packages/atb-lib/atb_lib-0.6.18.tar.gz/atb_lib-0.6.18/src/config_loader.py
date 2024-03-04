import json


def load_config(file_path):
    """
    Load a configuration file from the given file path.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        dict: The configuration data loaded from the file.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        config = json.load(file)
    return config
