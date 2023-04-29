import tkinter as tk
import openai
import os
import time
import threading
from options import options_command

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
        rewrite_result = rewrite(text_field.cget('text'))
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


def rewrite_prompts():
    # Generate GPT-4 prompts for each rewrite selection
    if rewrite_option == "From feedback":
        rewrite_prompt = f"Rewrite the text based on this feedback: {critique_field.cget('text')}"
    if rewrite_option == "Fix grammar":
        rewrite_prompt = "Rewrite the text to fix the grammar and ONLY the grammar."
    if rewrite_option == "Fix punctuation":
        rewrite_prompt = "Rewrite the text to fix the punctuation and ONLY the punctuation."
    if rewrite_option == "Fix spelling":
        rewrite_prompt = "Rewrite the text to fix the spelling and ONLY the spelling."
    if rewrite_option == "Formal":
        rewrite_prompt = "Rewrite the text to make it formal, try and keep a style of writing."
    if rewrite_option == "Informal":
        rewrite_prompt = "Rewrite the text to make it informal, try and keep a style of writing."
    if rewrite_option == "Casual":
        rewrite_prompt = "Rewrite the text to make it highly casual, try and keep a style of writing."
    if rewrite_option == "Condense text":
        rewrite_prompt = "Rewrite the text to make it more concise, and condense it."
    if rewrite_option == "Simplify language":
        rewrite_prompt = "Rewrite the text using simpler language and easier-to-understand terms."
    if rewrite_option == "Expand text":
        rewrite_prompt = "Rewrite the text by expanding on the ideas and providing more details."    
    if rewrite_option == "Make it persuasive":
        rewrite_prompt = "Rewrite the text to make it more persuasive and convincing."
    if rewrite_option == "Add humor":
        rewrite_prompt = "Rewrite the text by adding humor and making it more lighthearted."
    if rewrite_option == "Remove jargon":
        rewrite_prompt = "Rewrite the text by removing any jargon or technical terms and replacing them with simpler language."
    if rewrite_option == "Rephrase as a list":
        rewrite_prompt = "Rewrite the text by rephrasing it as a list, organizing the information in a clear and concise manner."
    if rewrite_option == "Rewrite for social media":
        rewrite_prompt = "Rewrite the text for a social media post, making it concise and engaging."

    #else:
        #rewrite_prompt = f"Rewrite the text based on this feedback: {critique_field.cget('text')}"
    return rewrite_prompt



def update_labels():
    critique_frame.place(anchor='nw', relx=0.0056, rely=0.2)
    analysis_frame.pack(pady=10)
    rewrite_text_button.place(anchor='nw', relx=0.131, rely=0.01)
    rewrite_text_field.place(anchor='nw', relx=0.1, rely=0.05)



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

3. Grammar: Check for proper grammar throughout the text. Errors in grammar will significantly lower this value.

4. Punctuation: Check for punctuation and proper capitalization in the text, if there is punctuation or capitalization missing, lower the value.

5. Spelling: Check for corrent spelling throughout the text. Errors in spelling will significantly lower this value.]

REMEMBER! DON'T RATE TOO HIGHLY, "100" MEANS THAT IT IS ABSOLUTE PERFECTION, AVERAGE TEXT IS ONLY 50!!!!! BE CRITICAL. RATE 25% LOWER THAN YOU THINK THEY SHOULD BE.
you must also output the setting/format/genre of the text - how is the text perceived to the reader?
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
    return output.choices[0].message.content

def critique(prompt):
    output = openai.ChatCompletion.create(
    model=get_model(),
    messages=[
      {"role": "system", "content": """When text is entered your job is to find the biggest problems in the text and write a !SHORT! and !BRIEF! critique on them. ONLY OUTPUT THE CRITIQUE. DO NOT WRITE ANYTHING OTHER THAN THE CRITIQUE. Output this in numerical format (1. 2. 3.), and make sure theres a line gap between each."""},
      {"role": "user", "content": prompt}
    ]
  )
    return output.choices[0].message.content

def rewrite(prompt):
    prompt_type = rewrite_prompts()
    print("prompt type: ", prompt_type)
    print(rewrite_option)
    output = openai.ChatCompletion.create(
    model=get_model(),
    messages=[
      {"role": "system", "content": f"""When text is entered your job is to rewrite the text in the style/format of [{prompt_type}]. Heavily weigh in [{prompt_type}] when creating the rewritten text."""},
      {"role": "user", "content": prompt}
    ]
  )
    return output.choices[0].message.content

# Start the main loop
root.mainloop()


