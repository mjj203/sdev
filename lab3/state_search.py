"""This script provides functionalities to manage and display US states data."""

import sys
from io import BytesIO
import matplotlib.pyplot as plt
import requests
from PIL import Image

STATES = {
    "Alabama": {
      "CODE": "AL",
      "CAPITAL": "Montgomery",
      "POPULATION": 196010,
      "FLOWER": "Camellia",
      "URL": "https://upload.wikimedia.org/wikipedia/commons/9/96/Camellia_japonica_flower_2.jpg"
    },
    "Alaska": {
      "CODE": "AK",
      "CAPITAL": "Juneau",
      "POPULATION": 31534,
      "FLOWER": "Forget-me-not",
      "URL": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Forget-me-not_close_600.jpg"
    },
    "Arizona": {
        "CODE": "AZ",
        "CAPITAL": "Phoenix",
        "POPULATION": 1651344,
        "FLOWER": "Saguaro Cactus Blossom",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/f/f1/Carnegiea_gigantea_%28Saguaro_cactus%29_blossoms.jpg"
    },
    "Arkansas": {
        "CODE": "AR",
        "CAPITAL": "Little Rock",
        "POPULATION": 201029,
        "FLOWER": "Apple Blossom",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Appletree_bloom_l.jpg"
    },
    "California": {
        "CODE": "CA",
        "CAPITAL": "Sacramento",
        "POPULATION": 528306,
        "FLOWER": "California Poppy",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/e/ec/California_poppy.jpg"
    },
    "Colorado": {
        "CODE": "CO",
        "CAPITAL": "Denver",
        "POPULATION": 699288,
        "FLOWER": "Rocky Mountain Columbine",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/9/94/Aquilegia_caerulea.jpg"
    },
    "Connecticut": {
        "CODE": "CT",
        "CAPITAL": "Hartford",
        "POPULATION": 119817,
        "FLOWER": "Mountain Laurel",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Kalmia_latifolia2.jpg"
    },
    "Delaware": {
        "CODE": "DE",
        "CAPITAL": "Dover",
        "POPULATION": 37892,
        "FLOWER": "Peach Blossom",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Peach_flowers.jpg"
    },
    "Florida": {
        "CODE": "FL",
        "CAPITAL": "Tallahassee",
        "POPULATION": 198631,
        "FLOWER": "Orange Blossom",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/b/b0/OrangeBloss_wb.jpg"
    },
    "Georgia": {
        "CODE": "GA",
        "CAPITAL": "Atlanta",
        "POPULATION": 490270,
        "FLOWER": "Cherokee Rose",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cherokee_rose.jpg"
    },
    "Hawaii": {
        "CODE": "HI",
        "CAPITAL": "Honolulu",
        "POPULATION": 337088,
        "FLOWER": "Hibiscus",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Maohauhele.jpg"
    },
    "Idaho": {
      "CODE": "ID",
      "CAPITAL": "Boise",
      "POPULATION": 240713,
      "FLOWER": "Syringa",
      "URL": "https://upload.wikimedia.org/wikipedia/commons/4/49/Lewis%27s_Mock-orange_NFUW_-_Umatilla_NF_Oregon.jpg"
    },
    "Illinois": {
        "CODE": "IL",
        "CAPITAL": "Springfield",
        "POPULATION": 111711,
        "FLOWER": "Violet",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/3/30/Viola_sororia.jpg"
    },
    "Indiana": {
        "CODE": "IN",
        "CAPITAL": "Indianapolis",
        "POPULATION": 871449,
        "FLOWER": "Peony",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/2/23/Paeonia_19.jpg"
    },
    "Iowa": {
        "CODE": "IA",
        "CAPITAL": "Des Moines",
        "POPULATION": 208734,
        "FLOWER": "Wild Rose",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Rosa_arkansana.jpg"
    },
    "Kansas": {
        "CODE": "KS",
        "CAPITAL": "Topeka",
        "POPULATION": 125353,
        "FLOWER": "Sunflower",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/a/a9/A_sunflower.jpg"
    },
    "Kentucky": {
        "CODE": "KY",
        "CAPITAL": "Frankfort",
        "POPULATION": 28523,
        "FLOWER": "Goldenrod",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Solidago_virgaurea_minuta0.jpg"
    },
    "Louisiana": {
        "CODE": "LA",
        "CAPITAL": "Baton Rouge",
        "POPULATION": 217665,
        "FLOWER": "Magnolia",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/7/78/Magnolia_flower_Duke_campus.jpg"
    },
    "Maine": {
        "CODE": "ME",
        "CAPITAL": "Augusta",
        "POPULATION": 19058,
        "FLOWER": "White Pine",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Pinus_strobus_cones.JPG"
    },
    "Maryland": {
        "CODE": "MD",
        "CAPITAL": "Annapolis",
        "POPULATION": 40397,
        "FLOWER": "Black-eyed Susan",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Rudbeckia_hirta_Indian_Summer.JPG"
    },
    "Massachusett": {
        "CODE": "MA",
        "CAPITAL": "Boston",
        "POPULATION": 617459,
        "FLOWER": "Mayflower",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Trailing_arbutus.jpg"
    },
    "Michigan": {
        "CODE": "MI",
        "CAPITAL": "Lansing",
        "POPULATION": 112460,
        "FLOWER": "Apple Blossom",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Appletree_bloom_l.jpg"
    },
    "Minnesota": {
        "CODE": "MN",
        "CAPITAL": "St. Paul",
        "POPULATION": 299830,
        "FLOWER": "Pink and White Lady's Slipper",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Cypripedium_reginae_Orchi_004.jpg"
    },
    "Mississippi": {
        "CODE": "MS",
        "CAPITAL": "Jackson",
        "POPULATION": 143776,
        "FLOWER": "Magnolia",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/7/78/Magnolia_flower_Duke_campus.jpg"
    },
    "Missouri": {
        "CODE": "MO",
        "CAPITAL": "Jefferson City",
        "POPULATION": 42535,
        "FLOWER": "Hawthorn",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/4/47/%28MHNT%29_Crataegus_monogyna_-_flowers_and_buds.jpg"
    },
    "Montana": {
        "CODE": "MT",
        "CAPITAL": "Helena",
        "POPULATION": 34690,
        "FLOWER": "Bitterroot",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Lewisia_rediviva_4.jpg"
    },
    "Nebraska": {
        "CODE": "NE",
        "CAPITAL": "Lincoln",
        "POPULATION": 295222,
        "FLOWER": "Goldenrod",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Solidago_virgaurea_minuta0.jpg"
    },
    "Nevada": {
        "CODE": "NV",
        "CAPITAL": "Carson City",
        "POPULATION": 59630,
        "FLOWER": "Sagebrush",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/6/60/Sagebrush.jpg"
    },
    "New Hampshi": {
        "CODE": "NH",
        "CAPITAL": "Concord",
        "POPULATION": 44606,
        "FLOWER": "Purple Lilac",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Lilac_%282%29.jpg"
    },
    "New Jersey": {
        "CODE": "NJ",
        "CAPITAL": "Trenton",
        "POPULATION": 90048,
        "FLOWER": "Purple Violet",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/3/30/Viola_sororia.jpg"
    },
    "New Mexico": {
        "CODE": "NM",
        "CAPITAL": "Santa Fe",
        "POPULATION": 89220,
        "FLOWER": "Yucca",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/5/56/Yucca_filamentosa.jpg"
    },
    "New York": {
        "CODE": "NY",
        "CAPITAL": "Albany",
        "POPULATION": 97593,
        "FLOWER": "Rose",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Rosa_sp.163.jpg"
    },
    "North Carolin": {
      "CODE": "NC",
      "CAPITAL": "Raleigh",
      "POPULATION": 472540,
      "FLOWER": "Dogwood",
      "URL": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Flowering_Dogwood_Cornus_florida_Yellow_Flowers_3008px.JPG"
    },
    "North Dakota": {
        "CODE": "ND",
        "CAPITAL": "Bismarck",
        "POPULATION": 75073,
        "FLOWER": "Wild Prairie Rose",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Rosa_arkansana.jpg"
    },
    "Ohio": {
        "CODE": "OH",
        "CAPITAL": "Columbus",
        "POPULATION": 907865,
        "FLOWER": "Scarlet Carnation",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Red_Carnation_NGM_XXXI_p507.jpg"
    },
    "Oklahoma": {
        "CODE": "OK",
        "CAPITAL": "Oklahoma City",
        "POPULATION": 697763,
        "FLOWER": "Oklahoma Rose",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Rose%2C_Oklahoma_-_Flickr_-_nekonomania.jpg"
    },
    "Oregon": {
      "CODE": "OR",
      "CAPITAL": "Salem",
      "POPULATION": 181620,
      "FLOWER": "Oregon Grape",
      "URL": "https://upload.wikimedia.org/wikipedia/commons/8/87/%28MHNT%29_Berberis_aquifolium_inflorecences_and_buds.jpg"
    },
    "Pennsylvania": {
        "CODE": "PA",
        "CAPITAL": "Harrisburg",
        "POPULATION": 50267,
        "FLOWER": "Mountain Laurel",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Kalmia_latifolia2.jpg"
    },
    "Rhode Island": {
        "CODE": "RI",
        "CAPITAL": "Providence",
        "POPULATION": 188877,
        "FLOWER": "Violet",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/3/30/Viola_sororia.jpg"
    },
    "South Carolina": {
        "CODE": "SC",
        "CAPITAL": "Columbia",
        "POPULATION": 137996,
        "FLOWER": "Yellow Jessamine",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/1/19/Gelsemium_sempervirensCDP140CA.jpg"
    },
    "South Dakota": {
        "CODE": "SD",
        "CAPITAL": "Pierre",
        "POPULATION": 13954,
        "FLOWER": "Pasque Flower",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Pulsatilla_vulgaris-700px.jpg"
    },
    "Tennessee": {
        "CODE": "TN",
        "CAPITAL": "Nashville",
        "POPULATION": 658525,
        "FLOWER": "Iris",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Iris_%27Gene_Wild%27_2007-05-13_383.jpg"
    },
    "Texas": {
        "CODE": "TX",
        "CAPITAL": "Austin",
        "POPULATION": 966292,
        "FLOWER": "Bluebonnet",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/3/33/Texas_Bluebonnet_%28Lupinus_texensis%29.jpg"
    },
    "Utah": {
        "CODE": "UT",
        "CAPITAL": "Salt Lake City",
        "POPULATION": 202272,
        "FLOWER": "Sego Lily",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/0/01/Sego_lily_cm.jpg"
    },
    "Vermont": {
        "CODE": "VT",
        "CAPITAL": "Montpelier",
        "POPULATION": 7988,
        "FLOWER": "Red Clover",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/5/56/Red_clover_closeup.jpg"
    },
    "Virginia": {
        "CODE": "VA",
        "CAPITAL": "Richmond",
        "POPULATION": 226472,
        "FLOWER": "American Dogwood",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Benthamidia_florida2.jpg"
    },
    "Washington": {
        "CODE": "WA",
        "CAPITAL": "Olympia",
        "POPULATION": 56510,
        "FLOWER": "Western Rhododendron",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Rhododendron_macrophyllum.JPG"
    },
    "West Virginia": {
      "CODE": "WV",
      "CAPITAL": "Charleston",
      "POPULATION": 46692,
      "FLOWER": "Rhododendron",
      "URL": "https://upload.wikimedia.org/wikipedia/commons/7/75/Rhododendron-by-eiffel-public-domain-20040617.jpg"
    },
    "Wisconsin": {
        "CODE": "WI",
        "CAPITAL": "Madison",
        "POPULATION": 269897,
        "FLOWER": "Wood Violet",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/3/30/Viola_sororia.jpg"
    },
    "Wyoming": {
        "CODE": "WY",
        "CAPITAL": "Cheyenne",
        "POPULATION": 64831,
        "FLOWER": "Indian Paintbrush",
        "URL": "https://upload.wikimedia.org/wikipedia/commons/7/79/Indian_Paintbrush_in_Grand_Teton_NP-NPS.jpg"
    }
}

