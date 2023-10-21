#!/usr/bin/env python3
import unittest
from datetime import datetime
from models import mail

class TestEmail(unittest.TestCase):

    def setUp(self):
        # Set up test data
        self.params = {
            "email": "test2@example.com",
            "name": "John Fille",
            "subject": "Test Email",
            "time": datetime.now(),
            "message": "This is a test email",
        }
    
    def test_send_email(self):
        # Test Email object creation and send
        response = mail.send(4, self.params)
        self.assertEqual(response["message"], "Email sent")
