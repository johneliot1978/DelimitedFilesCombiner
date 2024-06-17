# Description: command line python script to consolidates multiple files of a specified extension and any delimiter in the current directory into a single file with whatever delimiter you specify
import os
import pandas as pd
from io import StringIO
import argparse
import csv  # Add this import statement

def combine_csv_files(input_extension, input_delimiter, output_delimiter):
    # Get a list of all CSV files in the current directory with the specified extension
    csv_files = [file for file in os.listdir() if file.endswith(input_extension) and not file.startswith('csv_combined')]


    # Check if there are any CSV files
    if len(csv_files) == 0:
        print(f"No {input_extension} files found in the current directory.")
        exit()

    # Initialize total_rows with the number of header rows present in the input files
    total_rows = 0  # Updated initialization

    # Read and combine CSV files
    dfs = []
    for file in csv_files:
        print(f"Processing file: {file}")  # Debug message to show progress
        try:
            # Specify delimiter and treat all columns as strings
            df = pd.read_csv(file, delimiter=input_delimiter, dtype=str)
            dfs.append(df)
            total_rows += len(df)  # Counting all rows including the header row
        except pd.errors.ParserError as e:
            print(f"Error parsing file '{file}': {e}")
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    try:
                        pd.read_csv(StringIO(line))
                    except pd.errors.ParserError:
                        print(f"Skipped line {i+1} in file '{file}' due to parsing error.")
                        break

    # Combine all dataframes into one
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)

        # Extract input file extension and use it for output file
        output_extension = input_extension

        # Write the combined dataframe to a new CSV file with user-specified delimiter
        combined_df.to_csv(f'csv_combined{output_extension}', index=False, sep=output_delimiter, quoting=csv.QUOTE_NONE, escapechar='\\')


        # Count total rows excluding header rows
        print(f"CSV files successfully combined. Output file: csv_combined{output_extension}")
        print(f"Total rows combined: {total_rows}")
    else:
        print("No valid CSV files found to combine.")

if __name__ == "__main__":
    # Description of the script's purpose and functionality
    script_description = (
        "This script combines multiple files with any uniform delimiter in the current directory into a single file with the delimiter of your choice.\n"
    )

    # Initialize argument parser
    parser = argparse.ArgumentParser(description=script_description)

    # Add argument for file extension
    parser.add_argument("input_extension", help="Extension of the files to be processed (e.g., csv, txt, tsv)", metavar="input_extension")

    # Parse command line arguments
    args = parser.parse_args()

    # Check if the provided extension starts with a dot, if not, add it
    if not args.input_extension.startswith("."):
        args.input_extension = "." + args.input_extension

    # Prompt user for input file delimiter
    input_delimiter = input("Enter the delimiter character used in input files (e.g., comma, tab, etc..): ")

    # Prompt user for output file delimiter
    output_delimiter = input("Enter the delimiter character for the output file (e.g., comma, tab, etc..): ")

    # Combine CSV files using the specified extension and delimiters
    combine_csv_files(args.input_extension, input_delimiter, output_delimiter)