STATE_CODE_LOOKUP = {details["CODE"]: state for state, details in STATES.items()}


def validate_states_data():
    """Validates the data of each state in the global STATES dictionary.

    This function checks two aspects for each state:
    1. Presence of all required keys (CAPITAL, POPULATION, FLOWER, URL).
    2. The data type of the POPULATION key, ensuring it's an integer.

    Returns:
        bool: True if all states have the required keys and correct data types, False otherwise.

    Prints an error message and returns False if:
    - A state is missing one or more required keys.
    - The population value is not an integer.
    - A KeyError is encountered in the STATES data."""
    required_keys = {"CAPITAL", "POPULATION", "FLOWER", "URL"}
    try:
        for state, details in STATES.items():
            # Check if all required keys exist
            if not required_keys.issubset(details.keys()):
                missing_keys = required_keys - details.keys()
                print(f"Error: {state} is missing keys: {missing_keys}")
                return False

            # Check if population is an integer
            if not isinstance(details["POPULATION"], int):
                print(f"Error: Population for {state} is not an integer")
                return False

        return True

    except KeyError as e:
        print(f"KeyError encountered in states data: {e}")
        return False


def display_states():
    """For each state, the function prints its name, capital, population (formatted with commas),
    and the state flower. The states are displayed in alphabetical order.

    Exceptions:
        KeyError: If a required key is missing in the state's data, an error message is printed."""
    try:
        for state, details in sorted(STATES.items()):
            formatted_population = f"{details['POPULATION']:,}"
            print(
                f"{state}: Capital: {details['CAPITAL']}, "
                f"Population: {formatted_population}, Flower: {details['FLOWER']}"
            )
    except KeyError as e:
        print(f"KeyError: Missing data in the states dictionary - {e}")


