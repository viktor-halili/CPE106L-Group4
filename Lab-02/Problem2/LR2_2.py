def main():
    # Ask for filename
    filename = input("Enter filename: ")

    try:
        # Read all lines into a list, stripping the newline characters
        with open(filename, "r") as file:
            lines = [line.strip() for line in file]

        # Main loop
        while True:
            print(f"\nThe file has {len(lines)} lines.")
            choice = input("Enter a line number (1 to {}), or 0 to quit: ".format(len(lines)))

            # Validate input is a number
            if not choice.isdigit():
                print("Please enter a valid number.")
                continue

            choice = int(choice)

            # Exit condition
            if choice == 0:
                print("Exiting program.")
                break

            # Check if line number is valid
            if 1 <= choice <= len(lines):
                print(f"Line {choice}: {lines[choice - 1]}")
            else:
                print("Invalid line number. Try again.")

    except FileNotFoundError:
        print("Error: File not found.")

if _name_ == "_main_":
    main()