import csv
import os
from collections import defaultdict


class SetUpCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def read_csv(self):
        # If file path does not exist.
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found.")
        try:
            with open(self.file_path, mode='r') as file:
                # Turn CSV into dictionary using DictReader.
                reader = csv.DictReader(file)
                for row in reader:
                    self.data.append(row)
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")

    def convert_data(self):
        for row in self.data:
            # Data must be read as floats to perform calculations.
            try:
                row['Donation Amount'] = float(row['Donation Amount'])
            except ValueError:
                print(f"Invalid donation amount '{row['Donation Amount']}' found. Setting it to 0.0.")
                row['Donation Amount'] = 0.0


class DonorAnalysis:
    def __init__(self, historical_data, current_data):
        self.historical_data = historical_data
        self.current_data = current_data

    def compare_donors(self):
        # Sets storing old and current ID's.
        historical_donors = {row['ID'] for row in self.historical_data}
        current_donors = {row['ID'] for row in self.current_data}

        new_donors = current_donors - historical_donors  # Leaves donors that have not donated before.
        stopped_donors = historical_donors - current_donors  # Leaves donors that have not donated again.

        return new_donors, stopped_donors

    def compare_donations(self):
        # Dictionaries storing ID's as keys and the rest of the row a value.
        # Ex. {1:{*enter rest of row as dictionary*}}
        historical_dict = {row['ID']: row for row in self.historical_data}
        current_dict = {row['ID']: row for row in self.current_data}

        increased_donations = []
        decreased_donations = []

        for donor_id in current_dict:
            if donor_id in historical_dict:
                historical_amount = historical_dict[donor_id]['Donation Amount']
                current_amount = current_dict[donor_id]['Donation Amount']
                if current_amount > historical_amount:
                    # Adding tuple containing donor_id, historical_amount, current_amount to increased list.
                    increased_donations.append((donor_id, historical_amount, current_amount))
                elif current_amount < historical_amount:
                    # Adding tuple containing donor_id, historical_amount, current_amount to decreased list.
                    decreased_donations.append((donor_id, historical_amount, current_amount))

        return increased_donations, decreased_donations


class AnalyzeTrends:
    def __init__(self, data):
        # ALL data (both files combined).
        self.data = data

    def analyze_trends(self):
        monthly_donations = defaultdict(float)
        for row in self.data:
            date = row['Donation Date']
            month = date[:7]  # Extract YYYY-MM from YYYY-MM-DD
            # Keeping track of donation amount for stated month in monthly_donations dictionary.
            monthly_donations[month] += row['Donation Amount']
        # Sorted dictionary by YYYY-MM (earliest to latest).
        sorted_trends = sorted(monthly_donations.items())
        return sorted_trends


class CreateReport:
    def __init__(self, new_donors, stopped_donors, increased_donations, decreased_donations, trends):
        self.new_donors = new_donors
        self.stopped_donors = stopped_donors
        self.increased_donations = increased_donations
        self.decreased_donations = decreased_donations
        self.trends = trends

    def create_report(self):
        print("New Donors:")
        for donor in self.new_donors:
            print(donor)

        print("\nStopped Donors:")
        for donor in self.stopped_donors:
            print(donor)

        print("\nIncreased Donations:")
        for donor_id, old_amount, new_amount in self.increased_donations:
            print(f"Donor ID: {donor_id}, Old Amount: {old_amount}, New Amount: {new_amount}")

        print("\nDecreased Donations:")
        for donor_id, old_amount, new_amount in self.decreased_donations:
            print(f"Donor ID: {donor_id}, Old Amount: {old_amount}, New Amount: {new_amount}")

        print("\nMonthly Donation Trends:")
        for month, total in self.trends:
            print(f"Month: {month}, Total Donations: {total}")


def main():
    historical_file = '../data/SampleHistoricalFile.csv'
    current_file = '../data/SampleCurrentFile.csv'

    try:
        # First instance of SetUpCSV class using historical file (read and clean data).
        instance_historical = SetUpCSV(historical_file)
        instance_historical.read_csv()
        instance_historical.convert_data()

        # Second instance of SetUpCSV class using current file (read and clean data).
        instance_current = SetUpCSV(current_file)
        instance_current.read_csv()
        instance_current.convert_data()

        # First instance of DonorAnalysis class, comparing donors and donations of historical and current donors.
        analysis = DonorAnalysis(instance_historical.data, instance_current.data)
        new_donors, stopped_donors = analysis.compare_donors()
        increased_donations, decreased_donations = analysis.compare_donations()

        # First instance of AnalyzeTrends class, showing total donations per month (adding historical and current data).
        trends = AnalyzeTrends(instance_historical.data + instance_current.data).analyze_trends()

        # First instance of CreateReport class, generating report based on previously determined variables.
        instance_report = CreateReport(new_donors, stopped_donors, increased_donations, decreased_donations, trends)
        instance_report.create_report()

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
    