def get_state_name_from_code(code):
    """The function looks up the state code in the global STATE_CODE_LOOKUP dictionary
    and returns the corresponding state name.

    Args:
        code (str): The two-letter state code to look up.

    Returns:
        str: The name of the state corresponding to the provided code, or None if
        the code is not found.

    Prints an error message if the state code is not found in the STATE_CODE_LOOKUP dictionary."""
    try:
        return STATE_CODE_LOOKUP[code.upper()]
    except KeyError:
        print(f"State code '{code}' not found.")
        return None

def search_state():
    """This function prompts the user to enter either a state name or a two-letter state code. 
    It then looks up and displays the state's capital, population (formatted with commas), 
    and state flower. If the input is a two-letter code, it uses the get_state_name_from_code 
    function to find the corresponding state name.

    If the state or state code is not found in the STATES dictionary, an appropriate 
    message is printed. The function also attempts to display an image of the state's flower 
    if the state is found.

    Exceptions:
        Any exception is caught and an error message is printed, indicating an issue during 
        the search or data retrieval process."""
    try:
        identifier = input("Enter state name or 2-letter code: ").strip()

        # Check if the input is a two-letter code
        if len(identifier) == 2:
            state_name = get_state_name_from_code(identifier)
            if not state_name:
                print("State code not found.")
                return
        else:
            state_name = identifier.capitalize()

        if state_name in STATES:
            state_info = STATES[state_name]
            formatted_population = f"{state_info['POPULATION']:,}"
            print(
                f"Capital: {state_info['CAPITAL']}, "
                f"Population: {formatted_population}, Flower: {state_info['FLOWER']}"
            )
            display_state_flower_image(state_name)
        else:
            print("State not found.")

    except KeyError as e:
        print(f"Key error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred during image retrieval: {e}")


