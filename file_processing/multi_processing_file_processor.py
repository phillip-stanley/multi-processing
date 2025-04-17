import os
import shutil
import json
import multiprocessing
from datetime import datetime
from pydantic import ValidationError

from models import User

SRC_DIR = './test_data'
VALID_DEST_DIR = './output/validated'
INVALID_DEST_DIR = './output/failed'


def read_and_validate_json(file_path: str) -> None:
    """
    Read a JSON file and validate it against the User model.

    Args:
        file_path (str): The path to the JSON file

    Returns:
        None
    """
    print(f'\n--- processing file --- {multiprocessing.current_process().name}')
    try:
        with open(f"{SRC_DIR}/{file_path}", 'r') as file:
            data = json.load(file)

        user = User(**data)
        #print(f"validation successful! user: {user.name}")
        #print(f"validation successful! user: {file_path}")

        # move to valid_files directory
        shutil.copy(
            f"{SRC_DIR}/{file_path}",
            f"{VALID_DEST_DIR}/{file_path}"
        )

    except FileNotFoundError:
        print(f"Error: Invalid JSON format in '{file_path}'")
    except ValidationError as error:
        print('\n--- validation error ---')
        #print(f"Validation error: {error}")

        # move to invalid_files directory
        shutil.copy(
            f"{SRC_DIR}/{file_path}",
            f"{INVALID_DEST_DIR}/{file_path}"
        )

def process_json_files() -> datetime.time:
    """Validate all JSON files in the supplied directory.

    Returns:
        None
    """
    start_time = datetime.now()

    files = os.listdir(SRC_DIR)

    with multiprocessing.Pool() as pool:
        pool.map(read_and_validate_json, files)

    end_time = datetime.now()
    return end_time - start_time

if __name__ == '__main__':
    print('\n--- validating data ---')
    elapsed_time = process_json_files()
    print('\n--- completed validating data ---')
    print(f'\n--- time elapsed {elapsed_time} seconds ---')
