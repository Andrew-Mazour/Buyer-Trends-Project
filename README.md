# Charity Donation Analysis Tool

## Description
This Python script compares and analyzes charity donation data from two CSV files: historical and current data. It reads and processes the CSV files, identifies new and stopped donors, compares donation amounts, and analyzes monthly donation trends. The script then generates a comprehensive report based on these analyses. This tool is ideal for charity organizations looking to understand donation patterns and donor behavior over time.

## Structure
- **src/**: Contains the main Python script for analyzing the CSV data.
  - `script_main.py`: The main script that handles reading, comparing, analyzing, and reporting on the CSV data.

- **tests/**: Contains unit tests for validating the functionality of the scripts.
  - `test_script_main.py`: Unit tests for the functions and methods in `CharityDonationAnalysis.py`.

- **data/**: Contains sample CSV files used for testing and demonstration.
  - `SampleHistoricalFile.csv`: Example of a historical CSV file for comparison.
  - `SampleCurrentFile.csv`: Example of a current CSV file for comparison.

- **README.md**: Provides a description of the project and information about the repository.

## Running the Tests
To run the tests, navigate to the `tests/` directory and run the following command:

```bash
python -m unittest test_script_main.py
"# CharityProject" 
