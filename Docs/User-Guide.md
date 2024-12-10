# Expense Tracker Application User's Guide

## Introduction

This guide will help you install, set up, and run the Expense Tracker Application, a desktop tool built using Python's Tkinter for the UI and CSV for data storage. It lets you manage your expenses, create categories, log expenses, and visualize your spending.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python** (version 3.x) — Download and install from [python.org](https://www.python.org/)
- **pip** (Python package installer) — Typically included with Python. Verify installation with:
  ```
  python -m ensurepip --upgrade
  ```

## Required Libraries

1. **Tkinter** — This comes pre-installed with Python. Ensure it's installed by running:
   ```
   sudo apt-get install python3-tk
   ```

2. **Matplotlib** — Used for visualizing expenses. Install it using:
   ```
   pip install matplotlib
   ```

## Setup Instructions

### Step 1: Clone or Download the Repository

Make sure to clone or download the project into a suitable directory on your machine.

### Step 2: Set Up a Python Virtual Environment (Optional but Recommended)

1. Create a virtual environment (in the project directory):
   ```
   python3 -m venv env
   ```

2. Activate the environment:
   - On Windows:
     ```
     .\env\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source env/bin/activate
     ```

3. Install dependencies within the virtual environment:
   ```
   pip install -r requirements.txt
   ```

### Step 3: Verify and Install Required Packages

Ensure all necessary packages are installed:
```
pip install matplotlib
```

## Running the Application

Once you have set up your environment and installed the required libraries, follow these steps:

1. Run the application using the command:
   ```
   python main.py
   ```

2. The application window will launch, allowing you to manage categories, log expenses, and visualize data.

## How to Use the Application

### 1. Main Window Overview

Upon launching the application, you'll see:
- **Category Management Panel**: To create and delete categories and set budgets.
- **Expense Log Panel**: To add new expenses and associate them with categories.
- **Bar Chart Visualization**: A visual representation of your spending by category.

### 2. Creating Categories

- Navigate to the Category Management section.
- Enter a category name and budget amount.
- Click **Add Category** to create it.

### 3. Logging Expenses

- Go to the Expense Log section.
- Fill in the expense description, amount, and choose a category from the dropdown.
- Click **Add Expense** to record the entry.

### 4. Visualizing Expenses

- Click on the **View Chart** button to display a bar chart summarizing your expenses by category.

## Example Code for API or Key Usage (If Applicable)

The application does not use any third-party API keys, so there is no need for a `keys.py` or `.env` file for this project.

## Possible Errors and Troubleshooting

### Error: "No module named 'matplotlib'"
- **Solution**: Ensure you installed matplotlib by running:
  ```
  pip install matplotlib
  ```

### Error: "Tkinter not installed"
- **Solution**: Install Tkinter using:
  ```
  sudo apt-get install python3-tk
  ```

## Caveats and Limitations

- **UI Scaling**: The user interface may not scale well on all screen sizes or resolutions.
- **Empty Description Field**: You can save expenses without a description. It's advisable to add validation in future updates.
- **Data Overwrites**: Running two instances of the application at the same time may lead to data overwrites when saving.

## Future Improvements

- **Database Integration**: Move data storage to a database like SQLite or MySQL for scalability.
- **Multi-User Support**: Add user authentication and profile management.
- **Enhanced UI**: Improve the user interface for a more responsive and user-friendly experience.
- **Advanced Charts**: Include other types of data visualization like pie charts and trend lines.

By following this guide, users can install, set up, and run the Expense Tracker Application smoothly.
