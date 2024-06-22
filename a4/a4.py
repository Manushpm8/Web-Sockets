# Manush Murali
# mpmurali@uci.edu
# 14568752


# Class Imports
from pathlib import Path
from urllib import request,error
from OpenWeather import OpenWeather
from LastFM import LastFM
from ExtraCreditAPI import ExtraCreditAPI
import urllib
import os
import json
import time
import Profile
import ds_client
import ds_protocol
import a4_fnx_inp


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
    a4_fnx_inp.choice_command()
    z = input()
    if (z == "F"):
        # File System Input Statements
        a4_fnx_inp.file_input_command()
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

        try:
            # L Command: Listing the Files
            if (x[0] == "L"):
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
                        p = p / f"{x[3]}.dsu"
                        p.touch(exist_ok = True)
                        print(p)
                        profile_creator()
                        print("Profile Created")

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
                        a4_fnx_inp.E_command()
                        a4_fnx_inp.P_command()
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
                            elif("-pwd" in n):
                                profile.password = n[n.index("-pwd") + 1]
                                print("Password Updated")
                            # Edits Bio
                            elif("-bio" in n):
                                profile.bio = n[n.index("-bio") + 1]
                                print("Bio Updated")
                            # Adds a Post to the File System as well as the DS Server
                            elif("-addpost" in n):
                                while(len(n) < 3):
                                    print("Invalid Command - Post Missing")
                                pos = str(n[n.index("-addpost") + 1])
                                o = Profile.Post(entry = pos, timestamp = time.time())
                                profile.add_post(o)
                                print("Post Added")
                                a4_fnx_inp.post_input_command()
                                ans = input()
                                if(ans == "Yes"):
                                    srv = str(input("\nPlease Enter Server IP: "))
                                    port = 3021
                                    usr = profile.username
                                    pas = profile.password
                                    js = ds_protocol.join_command(usr, pas)
                                    js_msg = ds_client.communicator(srv, port, usr, pas, js)
                                    ds_msg = json.loads(js_msg)
                                    tok = ds_msg["response"]["token"]
                                    print(ds_msg["response"]["message"])
                                    ts = str(o.get_time())
                                    js = ds_protocol.post_command(tok, pos, ts)
                                    js_msg = ds_client.communicator(srv, port, usr, pas, js)
                                    print(ds_protocol.extract_json(js_msg).message)
                                else:
                                    pass
                            # Deletes a Post
                            elif("-delpost" in n):
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
                            elif("-pwd" in n):
                                print("Your password is: " + j["password"])
                            # Prints Bio
                            elif("-bio" in n):
                                print("Your bio is: " + j["bio"])
                            # Prints All Posts
                            elif("-posts" in n):
                                if(len(j["_posts"]) == 0):
                                    print("Sorry no posts!")
                                else:
                                    l = profile.get_posts()
                                    for i in range(len(l)):
                                        print("Post: " + l[i]["entry"])
                            # Prints a Specific Post
                            elif("-post" in n):
                                while(len(n) < 3):
                                    print("Invalid Command: Post ID Missing")
                                i = int(n[n.index("-post") + 1])
                                l = profile.get_posts()
                                print("Post: " + l[i]["entry"])
                            # Prints All Information
                            elif(n[1] == "-all"):
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
    
    # Internet Posts
    # This command adds and edits posts to the internet with new as well as existing user profiles.
    elif (z == "I"):
        a4_fnx_inp.internet_input_command()
        srv = str(input("Server IP: "))
        port = 3021
        a4_fnx_inp.profile_input_command()
        js = ""
        js_msg = ds_client.communicator(srv, port, "", "", js)
        pr = input()
        
        # Creates a New Profile With The DS Server & Adds a Post on the DS Server Along with Keywords If Necessary
        if (pr == "N"):
            usr = input("\nPlease Enter A Username: ")
            pas = input("Please Enter A Password: ")
            js = ds_protocol.join_command(usr, pas)
            js_msg = ds_client.communicator(srv, port, usr, pas, js)
            ds_msg = json.loads(js_msg)
            tok = ds_msg["response"]["token"]
            a4_fnx_inp.post_input_command()
            ans = input()
            if(ans == "Yes"):
                a4_fnx_inp.keyword_input_command()
                post = input("\nPlease Enter Your Post: ")
                while ("@weather" in post or "@lastfm" in post or "@extracredit" in post):
                    if ("@weather" in post):
                        ow = OpenWeather(92697, "US")
                        ow.set_apikey("260114f0fd09d1377a14e9e522a02d1b")
                        ow.load_data()
                        post = ow.transclude(post)
                    if ("@lastfm" in post):
                        lf = LastFM()
                        lf.set_apikey("e41b46349b52aa523730d47b8b1887ee")
                        lf.load_data()
                        post = lf.transclude(post)
                    if ("@extracredit" in post):
                        ec = ExtraCreditAPI()
                        EXTRACREDITAPIKEY = "8ea4935483f14bf5a264c44d923f30bd"
                        ec.set_apikey(EXTRACREDITAPIKEY)
                        ec.load_data()
                        post = ec.transclude(post)
                po = Profile.Post(entry = post, timestamp = time.time())
                ts = str(po.get_time())
                js = ds_protocol.post_command(tok, post, ts)
                js_msg = ds_client.communicator(srv, port, usr, pas, js)
            else:
                pass
        
        # Accesses An Existing Profile With The DS Server & Adds a Post on the DS Server Along with Keywords If Necessary.
        elif (pr == "E"):
            usr = input("\nPlease Enter Your Username: ")
            pas = input("Please Enter Your Password: ")
            js = ds_protocol.join_command(usr, pas)
            js_msg = ds_client.communicator(srv, port, usr, pas, js)
            ds_msg = json.loads(js_msg)
            tok = ds_msg["response"]["token"]
            print(ds_msg["response"]["message"])
            a4_fnx_inp.keyword_input_command()
            post = input("\nPlease Enter Your Post: ")
            while ("@weather" in post or "@lastfm" in post or "@extracredit" in post):
                if ("@weather" in post):
                    ow = OpenWeather(92697, "US")
                    ow.set_apikey("260114f0fd09d1377a14e9e522a02d1b")
                    ow.load_data()
                    post = ow.transclude(post)
                if ("@lastfm" in post):
                    lf = LastFM()
                    lf.set_apikey("e41b46349b52aa523730d47b8b1887ee")
                    lf.load_data()
                    post = lf.transclude(post)
                if ("@extracredit" in post):
                    ec = ExtraCreditAPI()
                    EXTRACREDITAPIKEY = "8ea4935483f14bf5a264c44d923f30bd"
                    ec.set_apikey(EXTRACREDITAPIKEY)
                    ec.load_data()
                    post = ec.transclude(post)
            po = Profile.Post(entry = post, timestamp = time.time())
            ts = str(po.get_time())
            js = ds_protocol.post_command(tok, post, ts)
            js_msg = ds_client.communicator(srv, port, usr, pas, js)
        
        # Adds/Updates The Bio Of User Profiles On The DS Server
        elif (pr == "B"):
            usr = input("\nPlease Enter Your Username: ")
            pas = input("Please Enter Your Password: ")
            js = ds_protocol.join_command(usr, pas)
            js_msg = ds_client.communicator(srv, port, usr, pas, js)
            ds_msg = json.loads(js_msg)
            tok = ds_msg["response"]["token"]
            print(ds_msg["response"]["message"])
            bio = input("\nPlease Enter Your Bio: ")
            b = [bio, time.time()]
            ts = str(b[1])
            js = ds_protocol.bio_command(tok, bio, ts)
            js_msg = ds_client.communicator(srv, port, usr, pas, js)
        
        else:
            print("ERROR - Invalid Command")
            exit
        print(ds_protocol.extract_json(js_msg).message)

    else:
        print("ERROR - Invalid Command")
print("Program Quit")
