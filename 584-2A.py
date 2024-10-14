import tkinter as tk
import csv
import os
from tkinter import messagebox

# CSV file to store categories, budgets, and expenses
CSV_FILE = 'categories_expenses.csv'

# Load data from CSV file
def load_data():
    data = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                category, budget, expenses = row[0], float(row[1]), float(row[2])
                data[category] = {'budget': budget, 'expenses': expenses}
    return data

# Save data to CSV file
def save_data(data):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for category, values in data.items():
            writer.writerow([category, values['budget'], values['expenses']])

# Add a new category and budget
def add_category():
    category = category_entry.get()
    budget = budget_entry.get()
    
    if category and budget:
        if category not in data:  # Check if category already exists
            data[category] = {'budget': float(budget), 'expenses': 0.0}
            save_data(data)
            category_listbox.insert(tk.END, category)
            category_dropdown['menu'].add_command(label=category, command=tk._setit(selected_category, category))
            selected_category.set(category)  # Update the selection
            messagebox.showinfo("Category Added", f"Category '{category}' added with a budget of {budget}.")
        else:
            messagebox.showwarning("Duplicate Category", "This category already exists.")
    else:
        messagebox.showwarning("Input Error", "Please enter both category and budget.")

# Add expense to the selected category
def add_expense():
    category = selected_category.get()
    expense = expense_entry.get()
    
    if category and expense:
        try:
            expense = float(expense)
            current_expenses = data[category]['expenses']
            budget = data[category]['budget']
            
            # Update the total expenses
            new_expenses = current_expenses + expense
            data[category]['expenses'] = new_expenses
            save_data(data)
            
            # Check if expenses exceed the budget
            if new_expenses > budget:
                messagebox.showwarning("Budget Exceeded", f"Warning: Expenses for '{category}' have exceeded the budget.")
            else:
                messagebox.showinfo("Expense Added", f"Expense of {expense} added to '{category}'.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the expense.")
    else:
        messagebox.showwarning("Selection Error", "Please select a category and enter an expense.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Category and Expense Manager")

# Load data from CSV
data = load_data()

# Category Section
tk.Label(root, text="Add New Category").grid(row=0, column=0, columnspan=2)

# Category Label and Entry
tk.Label(root, text="Category:").grid(row=1, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1)

# Budget Label and Entry
tk.Label(root, text="Budget:").grid(row=2, column=0)
budget_entry = tk.Entry(root)
budget_entry.grid(row=2, column=1)

# Add Category Button
add_category_btn = tk.Button(root, text="Add Category", command=add_category)
add_category_btn.grid(row=3, column=0, columnspan=2)

# Expense Section
tk.Label(root, text="Add Expense to Category").grid(row=4, column=0, columnspan=2)

# Dropdown to select a category for adding expense
tk.Label(root, text="Select Category:").grid(row=5, column=0)

# Check if there are categories, if not set a placeholder
categories = list(data.keys())
if not categories:
    categories = ["No categories available"]

selected_category = tk.StringVar(root)
selected_category.set(categories[0])  # Default to the first available category or placeholder

category_dropdown = tk.OptionMenu(root, selected_category, *categories)
category_dropdown.grid(row=5, column=1)

# Expense Label and Entry
tk.Label(root, text="Expense:").grid(row=6, column=0)
expense_entry = tk.Entry(root)
expense_entry.grid(row=6, column=1)

# Add Expense Button
add_expense_btn = tk.Button(root, text="Add Expense", command=add_expense)
add_expense_btn.grid(row=7, column=0, columnspan=2)

# Display existing categories in a listbox
tk.Label(root, text="Existing Categories").grid(row=8, column=0, columnspan=2)
category_listbox = tk.Listbox(root, height=6)
category_listbox.grid(row=9, column=0, columnspan=2)

# Load categories into the listbox
for category in data:
    category_listbox.insert(tk.END, category)

# Start Tkinter event loop
root.mainloop()