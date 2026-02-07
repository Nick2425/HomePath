# Data that is to be stored:
# Facial Data
# Age, Gender, Habits -- Smoking, Drinking
# Pets
# Name, Common Location.

import json
import os
import uuid

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(SCRIPT_DIR, 'Database')

# Ensure Database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

def save_data(
    user_id = None,
    password = None,
    age = None,
    gender = None,
    smoking_habit = None,
    drinking_habit = None,
    pets = [],
    dependents = [],
    name = None,
    phone_number = None,
    can_be_found_at = "",
    facial_data = {},
):
    
    """
    Formats the input data into a structured dictionary for storage.
    Args:
        age (int): Age of the person
    """
    data = {
        "password": password,
        "facial_data": facial_data,
        "user_id": user_id,
        "pets": pets,
        "personal_info": {
            "name": name,
            "phone_number": phone_number,
            "can_be_found_at": can_be_found_at,
            "age": age,
            "sex_at_birth": gender
        },
        "habits": {
            "smoking": smoking_habit,
            "drinking": drinking_habit
        }
    }
    store_data(data, f"{user_id}.json")

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
        filepath = os.path.join(DATABASE_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully stored in {filepath}")
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
        filepath = os.path.join(DATABASE_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
            print(f"Data successfully loaded from {filepath}")
            return data
        else:
            print(f"File {filepath} not found")
            return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
