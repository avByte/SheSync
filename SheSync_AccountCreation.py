import tkinter as tk
from tkinter import ttk

# Function to handle form submission
def create_account():
    name = name_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    selected_traits = [trait for trait, var in traits_vars.items() if var.get()]
    written_response = response_entry.get("1.0", tk.END).strip()
    
    # Print the form data to the console (or process it further)
    print(f"Name: {name}")
    print(f"Description: {description}")
    print(f"Selected Traits: {', '.join(selected_traits)}")
    print(f"Written Response: {written_response}")
    
    # You could also perform form validation or store this information in a database, etc.
    tk.messagebox.showinfo("Account Created", "Your account has been created successfully!")

# Initialize main window
root = tk.Tk()
root.title("Account Creation")
root.geometry("400x500")

# Name label and entry
tk.Label(root, text="Name").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

# Description label and text area
tk.Label(root, text="Description").pack(pady=5)
description_entry = tk.Text(root, height=4, width=40)
description_entry.pack(pady=5)

# Traits label and checkboxes
tk.Label(root, text="Select Traits").pack(pady=5)
traits_frame = tk.Frame(root)
traits_frame.pack(pady=5)

traits = ["Adventurous", "Creative", "Empathetic", "Logical", "Curious"]
traits_vars = {trait: tk.BooleanVar() for trait in traits}

for trait in traits:
    checkbox = tk.Checkbutton(traits_frame, text=trait, variable=traits_vars[trait])
    checkbox.pack(anchor="w")

# Written response label and text area
tk.Label(root, text="Written Response").pack(pady=5)
response_entry = tk.Text(root, height=4, width=40)
response_entry.pack(pady=5)

# Submit button
submit_button = ttk.Button(root, text="Create Account", command=create_account)
submit_button.pack(pady=20)

# Run the application
root.mainloop()