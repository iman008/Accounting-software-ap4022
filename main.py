import re
import time
import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

conn = sqlite3.connect("finance_manager.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    password TEXT,
    city TEXT,
    email TEXT,
    birthdate TEXT,
    security_question TEXT,
    security_answer TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS incomes (
    username TEXT,
    amount REAL,
    date TEXT,
    source TEXT,
    description TEXT,
    type TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
    username TEXT,
    amount REAL,
    date TEXT,
    category TEXT,
    description TEXT,
    type TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
    username TEXT,
    category TEXT
)''')

conn.commit()

def execute_query(query, params=()):
    cursor.execute(query, params)
    conn.commit()

def fetch_all(query, params=()):
    cursor.execute(query, params)
    return cursor.fetchall()

def fetch_one(query, params=()):
    cursor.execute(query, params)
    return cursor.fetchone()

def load_users():
    return {row[0]: row for row in fetch_all("SELECT * FROM users")}

def save_user(user_data):
    execute_query('''INSERT INTO users (username, first_name, last_name, phone, password, city, email, birthdate, security_question, security_answer)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', user_data)

def load_incomes(username):
    return fetch_all("SELECT * FROM incomes WHERE username=?", (username,))

def save_income(income_data):
    execute_query('''INSERT INTO incomes (username, amount, date, source, description, type)
                     VALUES (?, ?, ?, ?, ?, ?)''', income_data)

def load_expenses(username):
    return fetch_all("SELECT * FROM expenses WHERE username=?", (username,))

def save_expense(expense_data):
    execute_query('''INSERT INTO expenses (username, amount, date, category, description, type)
                     VALUES (?, ?, ?, ?, ?, ?)''', expense_data)

def load_categories(username):
    return [row[0] for row in fetch_all("SELECT category FROM categories WHERE username=?", (username,))]

def save_category(category_data):
    execute_query('''INSERT INTO categories (username, category)
                     VALUES (?, ?)''', category_data)

def is_valid_name(name):
    return name.isalpha()

def is_valid_phone(phone):
    return phone.isdigit() and phone.startswith("09") and len(phone) == 11

def is_valid_password(password):
    if len(password) < 6:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*()_+]", password):
        return False
    return True

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9]+@(gmail|yahoo)\.com$", email) is not None

def is_valid_birthdate(date_text):
    try:
        date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return 1920 <= date.year <= 2005
    except ValueError:
        return False

def is_valid_amount(amount):
    try:
        float_amount = float(amount)
        return float_amount > 0
    except ValueError:
        return False
    
def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_cities():
    return ["Tehran", "Mashhad", "Isfahan", "Karaj", "Tabriz", "Shiraz", "Qom", "Ahvaz", "Kermanshah", "Urmia"]

