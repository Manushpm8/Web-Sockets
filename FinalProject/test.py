from ds_messenger import *

dsm = DirectMessenger(dsuserver=None, username="Sped", password="Sped123")
return_val = dsm.send(message="Hello guys i am back", recipient="Bonasantamurali")
print(return_val)