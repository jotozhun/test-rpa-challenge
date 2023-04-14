import unittest

from utils.utils import find_dollar_ocurrence

class DollarPatternTest(unittest.TestCase):

    def setUp(self):
        """
        Prepares initial data to perform tests
        """
        self.ideal_patterns = ["$11.1",
                               "$111,111.11",
                               "11 dollars",
                               "11 USD"]
        self.phrases_without_patterns = ["Hey dear reviewer",
                                        "How you doing?",
                                        "I hope you like this unit tests."]
        self.phrases_with_patterns = ["I need $1 to buy ice cream",
                                      "2 dollars to buy two ice creams",
                                      "and 350 USD to pay rent lol"]

    def test_ideal_dollar_patterns(self):
        """
        This test checks phrases with only money amounts
        """
        for ideal_pattern in self.ideal_patterns:
            self.assertTrue(find_dollar_ocurrence(ideal_pattern))


    def test_phrases_with_dollar_patterns(self):
        """
        This test is more complex since it checks a real frase with
        any amount of money
        """
        for phrase in self.phrases_with_patterns:
            self.assertTrue(find_dollar_ocurrence(phrase))


    def test_phrases_to_fail_on_find_dollar_pattern(self):
        """
        This test is to fail when the phrase does not contain any
        amount of money
        """
        for phrase in self.phrases_without_patterns:
            self.assertFalse(find_dollar_ocurrence(phrase))
