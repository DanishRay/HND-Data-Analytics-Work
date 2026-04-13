# customer.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime, date
import os
from PIL import Image, ImageTk

# Import all the backend functions this UI needs
from Backend import (
    load_venues, is_venue_booked_on_date, is_venue_available,
    create_booking, load_bookings, customer_cancel_booking,
    get_system_setting, load_notifications, get_venue_attachments
)
from Config import GREY # Import constants needed by this UI

class CustomerMixin:
    # ==================================
    # CUSTOMER FEATURES (6) (Rule 2, 3.iii, 15, 18)
    # ==================================
    def customer_menu(self, frame):
        # Rule 2: All roles should have 6 features
        features = [
            ("1. Search & Book Venue", self.search_and_book_ui), # Rule 3.iii
            ("2. View My Bookings", self.view_my_bookings_ui),
            ("3. Cancel My Booking (Reason)", self.customer_cancel_booking_ui), # Rule 15
            ("4. View Notifications & Status Updates", self.customer_notifications_ui), # Rule 18
            ("5. View Venue Images/Attachments", self.customer_view_attachments_ui),
            ("6. View Cancellation Policy", self.customer_view_policy_ui), # Rule 15
        ]

        for text, command in features:
            ttk.Button(frame, text=text, command=command, width=50).pack(pady=5)

    def search_and_book_ui(self):
        """Customer Feature 1: Search and Book Venue (Rule 3.iii)"""
        self.clear_screen()
        ttk.Label(self.root, text="Customer: Search & Book Venue", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # --- Search/Filter Frame (Rule 3.iii: type of hall, date) ---
        filter_frame = ttk.Frame(self.root, padding="10", style='TFrame')
        filter_frame.pack(pady=10, padx=10, fill='x')
        
        # 1. Date Filter (Rule 3.iii)
        ttk.Label(filter_frame, text="Event Date (YYYY-MM-DD):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.search_date = ttk.Entry(filter_frame, width=15)
        self.search_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.search_date.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        
        # 2. Type of Hall Filter (Rule 3.iii)
        ttk.Label(filter_frame, text="Type of Hall:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        venue_types = ["(All Types)", "Ballroom", "Theatre", "Conference Hall", "Outdoor Space", "Other"]
        self.search_type = ttk.Combobox(filter_frame, values=venue_types, width=15, state='readonly')
        self.search_type.set(venue_types[0])
        self.search_type.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        # 3. Capacity/Price Range Filter (Rule 3.iii)
        ttk.Label(filter_frame, text="Min. Capacity:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.search_capacity = ttk.Entry(filter_frame, width=15)
        self.search_capacity.insert(0, "0")
        self.search_capacity.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Max. Price:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.search_price = ttk.Entry(filter_frame, width=15)
        self.search_price.insert(0, "99999")
        self.search_price.grid(row=1, column=3, sticky='w', padx=5, pady=5)

        ttk.Button(filter_frame, text="Search Venues", command=self.perform_venue_search, style='TButton').grid(row=0, column=4, rowspan=2, padx=15, sticky='ns')

        # --- Venue List Treeview ---
        self.venue_tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Type', 'Price', 'Capacity', 'Duration', 'Availability'), show='headings')
        self.venue_tree.heading('ID', text='ID')
        self.venue_tree.heading('Name', text='Venue Name')
        self.venue_tree.heading('Type', text='Type')
        self.venue_tree.heading('Price', text='Price/hr')
        self.venue_tree.heading('Capacity', text='Capacity')
        self.venue_tree.heading('Duration', text='Duration (hrs)')
        self.venue_tree.heading('Availability', text='Status on Date (Rule 3.vi)')
        
        self.venue_tree.column('ID', width=100)
        self.venue_tree.column('Name', width=180)
        self.venue_tree.column('Availability', width=150)
        
        self.venue_tree.pack(padx=10, pady=10, fill='both', expand=True)
        
        ttk.Button(self.root, text="Book Selected Venue", command=self.prompt_booking_details, style='TButton').pack(pady=10)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)
        
        self.perform_venue_search() # Initial load

    def perform_venue_search(self):
        """Performs search based on filters (Rule 3.iii)"""
        try:
            search_date_str = self.search_date.get()
            search_type = self.search_type.get()
            min_capacity = int(self.search_capacity.get())
            max_price = float(self.search_price.get())
            search_date_dt = datetime.strptime(search_date_str, "%Y-%m-%d").date()
            today = date.today()

            if search_date_dt < today:
                # Raise a error message for past dates
                messagebox.showerror("Input Error", "The chosen date must not be in the past.")
                return # Stop the function immediately
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input format for date/capacity/price: {e}")
            return
            
        # Clear previous results
        for item in self.venue_tree.get_children():
            self.venue_tree.delete(item)
            
        all_venues = load_venues()
        
        for v in all_venues:
            v_status = v.find('status').text
            v_type = v.find('type').text if v.find('type') is not None else 'Other'
            
            # 1. Filter by Venue Status (Rule 3.vi: hidden cannot be viewed)
            if v_status != 'active': # Only show 'active' (availability)
                continue
                
            v_capacity = int(v.find('capacity').text)
            v_price = float(v.find('price').text)
            v_duration = v.find('duration').text if v.find('duration') is not None else 'N/A'

            # 2. Filter by Search Criteria (Rule 3.iii: type of hall)
            if search_type != "(All Types)" and v_type != search_type:
                continue
                
            # 3. Filter by Capacity/Price Range (Rule 3.iii: capacity, price range)
            if v_capacity < min_capacity or v_price > max_price:
                continue

            # 4. NEW FILTER: Check against Venue Start Date 🗓️
            v_start_date_elem = v.find('start_date')
            if v_start_date_elem is not None and v_start_date_elem.text: 
                try:
                    v_start_date_str = v_start_date_elem.text
                    v_start_date_dt = datetime.strptime(v_start_date_str, "%Y-%m-%d").date()

                    if search_date_dt < v_start_date_dt:
                        continue

                except ValueError:
                    # If the date format in the XML is bad, skip the venue or assume it's valid.
                    # For robustness, we'll continue to the next venue.
                    continue
 
            # 5. Filter by Date Availability (Rule 3.vi: booked should be hidden/status shown)
            is_booked_for_day = is_venue_booked_on_date(v.find('id').text, search_date_str)

            if is_booked_for_day:
                availability_status = "Booked (Unavailable for day)" # Rule 3.vi: booked
            else:
                availability_status = "Available (Ready to book)" # Rule 3.vi: availability
                
            self.venue_tree.insert('', tk.END, values=(
                v.find('id').text, 
                v.find('name').text,
                v_type,
                v_price,
                v_capacity,
                v_duration,
                availability_status
            ))

    def prompt_booking_details(self):
        selected_item = self.venue_tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a venue to book.")
            return
            
        v_id, v_name, v_type, v_price_str, v_capacity_str, v_duration_str, v_status_on_date = self.venue_tree.item(selected_item, 'values')
        
        if v_status_on_date == "Booked (Unavailable for day)":
             messagebox.showerror("Booking Blocked", f"Venue {v_name} is fully booked on the selected date ({self.search_date.get()}). Please choose another date or venue.")
             return
             
        v_price = float(v_price_str)
        v_capacity = int(v_capacity_str)
        if v_duration_str == 'N/A':
            v_duration_max = 24  # Default max if not specified, to avoid error
        else:
            v_duration_max = int(v_duration_str)

        # Pop-up for booking details
        booking_window = tk.Toplevel(self.root)
        booking_window.title(f"Book Venue: {v_name}")
        booking_window.configure(bg=GREY)
        
        ttk.Label(booking_window, text=f"Booking Details for {v_name} ({v_id})", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Date (from search)
        ttk.Label(booking_window, text="Date:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        date_label = ttk.Label(booking_window, text=self.search_date.get())
        date_label.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        # Start Time
        ttk.Label(booking_window, text="Start Time (HH:MM 24hr):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        time_entry = ttk.Entry(booking_window, width=10)
        time_entry.insert(0, "09:00")
        time_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # Duration (Rule 3.iv)
        ttk.Label(booking_window, text=f"Duration (Max {v_duration_max} hrs):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        duration_entry = ttk.Entry(booking_window, width=10)
        duration_entry.insert(0, "4") # Default duration
        duration_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        
        # Capacity Required
        ttk.Label(booking_window, text=f"Guests (Max {v_capacity}):").grid(row=4, column=0, sticky='w', padx=5, pady=5)
        capacity_entry = ttk.Entry(booking_window, width=10)
        capacity_entry.insert(0, "10")
        capacity_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)
        
        def calculate_price():
            try:
                duration = int(duration_entry.get())
                total = duration * v_price
                total_price_label.config(text=f"RM {total:.2f}")
                return total
            except:
                total_price_label.config(text="Error in calculation.")
                return 0.0

        ttk.Label(booking_window, text="Total Price:").grid(row=5, column=0, sticky='w', padx=5, pady=5)
        total_price_label = ttk.Label(booking_window, text=f"RM 0.00", font=('Arial', 12, 'bold'))
        total_price_label.grid(row=5, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Button(booking_window, text="Calculate Price", command=calculate_price).grid(row=6, column=0, columnspan=2, pady=5)
        
        def perform_booking():
            try:
                date_str = self.search_date.get()
                time_str = time_entry.get()
                duration_hrs = int(duration_entry.get())
                capacity_required = int(capacity_entry.get())
                total_price = calculate_price()
                
                if total_price <= 0:
                     messagebox.showerror("Booking Error", "Price calculation error. Check duration input.")
                     return

                if duration_hrs > v_duration_max:
                    messagebox.showerror("Input Error", f"Duration exceeds maximum allowed ({v_duration_max} hours).")
                    return
                
                if capacity_required > v_capacity:
                     messagebox.showerror("Input Error", f"Capacity required exceeds venue capacity ({v_capacity}).")
                     return

                if not is_venue_available(v_id, date_str, time_str, duration_hrs):
                    messagebox.showerror("Availability Conflict", "The selected time slot conflicts with an existing confirmed booking.")
                    return

                # Booking is good, create it
                success, msg = create_booking(v_id, self.current_user_email, date_str, time_str, duration_hrs, capacity_required, total_price)
                if success:
                    messagebox.showinfo("Booking Confirmation", msg)
                    booking_window.destroy()
                    self.search_and_book_ui() # Refresh
                else:
                    messagebox.showerror("Booking Failed", msg)

            except ValueError:
                messagebox.showerror("Input Error", "Please ensure time is HH:MM and duration/guests are valid numbers.")
                
        ttk.Button(booking_window, text="Confirm Booking (PENDING Approval)", command=perform_booking, style='TButton').grid(row=7, column=0, columnspan=2, pady=15)

    def view_my_bookings_ui(self):
        self.clear_screen()
        ttk.Label(self.root, text="Customer: View My Bookings", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('ID', 'VenueID', 'Date', 'Time', 'Price', 'Status', 'Reason'), show='headings')
        tree.heading('ID', text='Booking ID (Rule 4)')
        tree.heading('VenueID', text='Venue ID')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Price', text='Total Price')
        tree.heading('Status', text='Status (Rule 18)')
        tree.heading('Reason', text='Cancel Reason')
        
        tree.column('ID', width=120)
        tree.column('Status', width=120)

        bookings = [b for b in load_bookings() if b.find('customer_email').text == self.current_user_email]
        for b in bookings:
            reason = b.find('cancellation_reason').text if b.find('cancellation_reason') is not None else ''
            tree.insert('', tk.END, values=(b.find('id').text, b.find('venue_id').text, b.find('date').text, b.find('time').text, b.find('total_price').text, b.find('status').text, reason))
            
        tree.pack(padx=10, pady=10, fill='both', expand=True)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def customer_cancel_booking_ui(self):
        """Customer Feature 3: Cancel My Booking (Rule 15)"""
        self.clear_screen()
        ttk.Label(self.root, text="Customer: Cancel My Booking (Rule 11, 15)", font=('Arial', 16, 'bold')).pack(pady=10)

        tree = ttk.Treeview(self.root, columns=('ID', 'VenueID', 'Date', 'Time', 'Price', 'Status'), show='headings')
        tree.heading('ID', text='Booking ID')
        tree.heading('VenueID', text='Venue ID')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Price', text='Total Price')
        tree.heading('Status', text='Status')
        
        bookings = [b for b in load_bookings() if b.find('customer_email').text == self.current_user_email]
        for b in bookings:
            status = b.find('status').text
            if status in ['CONFIRMED', 'PENDING']: 
                 tree.insert('', tk.END, values=(b.find('id').text, b.find('venue_id').text, b.find('date').text, b.find('time').text, b.find('total_price').text, status))
            
        tree.pack(padx=10, pady=10, fill='x')
        
        ttk.Button(self.root, text="Cancel Selected Booking", command=lambda: self.customer_cancel_action(tree)).pack(pady=10)
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def customer_cancel_action(self, tree):
        """Customer Feature 3: Cancels a booking, applying the refund policy and requiring reason. (Rule 15)"""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a reservation to cancel.")
            return

        b_id = tree.item(selected_item, 'values')[0]
        b_status = tree.item(selected_item, 'values')[5]

        if b_status not in ['CONFIRMED', 'PENDING']:
             messagebox.showwarning("Cancellation Blocked", f"This reservation is in status: {b_status} and cannot be modified or cancelled.")
             return

        if not messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel reservation {b_id}?"):
            return

        # Rule 15: Must have fixed valid reason
        reasons_str = get_system_setting('customer_cancellation_reasons')
        reasons = [r.strip() for r in reasons_str.split(';') if r.strip()]
        
        reason = simpledialog.askstring("Cancellation Reason (Rule 15)", 
                                        f"Select or enter your cancellation reason:\nOptions: {', '.join(reasons)}", 
                                        parent=self.root)
                                        
        if not reason:
             messagebox.showwarning("Warning", "Cancellation reason is mandatory (Rule 15).")
             return

        success, msg = customer_cancel_booking(b_id, self.current_user_email, reason)
        if success:
            messagebox.showinfo("Success", msg)
            self.customer_cancel_booking_ui()
        else:
            messagebox.showerror("Error", msg)

    def customer_notifications_ui(self):
        """Customer Feature 4: View Notifications & Status Updates (Rule 18)"""
        self.clear_screen()
        ttk.Label(self.root, text="Customer: Notifications & Booking Status Updates (Rule 18)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        tree = ttk.Treeview(self.root, columns=('Date', 'BookingID', 'Status', 'Message'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('BookingID', text='Booking ID')
        tree.heading('Status', text='Status')
        tree.heading('Message', text='Update Message')
        
        tree.column('Date', width=150)
        tree.column('BookingID', width=100)
        tree.column('Status', width=120)
        tree.column('Message', width=450)
        
        notifications = load_notifications(self.current_user_email)
        for created_at, b_id, status, msg in notifications:
            tree.insert('', tk.END, values=(created_at, b_id, status, msg))

        tree.pack(padx=10, pady=10, fill='both', expand=True)
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def customer_view_attachments_ui(self):
        """Customer Feature 5: View Venue Images/Attachments"""
        self.clear_screen()
        ttk.Label(self.root, text="Customer: View Venue Attachments (e.g., Floor Plans, Safety Docs)", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # 1. Select Venue
        ttk.Label(self.root, text="Select a Venue:").pack(pady=5)
        
        venues = load_venues()
        active_venues = [v for v in venues if v.find('status').text == 'active'] # Only show 'active' venues (Rule 3.vi)
        venue_options = {v.find('name').text: v.find('id').text for v in active_venues}
        self.selected_venue_view_id = tk.StringVar(self.root)
        
        if not venue_options:
            ttk.Label(self.root, text="No active venues available.").pack(pady=10)
            ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)
            return

        venue_names = list(venue_options.keys())
        self.selected_venue_view_id.set(venue_names[0])

        venue_combo = ttk.Combobox(self.root, values=venue_names, textvariable=self.selected_venue_view_id, state='readonly', width=50)
        venue_combo.pack(pady=5)

        # Attachment List
        self.attachment_tree = ttk.Treeview(self.root, columns=('Type', 'File Name', 'Path'), show='headings')
        self.attachment_tree.heading('Type', text='Attachment Type (Rule 16)')
        self.attachment_tree.heading('File Name', text='File Name')
        self.attachment_tree.heading('Path', text='Path')
        self.attachment_tree.column('Type', width=300)
        self.attachment_tree.column('File Name', width=300)
        self.attachment_tree.column('Path', width=0, stretch=tk.NO)
        self.attachment_tree.pack(padx=10, pady=10, fill='x')

        self.preview_label = ttk.Label(self.root, text="Select an attachment to preview the image.")
        self.preview_label.pack(pady=10, fill='x')

        self.attachment_tree.bind("<<TreeviewSelect>>", self.preview_attachment)

        def load_attachments():
            v_name = self.selected_venue_view_id.get()
            v_id = venue_options.get(v_name)
            
            for item in self.attachment_tree.get_children():
                self.attachment_tree.delete(item)
                
            attachments = get_venue_attachments(v_id)
            if not attachments:
                 self.attachment_tree.insert('', tk.END, values=('No attachments available.', '', ''))
                 return

            for attachment_type, file_path in attachments:
                file_name = os.path.basename(file_path)
                self.attachment_tree.insert('', tk.END, values=(attachment_type, file_name, file_path))
                
        ttk.Button(self.root, text="Load Attachments", command=load_attachments).pack(pady=10)
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=5)

    def preview_attachment(self, event):
        selected = self.attachment_tree.focus()
        if not selected:
            return

        values = self.attachment_tree.item(selected, 'values')
        if len(values) < 3:
            return

        attachment_type, file_name, file_path = values

        if not file_path:
            self.preview_label.config(image='', text="No file path available.")
            return

        ext = os.path.splitext(file_name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            try:
                img = Image.open(file_path)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                self.current_photo = ImageTk.PhotoImage(img)
                self.preview_label.config(image=self.current_photo, text="")
            except Exception as e:
                self.preview_label.config(image='', text=f"Error loading image: {e}")
        else:
            self.preview_label.config(image='', text="Selected file is not a supported image format. Preview only available for images.")

    def customer_view_policy_ui(self):
        """Customer Feature 6: View Cancellation Policy (Rule 15)"""
        self.clear_screen()
        ttk.Label(self.root, text="Customer: Cancellation and Refund Policy (Rule 15)", font=('Arial', 16, 'bold')).pack(pady=10)

        # Refund Threshold
        threshold = get_system_setting('refund_threshold_hours')
        ttk.Label(self.root, text=f"**Refund Eligibility Threshold**:", font=('Arial', 12, 'bold')).pack(pady=(15, 5))
        ttk.Label(self.root, text=f"Full refund is typically processed if cancellation occurs more than {threshold} hours before the event date/time.").pack(padx=20)
        ttk.Label(self.root, text="Cancellations within this period may result in no refund (see terms and conditions).").pack(padx=20)
        
        # Customer Reasons (Rule 15)
        customer_reasons_str = get_system_setting('customer_cancellation_reasons')
        customer_reasons = [r.strip() for r in customer_reasons_str.split(';') if r.strip()]
        ttk.Label(self.root, text="\n**Accepted Cancellation Reasons (Customer)**:", font=('Arial', 12, 'bold')).pack(pady=(15, 5))
        
        reasons_text = tk.Text(self.root, height=len(customer_reasons) + 1, width=60, wrap='word')
        for reason in customer_reasons:
            reasons_text.insert(tk.END, f"- {reason}\n")
        reasons_text.config(state=tk.DISABLED)
        reasons_text.pack(padx=20, pady=5)
        
        ttk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=20)