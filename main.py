from io import BytesIO
import matplotlib.pyplot as plt
import requests
from PIL import Image


states = {
    "Alabama": {
        "CODE": "AL",
        "CAPITAL": "Montgomery",
        "POPULATION": 196010,
        "FLOWER": "Camellia",
        "URL": "https://en.wikipedia.org/wiki/File:Camellia_japonica_flower_2.jpg",
    },
    "Alaska": {
        "CODE": "AK",
        "CAPITAL": "Juneau",
        "POPULATION": 31534,
        "FLOWER": "Forget-me-not",
        "URL": "https://en.wikipedia.org/wiki/File:Forget-me-not_close_600.jpg",
    },
    "Arizona": {
        "CODE": "AZ",
        "CAPITAL": "Phoenix",
        "POPULATION": 1651344,
        "FLOWER": "Saguaro Cactus Blossom",
        "URL": "https://en.wikipedia.org/wiki/File:Carnegiea_gigantea_(Saguaro_cactus)_blossoms.jpg",
    },
    "Arkansas": {
        "CODE": "AR",
        "CAPITAL": "Little Rock",
        "POPULATION": 201029,
        "FLOWER": "Apple Blossom",
        "URL": "https://en.wikipedia.org/wiki/File:Appletree_bloom_l.jpg",
    },
    "California": {
        "CODE": "CA",
        "CAPITAL": "Sacramento",
        "POPULATION": 528306,
        "FLOWER": "California Poppy",
        "URL": "https://en.wikipedia.org/wiki/File:California_poppy.jpg",
    },
    "Colorado": {
        "CODE": "CO",
        "CAPITAL": "Denver",
        "POPULATION": 699288,
        "FLOWER": "Rocky Mountain Columbine",
        "URL": "https://en.wikipedia.org/wiki/File:Aquilegia_caerulea.jpg",
    },
    "Connecticut": {
        "CODE": "CT",
        "CAPITAL": "Hartford",
        "POPULATION": 119817,
        "FLOWER": "Mountain Laurel",
        "URL": "https://en.wikipedia.org/wiki/File:Kalmia_latifolia2.jpg",
    },
    "Delaware": {
        "CODE": "DE",
        "CAPITAL": "Dover",
        "POPULATION": 37892,
        "FLOWER": "Peach Blossom",
        "URL": "https://en.wikipedia.org/wiki/File:Peach_flowers.jpg",
    },
    "Florida": {
        "CODE": "FL",
        "CAPITAL": "Tallahassee",
        "POPULATION": 198631,
        "FLOWER": "Orange Blossom",
        "URL": "https://en.wikipedia.org/wiki/File:OrangeBloss_wb.jpg",
    },
    "Georgia": {
        "CODE": "GA",
        "CAPITAL": "Atlanta",
        "POPULATION": 490270,
        "FLOWER": "Cherokee Rose",
        "URL": "https://en.wikipedia.org/wiki/File:Cherokee_rose.jpg",
    },
    "Hawaii": {
        "CODE": "HI",
        "CAPITAL": "Honolulu",
        "POPULATION": 337088,
        "FLOWER": "Hibiscus",
        "URL": "https://en.wikipedia.org/wiki/File:Maohauhele.jpg",
    },
    "Idaho": {
        "CODE": "ID",
        "CAPITAL": "Boise",
        "POPULATION": 240713,
        "FLOWER": "Syringa",
        "URL": "https://en.wikipedia.org/wiki/File:Lewis%27s_Mock-orange_NFUW_-_Umatilla_NF_Oregon.jpg",
    },
    "Illinois": {
        "CODE": "IL",
        "CAPITAL": "Springfield",
        "POPULATION": 111711,
        "FLOWER": "Violet",
        "URL": "https://en.wikipedia.org/wiki/File:Viola_sororia.jpg",
    },
    "Indiana": {
        "CODE": "IN",
        "CAPITAL": "Indianapolis",
        "POPULATION": 871449,
        "FLOWER": "Peony",
        "URL": "https://en.wikipedia.org/wiki/File:Paeonia_19.jpg",
    },
    "Iowa": {
        "CODE": "IA",
        "CAPITAL": "Des Moines",
        "POPULATION": 208734,
        "FLOWER": "Wild Rose",
        "URL": "https://en.wikipedia.org/wiki/File:Rosa_arkansana.jpg",
    },
    "Kansas": {
        "CODE": "KS",
        "CAPITAL": "Topeka",
        "POPULATION": 125353,
        "FLOWER": "Sunflower",
        "URL": "https://en.wikipedia.org/wiki/File:A_sunflower.jpg",
    },
    "Kentucky": {
        "CODE": "KY",
        "CAPITAL": "Frankfort",
        "POPULATION": 28523,
        "FLOWER": "Goldenrod",
        "URL": "https://en.wikipedia.org/wiki/File:Solidago_virgaurea_minuta0.jpg",
    },
    "Louisiana": {
        "CODE": "LA",
        "CAPITAL": "Baton Rouge",
        "POPULATION": 217665,
        "FLOWER": "Magnolia",
        "URL": "https://en.wikipedia.org/wiki/File:Magnolia_flower_Duke_campus.jpg",
    },
    "Maine": {
        "CODE": "ME",
        "CAPITAL": "Augusta",
        "POPULATION": 19058,
        "FLOWER": "White Pine",
        "URL": "https://en.wikipedia.org/wiki/File:Pinus_strobus_cones.JPG",
    },
    "Maryland": {
        "CODE": "MD",
        "CAPITAL": "Annapolis",
        "POPULATION": 40397,
        "FLOWER": "Black-eyed Susan",
        "URL": "https://en.wikipedia.org/wiki/File:Rudbeckia_hirta_Indian_Summer.JPG",
    },
    "Massachusett": {
        "CODE": "MA",
        "CAPITAL": "Boston",
        "POPULATION": 617459,
        "FLOWER": "Mayflower",
        "URL": "https://en.wikipedia.org/wiki/File:Trailing_arbutus.jpg",
    },
    "Michigan": {
        "CODE": "MI",
        "CAPITAL": "Lansing",
        "POPULATION": 112460,
        "FLOWER": "Apple Blossom",
        "URL": "https://en.wikipedia.org/wiki/File:Appletree_bloom_l.jpg",
    },
    "Minnesota": {
        "CODE": "MN",
        "CAPITAL": "St. Paul",
        "POPULATION": 299830,
        "FLOWER": "Pink and White Lady's Slipper",
        "URL": "https://en.wikipedia.org/wiki/File:Cypripedium_reginae_Orchi_004.jpg",
    },
    "Mississippi": {
        "CODE": "MS",
        "CAPITAL": "Jackson",
        "POPULATION": 143776,
        "FLOWER": "Magnolia",
        "URL": "https://en.wikipedia.org/wiki/File:Magnolia_flower_Duke_campus.jpg",
    },
    "Missouri": {
        "CODE": "MO",
        "CAPITAL": "Jefferson City",
        "POPULATION": 42535,
        "FLOWER": "Hawthorn",
        "URL": "https://en.wikipedia.org/wiki/File:(MHNT)_Crataegus_monogyna_-_flowers_and_buds.jpg",
    },
    "Montana": {
        "CODE": "MT",
        "CAPITAL": "Helena",
        "POPULATION": 34690,
        "FLOWER": "Bitterroot",
        "URL": "https://en.wikipedia.org/wiki/File:Lewisia_rediviva_4.jpg",
    },
    "Nebraska": {
        "CODE": "NE",
        "CAPITAL": "Lincoln",
        "POPULATION": 295222,
        "FLOWER": "Goldenrod",
        "URL": "https://en.wikipedia.org/wiki/File:Solidago_virgaurea_minuta0.jpg",
    },
    "Nevada": {
        "CODE": "NV",
        "CAPITAL": "Carson City",
        "POPULATION": 59630,
        "FLOWER": "Sagebrush",
        "URL": "https://en.wikipedia.org/wiki/File:Sagebrush.jpg",
    },
    "New Hampshi": {
        "CODE": "NH",
        "CAPITAL": "Concord",
        "POPULATION": 44606,
        "FLOWER": "Purple Lilac",
        "URL": "https://en.wikipedia.org/wiki/File:Lilac_(2).jpg",
    },
    "New Jersey": {
        "CODE": "NJ",
        "CAPITAL": "Trenton",
        "POPULATION": 90048,
        "FLOWER": "Purple Violet",
        "URL": "https://en.wikipedia.org/wiki/File:Viola_sororia.jpg",
    },
    "New Mexico": {
        "CODE": "NM",
        "CAPITAL": "Santa Fe",
        "POPULATION": 89220,
        "FLOWER": "Yucca",
        "URL": "https://en.wikipedia.org/wiki/File:Yucca_filamentosa.jpg",
    },
    "New York": {
        "CODE": "NY",
        "CAPITAL": "Albany",
        "POPULATION": 97593,
        "FLOWER": "Rose",
        "URL": "https://en.wikipedia.org/wiki/File:Rosa_sp.163.jpg",
    },
    "North Carolin": {
        "CODE": "NC",
        "CAPITAL": "Raleigh",
        "POPULATION": 472540,
        "FLOWER": "Dogwood",
        "URL": "https://en.wikipedia.org/wiki/File:Flowering_Dogwood_Cornus_florida_Yellow_Flowers_3008px.JPG",
    },
    "North Dakota": {
        "CODE": "ND",
        "CAPITAL": "Bismarck",
        "POPULATION": 75073,
        "FLOWER": "Wild Prairie Rose",
        "URL": "https://en.wikipedia.org/wiki/File:Rosa_arkansana.jpg",
    },
    "Ohio": {
        "CODE": "OH",
        "CAPITAL": "Columbus",
        "POPULATION": 907865,
        "FLOWER": "Scarlet Carnation",
        "URL": "https://en.wikipedia.org/wiki/File:Red_Carnation_NGM_XXXI_p507.jpg",
    },
    "Oklahoma": {
        "CODE": "OK",
        "CAPITAL": "Oklahoma City",
        "POPULATION": 697763,
        "FLOWER": "Oklahoma Rose",
        "URL": "https://en.wikipedia.org/wiki/File:Rose,_Oklahoma_-_Flickr_-_nekonomania.jpg",
    },
    "Oregon": {
        "CODE": "OR",
        "CAPITAL": "Salem",
        "POPULATION": 181620,
        "FLOWER": "Oregon Grape",
        "URL": "https://en.wikipedia.org/wiki/File:(MHNT)_Berberis_aquifolium_inflorecences_and_buds.jpg",
    },
    "Pennsylvania": {
        "CODE": "PA",
        "CAPITAL": "Harrisburg",
        "POPULATION": 50267,
        "FLOWER": "Mountain Laurel",
        "URL": "https://en.wikipedia.org/wiki/File:Kalmia_latifolia2.jpg",
    },
    "Rhode Island": {
        "CODE": "RI",
        "CAPITAL": "Providence",
        "POPULATION": 188877,
        "FLOWER": "Violet",
        "URL": "https://en.wikipedia.org/wiki/File:Viola_sororia.jpg",
    },
    "South Carolin": {
        "CODE": "SC",
        "CAPITAL": "Columbia",
        "POPULATION": 137996,
        "FLOWER": "Yellow Jessamine",
        "URL": "https://en.wikipedia.org/wiki/File:Gelsemium_sempervirensCDP140CA.jpg",
    },
    "South Dakota": {
        "CODE": "SD",
        "CAPITAL": "Pierre",
        "POPULATION": 13954,
        "FLOWER": "Pasque Flower",
        "URL": "https://en.wikipedia.org/wiki/File:Pulsatilla_vulgaris-700px.jpg",
    },
    "Tennessee": {
        "CODE": "TN",
        "CAPITAL": "Nashville",
        "POPULATION": 658525,
        "FLOWER": "Iris",
        "URL": "https://en.wikipedia.org/wiki/File:Iris_%27Gene_Wild%27_2007-05-13_383.jpg",
    },
    "Texas": {
        "CODE": "TX",
        "CAPITAL": "Austin",
        "POPULATION": 966292,
        "FLOWER": "Bluebonnet",
        "URL": "https://en.wikipedia.org/wiki/File:Texas_Bluebonnet_(Lupinus_texensis).jpg",
    },
    "Utah": {
        "CODE": "UT",
        "CAPITAL": "Salt Lake City",
        "POPULATION": 202272,
        "FLOWER": "Sego Lily",
        "URL": "https://en.wikipedia.org/wiki/File:Sego_lily_cm.jpg",
    },
    "Vermont": {
        "CODE": "VT",
        "CAPITAL": "Montpelier",
        "POPULATION": 7988,
        "FLOWER": "Red Clover",
        "URL": "https://en.wikipedia.org/wiki/File:Red_clover_closeup.jpg",
    },
    "Virginia": {
        "CODE": "VA",
        "CAPITAL": "Richmond",
        "POPULATION": 226472,
        "FLOWER": "American Dogwood",
        "URL": "https://en.wikipedia.org/wiki/File:Benthamidia_florida2.jpg",
    },
    "Washington": {
        "CODE": "WA",
        "CAPITAL": "Olympia",
        "POPULATION": 56510,
        "FLOWER": "Western Rhododendron",
        "URL": "https://en.wikipedia.org/wiki/File:Rhododendron_macrophyllum.JPG",
    },
    "West Virginia": {
        "CODE": "WV",
        "CAPITAL": "Charleston",
        "POPULATION": 46692,
        "FLOWER": "Rhododendron",
        "URL": "https://en.wikipedia.org/wiki/File:Rhododendron-by-eiffel-public-domain-20040617.jpg",
    },
    "Wisconsin": {
        "CODE": "WI",
        "CAPITAL": "Madison",
        "POPULATION": 269897,
        "FLOWER": "Wood Violet",
        "URL": "https://en.wikipedia.org/wiki/File:Viola_sororia.jpg",
    },
    "Wyoming": {
        "CODE": "WY",
        "CAPITAL": "Cheyenne",
        "POPULATION": 64831,
        "FLOWER": "Indian Paintbrush",
        "URL": "https://en.wikipedia.org/wiki/File:Indian_Paintbrush_in_Grand_Teton_NP-NPS.jpg",
    },
}

