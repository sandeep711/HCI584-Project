import tkinter as tk
import csv
import os
import matplotlib.pyplot as plt
from tkinter import messagebox, Toplevel, Listbox

# File to store categories and expenses data
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

# Function to update labels showing current and remaining budget
def update_budget_labels(category):
    current_expenses = data[category]['expenses']
    budget = data[category]['budget']
    remaining_budget = budget - current_expenses
    expenses_label.config(text=f"Current Expenses: {current_expenses}")
    remaining_budget_label.config(text=f"Remaining Budget: {remaining_budget}")

# Add a new category to the data
def add_category():
    category = category_entry.get()
    budget = budget_entry.get()
    
    if category and budget:
        if category not in data:
            data[category] = {'budget': float(budget), 'expenses': 0.0, 'details': []}
            save_data(data)
            refresh_categories(category)
            messagebox.showinfo("Category Added", f"Category '{category}' added with a budget of {budget}.")
        else:
            messagebox.showwarning("Duplicate Category", "This category already exists.")
    else:
        messagebox.showwarning("Input Error", "Please enter both category and budget.")

# Add an expense to the selected category
def add_expense():
    category = selected_category.get()
    expense = expense_entry.get()
    description = description_entry.get()
    
    if category and expense and description:
        try:
            expense = float(expense)
            data[category]['expenses'] += expense
            data[category]['details'].append(f"{description}: {expense}")
            save_data(data)
            
            if data[category]['expenses'] > data[category]['budget']:
                expense_details = "\n".join(data[category]['details'])
                messagebox.showwarning("Budget Exceeded", f"Expenses for '{category}' have exceeded the budget.\n\nDetails of expenses:\n{expense_details}")
            else:
                messagebox.showinfo("Expense Added", f"Expense of {expense} added to '{category}'.")
            
            update_budget_labels(category)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the expense.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields (category, expense, and description).")

# Refresh category dropdown and listbox
def refresh_categories(new_category=None):
    category_listbox.delete(0, tk.END)
    category_dropdown['menu'].delete(0, 'end')
    
    for category in data.keys():
        category_listbox.insert(tk.END, category)
        category_dropdown['menu'].add_command(label=category, command=tk._setit(selected_category, category))
        
    if new_category:
        selected_category.set(new_category)
    else:
        selected_category.set(next(iter(data.keys()), "No categories available"))

# Show a new window with recent expenses details
def show_recent_expenses():
    recent_window = Toplevel(root)
    recent_window.title("Recent Expenses")
    recent_window.config(bg="#2d3436")
    recent_window.geometry("350x300")
    
    recent_expenses_label = tk.Label(recent_window, text="Recent Expenses", font=("Helvetica", 14, "bold"), bg="#34495e", fg="white", pady=10)
    recent_expenses_label.pack(fill="x")
    
    listbox = Listbox(recent_window, width=50, height=15, bg="#34495e", fg="white", font=("Helvetica", 10))
    listbox.pack(pady=10)
    
    for category in data:
        for detail in data[category]['details']:
            listbox.insert(tk.END, f"{category} - {detail}")

# Plot expenses bar chart with labels and heading
def plot_expenses():
    categories = list(data.keys())
    expenses = [data[category]['expenses'] for category in categories]
    
    plt.figure(figsize=(8, 6))
    plt.bar(categories, expenses, color="#2a9d8f")
    plt.title("Expenses by Category", fontsize=14, fontweight='bold')
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("Total Expenses", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Initialize main application window
root = tk.Tk()
root.title("Category and Expense Manager")
root.geometry("500x600")
root.config(bg="#2d3436")

data = load_data()  # Load data from CSV file

# Header label
header = tk.Label(root, text="Expense Tracker", font=("Helvetica", 16, "bold"), bg="#3a86ff", fg="white", pady=10)
header.grid(row=0, column=0, columnspan=2, sticky="ew")

# Add New Category Section
tk.Label(root, text="Add New Category", font=("Helvetica", 14), bg="#2d3436", fg="#dfe6e9").grid(row=1, column=0, columnspan=2, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=2, column=1, padx=5, pady=5)
category_label = tk.Label(root, text="Category Name", bg="#2d3436", fg="#dfe6e9")
category_label.grid(row=2, column=0, padx=5, pady=5)

budget_entry = tk.Entry(root)
budget_entry.grid(row=3, column=1, padx=5, pady=5)
budget_label = tk.Label(root, text="Budget", bg="#2d3436", fg="#dfe6e9")
budget_label.grid(row=3, column=0, padx=5, pady=5)

add_category_btn = tk.Button(root, text="Add Category", command=add_category, bg="#2a9d8f", fg="white", relief="raised")
add_category_btn.grid(row=4, column=0, columnspan=2, pady=10)

# Add Expense Section
tk.Label(root, text="Add Expense to Category", font=("Helvetica", 14), bg="#2d3436", fg="#e76f51").grid(row=5, column=0, columnspan=2, pady=10)
selected_category = tk.StringVar(root)
categories = list(data.keys()) if data else ["No categories available"]
selected_category.set(categories[0])
category_dropdown = tk.OptionMenu(root, selected_category, *categories)
category_dropdown.grid(row=6, column=1, padx=5, pady=5)

expense_entry = tk.Entry(root)
expense_entry.grid(row=7, column=1, padx=5, pady=5)
expense_label = tk.Label(root, text="Expense Amount", bg="#2d3436", fg="#dfe6e9")
expense_label.grid(row=7, column=0, padx=5, pady=5)

description_entry = tk.Entry(root)
description_entry.grid(row=8, column=1, padx=5, pady=5)
description_label = tk.Label(root, text="Description", bg="#2d3436", fg="#dfe6e9")
description_label.grid(row=8, column=0, padx=5, pady=5)

add_expense_btn = tk.Button(root, text="Add Expense", command=add_expense, bg="#e76f51", fg="white", relief="raised")
add_expense_btn.grid(row=9, column=0, columnspan=2, pady=10)

# Recent Expenses Button
recent_expenses_btn = tk.Button(root, text="Recent Expenses", command=show_recent_expenses, bg="#3a86ff", fg="white", relief="raised")
recent_expenses_btn.grid(row=10, column=0, columnspan=2, pady=5)

# Labels for displaying expenses and remaining budget
expenses_label = tk.Label(root, text="Current Expenses: N/A", bg="#2d3436", fg="#dfe6e9", font=("Helvetica", 12))
expenses_label.grid(row=11, column=0, columnspan=2, pady=5)
remaining_budget_label = tk.Label(root, text="Remaining Budget: N/A", bg="#2d3436", fg="#dfe6e9", font=("Helvetica", 12))
remaining_budget_label.grid(row=12, column=0, columnspan=2, pady=5)

# Existing Categories List
category_listbox_label = tk.Label(root, text="Categories", bg="#2d3436", fg="white", font=("Helvetica", 12, "bold"))
category_listbox_label.grid(row=13, column=0, columnspan=2, pady=5)

category_listbox = Listbox(root, height=5, width=50, bg="#34495e", fg="white", font=("Helvetica", 10))
category_listbox.grid(row=14, column=0, columnspan=2, padx=5, pady=5)

# Plot Expenses Button
plot_expenses_btn = tk.Button(root, text="Plot Expenses", command=plot_expenses, bg="#2a9d8f", fg="white", relief="raised")
plot_expenses_btn.grid(row=15, column=0, columnspan=2, pady=10)

# Initialize the application with existing data
refresh_categories()

# Start the Tkinter main loop
root.mainloop()