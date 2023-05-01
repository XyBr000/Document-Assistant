import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground="grey")

    def _clear_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.configure(foreground="white")


def create_button(big_frame, text, command, relx, rely, font_obj):
    style = ttk.Style()
    style.configure("TButton", font=font_obj)
    button = ttk.Button(big_frame, text=text, command=command, bootstyle=SUCCESS)
    button.place(anchor='se', relx=relx, rely=rely)
    return button

def create_text_box(big_frame, width, height, relx, rely):
    text_box = ttk.Text(big_frame, wrap="word", width=width, height=height, borderwidth=2, relief="groove")
    text_box.place(anchor='se', relx=relx, rely=rely)
    return text_box


def create_label_frame(big_frame, text, fg, wraplength, pady, padx, font_obj):
    label = ttk.Label(big_frame, text=text, font=(font_obj, 16, "bold"), wraplength=wraplength, bootstyle=DARK)
    frame = ttk.LabelFrame(big_frame, text="", labelwidget=label, bootstyle=DARK)
    frame.place_forget()
    field = ttk.Label(frame, text="", font=(font_obj, 14), wraplength=wraplength, bootstyle=DARK)
    field.pack(pady=pady, padx=padx)
    return frame, field

def create_scrolled_frame(big_frame, width, height, scrollheight):
    sf = ScrolledFrame(master=None, width=width, height=height, autohide=True, scrollheight=scrollheight)
    #sf.pack(expand=YES)
    sf.place(anchor="center", relx=0.5, rely=0.5)
    return sf

def create_message(frame, text, fg, width, font_obj, relx, rely):
    # Calculate the number of lines in the text
    lines = text.count('\n') + 1
    wrapped_lines = sum([1 + (len(line) - 1) // width for line in text.split('\n')])
    if wrapped_lines <= 18:
        wrapped_lines = 18
    # Create the Text widget with the calculated height
    message = ttk.Text(master=frame, font=font_obj, foreground=fg, width=width, height=wrapped_lines)
    message.insert(tk.END, text)  # Insert the text into the Text widget
    message.configure(state="disabled", wrap='word')  # Disable editing and set wrap mode to 'word'
    message.place(anchor='n', relx=relx, rely=rely)
    return message


def create_combobox(big_frame, values, state, relx, rely, textvariable):
    combobox = ttk.Combobox(big_frame, values=values, state=state, bootstyle=PRIMARY, textvariable=textvariable)
    combobox.selection_clear()
    combobox.place(anchor='nw', relx=relx, rely=rely)
    return combobox

def create_entry(big_frame, relx, rely, width, textvariable, font_obj):
    entry = PlaceholderEntry(big_frame, width=width, textvariable=textvariable, font=font_obj, bootstyle=PRIMARY, exportselection=0, placeholder="Rename this save")
    entry.place(anchor='nw', relx=relx, rely=rely)
    return entry