# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884



# Class Imports
import unittest
from ds_messenger import *
import sys

class TestDsProtocol(unittest.TestCase):

# randomrandomrandomrandomrandomtestuser
    def test_send(self):
        direct_msg_obj = DirectMessenger("168.235.86.101","randomrandomrandomrandomrandomtestuser345","randomrandomrandomrandomrandomtestuser")
        direct_msg_obj = direct_msg_obj.send(message="Hello world",recipient="Hellopaaji")
        self.assertEqual(direct_msg_obj,True)

    def test_retrieve_new(self):
        direct_msg_obj = DirectMessenger("168.235.86.101","randomrandomrandomrandomrandomtestuser345","randomrandomrandomrandomrandomtestuser")
        lists = direct_msg_obj.retrieve_new()
        self.assertEqual(type(lists),type([]))

    def test_retrieve_all(self):
        direct_msg_obj = DirectMessenger("168.235.86.101","randomrandomrandomrandomrandomtestuser345","randomrandomrandomrandomrandomtestuser")
        lists = direct_msg_obj.retrieve_new()
        self.assertEqual(type(lists),type([]))


if __name__ == '__main__':
    unittest.main()

















