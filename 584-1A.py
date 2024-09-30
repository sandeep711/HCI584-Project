import tkinter as tk
import csv
import os
from tkinter import messagebox  

# CSV file to store categories and budgets
CSV_FILE = 'categories.csv'

# Load data from CSV file
def load_data():
    data = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                category, budget = row[0], float(row[1])
                data[category] = budget
    return data

# Add info to CSV file
def save_data(data):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for category, budget in data.items():
            writer.writerow([category, budget])

# Add category and budget
def add_category():
    category = category_entry.get()
    budget = budget_entry.get()
    
    if category and budget:
        data[category] = float(budget)  # Directly add without validation
        save_data(data)
        category_listbox.insert(tk.END, category)  # Add to listbox
        messagebox.showinfo("Category Added", f"Category '{category}' added with a budget of {budget}.")  # Confirmation message

# Initialize Tkinter window
root = tk.Tk()
root.title("Category Manager")

# Load data from CSV
data = load_data()

# Category Label and Entry
tk.Label(root, text="Category:").grid(row=0, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=0, column=1)

# Budget Label and Entry
tk.Label(root, text="Budget:").grid(row=1, column=0)
budget_entry = tk.Entry(root)
budget_entry.grid(row=1, column=1)

# Category Button
add_category_btn = tk.Button(root, text="Add Category", command=add_category)
add_category_btn.grid(row=2, column=0, columnspan=2)

# Display categories
category_listbox = tk.Listbox(root, height=6)
category_listbox.grid(row=3, column=0, columnspan=2)

# Load categories into listbox
for category in data:
    category_listbox.insert(tk.END, category)

# Start Tkinter event loop
root.mainloop()