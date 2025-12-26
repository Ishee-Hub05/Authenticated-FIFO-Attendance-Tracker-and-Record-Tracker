\Authenticated FIFO Attendance Tracker and Record Keeper
A Python-based desktop application that securely manages student attendance using the FIFO (First-In-First-Out) data structure. Built with Tkinter, the system ensures attendance records are stored and displayed in proper chronological order, even when backdated entries are added.

🚀 Features  
-Secure user registration and login  
-Password recovery using security questions  
-FIFO-based attendance storage (chronological order guaranteed)  
-Add attendance for current or skipped dates  
-View attendance by date or recent records  
-Course and subject management per user  
-Local file-based storage (no external database required)  
-Simple and user-friendly GUI  

⚙️ How It Works  
-Users register and log in using a username and password.  
-Authentication data is stored in a local users.json file.  
-Attendance is entered for a selected course and date.  
-Attendance records are stored using FIFO logic to maintain chronological order.  
-Users can view, edit, and manage attendance records through the GUI.  
-Each user has separate attendance files for organized record keeping.  

🛠️ Technologies Used  
-Python  
-Tkinter (for GUI)  
-JSON (user data storage)  
-Text files (attendance records)  
-FIFO Data Structure  

🎯 Learning Objectives  
-Understand and implement the FIFO data structure in a real-world application  
-Gain hands-on experience with Python GUI development using Tkinter  
-Learn file handling using JSON and text files  
-Implement basic authentication and validation mechanisms  
-Develop a modular and user-friendly desktop application  

▶️ How to Run  
Clone the repository:  
  git clone https://github.com/Ishee-Hub05/Authenticated FIFO Attendance Tracker and Record Keeper.git  
Navigate to the project directory:  
  cd Authenticated FIFO Attendance Tracker and Record Keeper    
Run the application:  
  python pj.py  

📂 Project Structure  
├── pj.py                  # Main application file  
├── users.json             # Stores registered user details  
├── *_attendance.txt       # FIFO-based attendance records  
└── README.md              # Project documentation  

📂 Example Output  
-Login and Registration window displayed  
-Attendance successfully recorded for selected date  
-Attendance records displayed in correct chronological (FIFO) order  
-User-specific attendance files created locally  
-Secure password recovery using security questions  
