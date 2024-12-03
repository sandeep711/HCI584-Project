import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Attempt to use a more modern Tk backend
try:
    import tkinter.tix as tix
except ImportError:
    tix = None

# File to store categories and expenses data
CSV_FILE = 'categories_expenses.csv'

# Load data from CSV file
def load_data():
    data = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                category, budget, expenses, *expense_details = row
                data[category] = {
                    'budget': float(budget), 
                    'expenses': float(expenses), 
                    'details': expense_details
                }
    return data

# Save data to CSV file
def save_data(data):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for category, values in data.items():
            writer.writerow([
                category, 
                values['budget'], 
                values['expenses']
            ] + values['details'])

# Function to update labels showing current and remaining budget
def update_budget_labels(category):
    current_expenses = data[category]['expenses']
    budget = data[category]['budget']
    remaining_budget = budget - current_expenses
    expenses_label.config(text=f"Current Expenses: ${current_expenses:.2f}")
    remaining_budget_label.config(text=f"Remaining Budget: ${remaining_budget:.2f}")
    
    # Update recent expenses treeview
    refresh_recent_expenses()

# Add a new category to the data
def add_category():
    category = category_entry.get().strip()
    budget = budget_entry.get().strip()
    
    if category and budget:
        try:
            budget = float(budget)
            if category not in data:
                data[category] = {'budget': budget, 'expenses': 0.0, 'details': []}
                save_data(data)
                refresh_categories(category)
                category_entry.delete(0, tk.END)
                budget_entry.delete(0, tk.END)
                messagebox.showinfo("Category Added", f"Category '{category}' added with a budget of ${budget:.2f}.")
            else:
                messagebox.showwarning("Duplicate Category", "This category already exists.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid budget amount.")
    else:
        messagebox.showwarning("Input Error", "Please enter both category and budget.")

# Add an expense to the selected category
def add_expense():
    category = selected_category.get()
    expense = expense_entry.get().strip()
    description = description_entry.get().strip()
    
    if category and expense and description:
        try:
            expense = float(expense)
            data[category]['expenses'] += expense
            data[category]['details'].append(f"{description}: {expense}")
            save_data(data)
            
            if data[category]['expenses'] > data[category]['budget']:
                messagebox.showwarning("Budget Exceeded", 
                    f"Expenses for '{category}' have exceeded the budget!\n"
                    f"Budget: ${data[category]['budget']:.2f}\n"
                    f"Total Expenses: ${data[category]['expenses']:.2f}"
                )
            
            # Clear expense entry fields
            expense_entry.delete(0, tk.END)
            description_entry.delete(0, tk.END)
            
            update_budget_labels(category)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for the expense.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields (category, expense, and description).")

# Refresh category dropdown and listbox
def refresh_categories(new_category=None):
    # Update category dropdown
    category_dropdown['menu'].delete(0, 'end')
    categories = list(data.keys())
    
    if categories:
        for category in categories:
            category_dropdown['menu'].add_command(
                label=category, 
                command=lambda cat=category: selected_category.set(cat)
            )
        
        # Set default category
        if new_category:
            selected_category.set(new_category)
        else:
            selected_category.set(categories[0])
    else:
        selected_category.set("No categories available")

# Refresh recent expenses treeview
def refresh_recent_expenses():
    # Clear existing items
    for i in recent_expenses_tree.get_children():
        recent_expenses_tree.delete(i)
    
    # Populate with recent expenses
    for category, details in data.items():
        for expense_detail in details['details']:
            description, amount = expense_detail.split(': ')
            recent_expenses_tree.insert('', 'end', values=(category, description, f"${float(amount):.2f}"))


def plot_detailed_expenses():
    plt.figure(figsize=(12, 7))
    
    # Prepare data for main and sub-expenses
    categories = []
    total_expenses = []
    sub_expenses = []
    sub_expense_details = []
    
    for category, cat_data in data.items():
        categories.append(category)
        total_expenses.append(cat_data['expenses'])
        
        # Collect sub-expenses and descriptions
        category_subs = []
        expense_details = []
        for detail in cat_data['details']:
            desc, amount = detail.split(': ')
            category_subs.append((desc, float(amount)))
            expense_details.append((desc, float(amount)))
        sub_expenses.append(category_subs)
        sub_expense_details.append(expense_details)
    
    # Create stacked bar chart for total expenses
    bar_width = 0.5
    bars = plt.bar(categories, total_expenses, width=bar_width, color='#2a9d8f', edgecolor='white')
    
    # Add sub-expense details with labels
    for i, (category_bars, sub_expense_list, expense_details) in enumerate(zip(bars, sub_expenses, sub_expense_details)):
        bottom = 0
        for desc, amount in sub_expense_list:
            plt.bar(category_bars.get_x() + bar_width/2, amount, width=bar_width/2, 
                    bottom=bottom, color='#e76f51', edgecolor='white', alpha=0.7)
            
            # Annotate the sub-expense
            plt.text(category_bars.get_x() + bar_width/2, bottom + amount / 2, 
                     f"{desc}\n${amount:.2f}", ha='center', va='center', fontsize=9, color='black')
            bottom += amount
    
    plt.title("Detailed Expenses by Category", fontsize=16, fontweight='bold')
    plt.xlabel("Categories", fontsize=12)
    plt.ylabel("Total Expenses", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


    
# Choose the most appropriate Tk root window
if tix and hasattr(tix, 'Tk'):
    root = tix.Tk()
else:
    root = tk.Tk()

root.title("Enhanced Expense Tracker")
root.geometry("700x800")
root.configure(bg="#2d3436")

# Custom style
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background="#2d3436", foreground="#dfe6e9")
style.configure('TButton', background="#2a9d8f", foreground="white")
style.configure('TEntry', background="white")