def display_population_graph():
    """This function sorts the states based on their population (in descending order)
    and selects the top 5. It then plots a bar graph showing these states and their 
    respective population values.

    The population data is expected to be integers in the STATES dictionary.

    Exceptions:
        ValueError: Raised and caught if there's an issue with the population data, 
                    such as incorrect formatting or data type."""
    try:
        # Sorting states based on population, which is already an integer
        top_states = sorted(
            STATES.items(), key=lambda x: x[1]["POPULATION"], reverse=True
        )[:5]
        names = [state[0] for state in top_states]
        values = [state[1]["POPULATION"] for state in top_states]

        plt.figure(figsize=(10, 6))
        plt.bar(names, values)
        plt.xlabel("States")
        plt.ylabel("Population")
        plt.title("Top 5 Populated States")
        plt.show()
    except ValueError:
        print("Error: There was an issue with the population data.")


def safe_update_state(state_name, key, value):
    """This function attempts to update the value of a specified key for a given state. 
    If the specified key or state does not exist in the STATES dictionary, a KeyError 
    is caught and handled.

    Args:
        state_name (str): The name of the state to be updated.
        key (str): The key in the state's dictionary to be updated (e.g., 'CAPITAL', 'POPULATION').
        value: The new value to assign to the specified key.

    Returns:
        bool: True if the update is successful, False if a KeyError is encountered.

    Raises:
        KeyError: If the specified state or key is not found in the STATES dictionary."""
    try:
        STATES[state_name][key] = value
    except KeyError as e:
        print(f"KeyError: Missing key in states data - {e}")
        return False
    return True


def add_or_update_state(state_name, **kwargs):
    """This function allows updating various attributes (like capital, population, flower,
    and URL) of a specified state. The updates are performed using a dictionary of lambda
    functions, each corresponding to a different attribute. If the specified state does not
    exist in the STATES dictionary, an error message is printed.

    Args:
        state_name (str): The name of the state to be updated.
        **kwargs: Variable keyword arguments representing the attributes to be updated
        and their new values. For example, population=500000 would update the
        'POPULATION' attribute.

    Returns:
        bool: True if all updates are successful and the states data is valid post-update,
        False otherwise.

    Note:
        The function utilizes 'safe_update_state' for the actual update process and
        validates the entire STATES data after the updates using 'validate_states_data'."""
    if state_name not in STATES:
        print(f"State '{state_name}' does not exist.")
        return False

    update_actions = {
        "capital": lambda value: safe_update_state(
            state_name, "CAPITAL", value
        ),
        "population": lambda value: safe_update_state(
            state_name, "POPULATION", value
        ),
        "flower": lambda value: safe_update_state(state_name, "FLOWER", value),
        "url": lambda value: safe_update_state(state_name, "URL", value),
    }

    for key, value in kwargs.items():
        if value and key in update_actions:
            if not update_actions[key](value):
                return False

    return validate_states_data()


