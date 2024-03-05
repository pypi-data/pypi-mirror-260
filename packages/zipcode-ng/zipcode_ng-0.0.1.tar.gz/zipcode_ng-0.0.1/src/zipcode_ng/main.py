import os
import json
from typing import List, Dict, TypedDict, Literal, Union


StateName = Literal[
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", 
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT - Abuja", "Gombe", 
    "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", 
    "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", 
    "Taraba", "Yobe", "Zamfara"
]

class TownType(TypedDict):
    town_name: str
    postal_code: str

class LocalGovernmentArea(TypedDict):
    lga_name: str
    towns: List[TownType]
    city: str

class StateInfo(TypedDict):
    name: StateName
    language: str
    tribe: str
    description: str
    cities: List[str]
    land_mass: str
    population_density: str
    region: Literal["North West", "North East", "North Central", "South West", "South South", "South East"]
    postal_code: str
    lgas: List[LocalGovernmentArea]

    
state_lgas_data: Dict[StateName, List[LocalGovernmentArea]] = {}

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_NAME = 'states data.json'

# Path to the JSON file relative to the current script
JSON_PATH = os.path.join(current_dir, JSON_FILE_NAME)

def _read_json_file() -> List[StateInfo]:
    """
    Read JSON data from a file and return it as a list of dictionaries.

    Returns:
        list: List of dictionaries representing the JSON data.
    """
    with open(JSON_PATH, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

STATES = _read_json_file()

def get_state_data(identifier: Union[str, StateName]) -> StateInfo:
    """
    Retrieve state data based on either the state name or its postal code.

    Args:
        identifier (Union[str, StateName]): Either the state name (str) or its postal code (str).

    Returns:
        StateInfo: Information about the state.

    Raises:
        ValueError: If the state is not found.
        TypeError: If the identifier type is invalid.
    """
    if isinstance(identifier, str):
        # Check if the identifier is a postal code
        for state_info in STATES:
            if state_info["postal_code"] == identifier:
                return state_info
        # If not a postal code, assume it's a state name
        for state_info in STATES:
            if state_info["name"].lower() == identifier.lower():
                return state_info
        raise ValueError("State not found")
    else:
        raise TypeError("Invalid identifier type")

def get_all_state_data() -> List[StateInfo]:
    """
    Retrieve information about all states.

    Returns:
        List[StateInfo]: Information about all states.
    """
    return STATES
