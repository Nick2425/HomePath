# Data that is to be stored:
# Facial Data
# Age, Gender, Habits -- Smoking, Drinking
# Pets
# Name, Common Location.

import json
import os


def save_data(
    age = None,
    sex_at_birth = None,
    smoking_habit = None,
    drinking_habit = None,
    pets = [],
    name = None,
    phone_number = None,
    can_be_found_at = "",
    facial_data = {},
    password = None
):
    
    """
    Formats the input data into a structured dictionary for storage.
    Args:
        age (int): Age of the person
    """
    data = {
        "password": password,
        "facial_data": facial_data,
        "user_id": name,
        "pets": pets,
        "personal_info": {
            "name": name,
            "phone_number": phone_number,
            "can_be_found_at": can_be_found_at,
            "age": age,
            "sex_at_birth": sex_at_birth
        },
        "habits": {
            "smoking": smoking_habit,
            "drinking": drinking_habit
        }
    }
    store_data(data, f"{name}.json")

def store_data(data, filename):
    """
    Stores data (facial data and pet information) to a JSON file.
    Args:
        data (dict): Dictionary containing:
            - facial_data: dict with age, gender, habits (smoking, drinking)
            - pets: list of dicts with name and common location
        filename (str): Name of the file to store data in
    Returns:
        bool: True if storage was successful, False otherwise
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully stored in {filename}")
        return True
    except Exception as e:
        print(f"Error storing data: {e}")
        return False

def load_data(filename="stored_data.json"):
    """
    Loads data from a JSON file.
    Args:
        filename (str): Name of the file to load data from
    Returns:
        dict: Loaded data or None if file doesn't exist
    """
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"Data successfully loaded from {filename}")
            return data
        else:
            print(f"File {filename} not found")
            return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
save_data(17, user_id="Nick", sex_at_birth="Male", smoking_habit="Occasional", drinking_habit="None", pets=["dog"], phone_number="123-456-7890", can_be_found_at="north_city", facial_data={})