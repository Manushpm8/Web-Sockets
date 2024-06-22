# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884



# Class Imports
import json
import ds_protocol
import time

# Test Variable Values
username = "Singham123"
password = "starship13"
user_token = "qwertyuiop123asdfghjkl456zxcvbnm7890"
message = "I love ICS 32"
recipient = "Professor"
timestamp = time.time()


print("\n")

# join_command()
print("join_command() Functionality:-")
c = ds_protocol.join_command(username, password)
print(c)

print("\n")

# directmessage_command()
print("directmessage_command() Functionality:-")
d = ds_protocol.directmessage_command(user_token, message, recipient, timestamp)
print(d)

print("\n")

# unreadmessages_command()
print("unreadmessages_command() Functionality:-")
e = ds_protocol.unreadmessages_command(user_token)
print(e)

print("\n")

# allmessages_command()
print("allmessages_command() Functionality:-")
f = ds_protocol.allmessages_command(user_token)
print(f)

print("\n")




