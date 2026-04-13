# Execute_program.py
import tkinter as tk
import traceback
from Application import VenueReservationApp # Import the main app class

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VenueReservationApp(root)
        root.mainloop()
    except Exception as e:
        # This forces the crash reason to print to the terminal
        print(f"FATAL STARTUP ERROR: {e}")
        traceback.print_exc()