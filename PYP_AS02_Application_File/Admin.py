# admin.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import csv
import json

# Import all the backend functions this UI needs
from Backend import (
    load_bookings, admin_approve_booking, log_action, load_venues, get_all_users,
    get_system_setting, update_system_setting, update_booking_status,
    approve_user, deactivate_user, create_user, staff_update_venue,
    admin_delete_venue, peak_booking_periods
)

class AdminMixin:
    # ==================================
    # ADMIN FEATURES (6) (Rule 2, 17)
    # ==================================
    def admin_menu(self, frame):
        # Rule 2: All roles should have 6 features
        features = [
            ("1. View All Customer Bookings", self.admin_view_all_bookings_ui),
            ("2. Approve/Confirm PENDING Bookings", self.admin_approve_booking_ui),
            ("3. Override or Cancel Bookings", self.admin_override_booking_ui),
            ("4. Manage User Accounts & Venues (Approval/Deletion)", self.admin_manage_users_and_venues_ui),
            ("5. Export System Data (CSV/JSON)", self.admin_export_data_ui), # Rule 17
            ("6. System Settings & Policy Management", self.admin_policy_settings_ui), # Rule 15
        ]

        for text, command in features:
            ttk.Button(frame, text=text, command=command, width=50).pack(pady=5)
            
    def admin_approve_booking_ui(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin: Approve Pending Bookings", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('ID', 'Customer', 'VenueID', 'Date', 'Time', 'Price', 'Status'), show='headings')
        tree.heading('ID', text='Booking ID')
        tree.heading('Customer', text='Customer Email')
        tree.heading('VenueID', text='Venue ID')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Price', text='Total Price')
        tree.heading('Status', text='Status')
        
        bookings = [b for b in load_bookings() if b.find('status').text == 'PENDING']
        for b in bookings:
            tree.insert('', tk.END, values=(b.find('id').text, b.find('customer_email').text, b.find('venue_id').text, b.find('date').text, b.find('time').text, b.find('total_price').text, b.find('status').text))
            
        tree.pack(padx=10, pady=10, fill='x')
        
        ttk.Button(self.root, text="Approve Selected Booking", command=lambda: self.admin_perform_approval(tree)).pack(pady=10)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def admin_perform_approval(self, tree):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a PENDING booking to approve.")
            return
        b_id = tree.item(selected_item, 'values')[0]
    
        if messagebox.askyesno("Confirm Approval", f"Are you sure you want to CONFIRM booking {b_id}?"):
            success, msg = admin_approve_booking(b_id, self.current_user_email)
            if success:
                messagebox.showinfo("Success", msg)
                self.admin_approve_booking_ui() 
            
            else:
                messagebox.showerror("Error", msg)


    def admin_export_data_ui(self):
        """Admin Feature 5: Export System Data (Rule 17)"""
        self.clear_screen()
        ttk.Label(self.root, text="Admin: Export System Data (Rule 17)", font=('Arial', 16, 'bold')).pack(pady=10)

        data_options = [
            ("Booking Records", 'bookings'),
            ("Venue Logs", 'venues'),
            ("User Activity Data", 'users'),
        ]
        
        data_var = tk.StringVar(self.root)
        data_var.set(data_options[0][0])
        
        format_var = tk.StringVar(self.root)
        format_var.set('CSV')

        frame = ttk.Frame(self.root, padding="10", style='TFrame')
        frame.pack(pady=10)
        
        ttk.Label(frame, text="Select Data Type:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.OptionMenu(frame, data_var, data_var.get(), *[opt[0] for opt in data_options]).grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(frame, text="Select Export Format:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        ttk.OptionMenu(frame, format_var, format_var.get(), 'CSV', 'JSON').grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Button(frame, text="Export Data", command=lambda: self.perform_data_export(data_var.get(), format_var.get())).grid(row=2, column=0, columnspan=2, pady=15, sticky='ew')
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def perform_data_export(self, data_type, export_format):
        data_map = {
            'Booking Records': ('bookings', load_bookings),
            'Venue Logs': ('venues', load_venues),
            'User Activity Data': ('users', get_all_users),
        }

        tag, loader_func = data_map.get(data_type)
        if not tag:
            messagebox.showerror("Error", "Invalid data type selected.")
            return

        data_elements = loader_func()

        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{export_format.lower()}",
            filetypes=[(f"{export_format} files", f"*.{export_format.lower()}")]
        )
        
        if not file_path:
            return

        try:
            export_data = []
            if data_elements:
                for element in data_elements:
                    item = {child.tag: child.text for child in element}
                    export_data.append(item)
            
            # Export logic (Rule 17: CSV or JSON)
            if export_format == 'CSV':
                if not export_data:
                    with open(file_path, 'w', newline='', encoding='utf-8') as f:
                        f.write('')
                    messagebox.showinfo("Export Success", f"Successfully created empty CSV file at:\n{file_path}")
                    return

                if tag == 'bookings':
                    keys = ['id', 'venue_id', 'customer_email', 'date', 'time', 'duration_hrs', 'capacity_required', 'total_price', 'booked_at', 'status', 'cancellation_reason']
                else:
                    all_keys = set()
                    for item in export_data:
                        all_keys.update(item.keys())
                    keys = sorted(list(all_keys))

                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    dict_writer = csv.DictWriter(f, fieldnames=keys, restval='')
                    dict_writer.writeheader()
                    dict_writer.writerows(export_data)

            elif export_format == 'JSON':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=4)
                    
            messagebox.showinfo("Export Success", f"Successfully exported {data_type} to {export_format} file at:\n{file_path}")
            log_action(self.current_user_email, f"Exported {data_type} to {export_format}.")

        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred during export: {e}")

    def admin_policy_settings_ui(self):
        """Admin Feature 6: System Settings & Policy Management (Rule 15)"""
        self.clear_screen()
        ttk.Label(self.root, text="Admin: System Settings & Policy Management (Rule 15)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, expand=True, fill='both')

        # --- Tab 1: Cancellation Policy ---
        policy_tab = ttk.Frame(notebook, style='TFrame')
        notebook.add(policy_tab, text=' Cancellation Policy (Rule 15) ')
        self.create_cancellation_policy_tab(policy_tab)

        # --- Tab 2: Refund Settings ---
        refund_tab = ttk.Frame(notebook, style='TFrame')
        notebook.add(refund_tab, text=' Refund Threshold ')
        self.create_refund_settings_tab(refund_tab)
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def create_cancellation_policy_tab(self, tab):
        # Admin Reasons (Rule 15)
        ttk.Label(tab, text="Admin Fixed Cancellation Reasons (separated by ';'):", font=('Arial', 12, 'bold')).pack(pady=10)
        admin_reasons = get_system_setting('admin_cancellation_reasons')
        self.admin_reasons_entry = tk.Text(tab, height=4, width=80)
        self.admin_reasons_entry.insert(tk.END, admin_reasons)
        self.admin_reasons_entry.pack(padx=10, pady=5)

        # Customer Reasons (Rule 15)
        ttk.Label(tab, text="Customer Fixed Cancellation Reasons (separated by ';'):", font=('Arial', 12, 'bold')).pack(pady=10)
        customer_reasons = get_system_setting('customer_cancellation_reasons')
        self.customer_reasons_entry = tk.Text(tab, height=4, width=80)
        self.customer_reasons_entry.insert(tk.END, customer_reasons)
        self.customer_reasons_entry.pack(padx=10, pady=5)

        ttk.Button(tab, text="Save Cancellation Reasons", command=self.save_cancellation_reasons).pack(pady=15)

    def save_cancellation_reasons(self):
        admin_reasons = self.admin_reasons_entry.get("1.0", tk.END).strip().replace('\n', '')
        customer_reasons = self.customer_reasons_entry.get("1.0", tk.END).strip().replace('\n', '')

        if not admin_reasons or not customer_reasons:
             messagebox.showerror("Error", "Both Admin and Customer cancellation reasons must be provided.")
             return

        update_system_setting('admin_cancellation_reasons', admin_reasons)
        update_system_setting('customer_cancellation_reasons', customer_reasons)
        messagebox.showinfo("Success", "Cancellation policies updated successfully.")

    def create_refund_settings_tab(self, tab):
        # Refund Threshold Setting (Mock)
        current_threshold = get_system_setting('refund_threshold_hours')
        ttk.Label(tab, text="Refund Threshold Setting:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        settings_frame = ttk.Frame(tab, padding="10", style='TFrame')
        settings_frame.pack(pady=10)
        
        ttk.Label(settings_frame, text="Cancellation Time Limit (hours):").grid(row=0, column=0, sticky='w', padx=5)
        self.setting_entry = ttk.Entry(settings_frame, width=10)
        self.setting_entry.insert(0, str(current_threshold))
        self.setting_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(settings_frame, text="Update Refund Threshold (Mock Save)", command=self.update_refund_threshold).grid(row=1, column=0, columnspan=2, pady=10)

    def update_refund_threshold(self):
        try:
            new_value = int(self.setting_entry.get())
            if new_value <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Threshold must be a positive whole number.")
            return

        if update_system_setting('refund_threshold_hours', new_value):
            messagebox.showinfo("Success (Mock)", f"Refund threshold updated to {new_value} hours (mock save).")
            self.admin_policy_settings_ui()
        else:
            messagebox.showerror("Error", "Failed to update refund threshold.")

    def admin_view_all_bookings_ui(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin: All Customer Bookings", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('ID', 'Customer', 'VenueID', 'Date', 'Time', 'Price', 'Status', 'Reason'), show='headings')
        tree.heading('ID', text='Booking ID')
        tree.heading('Customer', text='Customer Email')
        tree.heading('VenueID', text='Venue ID')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Price', text='Total Price')
        tree.heading('Status', text='Status')
        tree.heading('Reason', text='Cancellation Reason')
        tree.column('ID', width=120)
        tree.column('Customer', width=150)
        tree.column('VenueID', width=80)
        tree.column('Status', width=120)
        
        bookings = load_bookings()
        for b in bookings:
            b_id = b.find('id').text
            customer = b.find('customer_email').text
            venue_id = b.find('venue_id').text
            date_val = b.find('date').text
            time_val = b.find('time').text
            price = b.find('total_price').text
            status = b.find('status').text
            reason = b.find('cancellation_reason').text if b.find('cancellation_reason') is not None else ''

            tree.insert('', tk.END, values=(b_id, customer, venue_id, date_val, time_val, price, status, reason))
            
        tree.pack(padx=10, pady=10, fill='both', expand=True)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)
        
    def admin_override_booking_ui(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin: Override/Cancel Booking (Rule 11, 15)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('ID', 'Customer', 'VenueID', 'Date', 'Status'), show='headings')
        tree.heading('ID', text='Booking ID')
        tree.heading('Customer', text='Customer Email')
        tree.heading('VenueID', text='Venue ID')
        tree.heading('Date', text='Date')
        tree.heading('Status', text='Status')
        
        bookings = [b for b in load_bookings() if b.find('status').text in ['CONFIRMED', 'PENDING']]
        for b in bookings:
            tree.insert('', tk.END, values=(b.find('id').text, b.find('customer_email').text, b.find('venue_id').text, b.find('date').text, b.find('status').text))
            
        tree.pack(padx=10, pady=10, fill='x')
        ttk.Button(self.root, text="Cancel Selected Booking (Override)", command=lambda: self.admin_perform_cancellation(tree), style='TButton').pack(pady=10)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def admin_perform_cancellation(self, tree):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a booking to cancel.")
            return 
            
        b_id = tree.item(selected_item, 'values')[0]
        
        # Rule 15: Admin uses fixed valid reasons
        reasons_str = get_system_setting('admin_cancellation_reasons')
        reasons = [r.strip() for r in reasons_str.split(';') if r.strip()]
        
        reason = simpledialog.askstring("Cancellation Reason (Rule 15)", 
                                        f"Enter mandatory reason for cancelling Booking ID: {b_id}.\nOptions: {', '.join(reasons)}:", 
                                        parent=self.root)
                                        
        if not reason:
            messagebox.showwarning("Warning", "Cancellation reason is mandatory.")
            return
            
        if not messagebox.askyesno("Confirm Override", f"Are you sure you want to cancel booking {b_id}?\nReason: {reason}"):
            return

        success, msg = update_booking_status(b_id, 'CANCELLED_BY_ADMIN', self.current_user_email, reason) 
        
        if success:
            messagebox.showinfo("Success", msg)
            self.admin_override_booking_ui()
        else:
            messagebox.showerror("Error", msg)

    def admin_manage_users_and_venues_ui(self):
        """Admin Feature 4: Manage Users and Approve Venues."""
        self.clear_screen()
        ttk.Label(self.root, text="Admin: Manage Users & Venues", font=('Arial', 16, 'bold')).pack(pady=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, expand=True, fill='both')

        user_tab = ttk.Frame(notebook, style='TFrame')
        notebook.add(user_tab, text=' Manage Users ')
        self.create_user_management_tab(user_tab)

        venue_tab = ttk.Frame(notebook, style='TFrame')
        notebook.add(venue_tab, text=' Approve/Delete Venues ')
        self.create_venue_approval_tab(venue_tab)
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def create_user_management_tab(self, tab):
        tree = ttk.Treeview(tab, columns=('Email', 'Name', 'Role', 'Status'), show='headings')
        tree.heading('Email', text='Email')
        tree.heading('Name', text='Name')
        tree.heading('Role', text='Role')
        tree.heading('Status', text='Status')
        
        users = get_all_users()
        for u in users:
            role = u.find('role').text
            if role != 'superadmin':
                tree.insert('', tk.END, values=(u.find('email').text, u.find('name').text, role, u.find('status').text))
                
        tree.pack(padx=10, pady=10, fill='x')
        
        button_frame = ttk.Frame(tab, style='TFrame')
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Approve Pending", command=lambda: self.admin_perform_user_action(tree, 'approve')).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Create Staff", command=self.admin_create_staff_ui).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Deactivate User", command=lambda: self.admin_perform_user_action(tree, 'deactivate')).pack(side='left', padx=5)

    def admin_perform_user_action(self, tree, action):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", f"Please select a user to {action}.")
            return
            
        email = tree.item(selected_item, 'values')[0]
        
        if action == 'approve':
            success, msg = approve_user(email, self.current_user_email)
        elif action == 'deactivate':
            success, msg = deactivate_user(email, self.current_user_email)
        else:
            return

        if success:
            messagebox.showinfo("Success", msg)
            self.admin_manage_users_and_venues_ui()
        else:
            messagebox.showerror("Error", msg)

    def admin_create_staff_ui(self):
        name = simpledialog.askstring("Create Staff Account", "Enter Staff Full Name:")
        if not name: return

        email = simpledialog.askstring("Create Staff Account", "Enter Staff Email:")
        if not email: return

        password = simpledialog.askstring("Create Staff Account", "Enter Staff Password:", show='*')
        if not password: return

        success, message = create_user(email, password, name, "staff", "approved") 

        if success:
            messagebox.showinfo("Success", f"Staff account created and approved:\n{message}")
            self.admin_manage_users_and_venues_ui()
        else:
            messagebox.showerror("Error", message)

    def create_venue_approval_tab(self, tab):
        tree = ttk.Treeview(tab, columns=('ID', 'Name', 'Staff', 'Status', 'Description'), show='headings')
        tree.heading('ID', text='Venue ID')
        tree.heading('Name', text='Name')
        tree.heading('Staff', text='Submitted By')
        tree.heading('Status', text='Status (Rule 3.vi)')
        tree.heading('Description', text='Description')
        
        tree.column('ID', width=100)
        tree.column('Name', width=150)
        tree.column('Status', width=100)
        
        venues = load_venues()
        for v in venues:
            tree.insert('', tk.END, values=(v.find('id').text, v.find('name').text, v.find('added_by').text, v.find('status').text, v.find('description').text if v.find('description') is not None else ''))
            
        tree.pack(padx=10, pady=10, fill='both', expand=True)
        
        button_frame = ttk.Frame(tab, style='TFrame')
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Approve (Set 'active')", command=lambda: self.admin_perform_venue_action(tree, 'approve')).pack(side='left', padx=5) 
        ttk.Button(button_frame, text="Delete Venue (Rule 12)", command=lambda: self.admin_perform_venue_action(tree, 'delete')).pack(side='left', padx=5) 

    def admin_perform_venue_action(self, tree, action):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a venue to approve or delete.")
            return

        v_id, v_name, _, v_status, _ = tree.item(selected_item, 'values')

        if action == 'approve':
            if v_status == 'active':
                messagebox.showwarning("Warning", f"Venue {v_name} is already 'active'.")
                return
            
            update_data = {'status': 'active'}
            success, msg = staff_update_venue(v_id, update_data, self.current_user_email)
        
        elif action == 'delete':
             if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to PERMANENTLY delete venue {v_name}?\n\nIt will only be deleted if it has NO future bookings (Rule 12)."):
                return
             success, msg = admin_delete_venue(v_id, self.current_user_email)

        else:
            return

        if success:
            messagebox.showinfo("Success", msg)
            self.admin_manage_users_and_venues_ui() 
        else:
            messagebox.showerror("Error", msg)

    def admin_peak_stats_ui(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin: Peak Period Statistics", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('Date', 'Booking_Count', 'Venue'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Booking_Count', text='Bookings')
        tree.heading('Venue', text='Venue Example')
        
        stats = peak_booking_periods()
        for s in stats:
            tree.insert('', tk.END, values=s)
            
        tree.pack(padx=10, pady=10, fill='x')
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)