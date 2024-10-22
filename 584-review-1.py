import tkinter as tk
import csv
import os
from tkinter import messagebox

# CSV file to store categories, budgets, and expenses with descriptions
CSV_FILE = 'categories_expenses.csv'

# Load data from CSV file
def load_data():
    data = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                category, budget, expenses, expense_details = row[0], float(row[1]), float(row[2]), row[3:]
                data[category] = {'budget': budget, 'expenses': expenses, 'details': expense_details}
    return data

# Save data to CSV file
def save_data(data):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for category, values in data.items():
            writer.writerow([category, values['budget'], values['expenses']] + values['details'])

# Add a new category and budget
def add_category():
    category = category_entry.get()
    budget = budget_entry.get()
    
    if category and budget:
        if category not in data:  # Check if category already exists
            data[category] = {'budget': float(budget), 'expenses': 0.0, 'details': []}
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
    description = description_entry.get()
    
    if category and expense and description:
        try:
            expense = float(expense)
            current_expenses = data[category]['expenses']
            budget = data[category]['budget']
            
            # Update the total expenses and add the description
            new_expenses = current_expenses + expense
            data[category]['expenses'] = new_expenses
            data[category]['details'].append(f"{description}: {expense}")
            save_data(data)
            
            # Check if expenses exceed the budget
            if new_expenses > budget:
                expense_details = "\n".join(data[category]['details'])
                messagebox.showwarning("Budget Exceeded", f"Expenses for '{category}' have exceeded the budget.\n\nDetails of expenses:\n{expense_details}")
            else:
                messagebox.showinfo("Expense Added", f"Expense of {expense} added to '{category}'.")
            
            # Update the display of current expenses and remaining budget
            display_expenses_and_budget()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the expense.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields (category, expense, and description).")

# Display current expenses and remaining budget for the selected category
def display_expenses_and_budget(*args):
    category = selected_category.get()
    if category in data:
        current_expenses = data[category]['expenses']
        budget = data[category]['budget']
        remaining_budget = budget - current_expenses
        
        expenses_label.config(text=f"Current Expenses: {current_expenses}")
        remaining_budget_label.config(text=f"Remaining Budget: {remaining_budget}")
    else:
        expenses_label.config(text="Current Expenses: N/A")
        remaining_budget_label.config(text="Remaining Budget: N/A")

# Initialize Tkinter window
root = tk.Tk()
root.title("Category and Expense Manager")
root.config(bg="#f0f0f0")  # Light grey background

# Load data from CSV
data = load_data()

# Category Section
tk.Label(root, text="Add New Category", font=("Helvetica", 14, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

# Category Label and Entry
tk.Label(root, text="Category:", bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

# Budget Label and Entry
tk.Label(root, text="Budget:", bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=5, pady=5)
budget_entry = tk.Entry(root)
budget_entry.grid(row=2, column=1, padx=5, pady=5)

# Add Category Button
add_category_btn = tk.Button(root, text="Add Category", command=add_category, bg="#4CAF50", fg="white")
add_category_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Expense Section
tk.Label(root, text="Add Expense to Category", font=("Helvetica", 14, "bold"), bg="#f0f0f0").grid(row=4, column=0, columnspan=2, pady=10)

# Dropdown to select a category for adding expense
tk.Label(root, text="Select Category:", bg="#f0f0f0").grid(row=5, column=0, sticky="e", padx=5, pady=5)

# Check if there are categories, if not set a placeholder
categories = list(data.keys())
if not categories:
    categories = ["No categories available"]

selected_category = tk.StringVar(root)
selected_category.set(categories[0])  # Default to the first available category or placeholder

category_dropdown = tk.OptionMenu(root, selected_category, *categories)
category_dropdown.grid(row=5, column=1, padx=5, pady=5)

# Bind the dropdown to the function that updates the expense and budget info
selected_category.trace('w', display_expenses_and_budget)

# Expense Label and Entry
tk.Label(root, text="Expense Amount:", bg="#f0f0f0").grid(row=6, column=0, sticky="e", padx=5, pady=5)
expense_entry = tk.Entry(root)
expense_entry.grid(row=6, column=1, padx=5, pady=5)

# Expense Description Label and Entry
tk.Label(root, text="Expense Description:", bg="#f0f0f0").grid(row=7, column=0, sticky="e", padx=5, pady=5)
description_entry = tk.Entry(root)
description_entry.grid(row=7, column=1, padx=5, pady=5)

# Add Expense Button
add_expense_btn = tk.Button(root, text="Add Expense", command=add_expense, bg="#FF9800", fg="white")
add_expense_btn.grid(row=8, column=0, columnspan=2, pady=10)

# Labels to display current expenses and remaining budget
expenses_label = tk.Label(root, text="Current Expenses: N/A", bg="#f0f0f0", font=("Helvetica", 12))
expenses_label.grid(row=9, column=0, columnspan=2, pady=5)

remaining_budget_label = tk.Label(root, text="Remaining Budget: N/A", bg="#f0f0f0", font=("Helvetica", 12))
remaining_budget_label.grid(row=10, column=0, columnspan=2, pady=5)

# Display existing categories in a listbox
tk.Label(root, text="Existing Categories", font=("Helvetica", 14, "bold"), bg="#f0f0f0").grid(row=11, column=0, columnspan=2, pady=10)
category_listbox = tk.Listbox(root, height=6)
category_listbox.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

# Load categories into the listbox
for category in data:
    category_listbox.insert(tk.END, category)

# Add padding to widgets
for widget in root.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Start Tkinter event loop
root.mainloop()