import os
import shutil
import json
from pydantic import ValidationError

from file_processing.models.models import User

SRC_DIR = './test_data'
VALID_DEST_DIR = './output/valid_files'
INVALID_DEST_DIR = './output/invalid_files'

def read_and_validate_json(file_path: str) -> User:
    """
    Read a JSON file and validate it against the User model.

    Args:
        file_path (str): The path to the JSON file

    Returns:
        User object
    """
    try:
        with open(f"{SRC_DIR}/{file_path}", 'r') as file:
            data = json.load(file)

        user = User(**data)
        print(f"validation successful! user: {user.name}")

        # move to valid_files directory
        shutil.copy(
            f"{SRC_DIR}/{file_path}",
            f"{VALID_DEST_DIR}/{file_path}"
        )

        return user

    except FileNotFoundError:
        print(f"Error: Invalid JSON format in '{file_path}'")
    except ValidationError as error:
        print(f"Validation error: {error}")
        # move to invalid_files directory
        shutil.copy(
            f"{SRC_DIR}/{file_path}",
            f"{INVALID_DEST_DIR}/{file_path}"
        )

def process_json_files() -> None:
    """Validate all JSON files in the supplied directory.

    Returns:
        None
    """
    for file in os.listdir(SRC_DIR):
        if file.endswith('.json'):
            read_and_validate_json(file)

if __name__ == '__main__':
    print('\n--- validating data ---')
    process_json_files()
    print('\n--- completed validating data ---')
