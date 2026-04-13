# **Venue Reservation System**

### 

### **Project Overview**

The Venue Reservation System is a professional-grade desktop application designed to streamline the process of booking, managing, and auditing venue reservations. Built with a clean Pink and Grey aesthetic, the system employs a modular architecture where specific functionalities are separated into distinct roles: Admin, Staff, and Customer.



The application uses a mix of XML for structured data storage and flat-file logging for system transparency, ensuring a lightweight yet robust backend without the need for a heavy SQL server.



### **Core Features By Role**

The system follows a strict "Rule of 6," ensuring each user role has exactly six primary functional modules:



Admin (Superuser)

* Approval \& Management: Oversight of user account creation and venue status.



* Booking Control: Ability to override, confirm, or cancel any pending bookings.



* System Policy: Direct control over cancellation thresholds and refund rules.



* Data Portability: Features to export system data into CSV/JSON formats for external reporting.





2\. Staff (Moderators)

* Venue Lifecycle: Add new venues with detailed descriptions and manage existing listings.



* Attachment Management: Upload and organize visual assets or documentation for venues.



* Audit Logs: Access to staff activity logs to monitor operational history.



* Booking Validation: Specialized workflows for cancelling bookings with strict validation rules.





3\. Customer (End-Users)

* Discovery: Search for available venues and place real-time booking requests.



* Transparency: View personal booking history, status updates, and notifications.



* Self-Service: Cancel bookings according to the automated refund policy.



* Media Access: Browse venue images and attachments before making a decision.





### **Security \& Data**

* Authentication: Password security is managed via bcrypt hashing.



* Secondary Security: Administrative access requires a unique PIN (9999) in addition to standard credentials.



* Data Storage: Data is persisted in users.xml, venues.xml, bookings.xml, and settings.xml.



* Integrity: Built-in logic prevents the deletion of venues with active future bookings.

