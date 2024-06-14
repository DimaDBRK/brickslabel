import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from excel_service import get_info_by_id, get_all_ids
from label_service import create_label, generate_filename
import os
import webbrowser
from pathlib import Path
from dotenv import load_dotenv, set_key
from PIL import Image, ImageTk
from search_service import open_search_window

# Load environment variables from .env file
load_dotenv()
FONT_SIZE = int(os.getenv("FONT_SIZE", 12))
DATA_FILE_PATH = os.getenv("DATA_FILE_PATH", "")

def fetch_and_create_label():
    if not DATA_FILE_PATH:
        messagebox.showerror("Error", "Data file path is not set. Please set the path to the data file.")
        return

    if not os.path.exists(DATA_FILE_PATH):
        messagebox.showerror("Error", f"File '{DATA_FILE_PATH}' not found. Please place the file in the specified location and try again.")
        return

    search_id = id_entry.get()
    if not search_id:
        messagebox.showerror("Error", "Please enter an ID")
        return

    try:
        info = get_info_by_id(DATA_FILE_PATH, search_id, sheet_name="data")
    except KeyError as e:
        messagebox.showerror("Error", str(e))
        return

    if not info:
        messagebox.showerror("Error", "ID not found")
        return

    # Determine the Downloads directory
    downloads_directory = str(Path.home() / "Downloads")

    # Ensure the output directory exists
    os.makedirs(downloads_directory, exist_ok=True)

    output_filename = generate_filename(search_id)
    output_path = os.path.join(downloads_directory, output_filename)
    create_label(info, output_path)
    
    # Show custom success message with an open file button
    show_success_message(output_path)

def set_data_file_path():
    global DATA_FILE_PATH
    file_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),  # Set to current working directory
        title="Select Data File",
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
    )
    if file_path:
        DATA_FILE_PATH = file_path
        set_key('.env', 'DATA_FILE_PATH', DATA_FILE_PATH)
        messagebox.showinfo("Success", f"Data file path set to: {DATA_FILE_PATH}")

def open_file(file_path, window):
    if os.path.exists(file_path):
        webbrowser.open_new(file_path)
    else:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
    window.destroy()

def show_success_message(file_path):
    success_message = Toplevel()
    success_message.title("Success")
    success_message.geometry("300x150")

    tk.Label(success_message, text=f"Label created:\n{file_path}").pack(pady=10)

    tk.Button(success_message, text="Open File", command=lambda: open_file(file_path, success_message)).pack(pady=5)
    tk.Button(success_message, text="Close", command=success_message.destroy).pack(pady=5)

def load_logo(frame):
    logo_path = os.path.join(os.path.dirname(__file__), "images")
    for ext in ["Logo.gif", "Logo.png"]:
        full_path = os.path.join(logo_path, ext)
        if os.path.exists(full_path):
            img = Image.open(full_path)
            img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(frame, image=img)
            logo_label.image = img  # Keep a reference to avoid garbage collection
            logo_label.pack(pady=10)
            break

def search_id():
    if not DATA_FILE_PATH:
        messagebox.showerror("Error", "Data file path is not set. Please set the path to the data file.")
        return

    if not os.path.exists(DATA_FILE_PATH):
        messagebox.showerror("Error", f"File '{DATA_FILE_PATH}' not found. Please place the file in the specified location and try again.")
        return

    try:
        ids = get_all_ids(DATA_FILE_PATH, sheet_name="data")
    except KeyError as e:
        messagebox.showerror("Error", str(e))
        return

    open_search_window(root, ids, set_id)

def set_id(selected_id):
    id_entry.delete(0, tk.END)
    id_entry.insert(0, selected_id)

def run_gui():
    global id_entry, root

    root = tk.Tk()
    root.title("Label Generator")
    root.geometry("400x400")  # Set the window size

    frame = tk.Frame(root, padx=20, pady=20)  # Add padding around the frame
    frame.pack(pady=20)

    # Load and add logo to the top
    load_logo(frame)

    # Add search button above "Enter ID" label
    tk.Button(frame, text="Set Data File Path", command=set_data_file_path).pack(pady=5, anchor='e')
    
    search_button = tk.Button(frame, text="Search ID", command=search_id)
    search_button.pack(pady=5, anchor='e')

    tk.Label(frame, text="Enter ID:").pack(pady=5, anchor='w')
    id_entry = tk.Entry(frame)
    id_entry.pack(pady=5, anchor='w', fill='x')

    tk.Button(frame, text="Fetch and Create Label", command=fetch_and_create_label).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
