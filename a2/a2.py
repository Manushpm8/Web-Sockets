# Manush Murali
# mpmurali@uci.edu
# 14568752


# Class Imports
from pathlib import Path
import os
import json
import Profile
import a2_fnx_inp


# Profile Creator Function
# This function creates and saves a profile in the same directory as the python file according to the information provided by the user.
def profile_creator():
    usr = input("Please provide a username: ")
    pwd = input("Please provide a password: ")
    bio = input("Please provide a bio on yourself: ")
    global profile
    profile = Profile.Profile(username = usr, password = pwd)
    profile.bio = bio
    profile.save_profile(p)

# Recursive Functions
# These functions list the files of a directory according to the paremtrical information provided by the user.
def rec(a):
    # -r Command
    if (len(x) == 3):
        for i in a.iterdir():
            if (i.is_file() == True):
                print(i)
            else:
                print(i)
                a = i
                rec(a)
    # -s Command
    elif (x[3] == "-s"):
        if (len(x) > 4):
            for i in a.iterdir():
                if (i.is_file() == True and i.name == x[4]):
                    print(i)
                elif (i.is_dir() == True):
                    a = i
                    rec(a)
        else:
            print("ERROR")
    # -e Command
    elif (x[3] == "-e"):
        if (len(x) > 4):
            for i in a.iterdir():
                if (i.is_file() == True and i.suffix == f".{x[4]}"):
                    print(i)
                elif (i.is_dir() == True):
                    a = i
                    rec(a)
        else:
            print("ERROR")
    # -f Command
    elif (x[3] == "-f"):
        if (len(x) > 3):
            for i in a.iterdir():
                if (i.is_file() == True):
                    print(i)
                else:
                    a = i
                    rec(a)
        else:
            print("ERROR")

# Input Statements
q = ""
while (q != "Q"):
    a2_fnx_inp.input_command()
    n = input()
    x = n.strip().split()
    q = x[0]
    # Admin Mode
    if(x[0] == "admin"):
        print("You Have Entered Admin Mode\n")
        n = input()
        x = n.strip().split()
        p = Path(x[1])
    else:
        p = Path(x[1])
    global profile

