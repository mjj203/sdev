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
    datasets = {
        '1': ('PopChange.csv', ['Pop Apr 1', 'Pop Jul 1', 'Change Pop']),
        '2': ('Housing.csv', ['AGE', 'BEDRMS', 'BUILT', 'ROOMS', 'UTILITY'])
    }

    while True:
        choice = input("Which dataset would you like to load "
                       "(1 for PopChange, 2 for Housing, or 'exit' to quit)? ").lower()

        if choice == 'exit':
            print("Exiting the program.")
            break

        dataset_info = datasets.get(choice)
        if dataset_info:
            try:
                data_frame = pd.read_csv(dataset_info[0])
                analyze_and_plot(data_frame, dataset_info[1])
            except (FileNotFoundError, pd.errors.EmptyDataError,
                    pd.errors.ParserError, PermissionError) as err:
                print(f"Error reading file: {err}")
        else:
            print("Invalid choice. Please enter 1, 2, or 'exit'.")


def validate_data(data_frame: DataFrame, column: str) -> pd.Series:
    """
    Validate if the data in the column is numeric and not empty.

    Parameters:
    data_frame (DataFrame): The dataset to validate.
    column (str): The column name to validate.

    Returns:
    pd.Series: The validated data for the column.

    Raises:
    TypeError: If data in column is not numeric.
    ValueError: If the column has no data.
    """
    data = data_frame[column].dropna()
    if not pd.api.types.is_numeric_dtype(data):
        raise TypeError(f"Data in {column} is not numeric and cannot be analyzed.")
    if data.empty:
        raise ValueError(f"No data available in {column} for analysis.")
    return data


def calculate_statistics(data: pd.Series) -> None:
    """
    Calculate and print statistics for the data.

    Parameters:
    data (pd.Series): The data to calculate statistics on.
    """
    print(f"Count: {len(data)}")
    print(f"Mean: {np.mean(data)}")
    print(f"Standard Deviation: {np.std(data, ddof=1)}")  # Using sample standard deviation
    print(f"Min: {np.min(data)}")
    print(f"Max: {np.max(data)}")


def plot_histogram(data: pd.Series, column: str) -> None:
    """
    Plot a histogram for the data.

    Parameters:
    data (pd.Series): The data to plot.
    column (str): The column name for labeling the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins='auto', color='skyblue', alpha=0.7, edgecolor='black')
    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()


def analyze_and_plot(data_frame: DataFrame, columns: list[str]) -> None:
    """
    Perform analysis and plot histograms for specified columns in the dataset.

    Parameters:
    data_frame (DataFrame): The dataset to analyze.
    columns (list[str]): A list of columns in the dataset to analyze.
    """
    for column in columns:
        try:
            data = validate_data(data_frame, column)
            print(f"\nStatistics for {column}:")
            calculate_statistics(data)
            plot_histogram(data, column)
        except (TypeError, ValueError) as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    load_data()
