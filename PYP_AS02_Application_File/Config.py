
import os

# ==============================================================================
# 0. HARDCODED CONSTANTS & FILE PATHS
# ==============================================================================

# --- THEME COLORS ---
PINK = "#FFC0CB" # Soft Pink (Rule 14)
GREY = "#D3D3D3" # Light Grey (Rule 14)
DARK_GREY = "#A9A9A9" # Darker Grey for text/accents

# --- HARDCODED ADMIN CREDENTIALS & SPECIAL MARKERS (Rule 8, 9) ---
ADMIN_EMAIL = "@admin1234567" # Fixed to use the required format (Rule 9)
ADMIN_PIN = "9999" # Hardcoded PIN for secondary security (Rule 9)

# --- FILE PATHS ---
USERS_FILE = "users.xml"
VENUES_FILE = "venues.xml"
BOOKINGS_FILE = "bookings.xml"
SETTINGS_FILE = "settings.xml"
LOGS_FILE = "system_logs.txt" # Rule 6
VENUE_ATTACHMENTS_DIR = "venue_attachments" # Rule 16

# Ensure the attachments directory exists
if not os.path.exists(VENUE_ATTACHMENTS_DIR):
    os.makedirs(VENUE_ATTACHMENTS_DIR)