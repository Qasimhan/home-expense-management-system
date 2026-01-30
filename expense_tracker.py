import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="Home Expense Tracker", 
    page_icon="", 
    layout="wide",
    initial_sidebar_state="auto" 
)


st.markdown("""
    <style>
     Make the app more mobile-friendly */
    .main .block-container {
        padding-top: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Responsive font sizes */
    h1 {
        font-size: clamp(1.5rem, 5vw, 2.5rem) !important;
    }
    
    h2 {
        font-size: clamp(1.2rem, 4vw, 1.8rem) !important;
    }
    
    h3 {
        font-size: clamp(1rem, 3vw, 1.5rem) !important;
    }
    
    /* Make metrics more readable on mobile */
    [data-testid="stMetricValue"] {
        font-size: clamp(1rem, 4vw, 2rem) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: clamp(0.8rem, 2.5vw, 1rem) !important;
    }
    
    /* Ensure tables are scrollable on mobile */
    [data-testid="stDataFrame"] {
        overflow-x: auto;
        font-size: clamp(0.8rem, 2vw, 1rem);
    }
    
    /* Better form inputs on mobile */
    input, select, textarea {
        font-size: 16px !important; /* Prevents zoom on iOS 
    }
    
    /* Better spacing on mobile */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        /* Reduce gap between elements */
        .element-container {
            margin-bottom: 0.5rem;
        }
        
        /* Make sidebar collapsible on mobile */
        section[data-testid="stSidebar"] {
            width: 280px !important;
        }
    }
    
    /* Extra small devices */
    @media (max-width: 480px) {
        h1 {
            font-size: 1.5rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)
SALARY_FILE = "monthly_salary.csv"
EXPENSES_FILE = "expenses.csv"

def load_salary():
    """Load the monthly salary from file"""
    if os.path.exists(SALARY_FILE):
        df = pd.read_csv(SALARY_FILE)
        if not df.empty:
            return df.iloc[-1]['salary']  
    return 0.0

def save_salary(salary):
    """Save monthly salary to file"""
    df = pd.DataFrame({'salary': [salary], 'date': [datetime.now().strftime("%Y-%m-%d")]})
    if os.path.exists(SALARY_FILE):
        existing_df = pd.read_csv(SALARY_FILE)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_csv(SALARY_FILE, index=False)

def load_expenses():
    """Load all expenses from file"""
    if os.path.exists(EXPENSES_FILE):
        df = pd.read_csv(EXPENSES_FILE)
        return df
    return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Note'])

def save_expense(date, category, amount, note):
    """Save a new expense to file"""
    new_expense = pd.DataFrame({
        'Date': [date],
        'Category': [category],
        'Amount': [amount],
        'Note': [note]
    })
    
    df = load_expenses()
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(EXPENSES_FILE, index=False)

def calculate_total_expenses():
    """Calculate the sum of all expenses"""
    df = load_expenses()
    if not df.empty:
        return df['Amount'].sum()
    return 0.0

def calculate_remaining_balance(salary):
    """Calculate how much money is left"""
    total_expenses = calculate_total_expenses()
    return salary - total_expenses

st.title(" Home Expense Management System")
st.markdown("---")
st.sidebar.header(" Monthly Budget")

current_salary = load_salary()

if current_salary > 0:
    st.sidebar.success(f"Current Monthly Salary: PKR:{current_salary:,.2f}")

with st.sidebar.form("salary_form"):
    st.subheader("Set Monthly Salary")
    new_salary = st.number_input(
        "Enter your monthly salary", 
        min_value=0.0, 
        value=float(current_salary), 
        step=1000.0,
        help="Set your monthly income/budget"
    )
    submit_salary = st.form_submit_button("💾 Save Salary", use_container_width=True)
    
    if submit_salary:
        save_salary(new_salary)
        st.success(" Salary saved successfully!")
        st.rerun()

total_expenses = calculate_total_expenses()
remaining_balance = calculate_remaining_balance(current_salary)

st.header("📊 Financial Summary")

# Display summary metrics - will stack on mobile
summary_cols = st.columns(3, gap="small")

with summary_cols[0]:
    st.metric(
        "Monthly Salary", 
        f"PKR:{current_salary:,.2f}",
        help="Your monthly income"
    )

with summary_cols[1]:
    st.metric(
        "Total Expenses", 
        f"PKR:{total_expenses:,.2f}",
        help="Sum of all expenses"
    )

with summary_cols[2]:
    # Show in red if negative, green if positive
    if remaining_balance < 0:
        st.metric(
            "Remaining", 
            f"PKR:{remaining_balance:,.2f}", 
            delta="Over Budget!", 
            delta_color="inverse",
            help="Amount remaining from salary"
        )
    else:
        st.metric(
            "Remaining", 
            f"PKR:{remaining_balance:,.2f}",
            help="Amount remaining from salary"
        )

st.markdown("---")

st.header(" Add New Expense")

with st.form("expense_form"):
    form_col1, form_col2 = st.columns([1, 1])
    
    with form_col1:
     
        expense_date = st.date_input("Date", value=datetime.now())
        
       
        category = st.selectbox(
            "Category",
            ["Food", "Rent", "Electricity", "Gas", "Education", "Medical", "Other"]
        )
    
    with form_col2:
      
        amount = st.number_input("Amount (PKR)", min_value=0.0, step=10.0)
        
        
        note = st.text_input("Note (Optional)", "", max_chars=100)
    
  
    submit_expense = st.form_submit_button(" Add Expense", use_container_width=True)
    
    if submit_expense:
        if amount > 0:
            save_expense(expense_date, category, amount, note)
            st.success(" Expense added successfully!")
            st.rerun()  # Refresh the app
        else:
            st.error(" Please enter a valid amount!")

st.markdown("---")


st.header(" All Expenses")

expenses_df = load_expenses()

if not expenses_df.empty:
  
    expenses_df = expenses_df.sort_values('Date', ascending=False)
    
    st.dataframe(
        expenses_df, 
        use_container_width=True, 
        hide_index=True,
        height=350  
    )
    

    csv = expenses_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Expenses as CSV",
        data=csv,
        file_name=f'expenses_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        use_container_width=True
    )
    
    
    st.markdown("---")
    st.header(" Expense Analysis")
    
    chart_col1, chart_col2 = st.columns([1, 1], gap="large")
    
    with chart_col1:
        st.subheader("Expenses by Category")
        # Group expenses by category and sum amounts
        category_expenses = expenses_df.groupby('Category')['Amount'].sum().reset_index()
        st.bar_chart(category_expenses.set_index('Category'), height=300)
    
    with chart_col2:
        st.subheader("Category Breakdown")

        category_expenses = expenses_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        
        for category, amount in category_expenses.items():
            percentage = (amount / total_expenses) * 100
            st.write(f"**{category}:** PKR:{amount:,.2f} ({percentage:.1f}%)")
        

    
    st.markdown("---")
    st.header(" Expense Insights")
    
    insight_cols = st.columns([1, 1, 1])
    
    with insight_cols[0]:
       
        date_range = (pd.to_datetime(expenses_df['Date'].max()) - pd.to_datetime(expenses_df['Date'].min())).days + 1
        avg_per_day = total_expenses / max(date_range, 1)
        st.metric("Avg. Expense/Day", f"PKR:{avg_per_day:,.2f}")
    
    with insight_cols[1]:
      
        top_category = category_expenses.idxmax()
        top_amount = category_expenses.max()
        st.metric("Top Category", f"{top_category}", f"PKR:{top_amount:,.2f}")
    
    with insight_cols[2]:
        
        st.metric("Total Transactions", len(expenses_df))
    
    # Option to clear all data
    st.markdown("---")
    st.subheader(" Data Management")
    
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    
    with col_clear2:
        #CLEAR SINGLE EXPENSE NOT ALL DELETE ALL
        if st.button(" Clear All Expenses", type="secondary", use_container_width=True):
            if os.path.exists(EXPENSES_FILE):
                
                os.remove(EXPENSES_FILE)
                st.success(" All expenses cleared!")
                st.rerun()
    
else:
    st.info("📱 No expenses recorded yet. Add your first expense above! 👆")
    st.markdown("""
        ### How to use:
        1. **Set your monthly salary** in the sidebar (left menu on mobile)
        2. **Add expenses** using the form above
        3. **Track your spending** with charts and insights
        4. **View all transactions** in the table
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p> <strong>Tip:</strong> This app helps you track and manage your expenses effectively!</p>
        <p style='font-size: 0.9em;'>Powered by Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)