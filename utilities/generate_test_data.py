import os
import json
import random
import string
from pathlib import Path


def create_directories(base_dir: str = "test_data") -> tuple[Path, Path]:
    """Creates two directories to store `valid` and `invalid` directories

    Args:
        base_dir (str, optional): Base directory to create directories for. Defaults to "test_data".

    Returns:
        tuple[Path, Path]: A tuple containing the `valid` and `invalid` directories
    """
    valid_dir = Path(base_dir, "valid_files")
    invalid_dir = Path(base_dir, "invalid_files")

    valid_dir.mkdir(parents=True, exist_ok=True)
    invalid_dir.mkdir(parents=True, exist_ok=True)

    return valid_dir, invalid_dir

def generate_random_string(length: int = 10) -> str:
    """Generates a random string of `length` characters

    Args:
        length (int, optional): Length of string to generate. Defaults to 10.

    Return:
        str: A random string of `length` characters
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_valid_address() -> dict[str, any]:
    """Generate a valid address dictionary.

    Returns:
       dict[str, any]: A valid address dictionary
    """
    return {
        "street": f"{random.randint(1, 9999)} {generate_random_string(8)} st",
        "city": generate_random_string(10).capitalize(),
        "post_code": ''.join(random.choices(string.digits, k=5)),
    }

def generate_invalid_address() -> dict[str, any]:
    """Generate an invalid address dictionary.

    Notes:
        A random choice will be selected to generate an invalid address
        These will each fail validation but for different reasons.

    Returns
        dict[str, any]: An invalid address dictionary
    """
    invalid_address_opts = [
        {
            "street": f"{random.randint(1, 9999)} {generate_random_string(8)} st",
            "city": generate_random_string(10).capitalize(),
        },
        {
            "street": f"{random.randint(1, 9999)} {generate_random_string(8)} st",
            "city": generate_random_string(10).capitalize(),
            "post_code": generate_random_string(5),
        },
        {
            "street": f"{random.randint(1, 9999)} {generate_random_string(8)} st",
            "city": generate_random_string(10).capitalize(),
            "post_code": ''.join(random.choices(string.digits, k=random.choice([2, 4, 3]))),
        }
    ]
    return random.choice(invalid_address_opts)

def generate_valid_user(user_id: int) -> dict[str, any]:
    """Generate a valid user dictionary.

    Args:
        user_id (int, optional): User ID to generate a valid user dictionary.

    Returns
        dict[str, any]: A valid user dictionary
    """
    name = f"{generate_random_string(7).capitalize()} {generate_random_string(6).capitalize()}"
    email = f"{generate_random_string(5)}@{generate_random_string(6)}"

    return {
        "id": user_id,
        "email": email,
        "name": name,
        "age": random.randint(18, 80),
        "is_active": random.choice([True, False]),
        "tags": random.sample(['developer', 'manager', 'devops', 'data engineer', 'scrum master'], k=2),
        "address": generate_valid_address(),
    }

def generate_invalid_user(user_id: int) -> dict[str, any]:
    """Generate an invalid user dictionary.

    Args:
        user_id (int, optional): User ID to generate a valid user dictionary.

    Return:
        dict[str, any]: An invalid user dictionary
    """
    name = f"{generate_random_string(7).capitalize()} {generate_random_string(6).capitalize()}"
    email = f"{generate_random_string(5)}@{generate_random_string(6)}"

    invalid_user_opts = [
        { # invalid age
            "id": user_id,
            "email": email,
            "name": name,
            "age": generate_random_string(5),
            "is_active": random.choice([True, False]),
            "tags": random.sample(['developer', 'manager', 'devops', 'data engineer', 'scrum master'], k=2),
            "address": generate_invalid_address(),
        },
        {  # invalid email
            "id": user_id,
            "email": generate_random_string(15),
            "name": name,
            "age": random.randint(18, 80),
            "is_active": random.choice([True, False]),
            "tags": random.sample(['developer', 'manager', 'devops', 'data engineer', 'scrum master'], k=2),
            "address": generate_invalid_address(),
        },
        {  # invalid is_active
            "id": user_id,
            "email": email,
            "name": name,
            "age": random.randint(18, 80),
            "is_active": generate_random_string(2),
            "tags": random.sample(['developer', 'manager', 'devops', 'data engineer', 'scrum master'], k=2),
            "address": generate_invalid_address(),
        },
    ]
    return random.choice(invalid_user_opts)

def generate_test_files(num_valid_files: int = 10, num_invalid_files: int = 5, base_dir: str = "test_data") -> None:
    """Generate a specified number of valid and invalid JSON files for test data.

    Args:
        num_valid_files (int): Number of valid JSON files.
        num_invalid_files (int): Number of invalid JSON files.
        base_dir (str, optional): Base directory for generated JSON files. Defaults to "test_data".

    Returns:
        None
    """
    # Generate the directories for storing valid and invalid files
    # for the number of valid documents
    ## create file with valid user

    #valid_dir, invalid_dir = create_directories(base_dir)
    destination_dir = Path(base_dir)

    for i in range(num_valid_files):
        user_id = i + 1
        valid_user = generate_valid_user(user_id=user_id)
        file_path = destination_dir / f"valid_user_{user_id}.json"

        with open(file_path, "w") as file:
            json.dump(valid_user, file)

    for i in range(num_invalid_files):
        user_id = i + num_valid_files + 1
        invalid_user = generate_invalid_user(user_id=user_id)
        file_path = destination_dir / f"invalid_user_{user_id}.json"

        with open(file_path, "w") as file:
            json.dump(invalid_user, file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate test JSON files for validation testing")
    parser.add_argument("-v", "--valid", type=int, default=10, help="Number of valid test files to generate")
    parser.add_argument("-i", "--invalid", type=int, default=5, help="Number of invalid test files to generate")
    parser.add_argument("-d", "--dir", type=str, default="test_data", help="Base directory to save test files")

    args = parser.parse_args()

    generate_test_files(
        num_valid_files=args.valid,
        num_invalid_files=args.invalid,
        base_dir=args.dir,
    )