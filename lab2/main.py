"""
Menu-Driven Application

This script provides a command-line interface for a user to interact with a set of
functionalities, including generating secure passwords, calculating and formatting
percentages, determining the number of days until a specific date, solving for the
length of a triangle's leg using the Law of Cosines, and calculating the volume of
a Right Circular Cylinder.

Features:
- Generate Secure Password: Allows the user to generate a secure password based on
  their preferences for length and character types.
- Calculate and Format a Percentage: Calculates a percentage based on user-provided
  numerator and denominator, and formats the output to a specified number of decimal
  places.
- Days Until July 4, 2025: Calculates the number of days from the current date until
  July 4, 2025.
- Law of Cosines: Uses the Law of Cosines to calculate the length of a triangle's leg.
- Volume of a Right Circular Cylinder: Calculates the volume of a Right Circular
  Cylinder based on user-provided radius and height.
- Exit Program: Allows the user to exit the application.

The application runs in a loop, continuously providing the user with the menu options
until they choose to exit. Input validation is performed to ensure that all user
inputs are correct and within the expected ranges.

Dependencies:
- Python 3.6 or higher due to the usage of f-strings and other newer language features.
- The `math` module for mathematical calculations.
- The `datetime` module for date manipulations.

To run the script, simply execute it in a Python 3.6+ environment. The user will be
prompted to interact with the application through the command line.
"""
import datetime
import math
import secrets
import string


def generate_password():
    """function creates a password based on the specified length and complexity.
    The user is prompted to enter their desired password length and specify
    the types of characters they want to include."""
    try:
        length = int(input("Enter the length of the password: "))
        print("Select the complexity of the password (Type 'yes' or 'no' for each):")
        options = {
            'uppercase letters': string.ascii_uppercase,
            'lowercase letters': string.ascii_lowercase,
            'numbers': string.digits,
            'special characters': string.punctuation
        }

        characters = "".join(
            chars for option, chars in options.items() if input(f"Use {option}? ").lower() == 'yes'
            )

        if not characters:
            print("Please select at least one type of character for your password.")
            return

        password = ''.join(secrets.choice(characters) for _ in range(length))
        print("Generated Password:", password)
    except ValueError:
        print("Invalid input! Please enter an integer for the password length.")


def calculate_percentage():
    """This function calculates the percentage by dividing the numerator by the denominator,
    multiplying by 100, and then formatting the result to the specified number of decimal
    places. It includes input validation to ensure that the denominator is not zero, the
    number of decimal places is not negative, and the user enters valid numbers."""
    while True:
        try:
            numerator = float(input("Enter the numerator: "))
            denominator = float(input("Enter the denominator: "))
            if denominator == 0:
                print("The denominator cannot be zero as any number \
                    \ndivided by zero is undefined. Please re-enter the values.")
                continue
            decimal_points = int(input("Enter the number of decimal points for formatting: "))
            if decimal_points < 0:
                print("The number of decimal points cannot be negative. Please re-enter the value.")
                continue
            percentage = (numerator / denominator) * 100
            formatted_percentage = f"{percentage:.{decimal_points}f}%"
            print(f"The percentage is: {formatted_percentage}")
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
        except OverflowError:
            print("Error: The result is too large to be represented.")


def days_until_july_4_2025():
    """This function calculates the difference in days between the current date and
    July 4, 2025. It assumes that today’s date is obtained using the system’s local
    timezone. The result can be negative if the current date is past July 4, 2025."""
    today = datetime.date.today()
    july_4_2025 = datetime.date(2025, 7, 4)
    days_until = (july_4_2025 - today).days
    print(f"Days from today until July 4, 2025: {days_until}")


def law_of_cosines():
    """This function prompts the user to enter the lengths of sides a and b, as well as
    the included angle C. It performs input validation to ensure that the side lengths
    are positive, the angle is positive and less than 180 degrees. It then calculates
    the length of side c using the law of cosines and prints the result."""
    while True:
        try:
            a = float(input("Enter the length of side a: "))
            b = float(input("Enter the length of side b: "))
            angle_c = float(input("Enter the angle C in degrees: "))

            if a <= 0 or b <= 0 or angle_c <= 0 or angle_c >= 180:
                print("Invalid input. Side lengths and angle must \
                    \nbe positive, and angle must be less than 180 degrees.")
                continue

            # Convert angle to radians
            angle_c = math.radians(angle_c)

            # Law of Cosines formula to solve for c
            c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(angle_c))
            print(f"The length of side c is: {c}")
            break

        except ValueError:
            print("Invalid input. Please enter a number.")
        except OverflowError:
            print("Error: The result is too large to be represented.")


def volume_of_cylinder():
    """This function prompts the user to enter the radius and height of a cylinder. Both the
    radius and height must be positive numbers. The function will continue to prompt the user
    until valid input is provided. The volume is then calculated using the formula: V = πr^2h,
    where V is the volume, r is the radius, and h is the height of the cylinder."""
    while True:
        try:
            radius = float(input("Enter the radius of the cylinder: "))
            height = float(input("Enter the height of the cylinder: "))
            if radius <= 0 or height <= 0:
                print("Invalid input. Radius and height must be positive numbers.")
                continue
            v = (math.pi * radius**2) * height
            print(f"The volume of the right circular cylinder is: {v}")
            break
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """This program provides a command line user interface allowing the user to select from
    the following options:
        - generating a secure password
        - calculating and formatting a percentage
        - finding out the number of days until July 4, 2025
        - using the Law of Cosines to calculate the leg of a triangle
        - calculating the volume of a Right Circular Cylinder
        - exiting the program

    Each option in the menu corresponds to a specific function that will be executed upon
    selection. The user is prompted to input any required parameters for the selected
    function. Input validation is performed to ensure the correctness of the input data.

    The application will continue to run until the user chooses to exit."""
    menu_options = {
        'a': generate_password,
        'b': calculate_percentage,
        'c': days_until_july_4_2025,
        'd': law_of_cosines,
        'e': volume_of_cylinder,
        'f': lambda: print("Exiting the program. \
            \nThank you for using this application, Goodbye."),
    }
    while True:
        print("\n*** Main Menu ***")
        print("a: Generate Secure Password")
        print("b: Calculate and Format a Percentage")
        print("c: How many days from today until July 4, 2025?")
        print("d: Use the Law of Cosines to calculate the leg of a triangle.")
        print("e: Calculate the volume of a Right Circular Cylinder")
        print("f: Exit program")
        choice = input("Enter your choice (a/b/c/d/e/f): ")

        if choice in menu_options:
            menu_options[choice]()
            if choice == 'f':
                break
        else:
            print("Invalid choice. Please enter a letter from a to f.")

if __name__ == "__main__":
    main()
