def number(x):
    match x:
        case 1:
            print("1")
        case 2:
            print("2")
        case _:
            print("invalid")


def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please try again.")

if __name__ == '__main__':
    number(get_number("Enter a number: "))
