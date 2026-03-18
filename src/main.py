
def main():
    print("Enter a command")

    while True:
        command = input("> ").lower()

        if command == "build":
            print("building")
        elif command == "load":
            print("loading")
        elif command == "print":
            print("printing")
        elif command == "find":
            print("finding")
        elif command == "exit":
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()