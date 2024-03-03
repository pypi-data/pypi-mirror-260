import unittest
from DotDotDee.DotDotDee import Danielley

class TestDDD(unittest.TestCase):
    def test_ddd_folder_not_found(self):
        current_dir = '/home/user/otherproject' 
        folder_name = 'myproject'
        expected = "From Dot-Dot-Dee: We couldn't find iDDD"
        try:
            Danielley.DDD(folder_name)
        except Exception as e:
            self.assertEqual(expected, str(e))

    def test_ddd_windows_path(self):
        current_dir = 'C:\\Users\\user\\projects\\myproject'
        folder_name = 'myproject'
        expected = 'C:\\Users\\user'
        result = Danielley.DDD(folder_name)
        self.assertEqual(expected, result)