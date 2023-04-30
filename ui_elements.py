import tkinter as tk
from tkinter import font
from tkinter import ttk



def create_button(big_frame, text, command, relx, rely, font_obj):
    style = ttk.Style()
    style.configure("TButton", font=font_obj)
    button = ttk.Button(big_frame, text=text, command=command)
    button.place(anchor='se', relx=relx, rely=rely)
    return button

def create_text_box(big_frame, width, height, relx, rely):
    text_box = tk.Text(big_frame, wrap="word", width=width, height=height, borderwidth=2, relief="groove")
    text_box.place(anchor='se', relx=relx, rely=rely)
    return text_box


def create_label_frame(big_frame, text, fg, wraplength, pady, padx, font_obj):
    label = tk.Label(big_frame, text=text, font=(font_obj, 16, "bold"), fg=fg, wraplength=wraplength)
    frame = ttk.LabelFrame(big_frame, text="", labelwidget=label)
    frame.place_forget()
    field = tk.Label(frame, text="", font=(font_obj, 14), fg=fg, wraplength=wraplength)
    field.pack(pady=pady, padx=padx)
    return frame, field

def create_message(big_frame, text, fg, width, font_obj, relx, rely):
    message = tk.Message(big_frame, text=text, font=font_obj, fg=fg, width=width)
    message.place(anchor='n', relx=relx, rely=rely)
    return message


def create_combobox(big_frame, values, state, relx, rely):
    combobox = ttk.Combobox(big_frame, values=values, state=state)
    combobox.selection_clear()
    combobox.place(anchor='nw', relx=relx, rely=rely)
    return combobox