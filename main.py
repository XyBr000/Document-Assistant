import tkinter as tk
import openai
import os
import time
import threading
from options import options_command
from api_functions import analysis, critique, rewrite, rewrite_prompts

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")





from tkinter import ttk
from ttkthemes import ThemedTk


root = tk.Tk()
root.iconbitmap("icon.ico")

# Pack a big frame so, it behaves like the window background
big_frame = ttk.Frame(root)
big_frame.pack(fill="both", expand=True)

# Set the initial theme
root.tk.call("source", "theme/azure.tcl")
root.tk.call("set_theme", "dark")

root.title("GPT Document Helper")
root.geometry("1600x900+-7+0")  # Set window size (width x height)
root.resizable(width=False, height=False)

from tkinter import font
open_sans_font = font.Font(family="Open Sans")
root.option_add("*font", open_sans_font)



from configparser import ConfigParser
config = ConfigParser()
# Function to handle options menu opening



def check_labels():
    while(True):
        time.sleep(0.2)        
        if critique_field.cget("text") == "":
            ""
        else:
            update_labels()
            break


def update_analysis(inital):
    analysis_field.config(text="")
    # Use a thread to run the analysis function and update the analysis field
    def update_analysis_thread():
        if inital:
            analysis_result = analysis(textinput)
            while analysis_result == "":
                time.sleep(0.2)
            text_field.config(text=textinput)
        else:
            analysis_result = analysis(text_field.cget('text'))
        analysis_field.config(text=analysis_result)

    analysis_thread = threading.Thread(target=update_analysis_thread)
    analysis_thread.start()

def update_critique(initial):
    critique_field.config(text="")
    # Use a thread to run the critique function and update the critique field
    def update_critique_thread():
        if initial:
            critique_result = critique(textinput)
            while critique_result == "":
                time.sleep(0.2)
            text_field.config(text=textinput)
        else:
            critique_result = critique(text_field.cget('text'))
        critique_field.config(text=critique_result)

    critique_thread = threading.Thread(target=update_critique_thread)
    critique_thread.start()

def update_rewrite():
    # Use a thread to run the rewrite function and update the rewrite field
    def update_rewrite_thread():
        rewrite_result = rewrite(text_field.cget('text'), rewrite_option)
        text_field.config(text=rewrite_result)
        update_critique(initial=False)
        update_analysis(inital=False)

    rewrite_thread = threading.Thread(target=update_rewrite_thread)
    rewrite_thread.start()

# Function to handle submit text button
def on_button_click():
    long_thread = threading.Thread(target=check_labels)
    long_thread.start()
    global textinput
    textinput = text_box.get('1.0', 'end') #store text from input in variable
    update_analysis(inital=True) #update the analysis field
    update_critique(initial=True) #update the critique field
    text_box.delete('1.0', 'end') #clear input

# Submit Text Button
button = ttk.Button(big_frame, text="Submit Text!", command=on_button_click)
button.place(anchor='se', relx=0.99, rely=0.91)  # Add button to the main window with some padding

# Prompt Text Input
text_box = tk.Text(big_frame, wrap="word", width=140, height=10, borderwidth=2, relief="groove")
text_box.place(anchor='se', relx=0.922, rely=0.99)

# GPT criteria output field
analysis_label = tk.Label(big_frame, text="Analysis", font=(open_sans_font, 16, "bold"), fg="#f9cb9c", wraplength=300)
analysis_frame = ttk.LabelFrame(big_frame, text="", labelwidget=analysis_label)
analysis_frame.place_forget()
analysis_field = tk.Label(analysis_frame, text="", font=(open_sans_font, 14), fg="#f9cb9c", wraplength=300)
analysis_field.pack(pady=10, padx=25)  # Add label to the main window with some padding

# GPT criticism text field
critique_label = tk.Label(big_frame, text="Feedback", font=(open_sans_font, 16, "bold"), fg="#f9cb9c", wraplength=300)
critique_frame = ttk.LabelFrame(big_frame, text="", labelwidget=critique_label)
critique_frame.place_forget()
critique_field = tk.Label(critique_frame, text="", font=(open_sans_font, 14), fg="#f9cb9c", wraplength=300)
critique_field.pack(pady=20, padx=25)

# Full text document display
text_field = tk.Message(big_frame, text="", font=(open_sans_font, 10), fg="#9fc5e8", width=750)
text_field.place(anchor='n', relx=0.5, rely=0.3)

# Settings button
options_button = ttk.Button(big_frame, text="Options", command=lambda: options_command(root))
options_button.place(anchor='nw', relx=0.0056, rely=0.01)  # Add button to the main window with some padding



# Rewrite text dropdown list combobox
rewrite_text_label = tk.Label(big_frame, text="Rewrite Text", font=(open_sans_font, 16, "bold"), fg="#f9cb9c", wraplength=300)
rewrite_text_field = ttk.Combobox(big_frame, values=["From feedback", "Fix grammar", "Fix punctuation", "Fix spelling", "Formal", "Informal", "Casual", "Condense text", "Expand text", "Make it persuasive", "Add humor", "Remove jargon", "Rephrase as a list", "Rewrite for social media"], state="readonly")
rewrite_text_field.selection_clear()
rewrite_text_field.place_forget()

# Rewrite text button function
def on_rewrite_button_click():
    update_rewrite()

# Rewrite text button
rewrite_text_button = ttk.Button(big_frame, text="Rewrite Text", command=on_rewrite_button_click)
rewrite_text_button.place_forget()

# When combobox is changed clear highlight

def callback(eventObject):
    global rewrite_option
    rewrite_option = rewrite_text_field.get()
    rewrite_text_field.selection_clear()
rewrite_text_field.bind("<<ComboboxSelected>>", callback)


def update_labels():
    critique_frame.place(anchor='nw', relx=0.0056, rely=0.2)
    analysis_frame.pack(pady=10)
    rewrite_text_button.place(anchor='nw', relx=0.131, rely=0.01)
    rewrite_text_field.place(anchor='nw', relx=0.1, rely=0.05)





# Start the main loop
root.mainloop()


