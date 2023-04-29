import tkinter as tk
import openai
import os
import time
import threading

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")





from tkinter import ttk
from ttkthemes import ThemedTk
import sv_ttk


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
def options_command():
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


def check_labels():
    while(True):
        time.sleep(0.2)        
        print(critique_field.cget("text"))
        if critique_field.cget("text") == "":
            ""
        else:
            update_labels()
            break


# Function to handle submit text button
def on_button_click():
    long_thread = threading.Thread(target=check_labels)
    long_thread.start()
    textinput = text_box.get('1.0', 'end') #store text from input in variable
    analysis_output = analysis(textinput).choices[0].message.content #api
    critique_output = critique(textinput).choices[0].message.content
    analysis_field.config(text=analysis_output) #set the criteria to the output of gpt
    text_field.config(text=textinput) #set the text document text
    critique_field.config(text=critique_output)
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
options_button = ttk.Button(big_frame, text="Options", command=options_command)
options_button.place(anchor='nw', relx=0.0056, rely=0.01)  # Add button to the main window with some padding

def update_labels():
    print("test1")
    critique_frame.place(anchor='nw', relx=0.0056, rely=0.2)
    analysis_frame.pack(pady=10)




def get_model(): #check the config to see what model to use
    config.read('config.ini')
    gpt4_bool = config.getboolean('main', 'gpt4')
    if gpt4_bool == True:
        model_to_use = 'gpt-4'
    else:
        model_to_use = 'gpt-3.5-turbo'
    return model_to_use

# API request function
def analysis(prompt):
    output = openai.ChatCompletion.create(
    model=get_model(),
    messages=[
      {"role": "system", "content": """When text is entered your job is to reply in bullet point format to the following criteria on a scale of 0-100 (0 being the worst, 100 being perfect. An average text would score 50). 

[1. Readability: Assess the text based on how easy it is to read and understand. The harder it is to understand, the lower the value.

2. Organization: Evaluate the overall structure and organization of the text. Is the information presented in a logical order? Are there clear headings and subheadings that help guide the reader through the content? The less organized the text, the lower the value.

3. Grammar and Spelling: Check for proper grammar and spelling throughout the text. Errors in grammar and bad spelling will significantly lower this value.

4. Punctuation: Check for punctuation and proper capitalization in the text, if there is punctuation or capitalization missing, lower the value.

5. Spelling: Check for corrent spelling throughout the text. Errors in spelling will significantly lower this value.]

REMEMBER! DON'T RATE TOO HIGHLY, "100" MEANS THAT IT IS ABSOLUTE PERFECTION, AVERAGE TEXT IS ONLY 50!!!!! BE CRITICAL. RATE 25% LOWER THAN YOU THINK THEY SHOULD BE.
you must also output the setting of the text, for example: formal, casual, sarcastic, comedic, urgent, and many other types - how is the text perceived to the reader?
your response MUST be in the following format: 

setting

1. Readability: readability/100
2. Organization: organization/100
3. Grammar: grammar/100
4. Punctuation: punctuation/100
5. Spelling: spelling/100"""},
      {"role": "user", "content": prompt}
    ]
  )
    return output

def critique(prompt):
    output = openai.ChatCompletion.create(
    model=get_model(),
    messages=[
      {"role": "system", "content": """When text is entered your job is to find the biggest problems in the text and write a short critique on them. ONLY OUTPUT THE CRITIQUE. DO NOT WRITE ANYTHING OTHER THAN THE CRITIQUE. Output this in numerical format (1. 2. 3.), and make sure theres a line gap between each."""},
      {"role": "user", "content": prompt}
    ]
  )
    return output


# Start the main loop
root.mainloop()


