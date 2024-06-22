# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884



# Class Imports
import unittest
from ds_protocol import *
import sys

class TestDsProtocol(unittest.TestCase):


    def test_join_test(self):
        join_msg = join_command("168.235.86.101", 3021,"randomrandomrandomrandomrandomtestuser345", "randomrandomrandomrandomrandomtestuser")
        token = join_msg[0].response['token']
        self.assertEqual(len(token),36)
        self.assertEqual(join_msg[0].response["type"], "ok")


    def test_directmessage_test(self):
        join_msg = join_command("168.235.86.101", 3021,"randomrandomrandomrandomrandomtestuser345", "randomrandomrandomrandomrandomtestuser")
        token = join_msg[0].response['token']
        sent_message = directmessage_command("168.235.86.101",3021, "randomrandomrandomrandomrandomtestuser", "randomrandomrandomrandomrandomtestuser", token, "Hello", "himark")
        self.assertEqual(sent_message.response['type'],"ok")


    def test_request_unread_messages_test(self):
        join_msg = join_command("168.235.86.101", 3021,"randomrandomrandomrandomrandomtestuser345", "randomrandomrandomrandomrandomtestuser")
        token = join_msg[0].response['token']
        request_message_unread = unreadmessages_command("168.235.86.101",3021, "randomrandomrandomrandomrandomtestuser", "randomrandomrandomrandomrandomtestuser",token)
        self.assertEqual(request_message_unread.response['type'],"ok")
        

    def test_request_all_message_test(self):
        join_msg = join_command("168.235.86.101", 3021,"randomrandomrandomrandomrandomtestuser", "randomrandomrandomrandomrandomtestuser")
        token = join_msg[0].response['token']
        request_message_all = allmessages_command("168.235.86.101",3021, "randomrandomrandomrandomrandomtestuser", "randomrandomrandomrandomrandomtestuser",token)
        self.assertEqual(request_message_all.response['type'],"ok")






if __name__ == '__main__':
    unittest.main()



