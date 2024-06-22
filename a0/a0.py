try:
    a = int(input())
    print("+-+")
    print("| |")
    for i in range(0,a-1):
        print(("  " * (i)) + "+-+-+")
        print(("  " * (i+1)) + "| |")
    print(("  " * (a-1)) + "+-+")
except Exception as e:
    print(e)