def signup():
    def handle_signup():
        users = load_users()

        first_name = first_name_entry.get()
        if not is_valid_name(first_name):
            messagebox.showerror("Error", "Invalid first name. Use English letters only.")
            return

        last_name = last_name_entry.get()
        if not is_valid_name(last_name):
            messagebox.showerror("Error", "Invalid last name. Use English letters only.")
            return

        phone = phone_entry.get()
        if not is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone number. Must start with 09 and be 11 digits long.")
            return

        username = username_entry.get()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
            return

        password = password_entry.get()
        if not is_valid_password(password):
            messagebox.showerror("Error", "Invalid password. Must contain at least one lowercase letter, one uppercase letter, one digit, one symbol, and be at least 6 characters long.")
            return

        confirm_password = confirm_password_entry.get()
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        city = city_entry.get()
        if city not in get_cities():
            messagebox.showerror("Error", "Invalid city.")
            return

        email = email_entry.get()
        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email.")
            return

        birthdate = birthdate_entry.get()
        if not is_valid_birthdate(birthdate):
            messagebox.showerror("Error", "Invalid birthdate.")
            return

        security_question = security_question_entry.get()
        security_answer = security_answer_entry.get()

        user_data = (username, first_name, last_name, phone, password, city, email, birthdate, security_question, security_answer)
        save_user(user_data)
        messagebox.showinfo("Success", "Registration successful. You can now log in.")
        signup_window.destroy()

    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")

    tk.Label(signup_window, text="First Name").grid(row=0, column=0)
    first_name_entry = tk.Entry(signup_window)
    first_name_entry.grid(row=0, column=1)

    tk.Label(signup_window, text="Last Name").grid(row=1, column=0)
    last_name_entry = tk.Entry(signup_window)
    last_name_entry.grid(row=1, column=1)

    tk.Label(signup_window, text="Phone").grid(row=2, column=0)
    phone_entry = tk.Entry(signup_window)
    phone_entry.grid(row=2, column=1)

    tk.Label(signup_window, text="Username").grid(row=3, column=0)
    username_entry = tk.Entry(signup_window)
    username_entry.grid(row=3, column=1)

    tk.Label(signup_window, text="Password").grid(row=4, column=0)
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.grid(row=4, column=1)

    tk.Label(signup_window, text="Confirm Password").grid(row=5, column=0)
    confirm_password_entry = tk.Entry(signup_window, show="*")
    confirm_password_entry.grid(row=5, column=1)

    tk.Label(signup_window, text="City").grid(row=6, column=0)
    city_entry = tk.Entry(signup_window)
    city_entry.grid(row=6, column=1)

    tk.Label(signup_window, text="Email").grid(row=7, column=0)
    email_entry = tk.Entry(signup_window)
    email_entry.grid(row=7, column=1)

    tk.Label(signup_window, text="Birthdate (YYYY-MM-DD)").grid(row=8, column=0)
    birthdate_entry = tk.Entry(signup_window)
    birthdate_entry.grid(row=8, column=1)

    tk.Label(signup_window, text="Security Question").grid(row=9, column=0)
    security_question_entry = tk.Entry(signup_window)
    security_question_entry.grid(row=9, column=1)

    tk.Label(signup_window, text="Security Answer").grid(row=10, column=0)
    security_answer_entry = tk.Entry(signup_window)
    security_answer_entry.grid(row=10, column=1)

    tk.Button(signup_window, text="Sign Up", command=handle_signup).grid(row=11, column=0, columnspan=2)

