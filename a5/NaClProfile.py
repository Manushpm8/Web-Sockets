# Manush Murali
# mpmurali@uci.edu
# 14568752

# TODO: Install the pynacl library so that the following modules are available
# to your program.


# Class, Module, & Library Imports
import json, time, os
import nacl.utils
import nacl.secret
from nacl.public import PrivateKey, PublicKey, Box
from NaClDSEncoder import NaClDSEncoder
from nacl import encoding
from Profile import Profile
from Profile import Post
from Profile import DsuFileError
from Profile import DsuProfileError
from pathlib import Path



# TODO: Import the Profile and Post classes
# TODO: Import the NaClDSEncoder module
    
# TODO: Subclass the Profile class
"""
A subclass of Profile class that is responsible for generating profiles and ecrypting/decrypting posts in order to be saved in file or published online.
"""
class NaClProfile(Profile):
    def __init__(self):
        """
        TODO: Complete the initializer method. Your initializer should create the follow three 
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame 
        how you expect your class to be used though, so think it through.
        """
        self.public_key = ""
        self.private_key = ""
        self.keypair = ""
        super().__init__()
        global nacl_enc
        nacl_enc = NaClDSEncoder()
    
    """
    This function creates a keypair and sets it to the respective public and private key attributes.
    """
    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        TODO: Complete the generate_keypair method.

        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str    
        """
        nacl_enc = NaClDSEncoder()
        nacl_enc.generate()
        self.public_key = nacl_enc.public_key
        self.private_key = nacl_enc.private_key
        self.keypair = nacl_enc.keypair
        return self.keypair

    """
    This function loads and gets an already existing keypair and extracts a public and private key from it to set it to the respective class attributes.
    """
    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        TODO: Complete the import_keypair method.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer. 
        
        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        self.public_key = keypair[0:keypair.index("=") + 1]
        self.private_key = keypair[keypair.index("=") + 1:len(keypair)]
        self.keypair = keypair

    """
    This function encrypts and adds an entry to a file as a post.
    """
    def add_post(self, post: Post):
        """
        TODO: Override the add_post method to encrypt post entries.

        Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
        code that is already written in the parent class.

        NOTE: To call the method you are overriding as it exists in the parent class, you can use the built-in super keyword:
        
        super().add_post(...)
        """
        final_post = self.post_encrypter(str(post.get_entry()), nacl_enc.encode_public_key(self.public_key))
        post.set_entry(final_post)
        super().add_post(post)  

    """
    This function decrypts and gets all the entries of a file as posts.
    """
    def get_posts(self) -> list:
        """
        TODO: Override the get_posts method to decrypt post entries.

        Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
        decrypted before returning them to the calling code.

        :return: Post
        
        NOTE: To call the method you are overriding as it exists in the parent class you can use the built-in super keyword:
        super().get_posts()
        """
        posts = super().get_posts()
        result_posts = []
        for i in posts:
            final_post = self.post_decrypter(str(i.get_entry()), nacl_enc.encode_public_key(self.public_key))
            ts = i.get_time()
            post = Post()
            post.set_entry(final_post)
            post.set_time(ts)
            result_posts.append(post)
        return result_posts
    
    """
    This function loads an existing profile in order to print/edit it.
    """
    def load_profile(self, path: str) -> None:
        """
        TODO: Override the load_profile method to add support for storing a keypair.

        Since the DS Server is now making use of encryption keys rather than username/password attributes, you will 
        need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
        load_profile module and add any new attributes you wish to support.

        NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO. Just add
        support for your new attributes.
        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.keypair = obj['keypair']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    """
    This function encrypts an entry using the public key of the DS Server and the private key of an NaClProfile().
    """
    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.

        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post, 
        get_posts, and this method can call.
        
        :return: bytes 
        """ 
        publickey = nacl_enc.encode_public_key(public_key)
        final_post = self.post_encrypter(entry, publickey)
        return final_post.encode(encoding = "UTF-8")

    """
    This function encodes, encrypts, and then decodes decrypted entries.
    """
    def post_encrypter(self, entry:str, public_key:PublicKey) -> str:
        box_keys = Box(nacl_enc.encode_private_key(self.private_key), public_key)
        encoded_post = entry.encode(encoding = "UTF-8")
        encrypted_post = box_keys.encrypt(encoded_post, encoder = encoding.Base64Encoder)
        decoded_post = encrypted_post.decode(encoding = "UTF-8")
        return decoded_post

    """
    This function encodes, decrypts, and then decodes encrypted entries.
    """
    def post_decrypter(self, entry:str, public_key:PublicKey) -> str:
        box_keys = Box(nacl_enc.encode_private_key(self.private_key), public_key)
        encoded_post = entry.encode(encoding = "UTF-8")
        decrypted_message = box_keys.decrypt(encoded_post, encoder = encoding.Base64Encoder)
        decoded_post = decrypted_message.decode(encoding = "UTF-8")
        return decoded_post

    