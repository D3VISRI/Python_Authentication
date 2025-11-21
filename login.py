import random
import json
import os

#---------User Data--------#

class User:
    def __init__(self, name=None, email=None, phone=None, password=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password

#------Otp Service------#
class Otp:
    '''otp generation'''
    def generate(self, user):
        user.otp = str(random.randint(100000,999999))
        print("Your otp:", user.otp)
    '''Verification of Otp'''
    def  verifyotp(self, user):
        uotp = input("Enter your otp: ")

        if uotp == user.otp:
            print("OTP is correct")
            return True
        else:
            print("Wrong OTP")


            print("Enter 1 for retry same otp")
            print("Enter 2 regenerate otp")
            ui1 = int(input("Enter 1 or 2 otp"))
            if(ui1 == 1):
                return self.verifyotp(user)
            else:
                self.generate(user)
                self.verifyotp(user)

#------Menu Option------#
class Menu:
    def menu(self, user, auth):




        while True:

                print("Enter 1 to display profile")
                print("Enter 2 to change password")
                print("Enter 3 to logout")
                select = int(input("select your option"))

                if select == 1:
                    auth.display(user)
                elif select==2:
                    auth.changePassword(user)
                else:
                    exit()


#----Authentication includes signup login reset password and change password-----#

class Auth:
   

    '''calling class methods'''
    def __init__(self):
        self.user = User()
        self.otp_service = Otp()
        self.menu_service = Menu()

    '''saving user data to json formatting'''

    def save_user(self):
        user_data ={
            "name": self.user.name,
            "phone":self.user.phone,
            "email": self.user.email,
            "password": self.user.password
        }

        if not os.path.exists("users.json"):
            with open("users.json", "w") as f:
                json.dump([], f)


        with open("users.json", "r") as f:
            users = json.load(f)

        users.append(user_data)

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        print("User data saved to JSON file.")

   
    '''Checks the data present in json file to use it as database'''
    def isPresent(self, user_id):
        if not os.path.exists("users.json"):
            return False

        with open("users.json", "r") as f:
            data = json.load(f)


        

        for d in data:
            if d["email"] == user_id or d["phone"] == user_id :
                
                return True

        return False



    def signup(self):
        user = self.user

        user.name = input("Enter your name: ")
        user.email = input("Enter your email: ")
        user.phone = input("Enter your number")
        if self.isPresent(user.email or user.phone):
            print("user existed return to login")

            self.login()

            

    


        if not self.validEmail(user.email):
            print("Invalid email. Please use @gmail.com or @yahoo.com")
            return

        if not self.validPhone(user.phone):
            print("Invalid phone number")
            return
        
        user.password = input("Enter your password: ")

        if self.weakpassword(user.password):
            print("Password should contain more characters")
            return
        

        self.save_user()


        self.otp_service.generate(user)
        self.otp_service.verifyotp(user)

        print("successfully registered")

        self.login()

    '''User login method'''
    def login(self):

        print("---Login---")
        user_id = input("Enter your email or phone: ")

        # Check if user exists (supports email OR phone)
        if not self.isPresent(user_id):
            print("New User, please signup")
            self.signup()
            return

        # -------------------------------------------
        # ✅ Load JSON and find the matched user here
        # -------------------------------------------
        with open("users.json", "r") as f:
            data = json.load(f)

        matched_user = None
        for d in data:
            if d["email"] == user_id or d["phone"] == user_id:
                matched_user = d
                break
        # -------------------------------------------

        # Now use matched_user for password checking
        count = 0
        while count < 3:
            upassword = input("Enter your password: ")

            if matched_user["password"] == upassword:
                print("Login successful!")
                self.menu_service.menu(self.user, self)
                break
            else:
                print("Wrong password")
                count += 1

        if count == 3:
            self.resetPassword()
        
    def resetPassword(self):
        print("Reset Password using OTP")
        self.otp_service.verifyotp(self.user)

        self.user.password = input("Enter your new password: ")
        print("---Password reset success")
        self.login()

    def changePassword(self, user):
        old = input("Enter your old password")
        if(old!= user.password):
            print("Invalid Credentials")
            return
        '''if wrong password you cannot change the password'''

        newpassword = input("Enter your password: ")
        if(self.weakpassword(newpassword)):
            print("password should be strong.")
            return
        user.password = newpassword 
        print("Password updated or changed successfully")  

    '''View Profile using display function'''
    def display(self, user):
        print("name: "+ user.name)
        print("email: "+ user.email)
        print("Phone number: "+ user.phone)
    def validEmail(self, email):
        return email.endswith('@gmail.com') or email.endswith('@yahoo.com')
    
    '''Check if the phone number contains 10 digits or not '''
    def validPhone(self, phone):
        return phone.isdigit() and len(phone) == 10
    

    '''Password must contain capital letter and numericals too be Strong with 8 characters.'''
    def weakpassword(self, pwd):
        return len(pwd)<8 or pwd.isdigit() or pwd.isalpha()
    


#--- Class for running the whole code.----#
class App:
    def run(self):

        auth = Auth()
        auth.login()



App().run()















