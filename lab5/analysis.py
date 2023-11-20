"""
This module provides a user interface for loading and analyzing datasets.

It allows users to choose between two datasets: 'PopChange.csv' and 'Housing.csv'.
For the selected dataset, it performs statistical analysis and plots histograms 
for specified variables. The analysis includes count, mean, standard deviation, 
minimum, and maximum values of the chosen variables.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame


def load_data() -> None:
    """
    Prompt the user to choose a dataset to load and analyze.

    The function continues to prompt the user until they choose to exit.
    It handles invalid inputs by re-prompting the user. For valid inputs,
    it calls the analyze_and_plot function with the chosen dataset.
    """
    while True:
        choice = input("Which dataset would you like to load "
                       "(1 for PopChange, 2 for Housing, or 'exit' to quit)? ")

        if choice.lower() == 'exit':
            print("Exiting the program.")
            break

        if choice.isdigit() and choice in ['1', '2']:
            try:
                columns = []
                if choice == '1':
                    data_frame = pd.read_csv("PopChange.csv")
                    columns = ['Pop Apr 1', 'Pop Jul 1', 'Change Pop']
                elif choice == '2':
                    data_frame = pd.read_csv("Housing.csv")
                    columns = ['AGE', 'BEDRMS', 'BUILT', 'ROOMS', 'UTILITY']

                analyze_and_plot(data_frame, columns)

            except (FileNotFoundError, pd.errors.EmptyDataError,
                    pd.errors.ParserError, PermissionError) as err:
                print(f"Error reading file: {err}")
        else:
            print("Invalid choice. Please enter 1, 2, or 'exit'.")

def analyze_and_plot(data_frame: DataFrame, columns: list[str]) -> None:
    """
    Perform analysis and plot histograms for specified columns in the dataset.

    Parameters:
    data_frame (DataFrame): The dataset to analyze.
    columns (list[str]): A list of columns in the dataset to analyze.

    This function calculates and prints statistical data (count, mean, standard 
    deviation, min, and max) for each specified column and plots a histogram 
    for each of these columns.
    """
    for column in columns:
        try:
            data = data_frame[column].dropna()

            # Ensure data is numeric for statistical calculations
            if not pd.api.types.is_numeric_dtype(data):
                raise TypeError(f"Data in {column} is not numeric and cannot be analyzed.")

            # Check if the data column is empty
            if data.empty:
                raise ValueError(f"No data available in {column} for analysis.")

            print(f"\nStatistics for {column}:")
            print(f"Count: {len(data)}")
            print(f"Mean: {np.mean(data)}")
            print(f"Standard Deviation: {np.std(data)}")
            print(f"Min: {np.min(data)}")
            print(f"Max: {np.max(data)}")

            # Plotting the histogram
            plt.figure()
            plt.hist(data, bins='auto', color='blue', alpha=0.7)
            plt.title(f"Histogram of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.show()

        except (TypeError, ValueError) as err:
            print(f"Value Error: {err}")


if __name__ == "__main__":
    load_data()
