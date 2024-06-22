# UC Irvine
# ICS 32 - Fall'2021
# Assignment 1 (a1)


# Class Imports
from pathlib import Path
import os

# Input
q = ""
while (q != "Q"):0
    n = input()
    x = n.strip().split()
    q = x[0]
    if (len(x) < 2):
        print("ERROR")
    else:
        p = Path(x[1])

    # Part-1
    # Recursive Functions
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

    try:
        # Non-Recursive Functions
        # L Command
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

        # Part-2
        # C Command
        elif (x[0] == "C"):
            if (len(x) > 2):           
                if (x[2] == "-n"):
                    p = p / f"{x[3]}.dsu"
                    p.touch(exist_ok = True)
                    print(p)

        # D Command
        elif (x[0] == "D"):
            if (p.is_file() == True and p.suffix == ".dsu"):
                try:
                    p.unlink()
                    print(f"{p} DELETED")
                except Exception as e:
                    print("ERROR")
            else:
                print("ERROR")

        # R Command
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
    except Exception as e:
        print("ERROR")
