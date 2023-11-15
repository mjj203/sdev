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
This module provides tools for managing and displaying information about U.S. states.
It includes functionalities to read state data, validate the data integrity, update
state details, display state-related statistics, and interact with users through a
command-line interface.

Functions include:
- Reading and converting state data from CSV to JSON.
- Validating state data for completeness and correct data type.
- Displaying state details like capital, population, and state flower.
- Plotting population statistics in a bar graph.
- Updating state information based on user input.
- Handling user interactions in a menu-driven approach.

The module is designed to be run as a script, offering a user-friendly interface
for exploring and manipulating U.S. states data.

Note:
    The module relies on external libraries like 'matplotlib' for graphing and
    'requests' for network operations.
"""

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
    """
    Validate the data of each state in the global STATES dictionary.

    This function checks for the presence of all required keys (CAPITAL, POPULATION,
    FLOWER, URL) and the data type of the POPULATION key, ensuring it's an integer.

    Returns:
        bool: True if data is valid, False otherwise, with an error message printed.
    """
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
    """
    Display name, capital, population, and flower of each state in alphabetical order.

    Exceptions:
        KeyError: Prints an error message if a required key is missing.
    """
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
    """
    Retrieve the state name corresponding to a two-letter state code.

    Args:
        code (str): The two-letter state code.

    Returns:
        str: State name or None if code is not found, with an error message printed.
    """
    try:
        return STATE_CODE_LOOKUP[code.upper()]
    except KeyError:
        print(f"State code '{code}' not found.")
        return None

def search_state():
    """
    Search and display details of a state based on user input (name or code).

    The function handles state lookup, details display, and attempts to display
    an image of the state's flower.

    Exceptions:
        General exception: Prints an error message for search or data retrieval issues.
    """
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
    """
    Display a bar graph of the top 5 most populated states.

    Exceptions:
        ValueError: Handles incorrect population data formatting or type.
    """
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
    """
    Update the value of a specified key for a given state in the STATES dictionary.

    Args:
        state_name (str): Name of the state.
        key (str): Key to be updated (e.g., 'CAPITAL', 'POPULATION').
        value: New value for the specified key.

    Returns:
        bool: True if successful, False with an error message if KeyError occurs.
    """
    try:
        STATES[state_name][key] = value
    except KeyError as e:
        print(f"KeyError: Missing key in states data - {e}")
        return False
    return True


def add_or_update_state(state_name, **kwargs):
    """
    Update various attributes of a specified state.

    Args:
        state_name (str): Name of the state to be updated.
        **kwargs: Attributes to be updated and their new values.

    Returns:
        bool: True if updates successful and data valid, False otherwise.

    Note:
        Utilizes 'safe_update_state' and 'validate_states_data'.
    """
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
    """
    Prompt user for a state and update its population.

    Requests new population value and updates if valid. Handles state lookup and
    input validation.

    Exceptions:
        ValueError: Handles invalid numeric input for population.
    """
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
    """
    Display the image of a state's flower given its name.

    Args:
        state_name (str): Name of the state.

    Prints:
        Error messages for failed image display or if state not found.
    """
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
    """
    Print a farewell message and terminate the program execution.
    """
    print("Exiting the program. Goodbye!")
    sys.exit()


def main():
    """
    Present a menu to interact with the U.S. States Information system.

    Supports various operations like displaying state details, searching for a state,
    showing population graph, updating state population, and exiting.

    Exceptions:
        ValueError: Handles invalid number format for input.
        requests.exceptions.RequestException: Handles network errors.
        KeyboardInterrupt: Handles program interruption by the user.
    """
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
