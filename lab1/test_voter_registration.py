import pytest
import duckdb
from unittest.mock import patch
from voter_registration import validate_age, validate_country, validate_state, get_input

# Create a test DuckDB connection and cursor
conn = duckdb.connect(':memory:')  # In-memory database for this example
cursor = conn.cursor()

# Create table and insert valid states for testing
cursor.execute("""
CREATE TABLE valid_states (
    abbreviation VARCHAR
)
""")
valid_states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
for state in valid_states:
    cursor.execute("INSERT INTO valid_states VALUES (?)", (state,))

def test_validate_age():
    assert validate_age("25") == True
    assert validate_age("0") == False
    assert validate_age("-1") == False
    assert validate_age("130") == False
    assert validate_age("abc") == False

def test_validate_country():
    assert validate_country("United States") == True
    assert validate_country("USA") == True
    assert validate_country("Canada") == False

def test_validate_state():
    assert validate_state("TX") == True
    assert validate_state("CA") == True
    assert validate_state("InvalidState") == False

# test get_input function to return 'John' on the first call and 'exit' on the second call.
@patch('builtins.input', side_effect=['John', 'exit'])
def test_get_input(mock_input):
    with pytest.raises(SystemExit):
        get_input("First Name: ", lambda x: x.isalpha(), "Invalid input. Please enter a valid first name.")

# Test get_input function with an invalid input followed by the 'exit' command.
@patch('builtins.input', side_effect=['123', 'exit'])
def test_get_input_invalid_then_exit(mock_input):
    with pytest.raises(SystemExit):
        get_input("First Name: ", lambda x: x.isalpha(), "Invalid input. Please enter a valid first name.")

# Test get_input function to ensure it exits the application when 'exit' is entered.
@patch('builtins.input', return_value='exit')
def test_get_input_exit(mock_input):
    with pytest.raises(SystemExit):
        get_input("First Name: ", lambda x: x.isalpha(), "Invalid input. Please enter a valid first name.")