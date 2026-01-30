# 💰 Home Expense Management System

A simple and beginner-friendly expense tracker built with Python and Streamlit.

## 📋 Features

- ✅ Set monthly salary/income
- ✅ Add daily/weekly expenses with categories
- ✅ Automatic calculation of total expenses and remaining balance
- ✅ View all expenses in a table
- ✅ Visualize expenses with charts
- ✅ Data saved locally in CSV files
- ✅ Clean and simple user interface

## 🚀 How to Run

### Step 1: Install Python
Make sure you have Python 3.7 or higher installed on your computer.

### Step 2: Install Required Libraries
Open terminal/command prompt and run:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit pandas
```

### Step 3: Run the Application
```bash
streamlit run expense_tracker.py
```

The app will automatically open in your web browser at `http://localhost:8501`

## 📖 How to Use

1. **Set Monthly Salary**: Enter your monthly salary in the sidebar and click "Save Salary"
2. **Add Expense**: Fill in the expense form (date, category, amount, note) and click "Add Expense"
3. **View Summary**: See your total expenses and remaining balance in the summary section
4. **Analyze Expenses**: Scroll down to see all expenses in a table and charts by category
5. **Clear Data**: Use the "Clear All Expenses" button to start fresh

## 📂 Files Created

- `expense_tracker.py` - Main application code
- `monthly_salary.csv` - Stores your monthly salary (auto-created)
- `expenses.csv` - Stores all your expenses (auto-created)

## 🎓 Code Explanation for Beginners

### 1. Imports
```python
import streamlit as st      # For creating the web app
import pandas as pd         # For handling data (tables)
from datetime import datetime  # For working with dates
import os                   # For file operations
```

### 2. File Paths
```python
SALARY_FILE = "monthly_salary.csv"
EXPENSES_FILE = "expenses.csv"
```
These variables store the names of files where data is saved.

### 3. Helper Functions

**`load_salary()`**
- Reads the salary from CSV file
- Returns the most recent salary value
- Returns 0.0 if no salary is saved

**`save_salary(salary)`**
- Saves the salary to CSV file with current date
- Appends to existing file or creates new one

**`load_expenses()`**
- Reads all expenses from CSV file
- Returns a pandas DataFrame (like a table)
- Returns empty DataFrame if file doesn't exist

**`save_expense(date, category, amount, note)`**
- Creates a new expense record
- Adds it to existing expenses
- Saves everything to CSV file

**`calculate_total_expenses()`**
- Loads all expenses
- Sums up all the amounts
- Returns total

**`calculate_remaining_balance(salary)`**
- Calculates: Salary - Total Expenses
- Shows how much money is left

### 4. Streamlit Components Used

**`st.title()`** - Creates a large heading

**`st.header()`** - Creates a section heading

**`st.sidebar`** - Creates a sidebar on the left

**`st.form()`** - Creates a form with submit button

**`st.number_input()`** - Number input field

**`st.selectbox()`** - Dropdown menu

**`st.date_input()`** - Date picker

**`st.text_input()`** - Text input field

**`st.columns()`** - Creates side-by-side columns

**`st.metric()`** - Displays a metric card

**`st.dataframe()`** - Displays a data table

**`st.bar_chart()`** - Creates a bar chart

**`st.button()`** - Creates a clickable button

**`st.rerun()`** - Refreshes the app

### 5. How Data Flows

1. User enters salary → Saved to `monthly_salary.csv`
2. User adds expense → Saved to `expenses.csv`
3. App loads data from CSV files
4. Calculations happen (total, remaining)
5. Data displayed in tables and charts

### 6. CSV File Structure

**monthly_salary.csv**
```
salary,date
50000,2024-01-01
55000,2024-02-01
```

**expenses.csv**
```
Date,Category,Amount,Note
2024-01-15,Food,500,Groceries
2024-01-16,Rent,15000,Monthly rent
```

## 🎨 Customization Ideas

You can easily customize this app:

1. **Add more categories**: Edit the category list in `st.selectbox()`
2. **Change currency symbol**: Replace ₹ with $ or €
3. **Add date filter**: Filter expenses by date range
4. **Export to Excel**: Add a download button
5. **Add budget alerts**: Show warning when exceeding budget

## 🐛 Troubleshooting

**App doesn't start**
- Make sure Streamlit is installed: `pip install streamlit`
- Check Python version: `python --version` (should be 3.7+)

**Data not saving**
- Check if you have write permissions in the folder
- CSV files should be created automatically

**Charts not showing**
- Make sure you have added at least one expense
- Check that amounts are valid numbers

## 📝 Notes

- Data is stored locally on your computer
- CSV files are created in the same folder as the script
- No internet connection required
- All calculations happen instantly
- Simple and lightweight - no database needed!

## 🔜 Future Enhancements

- Monthly expense comparison
- Budget limits per category
- Export reports to PDF
- Multiple users support
- Recurring expenses
- Income sources tracking

---

**Made with ❤️ for beginners learning Python and Streamlit**
