import os
import configparser

history_dir = 'history'
current_config = configparser.ConfigParser()
count = 0

def set_history_index():
    global latest_history_index
    latest_history_index = count

def set_current_history_index():
    global current_history_index
    current_history_index = latest_history_index # change later to take current index


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

def create_new_history_index():
    global count
    count = update_history()
    

    os.mkdir(history_dir + '/' + str(latest_history_index + 1))
    config_dir = history_dir + '/' + str(latest_history_index + 1)
    current_config.clear()
    with open (config_dir + '/history.ini', 'w') as configfile:
        current_config.write(configfile)

    count = update_history()

def update_history_index(text_body, critique, analysis):
    global count
    count = update_history()
    set_history_index()
    set_current_history_index()

    print("crindex", current_history_index)
    config_dir = history_dir + '/' + str(current_history_index)
    current_config.clear()

    index_in_history = count_index_in_history()
    current_config[f'history{index_in_history}'] = {}
    current_config[f'history{index_in_history}']['text_body'] = text_body
    current_config[f'history{index_in_history}']['critique'] = critique
    current_config[f'history{index_in_history}']['analysis'] = analysis
    with open (config_dir + '/history.ini', 'w') as configfile:
        current_config.write(configfile)
        print(configfile)

    count = update_history()

def count_index_in_history():
    current_history_index = latest_history_index
    current_config.read(history_dir + '/' + str(current_history_index) + '/history.ini')
    length = len(current_config.sections())
    print("length", length)
    return length