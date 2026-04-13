# application.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

# Import config constants
from Config import GREY, PINK, DARK_GREY, ADMIN_EMAIL, ADMIN_PIN

# Import backend logic
from Backend import initialize_files, login_user, create_user, log_action

# Import the GUI Mixin classes from the other files
from Admin import AdminMixin
from Staff import StaffMixin
from Customer import CustomerMixin

# ==============================================================================
# 7. GUI APPLICATION (Updated Menus and Logic)
# ==============================================================================

# The main class now INHERITS from the Mixin classes
class VenueReservationApp(AdminMixin, StaffMixin, CustomerMixin):
    def __init__(self, root):
        self.root = root
        self.root.title("Venue Reservation System (Pink/Grey Theme)")
        self.root.geometry("1000x800") 

        # Apply Theme Colors (Rule 14)
        self.root.configure(bg=GREY)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=GREY)
        style.configure('TLabel', background=GREY, foreground=DARK_GREY)
        style.configure('TButton', background=PINK, foreground='black', borderwidth=1)
        style.map('TButton', background=[('active', PINK)])

        self.current_user_email = None
        self.current_user_role = None

        initialize_files() # This function is now in backend.py
        self.login_ui()

    def clear_screen(self):
        """Clears all widgets from the main window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- LOGIN & REGISTRATION UI ---

    def login_ui(self):
        self.clear_screen()

        frame = ttk.Frame(self.root, padding="20 20 20 20")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frame, text="System Login", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Email
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky='w', pady=5)
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.grid(row=1, column=1, pady=5)

        # Password
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1, pady=5)

        self.email_entry.bind('<KeyRelease>', self.admin_special_password_fill)

        # Buttons
        ttk.Button(frame, text="Login", command=self.perform_login).grid(row=3, column=0, columnspan=2, pady=15, sticky='ew')
        ttk.Button(frame, text="New Customer Registration", command=self.registration_ui).grid(row=4, column=0, columnspan=2, pady=5, sticky='ew')


    def admin_special_password_fill(self, event):
        """Rule 9: Auto-fills password and prepares for PIN check if Admin email is entered."""
        if self.email_entry.get() == ADMIN_EMAIL:
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, "hardcoded_trigger")
            self.password_entry.configure(show='*')
        else:
            self.password_entry.configure(state='normal')

    def perform_login(self):
        email = self.email_entry.get()
        if email == ADMIN_EMAIL:
            password = "hardcoded_trigger"
        else:
            password = self.password_entry.get()

        success, role, status_code, message = login_user(email, password)

        if success and status_code == "PIN_REQUIRED":
            self.prompt_admin_pin(email)
        elif success:
            self.current_user_email = email
            self.current_user_role = role
            messagebox.showinfo("Login Success", message)
            self.main_menu()
        else:
            messagebox.showerror(status_code, message)

    def prompt_admin_pin(self, email):
        """Rule 9: Prompts for Admin PIN after successful username/password trigger."""
        pin = simpledialog.askstring("Admin PIN Required", "Enter Admin PIN (for security):", parent=self.root, show='*')
        if pin == ADMIN_PIN:
            self.current_user_email = email
            self.current_user_role = 'superadmin'
            log_action(email, "Super Admin login successful with PIN.")
            messagebox.showinfo("Login Success", "Super Admin login successful.")
            self.main_menu()
        else:
            log_action(email, "Super Admin PIN check failed.")
            messagebox.showerror("PIN Error", "Incorrect PIN. Login failed.")
            self.login_ui()

    def registration_ui(self):
        """Registration UI (Rule 2, 3) - Email and Password in one pop-up/frame."""
        self.clear_screen()

        frame = ttk.Frame(self.root, padding="20 20 20 20")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frame, text="Customer Registration", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Name
        ttk.Label(frame, text="Full Name:").grid(row=1, column=0, sticky='w', pady=5)
        self.reg_name = ttk.Entry(frame, width=30)
        self.reg_name.grid(row=1, column=1, pady=5)

        # Email (Rule 2: one pop up)
        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        self.reg_email = ttk.Entry(frame, width=30)
        self.reg_email.grid(row=2, column=1, pady=5)

        # Password (Rule 2: one pop up)
        ttk.Label(frame, text="Password:").grid(row=3, column=0, sticky='w', pady=5)
        self.reg_password = ttk.Entry(frame, show="*", width=30)
        self.reg_password.grid(row=3, column=1, pady=5)

        ttk.Button(frame, text="Register", command=self.perform_registration).grid(row=4, column=0, columnspan=2, pady=15, sticky='ew')
        ttk.Button(frame, text="Back to Login", command=self.login_ui).grid(row=5, column=0, columnspan=2, pady=5, sticky='ew')

    def perform_registration(self):
        name = self.reg_name.get()
        email = self.reg_email.get()
        password = self.reg_password.get()

        if not all([name, email, password]):
            messagebox.showerror("Input Error", "All fields must be filled.")
            return

        success, message = create_user(email, password, name, "customer", "pending") # Status: pending (Rule 3)

        if success:
            messagebox.showinfo("Registration Success", f"{message}\nYour account is now 'Pending Approval' by an Admin.")
            self.login_ui()
        else:
            messagebox.showerror("Registration Error", message)

    # --- MAIN MENU UI ---
    def main_menu(self):
        self.clear_screen()

        header_frame = ttk.Frame(self.root, padding="10 10 10 10", relief='groove', style='TFrame')
        header_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(header_frame, text=f"Welcome, {self.current_user_role.capitalize()} ({self.current_user_email})",
                  font=('Arial', 16, 'bold'), foreground=DARK_GREY).pack(side='left')
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side='right')

        menu_frame = ttk.Frame(self.root, padding="10", style='TFrame')
        menu_frame.pack(pady=20)


        if self.current_user_role == 'superadmin':
            menu_title = "Admin Menu (6 Features)"
            self.admin_menu(menu_frame) # This method now comes from admin.py
        elif self.current_user_role == 'staff':
            menu_title = "Staff Menu (6 Features)"
            self.staff_menu(menu_frame) # This method now comes from staff.py
        elif self.current_user_role == 'customer':
            menu_title = "Customer Menu (6 Features)"
            self.customer_menu(menu_frame) # This method now comes from customer.py

        ttk.Label(menu_frame, text=menu_title,
                  font=('Arial', 14, 'italic'), foreground='black').pack(pady=10)

    def logout(self):
        log_action(self.current_user_email, "Logout successful.")
        self.current_user_email = None
        self.current_user_role = None
        self.login_ui()

    # ALL THE admin_...(), staff_...(), and customer_...() methods
    # have been moved to their respective files (admin.py, staff.py, customer.py)