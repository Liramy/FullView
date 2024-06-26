import os
import tkinter
from typing import Tuple
import sys
from cryptography.fernet import Fernet
import json
from os import path

import customtkinter
from tkinter import ttk
from tkinter import *

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

from PIL import Image, ImageTk


class LoginTabs(customtkinter.CTkTabview):
    def __init__(self, master, sock, comm, key,**kwargs):
        super().__init__(master, **kwargs)

        self.socket = sock
        self.command = comm
        self.key = key
        
        # create tabs
        self.add("Login")
        self.add("Register")
        
        self.tab("Login").grid_columnconfigure(0, weight=1)
        self.tab("Register").grid_columnconfigure(0, weight=1)

        # Define the fonts used
        self.label_font = customtkinter.CTkFont(family="Segoe UI", size=30)
        input_font = customtkinter.CTkFont(family="Segoe UI", size=15)

        #------------------------------------------------------------------------------
        # Login page
        
        # "log in" label
        self.label = customtkinter.CTkLabel(
            master=self.tab("Login"), 
            height=30, width=100, 
            font=self.label_font, text="Log in", 
            text_color=("#26272E", "#E9EFE7"))
        self.label.grid(row=0, column=0, padx=0, pady=10)
        
        # Username input textbox
        self.username_login = customtkinter.CTkEntry(self.tab("Login"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Username (4-16)")
        self.username_login.grid(row=1, column=0, padx=0, pady=10)
        
        # Password input textbox
        self.password_login = customtkinter.CTkEntry(self.tab("Login"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Password (6-30)", show="*")
        self.password_login.grid(row=2, column=0, padx=0, pady=10)
        
        # Login button
        self.login_button = customtkinter.CTkButton(self.tab("Login"), width=200, height= 75,
                                                    font=self.label_font, fg_color=("#C8CEC6", "#1E2025"),
                                                    corner_radius=20, text="Log In", command=self.log_in, 
                                                    hover_color=("gray30","#4F5263"))
        
        self.login_button.grid(row=3, column=0, padx=0, pady=50)
        
        #---------------------------------------------------------------#
        # Register Page:
        self.reg_label = customtkinter.CTkLabel(
            master=self.tab("Register"), 
            height=30, width=100, 
            font=self.label_font, text="Register", 
            text_color=("#26272E", "#E9EFE7"))
        self.reg_label.grid(row=0, column=0, padx=0, pady=10)
        
        # Username textbox
        self.username_register = customtkinter.CTkEntry(self.tab("Register"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Username (4-16)")
        self.username_register.grid(row=1, column=0, padx=0, pady=10)
        
        # Password textbox
        self.password_register = customtkinter.CTkEntry(self.tab("Register"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Password (6-30)", show="*")
        self.password_register.grid(row=2, column=0, padx=0, pady=10)
        
        # Password confirmation textbox
        self.password_confirm = customtkinter.CTkEntry(self.tab("Register"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Confirm Password", show="*")
        self.password_confirm.grid(row=3, column=0, padx=0, pady=10)
        
        # Register button
        self.register_button = customtkinter.CTkButton(self.tab("Register"), width=200, height= 75,
                                                    font=self.label_font, fg_color=("#C8CEC6", "#1E2025"),
                                                    corner_radius=20, text="Register", command=self.register, 
                                                    hover_color=("gray30","#4F5263"))
        self.register_button.grid(row=4, column=0, padx=0, pady=30)
        
    
    def log_in(self):
        """ Button event for loging in. Check validity of username and password. encrypt the data, send to server. 
        if server send 'Valid' message, continue to next screen 
        """
        username = self.username_login.get()
        password = self.password_login.get()
        
        if self.validation(username) and self.validation(password, False):
            data = self.encrypt_obj({"Log in":(username, password)}, symmetric_key=self.key) #pickle.dumps({"Log in":(username, password)})
            self.socket.send(data)
            answer = self.socket.recv(4096).decode()
            if answer == 'Valid':
                self.master.destroy()
            else:
                self.login_button.destroy()
                self.login_button = customtkinter.CTkButton(self.tab("Login"), width=200, height= 75,
                                                    font=self.label_font, fg_color=("#C8CEC6", "#1E2025"),
                                                    corner_radius=20, text="Invalid username or password", command=self.log_in, 
                                                    hover_color=("gray30","#4F5263"))
        
                self.login_button.grid(row=3, column=0, padx=0, pady=50)
        return
    
        
    def register(self):
        username = self.username_register.get()
        password = self.password_register.get()
        password_confirm = self.password_confirm.get()
        
        if (self.validation(username)) and (
            self.validation(password, False)) and (
            password == password_confirm):
                
            data = self.encrypt_obj({"Register":(username, password)}, symmetric_key=self.key)#pickle.dumps({"Register":(username, password)})
            self.socket.send(data)
            answer = self.socket.recv(4096).decode()
            if answer == 'Valid':
                self.register_button.destroy()
                self.register_button = customtkinter.CTkButton(self.tab("Register"), width=200, height= 75,
                                                        font=self.label_font, fg_color=("#C8CEC6", "#1E2025"),
                                                        corner_radius=20, text="Added user, please log in", command=self.register, 
                                                        hover_color=("gray30","#4F5263"))
                self.register_button.grid(row=4, column=0, padx=0, pady=30)
        else:
            self.register_button.destroy()
            self.register_button = customtkinter.CTkButton(self.tab("Register"), width=200, height= 75,
                                                    font=self.label_font, fg_color=("#C8CEC6", "#1E2025"),
                                                    corner_radius=20, text="Invalid username or password", command=self.register, 
                                                    hover_color=("gray30","#4F5263"))
            self.register_button.grid(row=4, column=0, padx=0, pady=30)
        return
        
    def validation(self, user_data, is_username=True):
        # User data for validation - Ease of access
        max_characters = 16 if is_username else 30 # 16 for username, 30 for password
        min_characters = 4 if is_username else 6 # 4 for username, 6 for password
        allowed_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_1234567890"\
                                if is_username else \
                                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_1234567890#$%&*-;"
        
        length = len(user_data)
        
        return (
            max_characters - length >= 0) and (
            length - min_characters >= 0) and all(
            char in allowed_characters for char in user_data)
            
    def encrypt_obj(self, obj, symmetric_key):
        encrypted_message = json.dumps(obj).encode()
        iv = os.urandom(16)  # Initialization vector
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(encrypted_message) + encryptor.finalize()

        payload = json.dumps({
            'iv': b64encode(iv).decode('utf-8'),
            'message': b64encode(encrypted_message).decode('utf-8')
        })
        return payload.encode()

    def decrypt_obj(self, enc, symmetric_key):
        json_data = json.loads(enc)
        iv = b64decode(json_data['iv'])
        encrypted_msg = b64decode(json_data['message'])

        cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(iv), backend=default_backend)
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_msg) + decryptor.finalize()
        return decrypted_message.decode()
    
    def load_key(self):
        key_path = "Client/public_key.pem"
        file_exists = path.exists(key_path)
        if file_exists:
            with open(key_path, "rb") as f:
                return serialization.load_pem_public_key(f.read())
        print("Error - no key found")
        return None
    

class LoginApp(customtkinter.CTk):
    """The login and register frames packed as an app

        Parameters
        ---------------------------
        command - A command used to send data to the server
        this command needs to be sending server user info 
        and getting confirmation as a result
    """
    def __init__(self, sock, key):
        super().__init__()
        
        self.socket = sock
        
        self.title("ClearView Login")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.tabview = LoginTabs(
            master=self, height=400, width=400, sock = self.socket, key=key, 
            fg_color=("#E9EFE7", "#26272E"), segmented_button_selected_color=("#2A2C35", "#2A2C35"),
            segmented_button_selected_hover_color=("#4F5263","#4F5263"), corner_radius=20, comm = exit)
        self.tabview.grid(row=0, column=1, padx=20, pady=10)
        
    def exit(self):
        self.destroy()
        
        
        