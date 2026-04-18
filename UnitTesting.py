import unittest
from Elite102BankingApp import validate_withdrawal

class TestingFunctions(unittest.TestCase):
    def test_negative_withdrawal(self):
        #if the amount is less than 0, then it should return negative
        self.assertEqual(validate_withdrawal(-10,100), "Negative Number")

    def test_valid_withdrawal(self):
        #the amount is valid, so it should return that it's okay
        self.assertEqual(validate_withdrawal(200,1000), "Valid Withdrawal")
    def test_insufficient(self):
        #the amount is greater than the balance
        self.assertEqual(validate_withdrawal(2000,1000), "Insufficient Funds")

if __name__ == "__main__": #it only runs this file directly, not the other imported files
    unittest.main()

'''Reference
def validate_withdrawal(amount, current_balance):
                        #amount it's withdrawing
                        #the total balance after withdrawing
'''