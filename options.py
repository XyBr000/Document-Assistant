from dotenv import load_dotenv
import os
from configparser import ConfigParser
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

load_dotenv()
config = ConfigParser()

# Function to handle options menu opening
def options_command(root):
    load_dotenv(override=True)

    def update_config():
        config.set('main', 'gpt4', str(checkbox_var.get()))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    config.read('config.ini')

    options_window = tk.Toplevel(root)
    options_window.iconbitmap("icon.ico")
    options_window.title("Options")
    options_window.geometry("600x200")
    options_window.resizable(width=False, height=False)

    checkbox_var = tk.BooleanVar(value=config.getboolean('main', 'gpt4'))
    if os.getenv('GPT_4') == "False":
        checkbox_var.set(False)
        update_config()
        checkbox = ttk.Checkbutton(options_window, text="GPT-4", variable=checkbox_var, onvalue=True, offvalue=False, command=update_config, state=tk.DISABLED)
    else:
        checkbox = ttk.Checkbutton(options_window, text="GPT-4", variable=checkbox_var, onvalue=True, offvalue=False, command=update_config)
    checkbox.pack(padx=80, pady=20)