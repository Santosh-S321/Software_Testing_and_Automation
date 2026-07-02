def validate_login(username, password):
    valid_username = "admin"
    valid_password = "1234"
    return username == valid_username and password == valid_password


if __name__ == "__main__":
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    if validate_login(username, password):
        print("Login Successful")
    else:
        print("Invalid Username or Password")