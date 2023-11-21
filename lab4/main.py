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
This module provides functionality for validating phone numbers and zip codes,
performing various matrix operations using NumPy, and running an interactive
matrix application.

It uses regular expressions for validation and NumPy for matrix operations.
The main application allows users to input matrices and perform operations
like addition, subtraction, and multiplication.
"""

import re
import numpy as np


def validate_phone_number(number):
    """
    Validate a phone number format.

    Args:
        number (str): The phone number to validate.

    Returns:
        bool: True if the phone number matches the XXX-XXX-XXXX format, False otherwise.
    """
    pattern = re.compile(r"^\d{3}-\d{3}-\d{4}$")
    return pattern.match(number) is not None


def validate_zip_code(zipcode):
    """
    Validate a zip code format.

    Args:
        zipcode (str): The zip code to validate.

    Returns:
        bool: True if the zip code matches the XXXXX-XXXX format, False otherwise.
    """
    pattern = re.compile(r"^\d{5}-\d{4}$")
    return pattern.match(zipcode) is not None


def get_matrix():
    """
    Prompt the user to input a 3x3 matrix, space-separated.

    Continuously prompts the user until a valid 3x3 numeric matrix is entered.

    Returns:
        numpy.ndarray: A 3x3 matrix entered by the user.
    """
    while True:
        try:
            print("Enter your 3x3 matrix (row by row, space-separated):")
            matrix = np.array([input().split() for _ in range(3)], dtype=float)
            if matrix.shape != (3, 3):
                raise ValueError
            return matrix
        except ValueError:
            print("Invalid matrix. Please enter a 3x3 numeric matrix.")


def matrix_operations(a, b):
    """
    Perform matrix operations on two given matrices.

    Args:
        a (numpy.ndarray): The first matrix.
        b (numpy.ndarray): The second matrix.

    Returns:
        numpy.ndarray: The result of the selected matrix operation.
    """
    while True:
        try:
            print("Select a Matrix Operation from the list below:")
            print(
                "a. Addition\
                \nb. Subtraction\
                \nc. Matrix Multiplication\
                \nd. Element by element multiplication"
            )
            choice = input().strip().lower()

            if choice == "a":
                return a + b
            if choice == "b":
                return a - b
            if choice == "c":
                return np.matmul(a, b)
            if choice == "d":
                return np.multiply(a, b)

            raise ValueError("Invalid choice. Please select a valid operation.")
        except ValueError as e:
            print(e)


def main():
    """
    Main function to run the matrix application.

    This function runs an interactive loop for the user to
    play with matrix operations.

    It includes validation of phone numbers and zip codes,
    matrix input, and performing matrix operations.
    """
    while True:
        print("***************** Welcome to the Python Matrix Application ***********")
        if (
            input("Do you want to play the Matrix Game? Enter Y for Yes or N for No: ")
            .strip()
            .upper()
            != "Y"
        ):
            break

        phone = input("Enter your phone number (XXX-XXX-XXXX): ")
        while not validate_phone_number(phone):
            phone = input(
                "Your phone number is not in correct format. Please re-enter: "
            )

        zipcode = input("Enter your zip code+4 (XXXXX-XXXX): ")
        while not validate_zip_code(zipcode):
            zipcode = input("Your zip code is not in correct format. Please re-enter: ")

        try:
            matrix1 = get_matrix()
            matrix2 = get_matrix()
            result = matrix_operations(matrix1, matrix2)
            print("The results are:\n", result)
            print("The Transpose is:\n", np.transpose(result))
            print("The row mean values of the results are:\n", np.mean(result, axis=1))
            print("The column mean values of the results are:\n", np.mean(result, axis=0))
        except ValueError as e:
            print("Value Error: ", e)
        except TypeError as e:
            print("Type Error: ", e)
            continue

        print("*********** Thanks for playing Python Numpy ***************")


if __name__ == "__main__":
    main()
