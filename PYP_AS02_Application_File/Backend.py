# backend.py
from datetime import datetime, date, timedelta
import os
import xml.etree.ElementTree as ET
import bcrypt
import random
import string
import shutil
import mimetypes
import csv
import json
import traceback

# Import all constants from our new config file
from Config import *

# ==============================================================================
# 1. CORE XML & UTILITY FUNCTIONS
# ==============================================================================

def load_data(filename):
    """Loads and returns the ElementTree and root element from an XML file."""
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        return tree, root
    except FileNotFoundError:
        return None, None
    except ET.ParseError:
        log_action("SYSTEM", f"Error parsing {filename}. File corrupted or empty.")
        return None, None

def save_data(tree, filename):
    """Saves the ElementTree back to the XML file."""
    try:
        tree.write(filename, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        log_action("SYSTEM", f"Error saving {filename}: {e}")

def log_action(user, action):
    """Logs system events with a timestamp. (Rule 6: Check the recorded)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User: {user} | Action: {action}\n"
    try:
        with open(LOGS_FILE, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write to log file: {e}")

def generate_unique_id(prefix):
    """Generates a unique ID (e.g., BOOK-12345). (Rule 4)"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}-{timestamp}-{rand}"

def initialize_files():
    """Ensures all required XML and log files exist on startup."""
    files = {
        USERS_FILE: 'users',
        VENUES_FILE: 'venues',
        BOOKINGS_FILE: 'bookings',
        SETTINGS_FILE: 'settings'
    }

    for filename, root_tag in files.items():
        if not os.path.exists(filename) or os.stat(filename).st_size == 0:
            root = ET.Element(root_tag)
            tree = ET.ElementTree(root)
            save_data(tree, filename)
            log_action("SYSTEM", f"Initialized new XML file: {filename}")

    # Ensure Super Admin account exists (Rule 8, 9)
    if get_user(ADMIN_EMAIL) is None:
        # Using a special password marker to trigger PIN check logic
        create_user(
            ADMIN_EMAIL,
            "HARDCODED_PIN_PASSWORD_BYPASS",
            "Super Admin",
            "superadmin",
            "approved"
        )
        log_action("SYSTEM", "Super Admin account initialized and **SAVED**.")
    else:
        log_action("SYSTEM", "Super Admin account found. Initialization skipped.")

    def create_hardcoded_admin():
        # 1. Use the core utility to load the data (handles file parsing errors)
        tree, root = load_data(USERS_FILE) 
    
        # 2. Check if the admin already exists (based on your hardcoded email)
        if root.find(f"./user[email='{ADMIN_EMAIL}']") is not None:
            return # Admin already exists, do nothing

        # If the admin does NOT exist, create the account:
    
        # 3. Create a default password hash (since bcrypt is installed)
        password_hash = bcrypt.hashpw(ADMIN_PIN.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
        # 4. Build the XML element for the new Admin
        admin_user = ET.SubElement(root, 'user')
        ET.SubElement(admin_user, 'email').text = ADMIN_EMAIL
        ET.SubElement(admin_user, 'password').text = password_hash
        ET.SubElement(admin_user, 'role').text = 'Admin' # Correct role
        ET.SubElement(admin_user, 'status').text = 'active'
    
        # 5. Save the updated XML tree
        save_data(tree, USERS_FILE)


# ==============================================================================
# 2. SECURITY & USER MANAGEMENT UTILITIES
# ==============================================================================

def hash_password(password):
    """Hashes a password using bcrypt. (Rule 1, 7: Password MUST be ## in xml)"""
    # The stored password in XML is the bcrypt hash, which is secure.
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password_input, hashed_password):
    """Checks the input password against the stored hash."""
    try:
        return bcrypt.checkpw(password_input.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False

def get_user(email):
    """Retrieves a user element from the USERS_FILE by email."""
    _, root = load_data(USERS_FILE)
    if root is not None:
        # XPath check for the user
        return root.find(f"./user[email='{email}']")
    return None

def get_all_users():
    """Retrieves all user elements."""
    _, root = load_data(USERS_FILE)
    if root is not None:
        return root.findall("./user")
    return []

def create_user(email, password_input, name, role, status="pending"):
    """Adds a new user to the XML file. (Rule 3)"""
    tree, root = load_data(USERS_FILE)
    if root is None:
        root = ET.Element('users')
        tree = ET.ElementTree(root)

    if get_user(email):
        return False, "Error: Email already exists."

    # Store the secure hash (or the special marker for Admin) (Rule 7)
    if role == 'superadmin':
        final_password = password_input # Store the hardcoded marker
    else:
        final_password = hash_password(password_input) # Store as bcrypt hash (Rule 7)

    user = ET.SubElement(root, 'user')
    ET.SubElement(user, 'email').text = email
    ET.SubElement(user, 'password').text = final_password
    ET.SubElement(user, 'name').text = name
    ET.SubElement(user, 'role').text = role
    ET.SubElement(user, 'status').text = status # 'pending', 'approved', 'deactivated'
    ET.SubElement(user, 'created_at').text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_data(tree, USERS_FILE)
    log_action("SYSTEM", f"New user created: {email} with role {role}. Status: {status}")
    return True, "User created successfully."

def login_user(email, password_input):
    """Authenticates a user based on email and password, handling Admin PIN logic. (Rule 9, 10)"""
    user_element = get_user(email)

    if user_element is None:
        return False, None, "Login Error", "User not found."

    role = user_element.find('role').text
    status = user_element.find('status').text
    stored_password = user_element.find('password').text

    if status == 'pending':
        return False, None, "Login Error", "Your account is pending admin approval."
    if status == 'deactivated':
        return False, None, "Login Error", "Your account has been deactivated."

    # --- ADMIN SPECIAL LOGIN LOGIC (Rule 9) ---
    if email == ADMIN_EMAIL and password_input == "hardcoded_trigger":
        return True, role, "PIN_REQUIRED", "Admin PIN is required."

    # --- STAFF/CUSTOMER LOGIN LOGIC (Rule 10) ---
    if check_password(password_input, stored_password):
        log_action(email, "Login successful.")
        return True, role, "Success", "Login successful."
    else:
        log_action(email, "Login failed: incorrect password.")
        return False, None, "Login Error", "Incorrect password."

def approve_user(email, admin_email):
    """Admin Feature: Approves a pending user (staff/customer)."""
    tree, root = load_data(USERS_FILE)
    user = root.find(f"./user[email='{email}']")
    if user is None:
        return False, "User not found."

    if user.find('status').text == 'approved':
        return False, "User is already approved."

    user.find('status').text = 'approved'
    save_data(tree, USERS_FILE)
    log_action(admin_email, f"Approved user: {email}.")
    return True, f"User {email} approved successfully."

def deactivate_user(email, admin_email):
    """Admin Feature: Deactivates an approved user."""
    tree, root = load_data(USERS_FILE)
    user = root.find(f"./user[email='{email}']")
    if user is None:
        return False, "User not found."

    if user.find('role').text == 'superadmin':
        return False, "Cannot deactivate the Super Admin account."

    if user.find('status').text == 'deactivated':
        return False, "User is already deactivated."

    user.find('status').text = 'deactivated'
    save_data(tree, USERS_FILE)
    log_action(admin_email, f"Deactivated user: {email}.")
    return True, f"User {email} deactivated successfully."

# ==============================================================================
# 3. VENUE MANAGEMENT UTILITIES
# ==============================================================================

# Venue Statuses (Rule 3.vi): pending_approval, active (availability), hidden
def load_venues():
    """Loads all venues from the XML file."""
    _, root = load_data(VENUES_FILE)
    return root.findall("./venue") if root is not None else []

def get_venue_by_id(v_id):
    """Retrieves a venue element by ID."""
    _, root = load_data(VENUES_FILE)
    if root is not None:
        return root.find(f"./venue[id='{v_id}']")
    return None

def add_venue(name, description, type, price, capacity, duration, staff_email, start_date):
    """Staff Feature 1: Adds a new venue from a form. (Rule 3.i, 3.ii, 3.iv)"""
    tree, root = load_data(VENUES_FILE)

    # Check for required fields (Rule 3.i error check)
    if not all([name, description, type, price, capacity, duration, staff_email, start_date]):
        return False, "Error: All fields (Name, Description, Type, Price, Capacity, Duration, Start_date) are required."

    if root.find(f"./venue[name='{name}']") is not None:
        return False, "Error: Venue name must be unique."

    try:
        float(price)
        int(capacity)
        int(duration)
    except ValueError:
        return False, "Error: Price must be a number, and Capacity/Duration must be integers."

    try:
        v_id = generate_unique_id("VEN")
        venue = ET.SubElement(root, 'venue')
        ET.SubElement(venue, 'id').text = v_id
        ET.SubElement(venue, 'name').text = name
        ET.SubElement(venue, 'description').text = description # Rule 3.ii
        ET.SubElement(venue, 'type').text = type # Rule 3.iii
        ET.SubElement(venue, 'price').text = price
        ET.SubElement(venue, 'capacity').text = capacity
        ET.SubElement(venue, 'duration').text = duration # Rule 3.iv
        ET.SubElement(venue, 'start_date').text = start_date
        # Initial status: pending_approval
        ET.SubElement(venue, 'status').text = 'pending_approval'
        ET.SubElement(venue, 'added_by').text = staff_email
        ET.SubElement(venue, 'added_at').text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_data(tree, VENUES_FILE)
        log_action(staff_email, f"Submitted new venue for approval: {name} ({v_id})")
        return True, f"Venue submitted successfully for Admin approval. ID: {v_id}"
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

def staff_update_venue(v_id, data, staff_email):
    """Staff Feature 2 / Rule 3.v: Updates a venue's details."""
    tree, root = load_data(VENUES_FILE)
    venue = root.find(f"./venue[id='{v_id}']")
    if venue is None:
        return False, "Venue not found."

    log_changes = []

    # Editable fields: price, capacity, description, duration, status, type (Rule 3.v)
    for key, value in data.items():
        if key in ['price', 'capacity', 'description', 'duration', 'status', 'type']:
            # Validate status (Rule 3.vi: availability is 'active')
            if key == 'status' and value not in ['active', 'hidden', 'pending_approval']:
                 return False, f"Invalid status: {value}. Use 'active', 'hidden', or 'pending_approval'."

            current_value = venue.find(key).text if venue.find(key) is not None else ''

            if current_value != str(value):
                log_changes.append(f"{key} changed from '{current_value}' to '{value}'")
                if venue.find(key) is not None:
                    venue.find(key).text = str(value)
                else:
                    ET.SubElement(venue, key).text = str(value)

    save_data(tree, VENUES_FILE)
    if log_changes:
        log_action(staff_email, f"Updated venue {v_id}. Changes: {', '.join(log_changes)}")

    return True, "Venue updated successfully."

def is_venue_booked_on_date(v_id, check_date_str):
    """Checks if a venue is booked for the entire day (Rule 3.vi: booked)."""
    bookings = load_bookings()
    for b in bookings:
        if b.find('venue_id').text == v_id and b.find('status').text in ['CONFIRMED', 'PENDING']:
            if b.find('date').text == check_date_str:
                # The assumption here is that if a booking exists on this date, 
                # the venue is considered "booked" for the day, which matches the rule:
                # "...should be hidden to the other customer cus its already been book by other custome..."
                # However, for granular booking, the time slot check is more accurate. 
                # For the customer list view, this simpler check is used for the "booked" status label.
                return True
    return False

def is_venue_booked(v_id):
    """Checks if a venue has any existing FUTURE CONFIRMED or PENDING bookings. (Rule 5, 12)"""
    bookings = load_bookings()
    today = datetime.now().date()
    for b in bookings:
        b_venue_id = b.find('venue_id').text
        b_status = b.find('status').text

        if b_venue_id == v_id and b_status in ['CONFIRMED', 'PENDING']:
            try:
                booking_date_str = b.find('date').text
                booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
                if booking_date >= today:
                    return True # Venue has a future or current active booking
            except:
                continue
    return False

def admin_delete_venue(v_id, admin_email):
    """Admin only: Deletes a venue only if it has NO future bookings (Rule 5, 12)."""
    if is_venue_booked(v_id):
        log_action(admin_email, f"Blocked deletion of venue {v_id}: It has current/future bookings.")
        # Rule 5 error message
        return False, "Sorry, this venue cannot be permanently deleted because it is already been used/booked. You must cancel all associated bookings first."

    tree, root = load_data(VENUES_FILE)
    venue = root.find(f"./venue[id='{v_id}']")

    if venue is None:
        return False, "Venue not found."

    root.remove(venue)
    save_data(tree, VENUES_FILE)
    log_action(admin_email, f"Permanently deleted venue: {v_id}.")
    return True, "Venue successfully deleted."

# Helper function for Staff to manage attachments (Rule 16)
def save_venue_attachment(v_id, file_path, attachment_type):
    """Saves a file path to the venue's XML entry. (Rule 16)"""
    tree, root = load_data(VENUES_FILE)
    venue = root.find(f"./venue[id='{v_id}']")
    if venue is None:
        return False, "Venue not found."

    venue_dir = os.path.join(VENUE_ATTACHMENTS_DIR, v_id)
    if not os.path.exists(venue_dir):
        os.makedirs(venue_dir)

    file_name = os.path.basename(file_path)
    destination = os.path.join(venue_dir, f"{attachment_type}_{file_name}")
    try:
        shutil.copy(file_path, destination)
    except Exception as e:
        return False, f"Failed to save file: {e}"

    attachments = venue.find('attachments')
    if attachments is None:
        attachments = ET.SubElement(venue, 'attachments')

    attachment = ET.SubElement(attachments, 'file')
    ET.SubElement(attachment, 'type').text = attachment_type
    ET.SubElement(attachment, 'path').text = destination

    save_data(tree, VENUES_FILE)
    return True, f"Attachment uploaded for venue {v_id}."

def get_venue_attachments(v_id):
    """Retrieves all attachments for a venue."""
    venue = get_venue_by_id(v_id)
    if venue is None:
        return []
    
    attachments_root = venue.find('attachments')
    if attachments_root is None:
        return []
    
    return [
        (file.find('type').text, file.find('path').text)
        for file in attachments_root.findall('file')
    ]

# ==============================================================================
# 4. BOOKING MANAGEMENT UTILITIES
# ==============================================================================

def load_bookings():
    """Loads all bookings from the XML file."""
    _, root = load_data(BOOKINGS_FILE)
    return root.findall("./booking") if root is not None else []

def get_booking_by_id(b_id):
    """Retrieves a booking element by ID."""
    _, root = load_data(BOOKINGS_FILE)
    if root is not None:
        return root.find(f"./booking[id='{b_id}']")
    return None

def is_venue_available(v_id, check_date, start_time, duration_hrs):
    """Checks if a venue is available for a specific date/time slot."""
    bookings = load_bookings()
    try:
        check_dt = datetime.strptime(f"{check_date} {start_time}", "%Y-%m-%d %H:%M")
        if check_dt < datetime.now():
            return False

    except ValueError:
        return False

    for b in bookings:
        if b.find('venue_id').text == v_id and b.find('status').text in ['CONFIRMED', 'PENDING']:

            booked_date_str = b.find('date').text
            booked_time_str = b.find('time').text
            booked_duration_hrs = int(b.find('duration_hrs').text)

            booked_dt = datetime.strptime(f"{booked_date_str} {booked_time_str}", "%Y-%m-%d %H:%M")
            booked_end_dt = booked_dt + timedelta(hours=booked_duration_hrs)

            # Conflict check: If the requested time slot overlaps with a confirmed booking
            if check_dt < booked_end_dt and (check_dt + timedelta(hours=duration_hrs)) > booked_dt:
                return False
    return True

def create_booking(v_id, customer_email, date_str, time_str, duration_hrs, capacity_required, total_price):
    """Customer Feature 2: Creates a new booking and assigns a unique Booking ID. (Rule 4)"""
    tree, root = load_data(BOOKINGS_FILE)
    b_id = generate_unique_id("BOOK") # Rule 4

    booking = ET.SubElement(root, 'booking')
    ET.SubElement(booking, 'id').text = b_id # Rule 4
    ET.SubElement(booking, 'customer_email').text = customer_email
    ET.SubElement(booking, 'venue_id').text = v_id
    ET.SubElement(booking, 'date').text = date_str
    ET.SubElement(booking, 'time').text = time_str
    ET.SubElement(booking, 'duration_hrs').text = str(duration_hrs)
    ET.SubElement(booking, 'capacity_required').text = str(capacity_required)
    ET.SubElement(booking, 'total_price').text = f"{total_price:.2f}"
    ET.SubElement(booking, 'status').text = 'PENDING' # New default status for approval flow
    ET.SubElement(booking, 'booked_at').text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_data(tree, BOOKINGS_FILE)
    log_action(customer_email, f"New booking created for venue {v_id}. ID: {b_id}. Status: PENDING")
    add_notification(customer_email, b_id, 'PENDING') # Rule 18
    return True, f"Booking submitted successfully! Your **Booking ID** is **{b_id}**. Status is PENDING approval."

def update_booking_status(b_id, new_status, user_email, reason=''):
    """Allows Admin/Staff to update booking status (e.g., CONFIRMED, MODIFIED, CANCELLED)."""
    tree, root = load_data(BOOKINGS_FILE)
    booking = root.find(f"./booking[id='{b_id}']")

    if booking is None:
        return False, "Booking not found."

    if new_status in ['CANCELLED_BY_ADMIN', 'CANCELLED_BY_CUSTOMER', 'CANCELLED_BY_STAFF']:
        # Store cancellation reason (Rule 15)
        reason_element = booking.find('cancellation_reason')
        if reason_element is None:
            reason_element = ET.SubElement(booking, 'cancellation_reason')
        reason_element.text = reason
    elif new_status == 'MODIFIED':
        modification_element = booking.find('modification_details')
        if modification_element is None:
            modification_element = ET.SubElement(booking, 'modification_details')
        modification_element.text = f"Modified by {user_email} on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    elif new_status == 'CONFIRMED':
        # Remove cancellation reason if re-confirming a previously cancelled booking (unlikely in this flow)
        reason_element = booking.find('cancellation_reason')
        if reason_element is not None:
            reason_element.text = ''

    booking.find('status').text = new_status
    save_data(tree, BOOKINGS_FILE)
    log_action(user_email, f"Booking {b_id} status updated to {new_status}.")

    add_notification(booking.find('customer_email').text, b_id, new_status) # Rule 18

    return True, f"Booking {b_id} status updated to {new_status}."

def admin_approve_booking(b_id, admin_email):
    """Admin Feature: Approves a PENDING booking."""
    tree, root = load_data(BOOKINGS_FILE)
    booking = root.find(f"./booking[id='{b_id}']")

    if booking is None:
        return False, "Booking not found."

    if booking.find('status').text != 'PENDING':
        return False, f"Booking is not PENDING. Current status: {booking.find('status').text}"

    # Change status to CONFIRMED
    booking.find('status').text = 'CONFIRMED'
    save_data(tree, BOOKINGS_FILE)
    log_action(admin_email, f"Booking {b_id} confirmed.")
    add_notification(booking.find('customer_email').text, b_id, 'CONFIRMED')
    return True, f"Booking {b_id} confirmed."

def customer_cancel_booking(b_id, customer_email, reason):
    """Customer Feature 3: Allows customer to cancel their own booking (Rule 11, 15)."""
    tree, root = load_data(BOOKINGS_FILE)
    booking = root.find(f"./booking[id='{b_id}']")

    if booking is None:
        return False, "Booking not found."

    if booking.find('customer_email').text != customer_email:
        return False, "You can only cancel your own reservations."

    if booking.find('status').text not in ['CONFIRMED', 'PENDING']:
        return False, f"Reservation is already in status: {booking.find('status').text} and cannot be cancelled."

    if not reason:
        return False, "A cancellation reason is required (Rule 15)."

    # Mock Refund Logic
    try:
        booking_dt = datetime.strptime(booking.find('date').text + " " + booking.find('time').text, "%Y-%m-%d %H:%M")
        time_until_booking = booking_dt - datetime.now()
        threshold = get_system_setting('refund_threshold_hours')

        if time_until_booking.total_seconds() < threshold * 3600:
            refund_msg = f"No refund (cancellation < {threshold} hours before event)."
        else:
            refund_msg = "Full refund processed (per policy)."
    except:
        refund_msg = "Refund policy check failed (date error)."

    # Rule 15: Store the reason
    reason_element = booking.find('cancellation_reason')
    if reason_element is None:
        reason_element = ET.SubElement(booking, 'cancellation_reason')
    reason_element.text = f"Cancelled by Customer: {reason}"

    booking.find('status').text = 'CANCELLED_BY_CUSTOMER'
    save_data(tree, BOOKINGS_FILE)
    log_action(customer_email, f"Cancelled booking: {b_id}. Reason: {reason}.")
    add_notification(customer_email, b_id, 'CANCELLED_BY_CUSTOMER')
    return True, f"Reservation {b_id} cancelled successfully. {refund_msg}"

def staff_cancel_booking_with_validation(b_id, staff_email, reason):
    """Staff Feature 5: Allows staff to cancel a booking with validation (Rule 13)."""
    tree, root = load_data(BOOKINGS_FILE)
    booking = root.find(f"./booking[id='{b_id}']")

    if booking is None:
        return False, "Booking not found."

    if booking.find('status').text in ['CANCELLED_BY_CUSTOMER', 'CANCELLED_BY_ADMIN', 'CANCELLED_BY_STAFF']:
        return False, "Booking is already cancelled."

    # Rule 13: System validation confirmation is handled in the UI.
    if not reason:
        return False, "A cancellation reason is mandatory (Rule 13)."

    # Store the reason
    reason_element = booking.find('cancellation_reason')
    if reason_element is None:
        reason_element = ET.SubElement(booking, 'cancellation_reason')
    reason_element.text = f"Cancelled by Staff: {reason}"

    booking.find('status').text = 'CANCELLED_BY_STAFF'

    save_data(tree, BOOKINGS_FILE)
    log_action(staff_email, f"STAFF OVERRIDE: Cancelled booking {b_id} for reason: {reason}.")
    add_notification(booking.find('customer_email').text, b_id, 'CANCELLED_BY_STAFF')
    return True, f"Booking {b_id} cancelled by Staff. Customer notified."


# ==============================================================================
# 5. NOTIFICATIONS UTILITIES (Rule 18)
# ==============================================================================

def load_notifications(customer_email):
    """Retrieves notifications for a specific customer. (Rule 18)"""
    notifications = []
    bookings = load_bookings()
    for b in bookings:
        if b.find('customer_email').text == customer_email:
            b_id = b.find('id').text
            status = b.find('status').text
            booked_at = b.find('booked_at').text

            notification_message = ""
            if status == 'PENDING':
                notification_message = f"Your booking {b_id} for venue {b.find('venue_id').text} is still **Pending** approval."
            elif status == 'CONFIRMED':
                notification_message = f"**APPROVED**: Your booking {b_id} has been **Approved**!"
            elif 'CANCELLED' in status:
                reason = b.find('cancellation_reason').text if b.find('cancellation_reason') is not None else 'No reason provided.'
                notification_message = f"**CANCELLED**: Your booking {b_id} has been **Cancelled** by Admin/Staff. Reason: {reason}"
            elif status == 'MODIFIED':
                 notification_message = f"**MODIFIED**: Your booking {b_id} has been **Modified**. Contact admin for details."

            notifications.append((booked_at, b_id, status, notification_message))

    # Sort by date (newest first)
    notifications.sort(key=lambda x: x[0], reverse=True)
    return notifications

def add_notification(customer_email, b_id, status):
    """Marker that the GUI should refresh the notification view. (Rule 18)"""
    pass


# ==============================================================================
# 6. MOCK DATA/UTILITIES FOR ADMIN/SETTINGS (Rule 15)
# ==============================================================================

def peak_booking_periods():
    """MOCK: Returns hardcoded data for peak periods."""
    return [
        ("2026-01-25", 5, "Hall A"),
        ("2026-01-15", 3, "Outdoor Space"),
        ("2026-02-01", 3, "Hall B"),
    ]

def get_system_setting(key):
    """MOCK: Simulates reading a system setting."""
    try:
        _, settings_root = load_data(SETTINGS_FILE)
        if settings_root is not None:
            setting = settings_root.find(f"./setting[key='{key}']")
            if setting is not None:
                if key == 'refund_threshold_hours':
                    return int(setting.find('value').text)
                return setting.find('value').text
    except Exception:
        pass
    # Default mock values (Rule 15)
    if key == 'refund_threshold_hours':
        return 48
    if key == 'admin_cancellation_reasons':
        # Rule 15: fixed valid reason - maintainece or the venue something2
        return "Maintenance;Venue Compliance Issue;Emergency Closure;System Override" 
    if key == 'customer_cancellation_reasons':
        return "Personal Emergency;Change of Plans;Found Other Venue;Date Conflict"
    return ''

def update_system_setting(key, value):
    """MOCK: Simulates saving a system setting to a mock XML file."""
    tree, root = load_data(SETTINGS_FILE)
    if root is None:
        root = ET.Element('settings')
        tree = ET.ElementTree(root)

    setting = root.find(f"./setting[key='{key}']")
    if setting is None:
        setting = ET.SubElement(root, 'setting')
        ET.SubElement(setting, 'key').text = key
        ET.SubElement(setting, 'value').text = str(value)
    else:
        setting.find('value').text = str(value)

    save_data(tree, SETTINGS_FILE)
    log_action(ADMIN_EMAIL, f"MOCK: Updated system setting {key} to {value}")
    return True