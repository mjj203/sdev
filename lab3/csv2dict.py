"""
A module for converting U.S. states data from CSV to JSON.

This script reads a CSV file with U.S. states information and converts it into
JSON format. It includes state attributes like code, capital, population, state
flower, and an image URL. The script handles data formatting and encoding issues
for accurate conversion.

Functions:
    read_states_csv_to_json(csv_filename, json_filename): 
        Converts states data from CSV to JSON. It cleans data (e.g., removing
        commas in population figures) and handles KeyError exceptions for missing
        columns in the CSV.

Usage:
    Run with two arguments: the CSV filename and the JSON filename.
    Example: 
        python script.py states.csv states.json
    The script checks for the correct number of command-line arguments and
    provides usage instructions if they are not met.

Note:
    The script expects specific column headers in the CSV file (STATE, CODE,
    CAPITAL, POPULATION, FLOWER, URL) and handles the UTF-8 byte order mark
    (BOM) for the state key.
"""

import csv
import json
import sys

def read_states_csv_to_json(csv_file, json_file):
    """
    Read state data from a CSV file and convert it to a JSON file.

    This function opens a CSV file, reads the data row by row, and constructs a dictionary
    with each state's details, including code, capital, population, flower, and a URL
    for the state's flower image. It then writes this data into a JSON file. The function
    handles the removal of commas in population numbers and adjusts URLs for the flower images.
    It also accounts for potential UTF-8 byte order mark (BOM) in the CSV file.

    Args:
        csv_filename (str): The filename of the source CSV file containing state data.
        json_filename (str): The filename of the target JSON file to which the data will be written.

    Note:
        The function expects the CSV file to have specific headers and handles KeyError
        exceptions that may occur if any expected columns are missing.
    """
    states_dict = {}

    with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            state_key = '\ufeffSTATE' if '\ufeffSTATE' in row else 'STATE'

            try:
                state = row[state_key]
                states_dict[state] = {
                    'CODE': row['CODE'],
                    'CAPITAL': row['CAPITAL'],
                    'POPULATION': int(
                        row['POPULATION'].replace(',', '')
                        ),  # Removing commas and converting to int
                    'FLOWER': row['FLOWER'],
                    'URL': row['URL'].replace(
                        'en.wikipedia.org/wiki/File:', 'upload.wikimedia.org/wikipedia/commons/'
                        )
                }
            except KeyError as e:
                print(f"KeyError: {e}")
                continue

    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(states_dict, jsonfile, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_filename> <json_filename>")
        sys.exit(1)

    csv_filename = sys.argv[1]
    json_filename = sys.argv[2]
    read_states_csv_to_json(csv_filename, json_filename)
