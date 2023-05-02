import os
import configparser
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import time
import re
import shutil

history_dir = 'history'
current_config = configparser.ConfigParser()
count = 0
current_save_index = 0

def set_history_index():
    global latest_history_index
    latest_history_index = count

def set_current_history_index():
    global current_history_index
    current_history_index = current_save_index


def update_history():
    count = 0
    for path in os.listdir(history_dir):
        if os.path.isdir(os.path.join(history_dir, path)):
            count += 1
    set_history_index()
    return count

count = update_history()


latest_history_index = count
current_history_index = latest_history_index

# Function to create a new history index
def create_new_history_index():
    name_thread = threading.Thread(target=name_history_files)
    name_thread.start()
    

    global count
    count = update_history()
    

    os.mkdir(history_dir + '/' + str(latest_history_index + 1))
    config_dir = history_dir + '/' + str(latest_history_index + 1)
    current_config.clear()
    with open (config_dir + '/history.ini', 'w') as configfile:
        current_config.write(configfile)

    count = update_history()
    combobox.set("Save: " + str(count))
    on_history_changed()

# Function to update the history index
def update_history_index(text_body, critique, analysis):
    global count
    count = update_history()
    set_history_index()
    set_current_history_index()

    config_dir = history_dir + '/' + str(current_history_index)

    index_in_history = count_index_in_history()
    current_config[f'history{index_in_history}'] = {}
    current_config[f'history{index_in_history}']['text_body'] = text_body
    current_config[f'history{index_in_history}']['critique'] = critique
    current_config[f'history{index_in_history}']['analysis'] = analysis

    if os.path.exists(config_dir):
        with open(config_dir + '/history.ini', 'w') as configfile:
            current_config.write(configfile)
    else:
        create_new_history_index()

    def wait_for_directory_creation():
        while not os.path.exists(config_dir):
            time.sleep(0.1)
            print("Waiting for directory to be created...")
        print("Directory created! ", config_dir)
        current_config[f'history{index_in_history}'] = {}
        current_config[f'history{index_in_history}']['text_body'] = text_body
        current_config[f'history{index_in_history}']['critique'] = critique
        current_config[f'history{index_in_history}']['analysis'] = analysis
        if os.path.exists(config_dir):
            with open(config_dir + '/history.ini', 'w') as configfile:
                current_config.write(configfile)
                print("config file written!", current_config)
        else:
            print("Directory not created!")

    wait_thread = threading.Thread(target=wait_for_directory_creation)
    wait_thread.start()

    count = update_history()

# Function to count the index in the history
def count_index_in_history():
    set_current_history_index()
    current_config.read(history_dir + '/' + str(current_history_index) + '/history.ini')
    length = len(current_config.sections())
    return length


# Function to handle history menu opening
def history_command(root):
    history_window = tk.Toplevel(root)
    history_window.iconbitmap("icon.ico")
    history_window.title("History")
    history_window.geometry("300x600")
    history_window.resizable(width=False, height=False)

# Function that gets the combobox from the main file
def get_combobox(combobox_input):
    global combobox
    combobox = combobox_input

def get_save_names():
    save_names = []
    save_config = configparser.ConfigParser()
    
    # Iterate through all directories in the directory
    for path in os.listdir(history_dir):
        dir_path = os.path.join(history_dir, path)
        save_name_file_path = os.path.join(dir_path, 'save_name.ini')

        if os.path.isdir(dir_path):
            if os.path.isfile(save_name_file_path):
                save_config.read(save_name_file_path)

                if 'save_name' in save_config:
                    save_name = save_config['save_name'].get('name')
                    if save_name:
                        save_names.append(save_name)
                    else:
                        save_names.append("")
                else:
                    save_names.append("")
            else:
                save_names.append("")

    return save_names

# Function that sets the combobox text for saves
def get_history_values():
    history_list = os.listdir(history_dir)

    # Filter the list to only include directories
    history_list = [int(item) for item in history_list if os.path.isdir(os.path.join(history_dir, item))]

    # If the list is empty, return
    if history_list == []:
        return
    # Sort the list numerically
    history_list.sort()
    save_names = get_save_names()

    # Combine history_list and save_names
    combined_list = []
    for index, history_item in enumerate(history_list):
        if index < len(save_names):
            save_name = save_names[index]
        else:
            save_name = ""
        combined_list.append(f"Save: {history_item} | {save_name}")

    combobox["values"] = tuple(combined_list)
    set_current_history_index()
    print(current_history_index)
    combobox.set(f"Save: {current_history_index} | {save_names[int(current_history_index) - 1]}")

# Funtion that handles the history combobox changing and sets the current save index
def on_history_changed():
    combo_text = combobox.get()
    dir_to_go = int(re.search(r'\d+', combo_text).group())
    dir_to_go = str(dir_to_go)
    global current_save_index
    current_save_index = dir_to_go
    for path in os.listdir(history_dir):
        if os.path.isdir(os.path.join(history_dir, path)):
            if path == dir_to_go:
                config_dir = history_dir + '/' + str(path)
                current_config.read(config_dir + '/history.ini')
                try:
                    return current_config['history0']['text_body'], current_config['history0']['critique'], current_config['history0']['analysis']
                except:
                    pass

# Function that clears the empty history folders
def clear_empty_history_folders():
    for path in os.listdir(history_dir):
        if os.path.isdir(os.path.join(history_dir, path)):
            config_dir = history_dir + '/' + str(path)
            
            config_deleter = configparser.ConfigParser()
            config_deleter.read(config_dir + '/history.ini')
            
            if len(config_deleter.sections()) == 0:
                try:
                    shutil.rmtree(config_dir)
                except:
                    pass
    on_history_changed()

# Function that renames the history folders to be in order
def name_history_files():
    empty_name_thread = threading.Thread(target=clear_empty_history_folders)
    empty_name_thread.start()
    time.sleep(3)
    folders = sorted([d for d in os.listdir(history_dir) if os.path.isdir(os.path.join(history_dir, d))])
    current_number = 1
    # First pass: Rename to temporary names
    for folder in folders:
        full_path = os.path.join(history_dir, folder)
        tmp_path = os.path.join(history_dir, f"tmp_{current_number}")
        os.rename(full_path, tmp_path)
        current_number += 1

    # Second pass: Rename back to new names
    for i in range(1, current_number):
        tmp_path = os.path.join(history_dir, f"tmp_{i}")
        new_path = os.path.join(history_dir, str(i))
        os.rename(tmp_path, new_path)
    get_history_values()



# Function that creates and updates a new config file to handle the save name
def create_update_save_name(save_name):
    if save_name == "Rename this save":
        save_name = ""
    save_config = configparser.ConfigParser()
    save_config['save_name'] = {}
    save_config['save_name']['name'] = save_name
    with open(history_dir + '/' + str(current_save_index) + '/save_name.ini', 'w') as configfile:
        save_config.write(configfile)
    get_history_values()