"""
Home Expense Management System with Authentication
Features: Mobile Number + Password + OTP Verification
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import hashlib
import time

# Set page configuration
st.set_page_config(
    page_title="Home Expense Tracker", 
    page_icon="💰", 
    layout="wide",
    initial_sidebar_state="auto" 
)

# Custom CSS for mobile responsiveness
st.markdown("""
    <style>
    /* Make the app more mobile-friendly */
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
        font-size: 16px !important;
    }
    
    /* Better spacing on mobile */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .element-container {
            margin-bottom: 0.5rem;
        }
        
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
    
    /* Login/Signup container styling */
    .auth-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 30px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# File paths
USERS_FILE = "users.csv"
SALARY_FILE = "monthly_salary.csv"
EXPENSES_FILE = "expenses.csv"

# ============================================
# AUTHENTICATION FUNCTIONS
# ============================================

def hash_password(password):
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load all registered users"""
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    return pd.DataFrame(columns=['mobile', 'password', 'name', 'created_at'])

def save_user(mobile, password, name):
    """Register a new user"""
    users_df = load_users()
    
    # Check if user already exists
    if mobile in users_df['mobile'].values:
        return False, "Mobile number already registered!"
    
    # Add new user
    new_user = pd.DataFrame({
        'mobile': [mobile],
        'password': [hash_password(password)],
        'name': [name],
        'created_at': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USERS_FILE, index=False)
    return True, "Registration successful!"

def verify_user(mobile, password):
    """Verify user credentials"""
    users_df = load_users()
    
    if mobile not in users_df['mobile'].values:
        return False, "Mobile number not registered!"
    
    user_data = users_df[users_df['mobile'] == mobile].iloc[0]
    
    if user_data['password'] == hash_password(password):
        return True, user_data['name']
    else:
        return False, "Incorrect password!"

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_simulation(mobile, otp):
    """
    Simulate sending OTP to mobile number
    In production, integrate with SMS API like Twilio, MSG91, or Fast2SMS
    """
    # For demo purposes, we'll display the OTP on screen
    # In production, this would send actual SMS
    return True

def get_user_filename(mobile, filename):
    """Create user-specific filename"""
    # Replace special characters in mobile number for filename
    safe_mobile = mobile.replace('+', '').replace(' ', '')
    return f"{safe_mobile}_{filename}"

# ============================================
# EXPENSE MANAGEMENT FUNCTIONS (User-specific)
# ============================================

def load_salary(mobile):
    """Load the monthly salary from user-specific file"""
    filename = get_user_filename(mobile, SALARY_FILE)
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        if not df.empty:
            return df.iloc[-1]['salary']
    return 0.0

def save_salary(mobile, salary):
    """Save monthly salary to user-specific file"""
    filename = get_user_filename(mobile, SALARY_FILE)
    df = pd.DataFrame({'salary': [salary], 'date': [datetime.now().strftime("%Y-%m-%d")]})
    if os.path.exists(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_csv(filename, index=False)

def load_expenses(mobile):
    """Load all expenses from user-specific file"""
    filename = get_user_filename(mobile, EXPENSES_FILE)
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        return df
    return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Note'])

def save_expense(mobile, date, category, amount, note):
    """Save a new expense to user-specific file"""
    filename = get_user_filename(mobile, EXPENSES_FILE)
    new_expense = pd.DataFrame({
        'Date': [date],
        'Category': [category],
        'Amount': [amount],
        'Note': [note]
    })
    
    df = load_expenses(mobile)
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(filename, index=False)

def delete_expense(mobile, index):
    """Delete a specific expense by index"""
    filename = get_user_filename(mobile, EXPENSES_FILE)
    df = load_expenses(mobile)
    if not df.empty and 0 <= index < len(df):
        df = df.drop(index).reset_index(drop=True)
        df.to_csv(filename, index=False)
        return True
    return False

def calculate_total_expenses(mobile):
    """Calculate the sum of all expenses"""
    df = load_expenses(mobile)
    if not df.empty:
        return df['Amount'].sum()
    return 0.0

def calculate_remaining_balance(mobile, salary):
    """Calculate how much money is left"""
    total_expenses = calculate_total_expenses(mobile)
    return salary - total_expenses

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_mobile' not in st.session_state:
    st.session_state.user_mobile = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'otp_code' not in st.session_state:
    st.session_state.otp_code = None
if 'otp_mobile' not in st.session_state:
    st.session_state.otp_mobile = None
if 'otp_timestamp' not in st.session_state:
    st.session_state.otp_timestamp = None
if 'temp_password' not in st.session_state:
    st.session_state.temp_password = None
if 'temp_name' not in st.session_state:
    st.session_state.temp_name = None

# ============================================
# AUTHENTICATION UI
# ============================================

def show_login_page():
    """Display login/signup page"""
    
    st.markdown("<h1 style='text-align: center;'>💰 Home Expense Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Manage your expenses with ease</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Create tabs for Login and Signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    # ========== LOGIN TAB ==========
    with tab1:
        st.subheader("Welcome Back!")
        
        with st.form("login_form"):
            mobile = st.text_input("📱 Mobile Number", placeholder="+92 XXX XXXXXXX", max_chars=15)
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if login_button:
                if not mobile or not password:
                    st.error("⚠️ Please fill in all fields!")
                elif len(mobile) < 10:
                    st.error("⚠️ Please enter a valid mobile number!")
                else:
                    # Verify credentials
                    success, result = verify_user(mobile, password)
                    
                    if success:
                        # Send OTP for verification
                        otp = generate_otp()
                        st.session_state.otp_code = otp
                        st.session_state.otp_mobile = mobile
                        st.session_state.temp_password = password
                        st.session_state.otp_timestamp = time.time()
                        st.session_state.otp_sent = True
                        
                        # Simulate sending OTP
                        send_otp_simulation(mobile, otp)
                        st.success(f"✅ OTP sent to {mobile}")
                        st.info(f"🔢 Your OTP is: **{otp}** (Demo Mode - In production, this will be sent via SMS)")
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
    
    # ========== SIGNUP TAB ==========
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("signup_form"):
            name = st.text_input("👤 Full Name", placeholder="Enter your name")
            mobile = st.text_input("📱 Mobile Number", placeholder="+92 XXX XXXXXXX", max_chars=15, key="signup_mobile")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a password", key="signup_password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
            
            signup_button = st.form_submit_button("📝 Sign Up", use_container_width=True)
            
            if signup_button:
                if not name or not mobile or not password or not confirm_password:
                    st.error("⚠️ Please fill in all fields!")
                elif len(mobile) < 10:
                    st.error("⚠️ Please enter a valid mobile number!")
                elif len(password) < 6:
                    st.error("⚠️ Password must be at least 6 characters!")
                elif password != confirm_password:
                    st.error("⚠️ Passwords do not match!")
                else:
                    # Register user
                    success, message = save_user(mobile, password, name)
                    
                    if success:
                        # Send OTP for verification
                        otp = generate_otp()
                        st.session_state.otp_code = otp
                        st.session_state.otp_mobile = mobile
                        st.session_state.temp_password = password
                        st.session_state.temp_name = name
                        st.session_state.otp_timestamp = time.time()
                        st.session_state.otp_sent = True
                        
                        send_otp_simulation(mobile, otp)
                        st.success(f"✅ {message}")
                        st.info(f"🔢 Your OTP is: **{otp}** (Demo Mode)")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

def show_otp_verification():
    """Display OTP verification page"""
    
    st.markdown("<h1 style='text-align: center;'>🔐 OTP Verification</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>OTP sent to: <strong>{st.session_state.otp_mobile}</strong></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Check OTP expiry (5 minutes)
    if st.session_state.otp_timestamp:
        elapsed_time = time.time() - st.session_state.otp_timestamp
        if elapsed_time > 300:  # 5 minutes
            st.error("⏰ OTP expired! Please login again.")
            if st.button("🔙 Back to Login"):
                st.session_state.otp_sent = False
                st.session_state.otp_code = None
                st.rerun()
            return
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info(f"🔢 **Demo OTP:** {st.session_state.otp_code}")
        st.caption("In production, OTP will be sent via SMS")
        
        with st.form("otp_form"):
            otp_input = st.text_input("Enter OTP", placeholder="Enter 6-digit OTP", max_chars=6)
            
            col_a, col_b = st.columns(2)
            with col_a:
                verify_button = st.form_submit_button("✅ Verify", use_container_width=True)
            with col_b:
                resend_button = st.form_submit_button("🔄 Resend OTP", use_container_width=True)
            
            if verify_button:
                if otp_input == st.session_state.otp_code:
                    # OTP verified - log in user
                    st.session_state.authenticated = True
                    st.session_state.user_mobile = st.session_state.otp_mobile
                    
                    # Get user name
                    users_df = load_users()
                    if st.session_state.otp_mobile in users_df['mobile'].values:
                        st.session_state.user_name = users_df[users_df['mobile'] == st.session_state.otp_mobile].iloc[0]['name']
                    
                    # Clear OTP data
                    st.session_state.otp_sent = False
                    st.session_state.otp_code = None
                    
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid OTP! Please try again.")
            
            if resend_button:
                # Generate new OTP
                new_otp = generate_otp()
                st.session_state.otp_code = new_otp
                st.session_state.otp_timestamp = time.time()
                send_otp_simulation(st.session_state.otp_mobile, new_otp)
                st.success(f"✅ New OTP sent!")
                st.info(f"🔢 Your new OTP is: **{new_otp}**")
                st.rerun()
        
        if st.button("🔙 Back to Login", use_container_width=True):
            st.session_state.otp_sent = False
            st.session_state.otp_code = None
            st.rerun()



def show_expense_tracker():
    """Display the main expense tracker interface"""
    
    user_mobile = st.session_state.user_mobile
    user_name = st.session_state.user_name
    
    # Title with user info
    col_title, col_logout = st.columns([3, 1])
    with col_title:
        st.title(f"💰 Welcome, {user_name}!")
    with col_logout:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_mobile = None
            st.session_state.user_name = None
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar for Monthly Salary
    st.sidebar.header("💵 Monthly Budget")
    
    current_salary = load_salary(user_mobile)
    
    if current_salary > 0:
        st.sidebar.success(f"Current Monthly Salary: PKR {current_salary:,.2f}")
    
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
            save_salary(user_mobile, new_salary)
            st.success("✅ Salary saved successfully!")
            st.rerun()
    
    # Calculate values
    total_expenses = calculate_total_expenses(user_mobile)
    remaining_balance = calculate_remaining_balance(user_mobile, current_salary)
    
    # Financial Summary
    st.header("📊 Financial Summary")
    
    summary_cols = st.columns(3, gap="small")
    
    with summary_cols[0]:
        st.metric(
            "Monthly Salary", 
            f"PKR {current_salary:,.2f}",
            help="Your monthly income"
        )
    
    with summary_cols[1]:
        st.metric(
            "Total Expenses", 
            f"PKR {total_expenses:,.2f}",
            help="Sum of all expenses"
        )
    
    with summary_cols[2]:
        if remaining_balance < 0:
            st.metric(
                "Remaining", 
                f"PKR {remaining_balance:,.2f}", 
                delta="Over Budget!", 
                delta_color="inverse",
                help="Amount remaining from salary"
            )
        else:
            st.metric(
                "Remaining", 
                f"PKR {remaining_balance:,.2f}",
                help="Amount remaining from salary"
            )
    
    st.markdown("---")
    
    # Add New Expense Form
    st.header("📝 Add New Expense")
    
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
        
        submit_expense = st.form_submit_button("➕ Add Expense", use_container_width=True)
        
        if submit_expense:
            if amount > 0:
                save_expense(user_mobile, expense_date, category, amount, note)
                st.success("✅ Expense added successfully!")
                st.rerun()
            else:
                st.error("⚠️ Please enter a valid amount!")
    
    st.markdown("---")
    
    # All Expenses
    st.header("📋 All Expenses")
    
    expenses_df = load_expenses(user_mobile)
    
    if not expenses_df.empty:
        expenses_df = expenses_df.sort_values('Date', ascending=False)
        
        # Add selection column for deletion
        expenses_display = expenses_df.copy()
        expenses_display.insert(0, 'Select', False)
        
        st.dataframe(
            expenses_df, 
            use_container_width=True, 
            hide_index=True,
            height=350
        )
        
        # Download button
        csv = expenses_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Expenses as CSV",
            data=csv,
            file_name=f'expenses_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        # Expense Analysis
        st.markdown("---")
        st.header("📈 Expense Analysis")
        
        chart_col1, chart_col2 = st.columns([1, 1], gap="large")
        
        with chart_col1:
            st.subheader("Expenses by Category")
            category_expenses = expenses_df.groupby('Category')['Amount'].sum().reset_index()
            st.bar_chart(category_expenses.set_index('Category'), height=300)
        
        with chart_col2:
            st.subheader("Category Breakdown")
            category_expenses = expenses_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
            
            for category, amount in category_expenses.items():
                percentage = (amount / total_expenses) * 100
                st.write(f"**{category}:** PKR {amount:,.2f} ({percentage:.1f}%)")
        
        # Expense Insights
        st.markdown("---")
        st.header("💡 Expense Insights")
        
        insight_cols = st.columns([1, 1, 1])
        
        with insight_cols[0]:
            date_range = (pd.to_datetime(expenses_df['Date'].max()) - pd.to_datetime(expenses_df['Date'].min())).days + 1
            avg_per_day = total_expenses / max(date_range, 1)
            st.metric("Avg. Expense/Day", f"PKR {avg_per_day:,.2f}")
        
        with insight_cols[1]:
            top_category = category_expenses.idxmax()
            top_amount = category_expenses.max()
            st.metric("Top Category", f"{top_category}", f"PKR {top_amount:,.2f}")
        
        with insight_cols[2]:
            st.metric("Total Transactions", len(expenses_df))
        
        # Data Management
        st.markdown("---")
        st.subheader("⚙️ Data Management")
        
        col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
        
        with col_clear2:
            if st.button("🗑️ Clear All Expenses", type="secondary", use_container_width=True):
                filename = get_user_filename(user_mobile, EXPENSES_FILE)
                if os.path.exists(filename):
                    os.remove(filename)
                    st.success("✅ All expenses cleared!")
                    st.rerun()
    
    else:
        st.info("📱 No expenses recorded yet. Add your first expense above! 👆")
        st.markdown("""
            ### How to use:
            1. **Set your monthly salary** in the sidebar
            2. **Add expenses** using the form above
            3. **Track your spending** with charts and insights
            4. **View all transactions** in the table
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 20px;'>
            <p>💡 <strong>Tip:</strong> This app helps you track and manage your expenses effectively!</p>
            <p style='font-size: 0.9em;'>Powered by Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if not st.session_state.authenticated:
    if st.session_state.otp_sent:
        show_otp_verification()
    else:
        show_login_page()
else:
    show_expense_tracker()