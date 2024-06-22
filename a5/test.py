from Profile import Profile, Post
from NaClProfile import NaClProfile

np = NaClProfile()
kp = np.generate_keypair()
np.save_profile("/Users/manush_murali/Documents/ICS32/a5/mass.dsu")

print("Open DSU file to check if message is encrypted.")

# Create a new NaClProfile object and load the dsu file.
np2 = NaClProfile()
np2.load_profile("/Users/manush_murali/Documents/ICS32/a5/mass.dsu")
# Import the keys
np2.import_keypair(kp)

