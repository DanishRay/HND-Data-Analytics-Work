# staff.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import os

# Import all the backend functions this UI needs
from Backend import (
    add_venue, save_venue_attachment, load_bookings, 
    staff_cancel_booking_with_validation, load_venues,
    get_venue_by_id, staff_update_venue
)
from Config import LOGS_FILE, GREY # Import constants needed by this UI

class StaffMixin:
    # ==================================
    # STAFF FEATURES (6) (Rule 2, 3, 13, 16)
    # ==================================
    def staff_menu(self, frame):
        # Rule 2: All roles should have 6 features
        features = [
            ("1. Add New Venue (Form)", self.staff_add_venue_ui), # Rule 3.i, 3.ii
            ("2. View/Update My Venues", self.staff_view_update_venues_ui), # Rule 3.v
            ("3. Manage Venue Images/Attachments", self.staff_manage_attachments_ui), # Rule 16
            ("4. View All Bookings", self.staff_view_all_bookings_ui),
            ("5. Cancel Customer Booking (Validation)", self.staff_cancel_booking_ui), # Rule 13
            ("6. View Staff Activity Logs", self.staff_view_logs_ui),
        ]

        for text, command in features:
            ttk.Button(frame, text=text, command=command, width=50).pack(pady=5)

    def staff_add_venue_ui(self):
        """Staff Feature 1: Add New Venue Form (Rule 3.i, 3.ii, 3.iv)"""
        self.clear_screen()
        ttk.Label(self.root, text="Staff: Add New Venue", font=('Arial', 16, 'bold')).pack(pady=10)
        
        form_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        form_frame.pack(pady=10, padx=10)
        
        # Row 1: Name
        ttk.Label(form_frame, text="Venue Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.v_name = ttk.Entry(form_frame, width=40)
        self.v_name.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        # Row 2: Type (Rule 3.iii criteria)
        ttk.Label(form_frame, text="Type of Hall (e.g., Ballroom, Theatre):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        venue_types = ["Ballroom", "Theatre", "Conference Hall", "Outdoor Space", "Other"]
        self.v_type = ttk.Combobox(form_frame, values=venue_types, width=38)
        self.v_type.set("Ballroom")
        self.v_type.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        # Row 3: Capacity
        ttk.Label(form_frame, text="Capacity:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.v_capacity = ttk.Entry(form_frame, width=40)
        self.v_capacity.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # Row 4: Price
        ttk.Label(form_frame, text="Price (per hour/slot):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.v_price = ttk.Entry(form_frame, width=40)
        self.v_price.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
        
        # Row 5: Duration (Rule 3.iv)
        ttk.Label(form_frame, text="Duration (Max hrs per booking, e.g., 8):").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.v_duration = ttk.Entry(form_frame, width=40)
        self.v_duration.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

        # Row 6: Description (Rule 3.ii)
        ttk.Label(form_frame, text="Description:").grid(row=5, column=0, sticky='nw', padx=5, pady=5)
        self.v_description = tk.Text(form_frame, height=5, width=40)
        self.v_description.grid(row=5, column=1, sticky='ew', padx=5, pady=5)

        # 7. Venue Start Date (When it becomes available)
        ttk.Label(form_frame, text="Start Date (YYYY-MM-DD):").grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.v_start_date = ttk.Entry(form_frame, width=40) # Changed variable name for consistency and width to 40
        self.v_start_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.v_start_date.grid(row=6, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Button(form_frame, text="Submit Venue for Approval", command=self.perform_add_venue, style='TButton').grid(row=7, column=0, columnspan=2, pady=15, sticky='ew') # Changed row from 6 to 7
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def perform_add_venue(self):
        name = self.v_name.get()
        description = self.v_description.get("1.0", tk.END).strip()
        type = self.v_type.get()
        price = self.v_price.get()
        capacity = self.v_capacity.get()
        duration = self.v_duration.get()
        start_date = self.v_start_date.get()
        
        try:
            # Check if the date format is valid
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Input Error", "Start Date must be in YYYY-MM-DD format.")
            return

        success, msg = add_venue(name, description, type, price, capacity, duration, self.current_user_email, start_date)
        
        if success:
            messagebox.showinfo("Success", msg)
            self.main_menu()
        else:
            messagebox.showerror("Input/Save Error", msg)

    def staff_manage_attachments_ui(self):
        """Staff Feature 3: Manage Venue Images Attachment (Rule 16)"""
        self.clear_screen()
        ttk.Label(self.root, text="Staff: Manage Venue Attachments (Rule 16)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # 1. Select Venue
        ttk.Label(self.root, text="Select Venue to manage attachments for:").pack(pady=5)
        
        venues = load_venues()
        venue_options = {v.find('name').text: v.find('id').text for v in venues if v.find('added_by').text == self.current_user_email}
        self.selected_venue_id = tk.StringVar(self.root)
        
        if not venue_options:
            ttk.Label(self.root, text="You have not added any venues.").pack(pady=10)
            ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)
            return

        venue_names = list(venue_options.keys())
        self.selected_venue_id.set(venue_names[0])

        venue_combo = ttk.Combobox(self.root, values=venue_names, textvariable=self.selected_venue_id, state='readonly', width=50)
        venue_combo.pack(pady=5)
        
        # 2. Attachment Type (Rule 16)
        ttk.Label(self.root, text="Attachment Type (Rule 16):").pack(pady=5)
        attachment_types = [
            "Floor Plans", 
            "Safety Certifications and Permit", 
            "Emergency Exit Routes", 
            "Setup and Preparation (Compliance/Safety)"
        ]
        self.attachment_type = tk.StringVar(self.root)
        self.attachment_type.set(attachment_types[0])
        
        type_combo = ttk.Combobox(self.root, values=attachment_types, textvariable=self.attachment_type, state='readonly', width=50)
        type_combo.pack(pady=5)

        # 3. Upload Button
        self.file_path = ""
        ttk.Button(self.root, text="Select File...", command=self.select_file_for_attachment).pack(pady=10)
        self.file_label = ttk.Label(self.root, text="No file selected.")
        self.file_label.pack(pady=5)
        
        ttk.Button(self.root, text="Upload Attachment", command=lambda: self.perform_attachment_upload(venue_options), style='TButton').pack(pady=15)
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def select_file_for_attachment(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_label.config(text=f"Selected: {os.path.basename(self.file_path)}")
        else:
            self.file_label.config(text="No file selected.")

    def perform_attachment_upload(self, venue_options):
        venue_name = self.selected_venue_id.get()
        v_id = venue_options.get(venue_name)
        attachment_type = self.attachment_type.get()

        if not v_id or not self.file_path:
            messagebox.showerror("Error", "Please select a venue and a file.")
            return

        success, msg = save_venue_attachment(v_id, self.file_path, attachment_type)
        if success:
            messagebox.showinfo("Success", f"Attachment uploaded successfully:\n{msg}")
            self.file_path = ""
            self.file_label.config(text="No file selected.")
        else:
            messagebox.showerror("Upload Error", msg)

    def staff_cancel_booking_ui(self):
        """Staff Feature 5: Cancel Customer Booking with Validation (Rule 13)"""
        self.clear_screen()
        ttk.Label(self.root, text="Staff: Cancel Customer Booking (Rule 13)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('ID', 'Customer', 'VenueID', 'Date', 'Status'), show='headings')
        tree.heading('ID', text='Booking ID')
        tree.heading('Customer', text='Customer Email')
        tree.heading('VenueID', text='Venue ID')
        tree.heading('Date', text='Date')
        tree.heading('Status', text='Status')

        # Only show current/future confirmed/pending bookings
        bookings = [b for b in load_bookings() if b.find('status').text in ['CONFIRMED', 'PENDING']]
        for b in bookings:
            tree.insert('', tk.END, values=(b.find('id').text, b.find('customer_email').text, b.find('venue_id').text, b.find('date').text, b.find('status').text))

        tree.pack(padx=10, pady=10, fill='x')
        
        ttk.Button(self.root, text="Cancel Selected Booking (Validation)", command=lambda: self.staff_perform_cancellation(tree), style='TButton').pack(pady=10)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def staff_perform_cancellation(self, tree):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a booking to cancel.")
            return
            
        b_id, customer_email, _, _, status = tree.item(selected_item, 'values')
        
        if status not in ['CONFIRMED', 'PENDING']:
             messagebox.showwarning("Cancellation Blocked", f"This booking is in status: {status} and cannot be cancelled.")
             return

        # Rule 13: System Validation
        if not messagebox.askyesno("CONFIRM CANCELLATION",
                                    f"Are you sure you want to cancel booking {b_id}?\n\n"
                                    f"This action cannot be undone and will notify the customer ({customer_email})."):
            return

        reason = simpledialog.askstring("Cancellation Reason", f"Enter mandatory reason for staff cancelling Booking ID: {b_id}:", parent=self.root)
        if not reason:
            messagebox.showwarning("Warning", "Cancellation reason is mandatory.")
            return

        success, msg = staff_cancel_booking_with_validation(b_id, self.current_user_email, reason)
        if success:
            messagebox.showinfo("Success", msg)
            self.staff_cancel_booking_ui()
        else:
            messagebox.showerror("Error", msg)
            
    def staff_view_all_bookings_ui(self):
        """Staff Feature 4: View All Bookings (Similar to Admin 1)"""
        self.clear_screen()
        ttk.Label(self.root, text="Staff: All Customer Bookings", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('ID', 'Customer', 'VenueID', 'Date', 'Time', 'Price', 'Status', 'Reason'), show='headings')
        tree.heading('ID', text='Booking ID')
        tree.heading('Customer', text='Customer Email')
        tree.heading('VenueID', text='Venue ID')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Price', text='Total Price')
        tree.heading('Status', text='Status')
        tree.heading('Reason', text='Cancellation Reason')
        
        tree.column('ID', width=100)
        tree.column('Customer', width=150)
        tree.column('VenueID', width=80)
        tree.column('Status', width=120)

        bookings = load_bookings()
        for b in bookings:
            reason = b.find('cancellation_reason').text if b.find('cancellation_reason') is not None else ''
            tree.insert('', tk.END, values=(
                b.find('id').text, 
                b.find('customer_email').text, 
                b.find('venue_id').text, 
                b.find('date').text, 
                b.find('time').text, 
                b.find('total_price').text, 
                b.find('status').text, 
                reason
            ))

        tree.pack(padx=10, pady=10, fill='both', expand=True)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def staff_view_logs_ui(self):
        """Staff Feature 6: View Staff Activity Logs (Rule 6: check the recorded)"""
        self.clear_screen()
        ttk.Label(self.root, text="Staff: Activity Logs (Logs_File)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        log_text = tk.Text(self.root, wrap='word', height=25, width=100)
        log_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        try:
            with open(LOGS_FILE, 'r') as f:
                content = f.read()
                # Filter to only show actions by staff (or actions where the user is the current staff)
                staff_logs = [line for line in content.splitlines() if f"User: {self.current_user_email}" in line or "Action: Submitted new venue" in line or "Action: Updated venue" in line or "STAFF OVERRIDE" in line]
                log_text.insert(tk.END, "\n".join(staff_logs))
        except FileNotFoundError:
            log_text.insert(tk.END, "Log file not found.")
        except Exception as e:
            log_text.insert(tk.END, f"Error reading log file: {e}")

        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def staff_view_update_venues_ui(self):
        """Staff Feature 2: View and Update Venues (Rule 3.v)"""
        self.clear_screen()
        ttk.Label(self.root, text="Staff: View/Update My Venues", font=('Arial', 16, 'bold')).pack(pady=10)
        
        venues = load_venues()
        my_venues = [v for v in venues if v.find('added_by').text == self.current_user_email]

        tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Type', 'Price', 'Capacity', 'Duration', 'Status'), show='headings')
        tree.heading('ID', text='Venue ID')
        tree.heading('Name', text='Name')
        tree.heading('Type', text='Type')
        tree.heading('Price', text='Price')
        tree.heading('Capacity', text='Capacity')
        tree.heading('Duration', text='Duration (hrs)')
        tree.heading('Status', text='Status (Rule 3.vi)')
        
        tree.column('ID', width=100)
        tree.column('Name', width=150)
        tree.column('Status', width=100)
        
        for v in my_venues:
            tree.insert('', tk.END, values=(
                v.find('id').text, 
                v.find('name').text,
                v.find('type').text if v.find('type') is not None else 'N/A',
                v.find('price').text,
                v.find('capacity').text,
                v.find('duration').text if v.find('duration') is not None else 'N/A',
                v.find('status').text
            ))

        tree.pack(padx=10, pady=10, fill='both', expand=True)
        
        ttk.Button(self.root, text="Modify Selected Venue", command=lambda: self.staff_modify_venue_details(tree)).pack(pady=10)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def staff_modify_venue_details(self, tree):
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a venue to modify.")
            return

        v_id = tree.item(selected_item, 'values')[0]
        venue = get_venue_by_id(v_id)
        
        if not venue:
            messagebox.showerror("Error", "Venue not found.")
            return

        modify_window = tk.Toplevel(self.root)
        modify_window.title(f"Modify Venue: {venue.find('name').text}")
        modify_window.configure(bg=GREY)

        fields = [
            ('Price:', 'price'),
            ('Capacity:', 'capacity'),
            ('Duration (hrs):', 'duration'),
            ('Type:', 'type'),
        ]
        
        entries = {}
        for i, (label_text, key) in enumerate(fields):
            ttk.Label(modify_window, text=label_text).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entries[key] = ttk.Entry(modify_window, width=30)
            entries[key].insert(0, venue.find(key).text if venue.find(key) is not None else '')
            entries[key].grid(row=i, column=1, sticky='ew', padx=5, pady=5)

        # Description (Rule 3.ii)
        ttk.Label(modify_window, text="Description:").grid(row=len(fields), column=0, sticky='nw', padx=5, pady=5)
        description_text = tk.Text(modify_window, height=5, width=30)
        description_text.insert(tk.END, venue.find('description').text if venue.find('description') is not None else '')
        description_text.grid(row=len(fields), column=1, sticky='ew', padx=5, pady=5)
        entries['description'] = description_text
        
        # Status (Rule 3.vi: hidden, availability ('active'), pending_approval)
        ttk.Label(modify_window, text="Status (Rule 3.vi):").grid(row=len(fields) + 1, column=0, sticky='w', padx=5, pady=5)
        
        status_var = tk.StringVar(modify_window)
        current_status = venue.find('status').text

        if current_status == 'pending_approval':
            status_options = ['pending_approval'] # Only show this option
            combo_state = 'disabled' # And disable the dropdown
        else:
            # If status is 'active' or 'hidden', it's already approved.
            # Don't allow changing it back to 'pending_approval'.
            status_options = ['active', 'hidden']
            combo_state = 'readonly'
        
        # Set the current value
        status_var.set(current_status if current_status in status_options else status_options[0])

        status_combo = ttk.Combobox(modify_window, textvariable=status_var, values=status_options, state=combo_state, width=28)
        status_combo.grid(row=len(fields) + 1, column=1, sticky='ew', padx=5, pady=5)
        entries['status_var'] = status_var

        def save_modifications():
            update_data = {}
            for key, entry in entries.items():
                if key == 'description':
                    update_data[key] = entry.get("1.0", tk.END).strip()
                elif key == 'status_var':
                    update_data['status'] = entry.get()
                else:
                    update_data[key] = entry.get()

            success, msg = staff_update_venue(v_id, update_data, self.current_user_email)
            if success:
                messagebox.showinfo("Success", msg)
                modify_window.destroy()
                self.staff_view_update_venues_ui() # Refresh the list
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(modify_window, text="Save & Update Venue (Rule 3.v)", command=save_modifications, style='TButton').grid(row=len(fields) + 2, column=0, columnspan=2, pady=15, sticky='ew', padx=5)

