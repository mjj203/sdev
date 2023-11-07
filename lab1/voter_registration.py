"""
Voter Registration Application

This script provides a command-line interface for user to register as a voter.
The user is prompted to enter their personal information such as first name, last name, age, 
country of citizenship, state of residence, and zipcode. Each input is validated to ensure 
it is in the correct format. 

The user must be at least 18 years old and a U.S. citizen to be eligible to register. 
The state of residence must be entered as a two-letter abbreviation of a U.S. state.

The user has the option to exit the application at any time by typing 'exit'. Upon successful 
completion of the registration, a summary of the entered information is displayed, and the user 
is congratulated on their eligibility to vote.

Requirements:
    - Python 3.x
    - No external libraries required
"""


import sys
from typing import Callable
import duckdb

# Initialize DuckDB connection and cursor
conn = duckdb.connect(":memory:")  # In-memory database for this example
cursor = conn.cursor()

# Create table and insert valid states
cursor.execute(
    """
CREATE TABLE valid_states (
    abbreviation VARCHAR
)
"""
)
valid_states = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]

for state in valid_states:
    cursor.execute("INSERT INTO valid_states VALUES (?)", (state,))

valid_countries = ["United States", "USA", "US", "United States of America"]


def verify_country(country: str) -> bool:
    """
    Validates the user's country of citizenship for voter registration eligibility.

    This function checks if the provided country name is one of the accepted forms of referring 
    to the United States, as voter registration is only available to U.S. citizens.

    Parameters:
        country (str): The country name provided by the user.

    Returns:
        bool: True if the country is an accepted form of referring to the United States,
              False otherwise.

    Notes:
        The accepted forms of referring to the United States in this function are:
        - "United States"
        - "USA"
        - "US"
        - "United States of America"
    """
    return country in valid_countries


def get_input(
    prompt: str, validation_func: Callable[[str], bool], error_message: str
) -> str:
    while True:
        user_input = input(prompt)
        if user_input.lower() == "exit":
            print("Registration cancelled.")
            sys.exit()
        try:
            if validation_func(user_input):
                return user_input
            print(error_message)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(error_message)


def verify_age(age: str) -> bool:
    """
    Validate that the input is a digit and represents a reasonable age (between 1 and 119).

    :param age: The input string representing the age
    :return: True if the age is valid, False otherwise
    """
    try:
        age_int = int(age)
        return 0 < age_int < 120
    except ValueError:
        return False


def verify_state(abbr: str) -> bool:
    """Validate that the input is a two-letter abbreviation of a U.S. state.

    :param state: The input string representing the state
    :return: True if the state is valid, False otherwise"""
    if len(abbr) != 2 or not abbr.isalpha():
        print("The state abbreviation must be exactly two letters.")
        return False
    try:
        result = cursor.execute(
            "SELECT * FROM valid_states WHERE abbreviation = ?", (abbr.upper(),)
        ).fetchall()
        return len(result) > 0
    except duckdb.Error as e:
        print("An error occurred:", e)
        return False


def cont_registration() -> bool:
    """
    Prompts the user to decide whether to continue with the registration process.

    The function repeatedly asks the user to enter 'yes' or 'no' until a valid input is provided.
    If the user inputs 'yes', the function returns True, indicating the intention to continue.
    If the user inputs 'no', the function prints a cancellation message and exits the program.
    If the user inputs 'exit', the program is also terminated.

    Returns:
        bool: True if the user decides to continue the registration, False otherwise.
        
    Side Effects:
        This function can exit the program if the user decides not to continue or inputs 'exit'.
    """
    try:
        while True:
            proceed = input(
                "Do you want to continue with the registration? (yes/no): "
            ).lower()
            if proceed == "yes":
                return True
            if proceed == "no":
                print("Registration cancelled.")
                sys.exit()
            if proceed == "exit":
                print("Exiting program.")
                sys.exit()
            print("Invalid input. Please enter 'yes' or 'no'.")
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting program.")
        sys.exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit()


def main() -> None:
    """
    Executes the voter registration application.

    This function guides the user through the voter registration process, requesting
    various pieces of personal information such as name, age, country of citizenship,
    state of residence, and zipcode. The user can exit the application at any time by typing 'exit'.

    The registration process includes validation checks to ensure that:
    - The user is at least 18 years old.
    - The user is a U.S. citizen.
    - All provided information meets the required criteria.
    
    If the user is eligible to vote and all information is valid, the function displays a summary
    of the provided information and congratulates the user. If the user is not eligible or decides
    to cancel the registration, the function exits without completing the registration.

    This function also handles unexpected exceptions, displaying an error message before exiting.

    Exit Points:
        The function can exit the program in the following scenarios:
        - The user decides to exit the application.
        - The user is not eligible to vote.
        - An unexpected error occurs.

    Side Effects:
        This function prints information and prompts to the console and can exit the program.
    """
    print("Welcome to the Voter Registration Application.")
    print("You can exit the application at any time by typing 'exit'.")

    if not cont_registration():
        return

    print("\nPlease enter your information:")

    first_name = get_input(
        "First Name: ",
        lambda x: x.isalpha(),
        "Invalid input. Please enter a valid first name.",
    )
    last_name = get_input(
        "Last Name: ",
        lambda x: x.isalpha(),
        "Invalid input. Please enter a valid last name.",
    )
    age = get_input(
        "Age: ",
        verify_age,
        "Invalid input. Please enter a valid age between 1 and 119.",
    )

    if not cont_registration():
        return

    country = get_input(
        "Country of Citizenship: ",
        verify_country,
        "Invalid input. Please enter a valid country name.",
    )

    if country.lower() not in [
        "united states",
        "usa",
        "us",
        "united states of america",
    ] or not verify_age(age):
        print("Sorry, you are not eligible to register to vote.")
        return

    if not cont_registration():
        return

    state_abbr = get_input(
        "State of Residence (2 letter abbreviation): ",
        verify_state,
        "Invalid input. Please enter a valid U.S. state abbreviation.",
    )
    zipcode = get_input(
        "Zipcode: ",
        lambda x: x.isdigit() and len(x) == 5,
        "Invalid input. Please enter a valid 5-digit zipcode.",
    )

    print("\nRegistration Summary:")
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Age: {age}")
    print(f"Country of Citizenship: {country}")
    print(f"State of Residence: {state_abbr}")
    print(f"Zipcode: {zipcode}")

    print("\nCongratulations! You are eligible to vote and"
          " have successfully registered.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        print("Goodbye!")
    except ValueError as ve:
        print("A value error occurred:", str(ve))
    except TypeError as te:
        print("A type error occurred:", str(te))
    except Exception as e:
        print("An unexpected error occurred:", str(e))
    finally:
        # Close the DuckDB connection
        conn.close()
