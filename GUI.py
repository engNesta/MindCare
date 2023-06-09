import tkinter as tk
import pygame

import Music_player
from Backend import Emotions
import customtkinter as ctk
import tkinter.messagebox as tkmb


# window

class LoginUI:
    def __init__(self):
        # Selecting GUI theme - dark, light , system (for system default)
        ctk.set_appearance_mode("dark")
        # Selecting color theme - blue, green, dark-blue
        ctk.set_default_color_theme("blue")
        width = 500
        height = 550
        self.app = ctk.CTk()

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.app.geometry("%dx%d+%d+%d" % (width, height, x, y))

        self.app.title("Modern Login UI using Customtkinter")

        label = ctk.CTkLabel(self.app, text="MINDCARE")
        label.pack(pady=20)

        frame = ctk.CTkFrame(master=self.app)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        label = ctk.CTkLabel(master=frame, text='Login / Register')
        label.pack(pady=12, padx=10)

        self.user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
        self.user_entry.pack(pady=12, padx=10)

        self.pass_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
        self.pass_entry.pack(pady=12, padx=10)

        button = ctk.CTkButton(master=frame, text='Login', command=self.login)
        button.pack(pady=12, padx=10)

        register_button = ctk.CTkButton(master=frame, text='Register', command=self.show_register)
        register_button.pack(pady=12, padx=10)

        self.register_frame = ctk.CTkFrame(master=frame)

        self.register_user_entry = ctk.CTkEntry(master=self.register_frame)
        self.register_user_entry.pack(pady=12, padx=10)

        self.register_pass_entry = ctk.CTkEntry(master=self.register_frame, show="*")
        self.register_pass_entry.pack(pady=12, padx=10)

        self.register_save_button = ctk.CTkButton(self.register_frame, text='Save', command=self.save)
        self.register_save_button.pack(pady=12, padx=10)

        self.register_cancel_button = ctk.CTkButton(self.register_frame, text='Cancel', command=self.hide_register)
        self.register_cancel_button.pack(pady=12, padx=10)

        self.hide_register()

    def show_register(self):
        self.register_frame.pack(pady=12, padx=10, fill='both', expand=True)

    def hide_register(self):
        self.register_frame.pack_forget()

    def save(self):
        with open('accounts.txt', 'a') as f:
            f.write(self.register_user_entry.get() + ',' + self.register_pass_entry.get() + '\n')

        tkmb.showinfo(title="Registration Successful", message="You have registered successfully")
        self.hide_register()
        self.app.withdraw()
        gui = GUI()
        gui.root.mainloop()

    def login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()
        with open('accounts.txt', 'r') as f:
            data = f.readlines()
        for line in data:
            line = line.strip().split(',')
            if line[0] == username:
                if line[1] == password:
                    tkmb.showinfo(title="Login Successful", message="You have logged in Successfully")
                    self.app.withdraw()
                    gui = GUI()
                    gui.root.mainloop()
                    return
                else:
                    tkmb.showwarning(title='Wrong Password', message='Please check your password')
                    return
        tkmb.showerror(title='User not found', message='Please check your username')

    def run(self):
        self.app.mainloop()


class GUI:
    def __init__(self):
        self.emotions = Emotions()

        # initialize pygame mixer
        pygame.mixer.init()
        # create main window
        width = 500
        height = 550

        self.root = tk.Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))

        self.root.title("MindCare")

        self.root.resizable(False, False)
        self.root.config(bg="#2C3E50")

        # create canvas
        self.canvas = tk.Canvas(self.root, width=500, height=550, bg="#2C3E50")
        self.canvas.pack()

        #create title
        self.canvas.create_text(250, 50, text="How are you feeling today??", font=("Helvetica", 26), fill="#ffffff")
        # create emoji buttons
        self.happy_btn = tk.Button(self.canvas, text="😊", bg="#2C3E50", font=("Helvetica", 36), padx=20, pady=10,
                                   command=lambda: self.update_emotion("Happy"))
        self.ok_btn = tk.Button(self.canvas, text="😐", bg="#2C3E50", font=("Helvetica", 36), padx=20, pady=10,
                                command=lambda: self.update_emotion("Ok"))
        self.sad_btn = tk.Button(self.canvas, text="😢", bg="#2C3E50", font=("Helvetica", 36), padx=20, pady=10,
                                 command=lambda: self.update_emotion("Sad"))

        # create meditate button
        self.meditate_btn = tk.Button(self.canvas, text="Meditate", bg="#3498DB", fg="#ffffff", font=("Helvetica", 16),
                                      padx=20, pady=10, command=self.open_meditate_window)

        # create quote label
        self.quote_label = tk.Label(self.canvas, text="", font=("Helvetica", 16), anchor="center", justify="center",
                                    wraplength=400, fg="#ffffff", bg="#2C3E50")

        # add buttons and quote label to canvas
        self.canvas.create_window(125, 250, window=self.happy_btn)
        self.canvas.create_window(250, 250, window=self.ok_btn)
        self.canvas.create_window(375, 250, window=self.sad_btn)
        self.canvas.create_window(250, 400, window=self.meditate_btn)
        self.canvas.create_window(250, 475, window=self.quote_label)

    def update_emotion(self, emotion_name):
        quote = self.emotions.get_quote(emotion_name.lower())
        self.quote_label.config(text=quote)

    def play_audio(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("Audio-1.mp3")
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()

    def open_meditate_window(self):
        # hide the main window
        self.root.withdraw()
        Music_player.run()


class MindCare:
    def __init__(self):
        self.login = LoginUI()

    def run(self):
        self.login.run()


mindcare = MindCare()
mindcare.run()