def login():
    def handle_login():
        users = load_users()
        username = username_entry.get()
        password = password_entry.get()

        if username in users and users[username][4] == password:
            messagebox.showinfo("Success", "Login successful.")
            login_window.destroy()
            user_menu(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    login_window = tk.Toplevel()
    login_window.title("Log In")

    tk.Label(login_window, text="Username").grid(row=0, column=0)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Password").grid(row=1, column=0)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(login_window, text="Log In", command=handle_login).grid(row=2, column=0, columnspan=2)

def add_income(username):
    def handle_add_income():
        amount = amount_entry.get()
        date = date_entry.get()
        source = source_entry.get()
        description = description_entry.get()
        type_ = type_entry.get()

        if not is_valid_amount(amount):
            messagebox.showerror("Error", "Invalid amount.")
            return

        if not is_valid_date(date):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        income_data = (username, amount, date, source, description, type_)
        save_income(income_data)
        messagebox.showinfo("Success", "Income added successfully.")
        add_income_window.destroy()

    add_income_window = tk.Toplevel()
    add_income_window.title("Add Income")

    tk.Label(add_income_window, text="Amount").grid(row=0, column=0)
    amount_entry = tk.Entry(add_income_window)
    amount_entry.grid(row=0, column=1)

    tk.Label(add_income_window, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
    date_entry = tk.Entry(add_income_window)
    date_entry.grid(row=1, column=1)

    tk.Label(add_income_window, text="Source").grid(row=2, column=0)
    source_entry = tk.Entry(add_income_window)
    source_entry.grid(row=2, column=1)

    tk.Label(add_income_window, text="Description").grid(row=3, column=0)
    description_entry = tk.Entry(add_income_window)
    description_entry.grid(row=3, column=1)

    tk.Label(add_income_window, text="Type").grid(row=4, column=0)
    type_entry = tk.Entry(add_income_window)
    type_entry.grid(row=4, column=1)

    tk.Button(add_income_window, text="Add Income", command=handle_add_income).grid(row=5, column=0, columnspan=2)

def add_expense(username):
    def handle_add_expense():
        amount = amount_entry.get()
        date = date_entry.get()
        category = category_entry.get()
        description = description_entry.get()
        type_ = type_entry.get()

        if not is_valid_amount(amount):
            messagebox.showerror("Error", "Invalid amount.")
            return

        if not is_valid_date(date):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        expense_data = (username, amount, date, category, description, type_)
        save_expense(expense_data)
        messagebox.showinfo("Success", "Expense added successfully.")
        add_expense_window.destroy()

    add_expense_window = tk.Toplevel()
    add_expense_window.title("Add Expense")

    tk.Label(add_expense_window, text="Amount").grid(row=0, column=0)
    amount_entry = tk.Entry(add_expense_window)
    amount_entry.grid(row=0, column=1)

    tk.Label(add_expense_window, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
    date_entry = tk.Entry(add_expense_window)
    date_entry.grid(row=1, column=1)

    tk.Label(add_expense_window, text="Category").grid(row=2, column=0)
    category_entry = tk.Entry(add_expense_window)
    category_entry.grid(row=2, column=1)

    tk.Label(add_expense_window, text="Description").grid(row=3, column=0)
    description_entry = tk.Entry(add_expense_window)
    description_entry.grid(row=3, column=1)

    tk.Label(add_expense_window, text="Type").grid(row=4, column=0)
    type_entry = tk.Entry(add_expense_window)
    type_entry.grid(row=4, column=1)

    tk.Button(add_expense_window, text="Add Expense", command=handle_add_expense).grid(row=5, column=0, columnspan=2)

def add_category(username):
    def handle_add_category():
        category = category_entry.get()
        category_data = (username, category)
        save_category(category_data)
        messagebox.showinfo("Success", "Category added successfully.")
        add_category_window.destroy()

    add_category_window = tk.Toplevel()
    add_category_window.title("Add Category")

    tk.Label(add_category_window, text="Category").grid(row=0, column=0)
    category_entry = tk.Entry(add_category_window)
    category_entry.grid(row=0, column=1)

    tk.Button(add_category_window, text="Add Category", command=handle_add_category).grid(row=1, column=0, columnspan=2)

def search_records(username):
    def handle_search():
        term = search_term_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        record_type = record_type_var.get()
        min_amount = min_amount_entry.get()
        max_amount = max_amount_entry.get()
        fields = [field for field, var in search_fields.items() if var.get()]

        query = "SELECT * FROM {} WHERE username=?".format(record_type)

        params = [username]
        if term:
            term_conditions = " OR ".join([f"{field} LIKE ?" for field in fields])
            query += f" AND ({term_conditions})"
            params += [f"%{term}%"] * len(fields)
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if min_amount:
            query += " AND amount >= ?"
            params.append(min_amount)
        if max_amount:
            query += " AND amount <= ?"
            params.append(max_amount)

        records = fetch_all(query, params)
        for record in records:
            results_tree.insert("", tk.END, values=record)

    search_window = tk.Toplevel()
    search_window.title("Search Records")

    tk.Label(search_window, text="Search Term").grid(row=0, column=0)
    search_term_entry = tk.Entry(search_window)
    search_term_entry.grid(row=0, column=1)

    tk.Label(search_window, text="Start Date (YYYY-MM-DD)").grid(row=1, column=0)
    start_date_entry = tk.Entry(search_window)
    start_date_entry.grid(row=1, column=1)

    tk.Label(search_window, text="End Date (YYYY-MM-DD)").grid(row=2, column=0)
    end_date_entry = tk.Entry(search_window)
    end_date_entry.grid(row=2, column=1)

    tk.Label(search_window, text="Record Type").grid(row=3, column=0)
    record_type_var = tk.StringVar(value="incomes")
    tk.Radiobutton(search_window, text="Incomes", variable=record_type_var, value="incomes").grid(row=3, column=1)
    tk.Radiobutton(search_window, text="Expenses", variable=record_type_var, value="expenses").grid(row=3, column=2)

    tk.Label(search_window, text="Min Amount").grid(row=4, column=0)
    min_amount_entry = tk.Entry(search_window)
    min_amount_entry.grid(row=4, column=1)

    tk.Label(search_window, text="Max Amount").grid(row=5, column=0)
    max_amount_entry = tk.Entry(search_window)
    max_amount_entry.grid(row=5, column=1)

    search_fields = {
        "amount": tk.IntVar(value=1),
        "date": tk.IntVar(value=1),
        "source": tk.IntVar(value=1),
        "description": tk.IntVar(value=1),
        "type": tk.IntVar(value=1),
    }
    tk.Label(search_window, text="Search In Fields").grid(row=6, column=0)
    for i, (field, var) in enumerate(search_fields.items()):
        tk.Checkbutton(search_window, text=field.capitalize(), variable=var).grid(row=6+i, column=1)

    tk.Button(search_window, text="Search", command=handle_search).grid(row=11, column=0, columnspan=2)

    results_tree = ttk.Treeview(search_window, columns=("username", "amount", "date", "source", "description", "type"), show='headings')
    for col in ("username", "amount", "date", "source", "description", "type"):
        results_tree.heading(col, text=col.capitalize())
    results_tree.grid(row=12, column=0, columnspan=2)

def generate_report(username):
    def handle_generate_report():
        record_type = record_type_var.get()
        filter_type = filter_type_var.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        query = f"SELECT * FROM {record_type} WHERE username=?"
        params = [username]

        if filter_type == "day":
            today = datetime.datetime.now().date()
            query += " AND date = ?"
            params.append(today)
        elif filter_type == "month":
            month_start = datetime.datetime.now().replace(day=1).date()
            next_month = datetime.datetime.now().replace(day=28) + datetime.timedelta(days=4)
            month_end = next_month.replace(day=1) - datetime.timedelta(days=1)
            query += " AND date BETWEEN ? AND ?"
            params.extend([month_start, month_end])
        elif filter_type == "year":
            year_start = datetime.datetime.now().replace(month=1, day=1).date()
            year_end = datetime.datetime.now().replace(month=12, day=31).date()
            query += " AND date BETWEEN ? AND ?"
            params.extend([year_start, year_end])
        elif filter_type == "custom":
            if not is_valid_date(start_date) or not is_valid_date(end_date):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        records = fetch_all(query, params)
        total_amount = sum(record[1] for record in records)

        results_tree.delete(*results_tree.get_children())
        for record in records:
            results_tree.insert("", tk.END, values=record)

        total_label.config(text=f"Total: {total_amount}")

    report_window = tk.Toplevel()
    report_window.title("Generate Report")

    tk.Label(report_window, text="Record Type").grid(row=0, column=0)
    record_type_var = tk.StringVar(value="incomes")
    tk.Radiobutton(report_window, text="Incomes", variable=record_type_var, value="incomes").grid(row=0, column=1)
    tk.Radiobutton(report_window, text="Expenses", variable=record_type_var, value="expenses").grid(row=0, column=2)

    tk.Label(report_window, text="Filter Type").grid(row=1, column=0)
    filter_type_var = tk.StringVar(value="day")
    tk.Radiobutton(report_window, text="Day", variable=filter_type_var, value="day").grid(row=1, column=1)
    tk.Radiobutton(report_window, text="Month", variable=filter_type_var, value="month").grid(row=1, column=2)
    tk.Radiobutton(report_window, text="Year", variable=filter_type_var, value="year").grid(row=1, column=3)
    tk.Radiobutton(report_window, text="Custom", variable=filter_type_var, value="custom").grid(row=1, column=4)

    tk.Label(report_window, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0)
    start_date_entry = tk.Entry(report_window)
    start_date_entry.grid(row=2, column=1)

    tk.Label(report_window, text="End Date (YYYY-MM-DD)").grid(row=2, column=2)
    end_date_entry = tk.Entry(report_window)
    end_date_entry.grid(row=2, column=3)

    tk.Button(report_window, text="Generate Report", command=handle_generate_report).grid(row=3, column=0, columnspan=4)

    results_tree = ttk.Treeview(report_window, columns=("username", "amount", "date", "category", "description"), show='headings')
    for col in ("username", "amount", "date", "category", "description"):
        results_tree.heading(col, text=col.capitalize())
    results_tree.grid(row=4, column=0, columnspan=4)

    total_label = tk.Label(report_window, text="Total: ")
    total_label.grid(row=5, column=0, columnspan=4)


def show_report_window(username, report_type):
    def handle_generate_report():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        min_amount = min_amount_entry.get()
        max_amount = max_amount_entry.get()
        
        records, total_amount, proportion, overall_total = generate_report(
            username, report_type, start_date, end_date, min_amount, max_amount
        )
        
        for record in records:
            results_tree.insert("", tk.END, values=record)
        
        summary_label.config(text=f"Total: {total_amount}, Proportion: {proportion:.2f}%, Overall Total: {overall_total}")

    report_window = tk.Toplevel()
    report_window.title(f"{report_type.capitalize()} Report")

    tk.Label(report_window, text="Start Date (YYYY-MM-DD)").grid(row=0, column=0)
    start_date_entry = tk.Entry(report_window)
    start_date_entry.grid(row=0, column=1)

    tk.Label(report_window, text="End Date (YYYY-MM-DD)").grid(row=1, column=0)
    end_date_entry = tk.Entry(report_window)
    end_date_entry.grid(row=1, column=1)

    tk.Label(report_window, text="Min Amount").grid(row=2, column=0)
    min_amount_entry = tk.Entry(report_window)
    min_amount_entry.grid(row=2, column=1)

    tk.Label(report_window, text="Max Amount").grid(row=3, column=0)
    max_amount_entry = tk.Entry(report_window)
    max_amount_entry.grid(row=3, column=1)

    tk.Button(report_window, text="Generate Report", command=handle_generate_report).grid(row=4, column=0, columnspan=2)

    results_tree = ttk.Treeview(report_window, columns=("username", "amount", "date", "source", "description", "type"), show='headings')
    for col in ("username", "amount", "date", "source", "description", "type"):
        results_tree.heading(col, text=col.capitalize())
    results_tree.grid(row=5, column=0, columnspan=2)

    summary_label = tk.Label(report_window, text="")
    summary_label.grid(row=6, column=0, columnspan=2)

def user_settings(username):
    def handle_update_settings():
        update_field = update_field_var.get()
        new_value = new_value_entry.get()

        if update_field == "password" and not is_valid_password(new_value):
            messagebox.showerror("Error", "Invalid password format.")
            return
        if update_field == "email" and not is_valid_email(new_value):
            messagebox.showerror("Error", "Invalid email format.")
            return
        if update_field == "birthdate" and not is_valid_birthdate(new_value):
            messagebox.showerror("Error", "Invalid birthdate format.")
            return

        query = f"UPDATE users SET {update_field} = ? WHERE username = ?"
        execute_query(query, (new_value, username))
        messagebox.showinfo("Success", "User information updated successfully.")
        settings_window.destroy()

    def handle_delete_user():
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this user?"):
            execute_query("DELETE FROM users WHERE username = ?", (username,))
            messagebox.showinfo("Success", "User deleted successfully.")
            settings_window.destroy()

    settings_window = tk.Toplevel()
    settings_window.title("User Settings")

    tk.Label(settings_window, text="Update Field").grid(row=0, column=0)
    update_field_var = tk.StringVar(value="password")
    tk.Radiobutton(settings_window, text="Password", variable=update_field_var, value="password").grid(row=0, column=1)
    tk.Radiobutton(settings_window, text="Email", variable=update_field_var, value="email").grid(row=0, column=2)
    tk.Radiobutton(settings_window, text="Birthdate", variable=update_field_var, value="birthdate").grid(row=0, column=3)
    tk.Radiobutton(settings_window, text="Phone", variable=update_field_var, value="phone").grid(row=0, column=4)
    tk.Radiobutton(settings_window, text="City", variable=update_field_var, value="city").grid(row=0, column=5)

    tk.Label(settings_window, text="New Value").grid(row=1, column=0)
    new_value_entry = tk.Entry(settings_window)
    new_value_entry.grid(row=1, column=1, columnspan=4)

    tk.Button(settings_window, text="Update Settings", command=handle_update_settings).grid(row=2, column=0, columnspan=5)
    tk.Button(settings_window, text="Delete User", command=handle_delete_user).grid(row=3, column=0, columnspan=5)


def user_menu(username):
    user_window = tk.Toplevel()
    user_window.title("User Menu")

    tk.Button(user_window, text="Add Income", command=lambda: add_income(username)).grid(row=0, column=0)
    tk.Button(user_window, text="Add Expense", command=lambda: add_expense(username)).grid(row=0, column=1)
    tk.Button(user_window, text="Add Category", command=lambda: add_category(username)).grid(row=1, column=0)
    tk.Button(user_window, text="Search Records", command=lambda: search_records(username)).grid(row=1, column=1)
    tk.Button(user_window, text="Generate Report", command=lambda: generate_report(username)).grid(row=2, column=0, columnspan=2)
    tk.Button(user_window, text="Settings", command=lambda: user_settings(username)).grid(row=3, column=0, columnspan=2)

root = tk.Tk()
root.title("Expense Tracker")

tk.Button(root, text="Register", command=signup).grid(row=0, column=0)
tk.Button(root, text="Log In", command=login).grid(row=0, column=1)

root.mainloop()
