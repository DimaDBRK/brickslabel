import tkinter as tk
from tkinter import Toplevel, Listbox, Entry, Button, Scrollbar

def open_search_window(parent, ids, set_id_callback):
    search_window = Toplevel(parent)
    search_window.title("Search ID")
    search_window.geometry("400x300")

    tk.Label(search_window, text="Search ID:").pack(pady=5)
    search_entry = Entry(search_window)
    search_entry.pack(pady=5)

    scrollbar = Scrollbar(search_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(search_window, yscrollcommand=scrollbar.set)
    listbox.pack(pady=5, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    for id_value in ids:
        listbox.insert(tk.END, id_value)

    def on_search():
        search_term = search_entry.get().lower()
        listbox.delete(0, tk.END)
        for id_value in ids:
            if search_term in str(id_value).lower():
                listbox.insert(tk.END, id_value)

    def on_select(event):
        selected_id = listbox.get(listbox.curselection())
        set_id_callback(selected_id)
        search_window.destroy()

    search_button = Button(search_window, text="Search", command=on_search)
    search_button.pack(pady=5)

    listbox.bind('<<ListboxSelect>>', on_select)

    search_window.transient(parent)
    search_window.grab_set()
    parent.wait_window(search_window)
