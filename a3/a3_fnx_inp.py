# Manush Murali
# mpmurali@uci.edu
# 14568752


# Module Imports
import Profile

# Input Statement Functions
# Input Choice Statements
def choice_command():
    print("\n\n\nHello! Would you like to post your information to your file system or to our server on the internet?\n")
    print("File System: \"F\"")
    print("Internet Server: \"I\"")

# File Input Statements
def file_input_command():
    print("\nWelcome to the ICS Journal Editor!\n")
    print("Select a Command:-")
    print("Create a Profile: \"C\"")
    print("Open a Profile: \"O\"")
    print("Quit Program: \"Q\"")
    print("Admin Mode: \"admin\"\n")

# Internet Input Statements:
def internet_input_command():
    print("\nWelcome to the DS Server Editor!\n")
    print("Please provide a Server IP:-")

# Profile Input Statements
def profile_input_command():
    print("\nChoose and enter one of the following:-")
    print("Join the DS Server as a new profile: \"N\"")
    print("Join the DS Server as an existing profile: \"E\"")
    print("Update/Add a bio to your profile: \"B\"") 
    

# Post Input Statements
def post_input_command():
    print("\nWould you like to post on the DS Server?")
    print("Yes/No")

# E Command Input Statements
def E_command():
    print("Choose Your Command:- \n")
    print("Edit - \"E\"")
    print(" Change Username: \"-usr\"")
    print(" Change Password: \"-pwd\"")
    print(" Change Bio: \"-bio\"")
    print(" Add Post: \"-addpost\"")
    print(" Delete Post: \"-delpost\"\n")

# P Command Input Statements
def P_command():
    print("Print - \"P\"")
    print(" Print Username: \"-usr\"")
    print(" Print Password: \"-pwd\"")
    print(" Print Bio: \"-bio\"")
    print(" All Posts \"-posts\"")
    print(" One Post: \"-post [ID]\"")
    print(" All Information: \"-all\"\n") 
 