# L Command: Listing the Files
    try:
        if(x[0] == "Q"):
            print("Program Quit")
            quit
        elif (x[0] == "L"):
            # No Command
            if (len(x) == 2):
                for i in p.iterdir():
                    if (i.is_file() == True): 
                        print(i)
                for i in p.iterdir():
                    if (i.is_dir() == True):
                        print(i)
            # -r Command
            elif (x[2] == "-r"):
                rec(p)
            # -f Command
            elif (x[2] == "-f"):
                for i in p.iterdir():
                    if (i.is_file() == True): 
                        print(i)
            # -s Command
            elif (x[2] == "-s"):
                if(len(x) > 3):
                    for i in p.iterdir():
                        if (i.name == x[3]):
                            print(i)
                else:
                    print("ERROR")
            # -e Command
            elif (x[2] == "-e"):
                if(len(x) > 3):
                    for i in p.iterdir():
                        if (i.suffix == f".{x[3]}"):
                            print(i)
                else:
                    print("ERROR")

        # C Command: Creating a File/Profile
        elif (x[0] == "C"):
            if (len(x) > 2):           
                if (x[2] == "-n"):
                    try:
                        p = p / f"{x[3]}.dsu"
                        p.touch(exist_ok = True)
                        print(p)
                        profile_creator()
                        print("Profile Created\n")
                        profile = Profile.Profile()
                        profile.load_profile(p)
                        f = open(p, mode = "r")
                        a2_fnx_inp.E_command()
                        a2_fnx_inp.P_command()
                        a2_fnx_inp.Q_command()
                        m = input()
                        n = m.strip().split()
                        j = {}
                        for i in f:
                            j = json.loads(i)
                        
                        # E Command - Edits a Profile
                        if(n[0] == "E"):
                            # Edits Username
                            if("-usr" in n):
                                profile.username = n[n.index("-usr") + 1]
                                print("Username Updated")
                            # Edits Password
                            if("-pwd" in n):
                                profile.password = n[n.index("-pwd") + 1]
                                print("Password Updated")
                            # Edits Bio
                            if("-bio" in n):
                                profile.bio = n[n.index("-bio") + 1]
                                print("Bio Updated")
                            # Adds a Post
                            if("-addpost" in n):
                                while(len(n) < 3):
                                    print("Invalid Command - Post Missing")
                                o = Profile.Post(entry = n[n.index("-addpost") + 1])
                                profile.add_post(o)
                                print("Post Added")
                            # Deletes a Post
                            if("-delpost" in n):
                                while(len(n) < 3):
                                    print("Invalid Command - Post ID Missing")
                                print("Post Deleted")                        
                                profile.del_post(int(n[n.index("-delpost") + 1]))
                            profile.save_profile(p)
                        
                        # P Command - Prints a Profile
                        elif(n[0] == "P"):
                            # Prints Username
                            if("-usr" in n):
                                print("Your username is: " + j["username"])
                            # Prints Password
                            if("-pwd" in n):
                                print("Your password is: " + j["password"])
                            # Prints Bio
                            if("-bio" in n):
                                print("Your bio is: " + j["bio"])
                            # Prints All Posts
                            if("-posts" in n):
                                if(len(j["_posts"]) == 0):
                                    print("Sorry no posts!")
                                else:
                                    l = profile.get_posts()
                                    for i in range(len(l)):
                                        print("Post: " + l[i]["entry"])
                            # Prints a Specific Post
                            if("-post" in n):
                                while(len(n) < 3):
                                    print("Invalid Command: Post ID Missing")
                                i = int(n[n.index("-post") + 1])
                                l = profile.get_posts()
                                print("Post: " + l[i]["entry"])
                            # Prints All Information
                            if(n[1] == "-all"):
                                print("Here are all your information")
                                print("Username: " + j["username"])
                                print("Password: " + j["password"])
                                print("Bio: " + j["bio"])
                                l = profile.get_posts()
                                for i in range(len(l)):
                                    print("Post: " + l[i]["entry"])
                    except Exception as e:
                        print(e)

        # D Command: Deleting the File
        elif (x[0] == "D"):
            if (p.is_file() == True and p.suffix == ".dsu"):
                try:
                    p.unlink()
                    print(f"{p} DELETED")
                except Exception as e:
                    print("ERROR")
            else:
                print("ERROR")

        # R Command: Reading the File
        elif (x[0] == "R"):
            if (p.is_file() == True and p.suffix == ".dsu"):
                try:
                    f = open(p, mode = "r")
                    if(os.path.getsize(p) == 0):
                        print("EMPTY")
                    else:
                        for i in f:
                            print(i.strip())
                    f.close()
                except:
                    print("ERROR")
            else:
                print("ERROR")
        
        # O Command: Opening the Profile
        elif(x[0] == "O"):
            if(p.is_file() == True and p.suffix == ".dsu"):
                try:
                    profile = Profile.Profile()
                    profile.load_profile(p)
                    f = open(p, mode = "r")
                    print("File Opened")
                    a2_fnx_inp.E_command()
                    a2_fnx_inp.P_command()
                    a2_fnx_inp.Q_command()
                    m = input()
                    n = m.strip().split()
                    j = {}
                    for i in f:
                        j = json.loads(i)
                    
                    # E Command - Edits a Profile
                    if(n[0] == "E"):
                        # Edits Username
                        if("-usr" in n):
                            profile.username = n[n.index("-usr") + 1]
                            print("Username Updated")
                        # Edits Password
                        if("-pwd" in n):
                            profile.password = n[n.index("-pwd") + 1]
                            print("Password Updated")
                        # Edits Bio
                        if("-bio" in n):
                            profile.bio = n[n.index("-bio") + 1]
                            print("Bio Updated")
                        # Adds a Post
                        if("-addpost" in n):
                            while(len(n) < 3):
                                print("Invalid Command - Post Missing")
                            o = Profile.Post(entry = n[n.index("-addpost") + 1])
                            profile.add_post(o)
                            print("Post Added")
                        # Deletes a Post
                        if("-delpost" in n):
                            while(len(n) < 3):
                                print("Invalid Command - Post ID Missing")
                            print("Post Deleted")                        
                            profile.del_post(int(n[n.index("-delpost") + 1]))
                        profile.save_profile(p)
                    
                    # P Command - Prints a Profile
                    elif(n[0] == "P"):
                        # Prints Username
                        if("-usr" in n):
                            print("Your username is: " + j["username"])
                        # Prints Password
                        if("-pwd" in n):
                            print("Your password is: " + j["password"])
                        # Prints Bio
                        if("-bio" in n):
                            print("Your bio is: " + j["bio"])
                        # Prints All Posts
                        if("-posts" in n):
                            if(len(j["_posts"]) == 0):
                                print("Sorry no posts!")
                            else:
                                l = profile.get_posts()
                                for i in range(len(l)):
                                    print("Post: " + l[i]["entry"])
                        # Prints a Specific Post
                        if("-post" in n):
                            while(len(n) < 3):
                                print("Invalid Command: Post ID Missing")
                            i = int(n[n.index("-post") + 1])
                            l = profile.get_posts()
                            print("Post: " + l[i]["entry"])
                        # Prints All Information
                        if(n[1] == "-all"):
                            print("Here are all your information")
                            print("Username: " + j["username"])
                            print("Password: " + j["password"])
                            print("Bio: " + j["bio"])
                            l = profile.get_posts()
                            for i in range(len(l)):
                                print("Post: " + l[i]["entry"])
                except Exception as e:
                    print(e)
            else:
                print("File Error")
    except Exception as e:
        print("ERROR")
