import tkinter as tk
import threading
import time
from tkinter import font
from ui_elements import create_button, create_text_box, create_label_frame, create_message, create_combobox, create_scrolled_frame
from options import options_command
from api_functions import analysis, critique, rewrite, rewrite_prompts, get_critique_field

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = tk.Tk()
style = ttk.Style("documenthelper")
open_sans_font = font.Font(family="Open Sans")
root.option_add("*font", open_sans_font)
root.iconbitmap("icon.ico")

# Pack a big frame so, it behaves like the window background
big_frame = ttk.Frame(root)
big_frame.pack(fill="both", expand=True)

# Set the initial theme
#root.tk.call("source", "theme/azure.tcl")
#root.tk.call("set_theme", "dark")

root.title("GPT Document Helper")
root.geometry("1600x900+-7+0")  # Set window size (width x height)
root.resizable(width=False, height=False)

from tkinter import font
open_sans_font = font.Font(family="Open Sans")
root.option_add("*font", open_sans_font)

from configparser import ConfigParser
config = ConfigParser()
textinput = ""
def scrolled_text():
    global text_field_base
    text_field_base = create_message(big_frame, text=textinput, fg="#9fc5e8", width=85, font_obj=open_sans_font, relx=2.5, rely=5)

    scrolled_frame = create_scrolled_frame(big_frame, width=800, height=350, scrollheight=text_field_base.winfo_reqheight())
    global text_field
    text_field = create_message(scrolled_frame, text=text_field_base.get(1.0, tk.END), fg="#9fc5e8", width=85, font_obj=open_sans_font, relx=0.5, rely=0)

def check_labels():
    while True:
        time.sleep(0.2)
        if critique_field.cget("text") == "":
            ""
        else:
            update_labels()
            break

def update_analysis(inital):
    analysis_field.config(text="")
    def update_analysis_thread():
        if inital:
            analysis_result = analysis(textinput)
            while analysis_result == "":
                time.sleep(0.2)
            text_field_base.insert(tk.END, textinput)
            scrolled_text()
        else:
            analysis_result = analysis(text_field.cget('text'))
        analysis_field.config(text=analysis_result)

    analysis_thread = threading.Thread(target=update_analysis_thread)
    analysis_thread.start()

def update_critique(initial):
    critique_field.config(text="")
    def update_critique_thread():
        if initial:
            critique_result = critique(textinput)
            get_critique_field(critique_result) #send the critique field to the api_functions.py file            
            while critique_result == "":
                time.sleep(0.2)
            text_field_base.insert(tk.END, textinput)
            scrolled_text()
        else:
            critique_result = critique(text_field.cget('text'))
            get_critique_field(critique_result) #send the critique field to the api_functions.py file
        critique_field.config(text=critique_result)

    critique_thread = threading.Thread(target=update_critique_thread)
    critique_thread.start()

def update_rewrite():
    def update_rewrite_thread():
        rewrite_result = rewrite(text_field.cget('text'), rewrite_option)
        text_field.config(text=rewrite_result)
        update_critique(initial=False)
        update_analysis(inital=False)

    rewrite_thread = threading.Thread(target=update_rewrite_thread)
    rewrite_thread.start()

def on_button_click():
    long_thread = threading.Thread(target=check_labels)
    long_thread.start()
    text_field.update_idletasks() 
    text_field_base.update_idletasks() 
    global textinput
    textinput = text_box.get('1.0', 'end')
    update_analysis(inital=True)
    update_critique(initial=True)
    text_box.delete('1.0', 'end')

button = create_button(big_frame, text="Submit Text!", command=on_button_click, relx=0.9954, rely=0.899, font_obj=open_sans_font)

text_box = create_text_box(big_frame, width=140, height=10, relx=0.922, rely=0.99)

analysis_frame, analysis_field = create_label_frame(big_frame, text="Analysis", fg="#f9cb9c", wraplength=300, pady=10, padx=25, font_obj=open_sans_font)

critique_frame, critique_field = create_label_frame(big_frame, text="Feedback", fg="#f9cb9c", wraplength=300, pady=20, padx=25, font_obj=open_sans_font)

scrolled_text()

options_button = create_button(big_frame, text="Options", command=lambda: options_command(root), relx=0.075, rely=0.045, font_obj=open_sans_font)

rewrite_text_label = tk.Label(big_frame, text="Rewrite Text", font=(open_sans_font, 16, "bold"), fg="#f9cb9c", wraplength=300)
rewrite_text_field = create_combobox(big_frame, values=["From feedback", "Fix grammar", "Fix punctuation", "Fix spelling", "Formal", "Informal", "Casual", "Condense text", "Expand text", "Make it persuasive", "Add humor", "Remove jargon", "Rephrase as a list", "Rewrite for social media"], state="readonly", relx=0.1, rely=0.05)
rewrite_text_field.place_forget()

def callback(eventObject):
    global rewrite_option
    rewrite_option = rewrite_text_field.get()
    rewrite_text_field.selection_clear()

rewrite_text_field.bind("<<ComboboxSelected>>", callback)

def on_rewrite_button_click():
    update_rewrite()

rewrite_text_button = create_button(big_frame, text="Rewrite Text", command=on_rewrite_button_click, relx=0.197, rely=0.045, font_obj=open_sans_font)
rewrite_text_button.place_forget()



def update_labels():
    critique_frame.place(anchor='nw', relx=0.0056, rely=0.2)
    rewrite_text_button.place(anchor="se", relx=0.197, rely=0.045, bordermode="inside")
    rewrite_text_field.place(relx=0.1, rely=0.05)
    analysis_frame.pack(pady=10)
root.mainloop()