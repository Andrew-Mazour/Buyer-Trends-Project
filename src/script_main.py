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
                row['Purchase Amount'] = float(row['Purchase Amount'])
            except ValueError:
                print(f"Invalid purchase amount '{row['Purchase Amount']}' found. Setting it to 0.0.")
                row['Purchase Amount'] = 0.0


class PurchaseAnalysis:
    def __init__(self, historical_data, current_data):
        self.historical_data = historical_data
        self.current_data = current_data

    def compare_buyers(self):
        # Sets storing old and current ID's.
        historical_buyers = {row['ID'] for row in self.historical_data}
        current_buyers = {row['ID'] for row in self.current_data}

        new_buyers = current_buyers - historical_buyers  # Leaves buyers that have not bought before.
        stopped_buyers = historical_buyers - current_buyers  # Leaves buyers that have not bought again.

        return new_buyers, stopped_buyers

    def compare_purchases(self):
        # Dictionaries storing ID's as keys and the rest of the row a value.
        # Ex. {1:{*enter rest of row as dictionary*}}
        historical_dict = {row['ID']: row for row in self.historical_data}
        current_dict = {row['ID']: row for row in self.current_data}

        increased_purchases = []
        decreased_purchases = []

        for customer_id in current_dict:
            if customer_id in historical_dict:
                historical_amount = historical_dict[customer_id]['Purchase Amount']
                current_amount = current_dict[customer_id]['Purchase Amount']
                if current_amount > historical_amount:
                    # Adding tuple containing customer_id, historical_amount, current_amount to increased list.
                    increased_purchases.append((customer_id, historical_amount, current_amount))
                elif current_amount < historical_amount:
                    # Adding tuple containing customer_id, historical_amount, current_amount to decreased list.
                    decreased_purchases.append((customer_id, historical_amount, current_amount))

        return increased_purchases, decreased_purchases


class AnalyzeTrends:
    def __init__(self, data):
        # ALL data (both files combined).
        self.data = data

    def analyze_trends(self):
        monthly_purchases = defaultdict(float)
        for row in self.data:
            date = row['Purchase Date']
            month = date[:7]  # Extract YYYY-MM from YYYY-MM-DD
            # Keeping track of purchase amount for stated month in monthly_purchases dictionary.
            monthly_purchases[month] += row['Purchase Amount']
        # Sorted dictionary by YYYY-MM (earliest to latest).
        sorted_trends = sorted(monthly_purchases.items())
        return sorted_trends


class CreateReport:
    def __init__(self, new_buyers, stopped_buyers, increased_purchases, decreased_purchases, trends):
        self.new_buyers = new_buyers
        self.stopped_buyers = stopped_buyers
        self.increased_purchases = increased_purchases
        self.decreased_purchases = decreased_purchases
        self.trends = trends

    def create_report(self):
        print("New Buyers:")
        for buyer in self.new_buyers:
            print(buyer)

        print("\nStopped Buyers:")
        for buyer in self.stopped_buyers:
            print(buyer)

        print("\nIncreased Purchases:")
        for customer_id, old_amount, new_amount in self.increased_purchases:
            print(f"Customer ID: {customer_id}, Old Amount: {old_amount}, New Amount: {new_amount}")

        print("\nDecreased Purchases:")
        for customer_id, old_amount, new_amount in self.decreased_purchases:
            print(f"Customer ID: {customer_id}, Old Amount: {old_amount}, New Amount: {new_amount}")

        print("\nMonthly Purchasing Trends:")
        for month, total in self.trends:
            print(f"Month: {month}, Total Purchases: {total}")


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

        # First instance of PurchaseAnalysis class, comparing buyers and purchases of historical and current buyers.
        analysis = PurchaseAnalysis(instance_historical.data, instance_current.data)
        new_buyers, stopped_buyers = analysis.compare_buyers()
        increased_purchases, decreased_purchases = analysis.compare_purchases()

        # First instance of AnalyzeTrends class, showing total purchases per month (adding historical and current data).
        trends = AnalyzeTrends(instance_historical.data + instance_current.data).analyze_trends()

        # First instance of CreateReport class, generating report based on previously determined variables.
        instance_report = CreateReport(new_buyers, stopped_buyers, increased_purchases, decreased_purchases, trends)
        instance_report.create_report()

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
    