# Load data
data = load_data()

# Header
header = ttk.Label(root, text="Enhanced Expense Tracker", 
                   font=("Helvetica", 18, "bold"), 
                   background="#3a86ff", 
                   foreground="white", 
                   padding=10)
header.pack(fill='x', pady=(0, 10))

# Frame for input sections
input_frame = ttk.Frame(root, style='TFrame')
input_frame.pack(padx=20, fill='x')

# Add New Category Section
category_label = ttk.Label(input_frame, text="Add New Category", font=("Helvetica", 14))
category_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=5)

category_name_label = ttk.Label(input_frame, text="Category Name:")
category_name_label.grid(row=1, column=0, sticky='e', padx=5)
category_entry = ttk.Entry(input_frame, width=30)
category_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

budget_label = ttk.Label(input_frame, text="Budget:")
budget_label.grid(row=2, column=0, sticky='e', padx=5)
budget_entry = ttk.Entry(input_frame, width=30)
budget_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)

add_category_btn = ttk.Button(input_frame, text="Add Category", command=add_category)
add_category_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Add Expense Section
expense_label = ttk.Label(input_frame, text="Add Expense to Category", font=("Helvetica", 14))
expense_label.grid(row=4, column=0, columnspan=2, sticky='w', pady=5)

selected_category = tk.StringVar(root)
categories = list(data.keys()) if data else ["No categories available"]
selected_category.set(categories[0] if categories else "No categories available")

category_dropdown_label = ttk.Label(input_frame, text="Category:")
category_dropdown_label.grid(row=5, column=0, sticky='e', padx=5)
category_dropdown = ttk.OptionMenu(input_frame, selected_category, *categories)
category_dropdown.grid(row=5, column=1, sticky='w', padx=5, pady=5)

expense_amount_label = ttk.Label(input_frame, text="Expense Amount:")
expense_amount_label.grid(row=6, column=0, sticky='e', padx=5)
expense_entry = ttk.Entry(input_frame, width=30)
expense_entry.grid(row=6, column=1, sticky='w', padx=5, pady=5)

description_label = ttk.Label(input_frame, text="Description:")
description_label.grid(row=7, column=0, sticky='e', padx=5)
description_entry = ttk.Entry(input_frame, width=30)
description_entry.grid(row=7, column=1, sticky='w', padx=5, pady=5)

add_expense_btn = ttk.Button(input_frame, text="Add Expense", command=add_expense)
add_expense_btn.grid(row=8, column=0, columnspan=2, pady=10)

# Budget Status Labels
expenses_label = ttk.Label(input_frame, text="Current Expenses: $0.00", font=("Helvetica", 12, "bold"))
expenses_label.grid(row=9, column=0, columnspan=2, pady=5)

remaining_budget_label = ttk.Label(input_frame, text="Remaining Budget: $0.00", font=("Helvetica", 12, "bold"))
remaining_budget_label.grid(row=10, column=0, columnspan=2, pady=5)

# Recent Expenses Section
recent_expenses_label = ttk.Label(input_frame, text="Recent Expenses", font=("Helvetica", 14))
recent_expenses_label.grid(row=11, column=0, columnspan=2, sticky='w', pady=5)

# Treeview for Recent Expenses
recent_expenses_tree = ttk.Treeview(input_frame, columns=('Category', 'Description', 'Amount'), show='headings', height=5)
recent_expenses_tree.grid(row=12, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

# Define column headings
recent_expenses_tree.heading('Category', text='Category')
recent_expenses_tree.heading('Description', text='Description')
recent_expenses_tree.heading('Amount', text='Amount')

# Plot Expenses Button
plot_expenses_btn = ttk.Button(input_frame, text="Plot Detailed Expenses", command=plot_detailed_expenses)
plot_expenses_btn.grid(row=13, column=0, columnspan=2, pady=10)

# Initialize the application with existing data
refresh_categories()
refresh_recent_expenses()

# Start the Tkinter main loop
root.mainloop()