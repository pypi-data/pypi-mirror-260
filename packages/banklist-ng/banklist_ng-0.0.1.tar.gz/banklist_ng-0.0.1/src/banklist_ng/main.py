import os
import json
from typing import List, Optional, TypedDict

class BankInfo(TypedDict):
   """
   Represents a collection of bank data.
   """
   id: int
   type: str
   nipCode: str
   name: str
   slug: Optional[str]
   code: Optional[str]
   ussd: Optional[str]
   logo: Optional[str]


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file relative to the current script
JSON_PATH = os.path.join(current_dir, 'banks data.json')

def _read_json_file(json_file_path: str) -> List[BankInfo]:
    """
    Read JSON data from a file and return it as a list of dictionaries.

    Args:
        json_file_path (str): Path to the JSON file.

    Returns:
        list: List of dictionaries representing the JSON data.
    """
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

banks_data = _read_json_file(JSON_PATH)

def fetch_banks() -> List[BankInfo]:
    """
    Fetches a list of banks and their data.

    Returns: Data on banks.
    """
    return banks_data


def filter_banks_by_keyword(keyword: str) -> List[BankInfo]:
   """
   Filters banks based on a given keyword in their name property.

   Args:
      keyword (str): The keyword to search for in bank names.

   Returns:
      List[Dict[str, Any]]: A list of dictionaries containing bank data that matches the keyword.
   """
   filtered_banks = [bank for bank in banks_data if keyword.lower() in bank["name"].lower()]
   return filtered_banks
