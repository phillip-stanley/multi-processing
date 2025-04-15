from pathlib import Path
import json

ROOT_DIR = Path(__file__).parent.parent

def create_sample_json(file_path: str, valid: bool = True) -> None:
    """Create a sample JSON file for testing

    Args:
        file_path (str): The path to the file
        valid (bool, optional): Whether the file should be valid. Defaults to True.

    Returns None
    """
    if valid:
        data = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "is_active": True,
            "tags": ["developer", "python"],
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "post_code": "12345"
            },
        }
    else:
        data = {
            "id": "not_an_integer",  # Wrong type
            "name": "Jane Doe",
            "email": "invalid-email",  # Invalid email format
            "address": {
                "street": "456 Oak Ave",
                "city": "Somewhere",
                "post_code": "ABC12"  # Invalid zip code
            },
        }

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Sample JSON file created at: {file_path}")


if __name__ == "__main__":
    print('\n--- Creating Sample JSON ---')
    create_sample_json(f"{ROOT_DIR}/test_data/valid_user.json", valid=True)
    create_sample_json(f"{ROOT_DIR}/test_data/invalid_user.json", valid=False)
    print('\n--- Finished creating Sample JSON ---')