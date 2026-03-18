
def main():
    print("Enter a command")
    command = input("> ").lower()

    if command == "build":
        print("building")
    elif command == "load":
        print("loading")
    elif command == "print":
        print("printing")
    elif command == "find":
        print("finding")
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()