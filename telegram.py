
import unittest
import telegram

class TestTelegram(unittest.TestCase):

    def test_add_user(self):
        # Normal case
        user = {'name': 'John', 'id': 1}
        telegram.add_user(user)
        self.assertIn(user, telegram.users)
        
        # Edge case - no name
        user = {'id': 2}
        with self.assertRaises(ValueError):
            telegram.add_user(user)
            
        # Edge case - duplicate id 
        user = {'name': 'Jane', 'id': 1}
        with self.assertRaises(ValueError):
            telegram.add_user(user)
            
