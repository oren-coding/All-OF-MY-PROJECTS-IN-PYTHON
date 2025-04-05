def greet_user(first_name, last_name):
    print("Hello", first_name.capitalize() + " " + last_name.capitalize() + "!")

def compare_numbers(first_number, second_number):
    if first_number > second_number:
        print("The first number is greater than the second number")
    else:
        print("The second number is greater than the first number")

print("Hello World!")

first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
greet_user(first_name, last_name)

first_number = int(input("Enter the first number: "))
second_number = int(input("Enter the second number: "))
compare_numbers(first_number, second_number)