state_code_lookup = {details["CODE"]: state for state, details in states.items()}


def validate_states_data(states):
    required_keys = {"CAPITAL", "POPULATION", "FLOWER", "URL"}
    try:
        for state, details in states.items():
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
    except Exception as e:
        print(f"An unexpected error occurred during validation: {e}")
        return False


def display_states(states):
    try:
        for state, details in sorted(states.items()):
            formatted_population = "{:,}".format(details["POPULATION"])
            print(
                f"{state}: Capital: {details['CAPITAL']}, Population: {formatted_population}, Flower: {details['FLOWER']}"
            )
    except KeyError as e:
        print(f"KeyError: Missing data in the states dictionary - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_state_name_from_code(state_code_lookup, code):
    try:
        return state_code_lookup[code.upper()]
    except KeyError:
        print(f"State code '{code}' not found.")


def search_state(states, state_code_lookup):
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

        if state_name in states:
            state_info = states[state_name]
            formatted_population = "{:,}".format(state_info["POPULATION"])
            print(
                f"Capital: {state_info['CAPITAL']}, Population: {formatted_population}, Flower: {state_info['FLOWER']}"
            )
            display_state_flower_image(state_name)
        else:
            print("State not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


def display_population_graph(states):
    try:
        # Sorting states based on population, which is already an integer
        top_states = sorted(
            states.items(), key=lambda x: x[1]["POPULATION"], reverse=True
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
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def safe_update_state(states, state_name, key, value):
    try:
        states[state_name][key] = value
    except KeyError as e:
        print(f"KeyError: Missing key in states data - {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    return True


def add_or_update_state(states, state_name, **kwargs):
    if state_name not in states:
        print(f"State '{state_name}' does not exist.")
        return False

    update_actions = {
        "capital": lambda value: safe_update_state(
            states, state_name, "CAPITAL", value
        ),
        "population": lambda value: safe_update_state(
            states, state_name, "POPULATION", value
        ),
        "flower": lambda value: safe_update_state(states, state_name, "FLOWER", value),
        "url": lambda value: safe_update_state(states, state_name, "URL", value),
    }

    for key, value in kwargs.items():
        if value and key in update_actions:
            if not update_actions[key](value):
                return False

    return validate_states_data(states)


def update_population(states):
    identifier = input("Enter state name or 2-letter code: ").strip()
    state_name = (
        get_state_name_from_code(states, identifier)
        if len(identifier) == 2
        else identifier.capitalize()
    )

    if state_name in states:
        try:
            new_population = input(f"Enter the new population for {state_name}: ")
            population_int = int(new_population.replace(",", ""))  # Convert to integer

            if add_or_update_state(
                states, state_name, population=population_int
            ):  # Pass integer directly
                print("Population updated.")
            else:
                print("Failed to update population. Invalid data.")

        except ValueError:
            print("Invalid input: Population must be a numeric value.")
    else:
        print("State not found.")


def display_state_flower_image(states, state_name):
    if state_name in states:
        url = states[state_name]["URL"]
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Try to open the image
                try:
                    img = Image.open(BytesIO(response.content))
                    plt.imshow(img)
                    plt.axis("off")  # Turn off axis numbers
                    plt.show()
                except Exception:
                    print(
                        f"Failed to open the image from {url}. The file may not be an image or might be corrupted."
                    )
            else:
                print(
                    f"Failed to download the image from {url}. HTTP status code: {response.status_code}"
                )
        except requests.exceptions.RequestException:
            print(f"Failed to download the image from {url} due to a network error.")
    else:
        print(f"State '{state_name}' not found.")


def exit_program():
    print("Exiting the program. Goodbye!")
    exit()


def main():
    options = {
        "1": lambda: display_states(states),
        "2": lambda: search_state(states, state_code_lookup),
        "3": lambda: display_population_graph(states),
        "4": lambda: update_population(states),
        "5": exit_program,  # No lambda needed if exit_program takes no arguments
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
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if validate_states_data(
        states
    ):  # Ensure the states data is valid before starting the program
        main()
    else:
        print("The states data failed validation and the program cannot start.")
