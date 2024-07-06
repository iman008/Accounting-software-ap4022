import tkinter as tk
from tkinter import messagebox

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

    # Create the signup window
    signup_window = tk.Toplevel()
    signup_window.title("Sign Up")

    # Labels and Entries
    fields = [
        ("First Name", tk.Entry(signup_window)),
        ("Last Name", tk.Entry(signup_window)),
        ("Phone", tk.Entry(signup_window)),
        ("Username", tk.Entry(signup_window)),
        ("Password", tk.Entry(signup_window, show="*")),
        ("Confirm Password", tk.Entry(signup_window, show="*")),
        ("City", tk.Entry(signup_window)),
        ("Email", tk.Entry(signup_window)),
        ("Birthdate (YYYY-MM-DD)", tk.Entry(signup_window)),
        ("Security Question", tk.Entry(signup_window)),
        ("Security Answer", tk.Entry(signup_window))
    ]

    for index, (label_text, entry_widget) in enumerate(fields):
        tk.Label(signup_window, text=label_text).grid(row=index, column=0, sticky='e', padx=10, pady=5)
        entry_widget.grid(row=index, column=1, padx=10, pady=5)
    
    # Sign Up Button
    signup_button = tk.Button(signup_window, text="Sign Up", command=handle_signup)
    signup_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

    # Adjust window size and center on screen
    signup_window.update_idletasks()
    width = signup_window.winfo_width()
    height = signup_window.winfo_height()
    x = (signup_window.winfo_screenwidth() // 2) - (width // 2)
    y = (signup_window.winfo_screenheight() // 2) - (height // 2)
    signup_window.geometry(f"{width}x{height}+{x}+{y}")

    # Run the main loop
    signup_window.mainloop()
