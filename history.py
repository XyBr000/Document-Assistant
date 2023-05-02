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

def on_closing():
    stop_event.set()
stop_event = threading.Event()

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
    on_history_changed("save")

# Function to update the history index
def update_history_index(text_body, critique, analysis):
    current_config.clear() # Clear the config file so old data doesn't get saved
    global count
    count = update_history()
    set_history_index()
    set_current_history_index()

    config_dir = history_dir + '/' + str(current_history_index)
    if config_dir == "history/0": # history/0 is invalid
        config_dir = "history/1"

    index_in_history = count_index_in_history()
    current_config[f'history{index_in_history}'] = {}
    current_config[f'history{index_in_history}']['text_body'] = text_body
    current_config[f'history{index_in_history}']['critique'] = critique
    current_config[f'history{index_in_history}']['analysis'] = analysis

    try:
        if current_config[f'history{index_in_history-1}']['critique'] == critique: # If the save is the same as the previous save, don't save it
            if current_config[f'history{index_in_history-1}']['analysis'] == analysis:
                return
    except: # if there is no previous save, just pass
        pass

    if os.path.exists(config_dir):
        with open(config_dir + '/history.ini', 'w') as configfile:
            current_config.write(configfile)
    else:
        create_new_history_index()

    def wait_for_directory_creation():
        while not os.path.exists(config_dir):
            time.sleep(0.1)
            create_new_history_index()
            print("Waiting for directory to be created...", config_dir)
        print("Directory created! ", config_dir)
        current_config[f'history{index_in_history}'] = {}
        current_config[f'history{index_in_history}']['text_body'] = text_body
        current_config[f'history{index_in_history}']['critique'] = critique
        current_config[f'history{index_in_history}']['analysis'] = analysis
        if os.path.exists(config_dir):
            with open(config_dir + '/history.ini', 'w') as configfile:
                current_config.write(configfile)
                update_selected_version()
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





# Function that loops through all the history folders and finds the save names
def get_save_names():
    save_names = []
    save_config = configparser.ConfigParser()
    
    # Iterate through all directories in the directory
    for path in os.listdir(history_dir):
        dir_path = os.path.join(history_dir, path)
        save_name_file_path = os.path.join(dir_path, 'save_name.ini')

        if os.path.isdir(dir_path): # If the path is a directory
            if os.path.isfile(save_name_file_path): # If the save name file exists
                save_config.read(save_name_file_path) # Read the save name file

                if 'save_name' in save_config: # If the save name section exists
                    save_name = save_config['save_name'].get('name')
                    if save_name: # If the save name is not empty apply the save name
                        save_names.append(save_name)
                    else:
                        save_names.append("Unnamed Save") 
                else:
                    save_names.append("Unnamed Save")
            else:
                save_names.append("Unnamed Save")

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
    for index, history_item in enumerate(history_list): # Iterate through the history list
        if index < len(save_names): 
            save_name = save_names[index] # If there is a save name, set it to the save name
        else:
            save_name = "" # If there is no save name, set it to an empty string
        combined_list.append(f"Save: {history_item} | {save_name}") # Combine the history item and the save name and save prefix

    combobox['values'] = tuple(combined_list)
    set_current_history_index()
    combobox.set(f"Save: {current_history_index} | {save_names[int(current_history_index) - 1]}")


# Function that gets the latest version index
def get_latest_version_index(config_dir):
    version_config = configparser.ConfigParser()
    version_config.read(config_dir + '/history.ini')
    sections = version_config.sections()
    latest_index = len(sections) - 1
    if latest_index == -1: # If there are no sections, set the latest index to 0
        latest_index = 0
    return latest_index



# Funtion that handles the history combobox changing and sets the current save index
def on_history_changed(save_or_version):
    try:
        combo_text = combobox.get()
        dir_to_go = int(re.search(r'\d+', combo_text).group())
        dir_to_go = str(dir_to_go)
        global current_save_index
        current_save_index = dir_to_go
        set_current_history_index()
        for path in os.listdir(history_dir):
            if os.path.isdir(os.path.join(history_dir, path)):
                if path == dir_to_go:
                    if save_or_version == "save": # If the save combobox was changed set the values to the latest version
                        config_dir = history_dir + '/' + str(path)
                        current_config.read(config_dir + '/history.ini')
                        latest_version = get_latest_version_index(config_dir) # Get the latest version index 
                    if save_or_version == "version": # If the version combobox was changed set values to the version
                        latest_version = update_version_combobox()
                        latest_version = int(latest_version) - 1
                    try:
                        return current_config[f'history{latest_version}']['text_body'], current_config[f'history{latest_version}']['critique'], current_config[f'history{latest_version}']['analysis']
                    except:
                        pass
    except AttributeError: # This error only means that there are no history folders yet created and can be ignored
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
    on_history_changed("save")

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



    #VERSION CODE
def get_version_combobox(combobox_input):
    global version_combobox
    version_combobox = combobox_input

def get_version_values():
    set_current_history_index()
    config_dir = history_dir + '/' + str(current_history_index)
    latest_index = get_latest_version_index(config_dir)
    version_values = []
    for i in range(0, latest_index + 1):
        version_values.append(i + 1)
    return version_values

def update_version_combobox():
    version_list = get_version_values()
    combined_list = []
    for item in enumerate(version_list):
        combined_list.append(f"Version: {item[1]}")

    version_combobox['values'] = tuple(combined_list)
    selected_value = version_combobox.get()
    match = re.search(r'\d+', selected_value)
    if match:
        parsed_value = int(match.group())
    else:
        parsed_value = 0
    return parsed_value

def update_selected_version():
    set_current_history_index()
    config_dir = history_dir + '/' + str(current_history_index)
    version_combobox_value = get_latest_version_index(config_dir)
    version_combobox.set("Version: " + str(version_combobox_value + 1))

def has_list_changed(old_list, new_list):
    return old_list != new_list

def on_list_changed():
    print("List has been updated/changed.")

def continuous_version_check(callback):
    old_version_list = get_version_values()
    while not stop_event.is_set():
        time.sleep(0.2)
        current_list = get_version_values()
        if has_list_changed(old_version_list, current_list):
            update_selected_version()
            old_version_list = current_list
            print("list updated")
            callback()


version_check_loop_thread = threading.Thread(target=continuous_version_check, args=(on_list_changed,))
version_check_loop_thread.start()
        