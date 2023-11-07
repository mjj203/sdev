import csv
import json
import sys

def read_states_csv_to_json(csv_filename, json_filename):
    STATES = {}

    with open(csv_filename, newline='', encoding='utf-8-sig') as csvfile:  # Adjusted encoding here
        reader = csv.DictReader(csvfile)

        for row in reader:
            state_key = '\ufeffSTATE' if '\ufeffSTATE' in row else 'STATE'  # Adjust key based on BOM

            try:
                state = row[state_key]
                STATES[state] = {
                    'CODE': row['CODE'],
                    'CAPITAL': row['CAPITAL'],
                    'POPULATION': int(row['POPULATION'].replace(',', '')),  # Removing commas and converting to int
                    'FLOWER': row['FLOWER'],
                    'URL': row['URL'].replace('en.wikipedia.org/wiki/File:', 'upload.wikimedia.org/wikipedia/commons/')
                }
            except KeyError as e:
                print(f"KeyError: {e}")
                continue

    with open(json_filename, 'w') as jsonfile:
        json.dump(STATES, jsonfile, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_filename> <json_filename>")
        sys.exit(1)

    csv_filename = sys.argv[1]
    json_filename = sys.argv[2]
    read_states_csv_to_json(csv_filename, json_filename)
