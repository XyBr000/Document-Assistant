import tkinter as tk
import os
from dotenv import load_dotenv, set_key
import openai
import sys
load_dotenv()


def gpt3_checker():
    output = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "return pong"},
    {"role": "user", "content": "ping"}
  ]
)
    if output.choices[0].message.content == "pong":
        return 1

def gpt4_checker():
    output = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
    {"role": "system", "content": "return pong"},
    {"role": "user", "content": "ping"}
  ]
)
    if output.choices[0].message.content == "pong":
        return 1
def submit_api_key():
    api_key = entry.get()
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        set_key('.env', "OPENAI_API_KEY", api_key)
        popup.destroy()
        os.system('python run.py')

api_check = 0 #check if api key works
gpt4_check = 0 #check if gpt-4 is enabled on account
print("api_check ", api_check)
openai.api_key = os.getenv("OPENAI_API_KEY")

help_text = "Go to (https://platform.openai.com/account/api-keys) to find your key."

if api_check == 0 and openai.api_key != "":
    try:
         api_check = gpt3_checker()
    except openai.error.AuthenticationError:
         api_check = 0
         help_text = "Key invalid or no balance on OpenAI account. \n Go to https://platform.openai.com/account/api-keys to find your key, \n or go to https://platform.openai.com/account/usage to view your billing & usage."
         print('Key invalid or no balance on OpenAI account. Go to https://platform.openai.com/account/api-keys to find your key, or go to https://platform.openai.com/account/usage to view your billing & usage.')
         set_key('.env', "OPENAI_API_KEY", "")
         openai.api_key = ""
    if api_check == 1:
         try:
                gpt4_check = gpt4_checker()
         except openai.error.AuthenticationError:
                gpt4_check = 0


print("openai api key: ", openai.api_key)


if api_check == 0:
    print(f'OPENAI_API_KEY is not set or empty')
    # Create a pop-up that asks for API key
    popup = tk.Tk()
    popup.title("API Key")
    popup.geometry("450x150")  # Set window size (width x height)

    label = tk.Label(popup, text="Enter your OpenAI API Key:")
    label.pack()

    entry = tk.Entry(popup)
    entry.pack()

    submit_button = tk.Button(popup, text="Submit", command=submit_api_key)
    submit_button.pack()

    info_label = tk.Label(popup, text=help_text)
    info_label.pack(pady=10)


    popup.mainloop()

if gpt4_check == 1:
    set_key('.env', 'GPT_4', 'True')
else:
    set_key('.env', 'GPT_4', 'False')




if api_check == 1:
    set_key('.env', 'GPT_3', 'True')
    try:
        popup.destroy()
    except:
        print("API key valid, running main.py")
    os.system('python main.py')
    