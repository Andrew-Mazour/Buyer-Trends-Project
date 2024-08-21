import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from GitHub.CharityProject.src.script_main import SetUpCSV, PurchaseAnalysis, AnalyzeTrends, CreateReport


class TestSetUpCSV(unittest.TestCase):

    def test_read_csv_file_not_found(self):
        checker = SetUpCSV("test_fake.csv")
        with self.assertRaises(FileNotFoundError):
            checker.read_csv()

    # @patch mimics actual files using testing data provided.
    @patch("builtins.open", new_callable=mock_open, read_data="ID,Buyer Name,Purchase Amount,Purchase Date"
                                                              "\n1,100.50,2024-01-15"
                                                              "\n2,200.00,2024-02-20"
                                                              "\n3,invalid_amount,2024-03-25\n")
    @patch("os.path.exists", return_value=True)  # Ensure file path works using @patch
    def test_read_csv(self, mock_exists, mock_file):
        checker = SetUpCSV("test.csv")
        checker.read_csv()
        # Ensures length of data is 4 (3 indices).
        self.assertEqual(len(checker.data), 3)
        # Ensures order is correct, starting with ID 1 (strips whitespaces).
        self.assertEqual(checker.data[0]['ID'].strip(), '1')

    @patch("builtins.open", new_callable=mock_open, read_data="ID,Buyer Name,Purchase Amount,Purchase Date"
                                                              "\n1,100.50,2024-01-15"
                                                              "\n2,200.00,2024-02-20"
                                                              "\n3,invalid_amount,2024-03-25\n")
    @patch("os.path.exists", return_value=True)  # Ensure file path works using @patch
    def test_convert_data(self, mock_exists, mock_file):
        checker = SetUpCSV("test.csv")
        checker.read_csv()
        checker.convert_data()
        # Check that purchase amounts have been converted to floats.
        self.assertEqual(checker.data[2]['Donation Amount'], 0.0)
        self.assertEqual(checker.data[0]['Donation Amount'], 100.50)


class TestPurchaseAnalysis(unittest.TestCase):

    def setUp(self):
        # Create sample historical and current data.
        self.historical_data = [
            {"ID": "1", "Purchase Amount": 100.50},
            {"ID": "2", "Purchase Amount": 200.00}
        ]
        self.current_data = [
            {"ID": "2", "Purchase Amount": 250.00},
            {"ID": "3", "Purchase Amount": 300.00}
        ]
        # Setting analysis instance from script_main to use new sample data.
        self.analysis = PurchaseAnalysis(self.historical_data, self.current_data)

    def test_compare_buyers(self):
        # Find new and stopped buyers based on sample data (testing compare_buyers() function).
        new_buyers, stopped_buyers = self.analysis.compare_buyers()
        self.assertEqual(new_buyers, {"3"})
        self.assertEqual(stopped_buyers, {"1"})

    def test_compare_purchases(self):
        # Find increased and decreased purchases based on sample data (testing compare_purchases() function).
        increased_purchases, decreased_purchases = self.analysis.compare_purchases()
        self.assertEqual(len(increased_purchases), 1)  # One consistent buyer that increased purchases.
        self.assertEqual(len(decreased_purchases), 0)  # No buyers decreased purchases.
        # Expected tuple containing: (buyer_id, historical_amount, current_amount).
        self.assertEqual(increased_purchases[0], ("2", 200.00, 250.00))


class TestAnalyzeTrends(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"ID": "1", "Purchase Amount": 100.50, "Purchase Date": "2024-01-15"},
            {"ID": "2", "Purchase Amount": 200.00, "Purchase Date": "2024-02-20"},
            {"ID": "3", "Purchase Amount": 300.00, "Purchase Date": "2024-03-25"}
        ]
        self.trend_analysis = AnalyzeTrends(self.data)

    def test_analyze_trends(self):
        # Test analyze_trends() function using sample data.
        trends = self.trend_analysis.analyze_trends()
        expected_trends = [("2024-01", 100.50), ("2024-02", 200.00), ("2024-03", 300.00)]
        self.assertEqual(trends, expected_trends)


class TestCreateReport(unittest.TestCase):

    def setUp(self):
        self.new_buyers = {"3"}
        self.stopped_buyers = {"1"}
        self.increased_purchases = [("2", 200.00, 250.00)]
        self.decreased_purchases = []
        self.trends = [("2024-01", 100.50), ("2024-02", 200.00), ("2024-03", 300.00)]

        self.report_creator = CreateReport(
            self.new_buyers, self.stopped_buyers,
            self.increased_purchases, self.decreased_purchases,
            self.trends
        )

    #  Replaces the standard output stream with a StringIO object to capture any output generated.
    #  by the create_report() method.
    @patch('sys.stdout', new_callable=StringIO)
    def test_create_report(self, mock_stdout):
        # Testing create_report() on sample data.
        self.report_creator.create_report()
        output = mock_stdout.getvalue()  # Retrieves the captured output from the StringIO object.
        # All test below ensure the create_report() function contains string and output.
        self.assertIn("New Buyers:", output)
        self.assertIn("Stopped Buyers:", output)
        self.assertIn("Increased Purchases:", output)
        self.assertIn("Monthly Purchasing Trends:", output)


if __name__ == '__main__':
    unittest.main()
