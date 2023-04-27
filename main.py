import tkinter as tk
import openai
import os

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")





from tkinter import ttk
from ttkthemes import ThemedTk
import sv_ttk


root = tk.Tk()

# Pack a big frame so, it behaves like the window background
big_frame = ttk.Frame(root)
big_frame.pack(fill="both", expand=True)

# Set the initial theme
root.tk.call("source", "theme/azure.tcl")
root.tk.call("set_theme", "dark")

root.title("GPT Document Helper")
root.geometry("1600x900")  # Set window size (width x height)
root.resizable(width=False, height=False)

from tkinter import font
open_sans_font = font.Font(family="Open Sans")
root.option_add("*font", open_sans_font)


# Function to handle submit text button
def on_button_click():
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
text_box = tk.Text(root, wrap="word", width=140, height=10, borderwidth=2, relief="groove")
text_box.place(anchor='se', relx=0.922, rely=0.99)
# GPT criteria output field
analysis_field = ttk.Label(big_frame, text="", font=(open_sans_font, 14))
analysis_field.pack(pady=10)  # Add label to the main window with some padding

critique_field = ttk.Label(big_frame, text="", font=(open_sans_font, 14), wraplength=300)
critique_field.pack(padx=50, anchor='nw')

# Full text document display
text_field = tk.Message(big_frame, text="", font=(open_sans_font, 10), width=750)
text_field.place(anchor='center', relx=0.5, rely=0.35)


# API request function
def analysis(prompt):
  output = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": """When text is entered your job is to reply in bullet point format to the following criteria on a scale of 0-100 (0 being the worst, 100 being perfect. An average text would score 50). 

[1. Readability: Assess the text based on how easy it is to read and understand. The harder it is to understand, the lower the value.

2. Organization: Evaluate the overall structure and organization of the text. Is the information presented in a logical order? Are there clear headings and subheadings that help guide the reader through the content? The less organized the text, the lower the value.

3. Grammar and Spelling: Check for proper grammar and spelling throughout the text. Errors in grammar and bad spelling will significantly lower this value.

4. Punctuation: Check for punctuation and proper capitalization in the text, if there is punctuation or capitalization missing, lower the value.

5. Spelling: Check for corrent spelling throughout the text. Errors in spelling will significantly lower this value.]

REMEMBER! DON'T RATE TOO HIGHLY, "100" MEANS THAT IT IS ABSOLUTE PERFECTION, AVERAGE TEXT IS ONLY 50!!!!! BE CRITICAL.
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
  model="gpt-4",
  messages=[
    {"role": "system", "content": """When text is entered your job is to find the biggest problems in the text and write a short critique on them. ONLY OUTPUT THE CRITIQUE. DO NOT WRITE ANYTHING OTHER THAN THE CRITIQUE."""},
    {"role": "user", "content": prompt}
  ]
)
  return output


# Start the main loop
root.mainloop()


