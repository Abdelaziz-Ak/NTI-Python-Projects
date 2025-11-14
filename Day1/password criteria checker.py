# Method #1
password = input("Enter your password: ")

has_upper = False
has_lower = False
has_digit = False
has_special = False

for char in password:
    if char.isupper():
        has_upper = True
    elif char.islower():
        has_lower = True
    elif char.isdigit():
        has_digit = True

if len(password) < 8:
    print("Too short password, Minimum 8 characters")
else:
    if all([has_upper, has_lower, has_digit, has_special]):
        print("Strong password")
    else:
        print("Weak password")


# Method #2
import re

password = input("Enter your password: ")
if len(password) < 8:
    print ("Too short password")
elif not re.search("[0-9]", password):
    print ("Weak password, add numbers")
elif not re.search("[A-Z]", password):
    print ("Weak password, add uppercase characters")
elif not re.search("[a-z]", password):
    print ("Weak password, add lowercase characters")
elif not re.search("[!@#$%^&*(),.:?<>", password):
    print ("Weak password, add speciall characters")
