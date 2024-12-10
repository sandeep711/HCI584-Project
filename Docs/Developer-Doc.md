# Expense Tracker Application

## Overview

The **Expense Tracker Application** is a desktop-based tool built using Python's Tkinter library for UI and CSV for data storage. It allows users to manage their expenses by:
- Creating categories and budgets
- Adding expenses with descriptions
- Visualizing expenses using a bar chart

## Final Features

The following features from the initial planning specs are implemented:
- **Category Management**: Add, delete, and set budgets for categories
- **Expense Tracking**: Log expenses with associated descriptions under categories
- **Visualization**: Plot a bar chart showing total expenses by category
- **Data Persistence**: Save and load category data and expenses using CSV files

## Code Walkthrough

### Main Components

1. **App Initialization**:
   - **File**: `main.py`
   - **Function**: `main()`
   - Initializes the Tkinter root window and loads data from `data.csv`

2. **Category Management**:
   - **Class**: `CategoryManager`
   - **Key Functions**:
     - `add_category`: Adds a new category to the data dictionary
     - `delete_category`: Removes an existing category and its associated data

3. **Expense Tracking**:
   - **Class**: `ExpenseManager`
   - **Key Functions**:
     - `add_expense`: Validates user input and logs an expense with description
     - `save_data`: Writes the updated data dictionary to `data.csv`

4. **Visualization**:
   - **Module**: matplotlib
   - **Key Function**: `plot_expenses`
     - Reads data from the current session and plots a bar chart with category labels and values

5. **UI Layout**:
   - All UI components are arranged using Tkinter's grid layout

## Deployment

Ensure the following libraries/programs are installed and ready to go:

1. Python - Download and install Python from the official Python website.
2. Tkinter – run this code to install Tkinter : `sudo apt-get install python3-tk`
3. Matplotlib – run this code to install Matplotlib : `pip install matplotlib`
4. Pip – Ensure pip is installed - `python -m ensurepip --upgrade`

## Running the Application

Once the environment is set up and dependencies are installed, run this line of code to start the application : `python3 main.py`

## MacOS

From my experience with working on this project, Tkinter can face compatibility issues on macOS, particularly when run in VS Code's integrated terminal. To mitigate these issues, it's best to use an isolated Python virtual environment.

Instructions for those are:
1. Setup Virtual Environment : `python3 -m venv tkinter_env`
2. Activate the Environment: `source tkinter_env/bin/activate`
3. Install Required Packages : `python3 -m ensurepip --upgrade`
4. Final step is to run the application as usual :  `python3 main.py`

## Issues

1. UI scaling is inconsistent.
2. **Empty Description Field**: The current implementation allows saving expenses without a description, which may reduce clarity for the user. Validation is recommended.
3. **Data Overwrites**: If two instances of the application run simultaneously, changes may overwrite one another when saving.

## Future Works

1. Migrate data storage from CSV to a relational database like SQLite or MySQL.
2. Add multi-user support and user authentication for a more professional look.

## Conclusion

This guide serves as a comprehensive resource for developers working on the Expense Tracker Application. It provides an overview of the project structure, details user interaction with the app, and highlights areas for improvement and future work.
