import unittest
import pandas as pd
from qe import qe

class TestQe(unittest.TestCase):
    def test_open_in_excel(self):
        # Create a simple dataframe
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        # Use the package function to open it in Excel
        # Assuming the function is qe.open_in_excel
        success = qe.qe(df)

        # Check if the operation was successful
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()