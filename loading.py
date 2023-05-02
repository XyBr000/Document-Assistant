import tkinter as tk
import time
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def on_closing_load():
    stop_event.set()
stop_event = threading.Event()

def toggle_loading(parent, toggle):
    if toggle == "disable":
        for child in parent.winfo_children():
            if isinstance(child, ttk.Button):
                child.configure(state='disabled')
            elif isinstance(child, ttk.Combobox):
                child.state(['disabled'])
            else:
                toggle_loading(child, toggle)
    if toggle == "enable":
        for child in parent.winfo_children():
            if isinstance(child, ttk.Button):
                child.configure(state='normal')
            elif isinstance(child, ttk.Combobox):
                child.state(['!disabled'])
            else:
                toggle_loading(child, toggle)

def threaded_wait(old_analysis, old_critique, analysis, critique, root):
    is_finished = False
    new_analysis = analysis.cget("text")
    new_critique = critique.cget("text")
    while not is_finished and not stop_event.is_set():
        #print("waiting for outputs")
        if old_analysis != new_analysis or new_analysis == "":
            print("analysis changed")
            new_analysis = analysis.cget("text")
        if old_critique != new_critique or new_critique == "":
            print("critique changed")
            new_critique = critique.cget("text")
        if old_analysis != new_analysis and old_critique != new_critique and new_analysis != "" and new_critique != "":
            is_finished = True
            toggle_loading(root, "enable")
        else:
            is_finished = False
        new_analysis = analysis.cget("text")
        new_critique = critique.cget("text")
        time.sleep(0.1)


def load_wait_for_outputs(analysis, critique, root):
    toggle_loading(root, "disable")
    old_analysis = analysis.cget("text")
    old_critique = critique.cget("text")
    load_thread = threading.Thread(target=threaded_wait, args=(old_analysis, old_critique, analysis, critique, root))
    load_thread.start()
