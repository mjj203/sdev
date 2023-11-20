# =================================================================
#
# Authors: Michael Jones <mjones467@student.umgc.edu>
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

"""
A utility module for converting state data from CSV to JSON format,
with a focus on secure file handling.

This module contains two primary functions: `sanitize_filename` and `read_states_csv_to_json`. 
`sanitize_filename` ensures filename safety by removing directory components and blocking access
to protected directories and hidden files, thus mitigating file path traversal vulnerabilities.
`read_states_csv_to_json` reads state data from a given CSV file and converts it into a structured
JSON format.

It processes and organizes information such as state codes, capitals, populations, state flowers,
and associated image URLs.

The module is designed for use as a command-line tool.
It requires two arguments: the source CSV filename and the target JSON filename.
Its implementation emphasizes secure practices in file handling and efficient data
transformation between popular data formats.

Usage:
    Run the script from the command line with the CSV and JSON filenames as arguments.
    Example: python script.py <csv_filename> <json_filename>
"""

import csv
import json
import os
import sys


def sanitize_filename(filename):
    """
    Sanitize the filename by removing directory components and checking for protected paths.

    Args:
        filename (str): The filename to sanitize.

    Returns:
        str: The sanitized filename if safe, otherwise raises a ValueError.
    """
    # Remove directory components
    sanitized = os.path.basename(filename)

    # Reject filenames that attempt to access protected directories or hidden files
    protected_directories = ["/etc", "/root"]
    if sanitized.startswith(".") or any(
        sanitized.startswith(dir) for dir in protected_directories
    ):
        raise ValueError(
            "Access to protected directories or hidden files is not allowed."
        )

    return sanitized


def read_states_csv_to_json(csv_file, json_file):
    """
    Convert state data from a CSV file to a JSON file format.

    This function reads state data from a specified CSV file and writes it into a JSON file.
    It constructs a dictionary with details for each state, including its code, capital, population,
    state flower, and a URL for an image of the state's flower. The population numbers are cleansed
    of commas and converted to integers, and the URLs for the flower images are modified for direct
    access.

    The function handles UTF-8 byte order mark (BOM) in the CSV file and expects specific headers in
    the CSV file. It manages KeyError exceptions that may occur if any expected columns are missing.

    Args:
        csv_file (str): Path to the source CSV file containing state data.
        json_file (str): Path to the target JSON file for output.

    Raises:
        KeyError: If an expected column is missing in the CSV file.

    Note:
        The CSV file should have headers: 'STATE', 'CODE', 'CAPITAL', 'POPULATION', 'FLOWER', 'URL'.
    """
    states_dict = {}

    with open(csv_file, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            state_key = "\ufeffSTATE" if "\ufeffSTATE" in row else "STATE"

            try:
                state = row[state_key]
                states_dict[state] = {
                    "CODE": row["CODE"],
                    "CAPITAL": row["CAPITAL"],
                    "POPULATION": int(
                        row["POPULATION"].replace(",", "")
                    ),  # Removing commas and converting to int
                    "FLOWER": row["FLOWER"],
                    "URL": row["URL"].replace(
                        "en.wikipedia.org/wiki/File:",
                        "upload.wikimedia.org/wikipedia/commons/",
                    ),
                }
            except KeyError as key_error:
                print(f"KeyError: {key_error}")
                continue

    with open(json_file, "w", encoding="utf-8") as jsonfile:
        json.dump(states_dict, jsonfile, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_filename> <json_filename>")
        sys.exit(1)

    try:
        # Sanitize input filenames
        csv_filename = sanitize_filename(sys.argv[1])
        json_filename = sanitize_filename(sys.argv[2])
    except ValueError as e:
        print(e)
        sys.exit(1)

    read_states_csv_to_json(csv_filename, json_filename)
