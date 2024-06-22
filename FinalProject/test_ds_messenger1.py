# Manush Murali
# mpmurali@uci.edu
# 14568752

# Shreyas V Chandramouli
# svchand1@uci.edu
# 70688884



# Class Imports
from ds_messenger import DirectMessage, DirectMessenger



directMessageobject = DirectMessage(recipient="kungfupanda345",message="Hello world")

print(directMessageobject.get_recipient())

print(directMessageobject.get_message())

directMessengerObject = DirectMessenger(dsuserver=None, username="kungfupanda345", password="passwordpanda")

return_val = directMessengerObject.send(message="Hello guys i am back", recipient="kungfupanda929292929")

print(return_val)



directMessengerObject2 = DirectMessenger(dsuserver=None, username="kungfupanda929292929", password="passwordpanda345")

retrieve_new_return_value  = directMessengerObject2.retrieve_new()

for i in retrieve_new_return_value:
    print(i.get_message())

retrieve_all_return_value = directMessengerObject2.retrieve_all()

for i in retrieve_new_return_value:
    print(i.get_message())