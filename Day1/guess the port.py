
print ("Guess The Port")

secret_port = 4455
while True:
    input_port = int(input("Enter the secret port: "))
    if input_port == secret_port:
        print("You're FREE NOW")
        break
    print("Ha ha! You're STUCK IN MY LOOP")