def update_population():
    """This function prompts the user to enter either a state name or its two-letter code.
    It then requests the new population value for that state. If the entered identifier
    is a two-letter code, it uses 'get_state_name_from_code' to find the corresponding 
    state name. The population is updated only if the state exists in STATES.

    The function checks the validity of the new population input, ensuring it's a numeric value.
    If the new population is valid, it is updated in the STATES dictionary.

    Exceptions:
        ValueError: Raised and handled if the entered population is not a valid numeric value.

    Prints:
        A message indicating whether the population update was successful or not.
        Error messages for invalid inputs or if the state is not found."""
    identifier = input("Enter state name or 2-letter code: ").strip()
    state_name = (
        get_state_name_from_code(identifier)
        if len(identifier) == 2
        else identifier.capitalize()
    )

    if state_name in STATES:
        try:
            new_population = input(f"Enter the new population for {state_name}: ")
            population_int = int(new_population.replace(",", ""))  # Convert to integer

            if add_or_update_state(
                state_name, population=population_int
            ):  # Pass integer directly
                print("Population updated.")
            else:
                print("Failed to update population. Invalid data.")

        except ValueError:
            print("Invalid input: Population must be a numeric value.")
    else:
        print("State not found.")


def display_state_flower_image(state_name):
    """Given a state name, the function fetches the image URL from the global STATES dictionary
    and attempts to download and display the image. It handles various exceptions such as 
    failure to download the image or if the image cannot be opened.

    Args:
        state_name (str): The name of the state for which the flower image will be displayed.

    Prints:
        A message indicating the reason for any failure in displaying the image, such as
        network errors, invalid URLs, or corrupted image files.
        An error message if the specified state is not found in the STATES dictionary."""
    if state_name in STATES:
        url = STATES[state_name]["URL"]
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Try to open the image
                try:
                    img = Image.open(BytesIO(response.content))
                    plt.imshow(img)
                    plt.axis("off")  # Turn off axis numbers
                    plt.show()
                except IOError:
                    print(
                        f"Failed to open the image from {url}. "
                        f"The file may not be an image or might be corrupted."
                    )
            else:
                print(
                    f"Failed to download the image from {url}. "
                    f"HTTP status code: {response.status_code}"
                )
        except requests.exceptions.RequestException:
            print(f"Failed to download the image from {url} due to a network error.")
    else:
        print(f"State '{state_name}' not found.")


def exit_program():
    """This function prints a farewell message and then terminates the execution of the program.
    It uses the built-in 'exit' function to stop the program."""
    print("Exiting the program. Goodbye!")
    sys.exit()


def main():
    """This function presents a menu of options to the user, allowing them to interact with 
    the U.S. States Information system. It supports displaying state details, searching 
    for a state, showing a population graph, updating state population, and exiting the program.

    The user's choice is processed and the corresponding function is executed. The program 
    continues to display the menu and accept input until the user chooses to exit. The function 
    handles various exceptions related to invalid input and network issues.

    Exceptions:
        ValueError: Raised and caught if there's an invalid input for number format.
        requests.exceptions.RequestException: Caught if there's a network error during a request.
        KeyboardInterrupt: Caught when the user interrupts the program execution (e.g., Ctrl+C)."""
    options = {
        "1": display_states,
        "2": search_state,
        "3": display_population_graph,
        "4": update_population,
        "5": exit_program  # No lambda needed if exit_program takes no arguments
    }
    while True:
        try:
            print("\nU.S. States Information")
            print("1. Display all states")
            print("2. Search for a state")
            print("3. Display population graph")
            print("4. Update state population")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice in options:
                options[choice]()  # Call the chosen function
            else:
                print("Invalid option. Please try again.")

        except ValueError:
            print("Value error: Invalid number format.")
        except requests.exceptions.RequestException:
            print("Network error: Failed to perform a network request.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by the user. Exiting...")
            break


if __name__ == "__main__":
    if validate_states_data():  # Ensure the states data is valid before starting the program
        main()
    else:
        print("The states data failed validation and the program cannot start.")
