import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime, timedelta
import os
import json

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

USERS = load_users()

def show_registration_window():
    reg_window = tk.Toplevel()
    reg_window.title("Register")
    reg_window.geometry("400x550")
    reg_window.configure(bg="#5b5b5b")

    tk.Label(reg_window, text="Register New User", font=("Helvetica", 14, "bold"), bg="#5b5b5b", fg="white").pack(pady=10)

    tk.Label(reg_window, text="Username:", bg="#5b5b5b", fg="white").pack()
    username_entry = tk.Entry(reg_window)
    username_entry.pack()

    tk.Label(reg_window, text="Password:", bg="#5b5b5b", fg="white").pack()
    password_entry = tk.Entry(reg_window, show="*")
    password_entry.pack()

    tk.Label(reg_window, text="Security Question:", bg="#5b5b5b", fg="white").pack()
    question_text = tk.Text(reg_window, height=3, width=40)
    question_text.pack()

    tk.Label(reg_window, text="Answer:", bg="#5b5b5b", fg="white").pack()
    answer_entry = tk.Entry(reg_window)
    answer_entry.pack()

    tk.Label(reg_window, text="Courses (space-separated):", bg="#5b5b5b", fg="white").pack()
    courses_text = tk.Text(reg_window, height=3, width=40)
    courses_text.pack()

    tk.Label(reg_window, text="Subjects (space-separated):", bg="#5b5b5b", fg="white").pack()
    subjects_text = tk.Text(reg_window, height=3, width=40)
    subjects_text.pack()

    def register_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        question = question_text.get("1.0", tk.END).strip()
        answer = answer_entry.get().strip()
        courses = courses_text.get("1.0", tk.END).strip().split()
        subjects = subjects_text.get("1.0", tk.END).strip().split()

        if not username or not password or not question or not answer or not courses or not subjects:
            messagebox.showerror("Error", "All fields are required.")
            return
        if username in USERS:
            messagebox.showerror("Error", "Username already exists.")
            return

        USERS[username] = {
            "password": password,
            "security_question": question,
            "security_answer": answer.lower(),
            "courses": courses,
            "subjects": subjects
        }
        save_users(USERS)
        messagebox.showinfo("Success", "Registration successful.")
        reg_window.destroy()

    tk.Button(reg_window, text="Register", bg="#66cc33", fg="white", command=register_user).pack(pady=20)

def show_login_window():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x350")
    login_window.configure(bg="#5b5b5b")

    tk.Label(login_window, text="Username:", bg="#5b5b5b", fg="white").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg="#5b5b5b", fg="white").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    forgot_frame = tk.Frame(login_window, bg="#5b5b5b")
    forgot_question_label = tk.Label(forgot_frame, text="", bg="#5b5b5b", fg="white", wraplength=350, justify="left")
    forgot_answer_entry = tk.Entry(forgot_frame)
    forgot_submit_btn = tk.Button(forgot_frame, text="Submit Answer", bg="#66cc33", fg="white")

    def try_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        user_data = USERS.get(username)
        if user_data and user_data["password"] == password:
            login_window.destroy()
            launch_main_app(username, user_data["courses"], user_data["subjects"])
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def show_forgot_password():
        username = username_entry.get().strip()
        if username not in USERS:
            messagebox.showerror("Error", "Username not found. Please enter a valid username first.")
            return

        user_data = USERS[username]
        forgot_question_label.config(text=f"Security Question:\n{user_data['security_question']}")
        forgot_answer_entry.delete(0, tk.END)

        forgot_frame.pack(pady=10)
        forgot_question_label.pack(pady=5)
        forgot_answer_entry.pack(pady=5)
        forgot_submit_btn.pack(pady=5)

    def check_forgot_answer():
        username = username_entry.get().strip()
        user_data = USERS.get(username)
        if not user_data:
            messagebox.showerror("Error", "Username not found.")
            return

        answer = forgot_answer_entry.get().strip().lower()
        if answer == user_data.get("security_answer"):
            messagebox.showinfo("Password Retrieved", f"Your password is: {user_data['password']}")
            forgot_frame.pack_forget()
        else:
            messagebox.showerror("Error", "Incorrect answer.")

    forgot_submit_btn.config(command=check_forgot_answer)

    tk.Button(login_window, text="Login", bg="#66cc33", fg="white", command=try_login).pack(pady=10)
    tk.Button(login_window, text="Forgot Password?", bg="#66cc33", fg="white", command=show_forgot_password).pack(pady=5)
    tk.Button(login_window, text="Register", bg="#66cc33", fg="white", command=show_registration_window).pack(pady=5)

    login_window.mainloop()

def launch_main_app(username, courses, subjects):
    ATTENDANCE_FILE = f"{username}_attendance.txt"

    root = tk.Tk()
    root.title(f"Attendance Management System - {username}")
    root.geometry("700x700")
    root.configure(bg="#5b5b5b")

    frame = tk.Frame(root, bg="#5b5b5b")
    frame.pack(pady=20)

    tk.Label(frame, text="Attendance Management System", font=("Helvetica", 18, "bold"), bg="#5b5b5b", fg="white").pack(pady=10)

    def save_attendance(date, course, subject, section, semester, present_students):
        entry = f"{date} | {course} | {subject} | {section} | {semester} | {present_students.strip()}\n"
        lines = []
        if os.path.exists(ATTENDANCE_FILE):
            with open(ATTENDANCE_FILE, 'r') as f:
                lines = f.readlines()
        lines.append(entry)
        lines = sorted(lines, key=lambda x: datetime.strptime(x.split('|')[0].strip(), "%d/%m/%Y"))
        with open(ATTENDANCE_FILE, 'w') as f:
            f.writelines(lines)

    def read_attendance():
        if not os.path.exists(ATTENDANCE_FILE):
            return []
        with open(ATTENDANCE_FILE, 'r') as f:
            return f.readlines()

    def manual_attendance(title, default_date=None):
        window = tk.Toplevel(root)
        window.title(title)
        window.geometry("450x700")
        window.configure(bg="#5b5b5b")

        tk.Label(window, text="Date (dd/mm/yyyy):", bg="#5b5b5b", fg="white").pack()
        date_entry = tk.Entry(window)
        if default_date:
            date_entry.insert(0, default_date)
        date_entry.pack(pady=5)

        tk.Label(window, text="Select Course", bg="#5b5b5b", fg="white").pack()
        course = ttk.Combobox(window, values=courses, state="readonly")
        course.pack(pady=5)

        tk.Label(window, text="Select Subject", bg="#5b5b5b", fg="white").pack()
        subject = ttk.Combobox(window, values=subjects, state="readonly")
        subject.pack(pady=5)

        section = tk.Entry(window)
        semester = ttk.Combobox(window, values=[str(i) for i in range(1, 11)], state="readonly") 
        semester.current(0)  # Sets default to "1"
        total_students = tk.Entry(window)
        present_students = tk.Text(window, height=3)
        absentees = tk.Text(window, height=3)

        for label, widget in zip(
            ["Section", "Semester", "Total Students (digits only)", "Present Students (space-separated digits only)", "Absentees (space-separated digits only)"],
            [section, semester, total_students, present_students, absentees]
        ):
            tk.Label(window, text=label, bg="#5b5b5b", fg="white").pack()
            widget.pack(pady=5)

        def submit():
            date = date_entry.get().strip()
            selected_course = course.get().strip()
            selected_subject = subject.get().strip()
            sec = section.get().strip()
            sem = semester.get().strip()
            total_str = total_students.get().strip()
            present_str = present_students.get("1.0", tk.END).strip()
            absent_str = absentees.get("1.0", tk.END).strip()

            # Check all required fields filled except present/absent
            if not (date and selected_course and selected_subject and sec and sem and total_str):
                messagebox.showerror("Error", "Date, Course, Subject, Section, Semester, and Total Students must be filled.")
                return

            # Validate date format
            try:
                datetime.strptime(date, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format.")
                return

            # Validate total_students is digit and positive
            if not total_str.isdigit() or int(total_str) <= 0:
                messagebox.showerror("Error", "Total Students must be a positive integer.")
                return
            total = int(total_str)

            # Check present and absent rules
            if (present_str and absent_str) or (not present_str and not absent_str):
                messagebox.showerror("Error", "Fill exactly one of Present Students or Absentees.")
                return

            # Validate present students or absentees
            def validate_space_separated_digits(s):
                if not s:
                    return False
                parts = s.split()
                return all(part.isdigit() for part in parts)

            if present_str:
                if not validate_space_separated_digits(present_str):
                    messagebox.showerror("Error", "Present Students must be space-separated digits only.")
                    return
                present_list = [int(x) for x in present_str.split()]
                if any(x < 1 or x > total for x in present_list):
                    messagebox.showerror("Error", "Present Students roll numbers must be between 1 and Total Students.")
                    return
            else:
                # Absentees given
                if not validate_space_separated_digits(absent_str):
                    messagebox.showerror("Error", "Absentees must be space-separated digits only.")
                    return
                absent_list = [int(x) for x in absent_str.split()]
                if any(x < 1 or x > total for x in absent_list):
                    messagebox.showerror("Error", "Absentees roll numbers must be between 1 and Total Students.")
                    return
                # Calculate present as total students minus absentees
                all_students = set(range(1, total + 1))
                present_set = all_students - set(absent_list)
                present_list = sorted(present_set)
                present_str = ' '.join(str(x) for x in present_list)

            save_attendance(date, selected_course, selected_subject, sec, sem, present_str)
            messagebox.showinfo("Success", "Attendance added.")
            window.destroy()

        tk.Button(window, text="Submit", bg="#66cc33", fg="white", command=submit).pack(pady=10)

    def edit_courses_subjects():
        confirm_pass = simpledialog.askstring("Confirm Password", "Enter password:", show="*")
        if confirm_pass != USERS[username]["password"]:
            messagebox.showerror("Error", "Incorrect password.")
            return

        edit_win = tk.Toplevel(root)
        edit_win.title("Edit Courses and Subjects")
        edit_win.geometry("400x250")
        edit_win.configure(bg="#5b5b5b")

        tk.Label(edit_win, text="New Courses (space-separated):", bg="#5b5b5b", fg="white").pack()
        courses_entry = tk.Entry(edit_win)
        courses_entry.insert(0, ' '.join(courses))
        courses_entry.pack(pady=5)

        tk.Label(edit_win, text="New Subjects (space-separated):", bg="#5b5b5b", fg="white").pack()
        subjects_entry = tk.Entry(edit_win)
        subjects_entry.insert(0, ' '.join(subjects))
        subjects_entry.pack(pady=5)

        def save_changes():
            new_courses = courses_entry.get().strip().split()
            new_subjects = subjects_entry.get().strip().split()
            if not new_courses or not new_subjects:
                messagebox.showerror("Error", "Courses and Subjects cannot be empty.")
                return
            USERS[username]["courses"] = new_courses
            USERS[username]["subjects"] = new_subjects
            save_users(USERS)
            messagebox.showinfo("Updated", "Courses and subjects updated. Please restart to reflect changes.")
            edit_win.destroy()

        tk.Button(edit_win, text="Save Changes", bg="#66cc33", fg="white", command=save_changes).pack(pady=10)

    def upload_attendance():
        records = read_attendance()
        if not records:
            messagebox.showinfo("Info", "No attendance records to upload.")
            return
        confirm = messagebox.askquestion("Upload", f"Next to upload:\n{records[0]}\n\nConfirm upload?")
        if confirm == 'yes':
            with open(ATTENDANCE_FILE, 'w') as f:
                f.writelines(records[1:])
            messagebox.showinfo("Success", "Uploaded and removed from file.")

    def show_recent():
        n = simpledialog.askinteger("Input", "Enter number of recent months:")
        if n is None:
            return

        now = datetime.now()
        records = read_attendance()
        result = []

        for line in records:
            try:
                date_str = line.split('|')[0].strip()
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                if now - date_obj <= timedelta(days=n * 30):
                    result.append(line)
            except:
                continue

        if not result:
            messagebox.showinfo("Result", "No records found in the given range.")
            return

        window = tk.Toplevel(root)
        window.title("Recent Attendance Records")
        window.geometry("600x400")
        window.configure(bg="#5b5b5b")
        text = tk.Text(window, wrap=tk.WORD, bg="#5b5b5b", fg="white")
        text.insert(tk.END, ''.join(result))
        text.pack(expand=True, fill='both')

    def view_by_date():
        date_str = simpledialog.askstring("Enter Date", "Enter date (dd/mm/yyyy):")
        if not date_str:
            return

        try:
            datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use dd/mm/yyyy.")
            return

        records = read_attendance()
        result = [line for line in records if line.startswith(date_str)]

        if not result:
            messagebox.showinfo("Result", "No attendance found for that date.")
            return

        window = tk.Toplevel(root)
        window.title(f"Attendance on {date_str}")
        window.geometry("600x300")
        window.configure(bg="#5b5b5b")
        text = tk.Text(window, wrap=tk.WORD, bg="#5b5b5b", fg="white")
        text.insert(tk.END, ''.join(result))
        text.pack(expand=True, fill='both')

    btn_params = {"width":30, "bg": "#66cc33", "fg":"white"}

    tk.Button(frame, text="Add Today's Attendance", command=lambda: manual_attendance("Add Today's Attendance", datetime.now().strftime("%d/%m/%Y")), **btn_params).pack(pady=10)
    tk.Button(frame, text="Add Skipped Date Attendance", command=lambda: manual_attendance("Skipped Attendance"), **btn_params).pack(pady=10)
    tk.Button(frame, text="Upload Attendance", command=upload_attendance, **btn_params).pack(pady=10)
    tk.Button(frame, text="Show Last N Months Attendance", command=show_recent, **btn_params).pack(pady=10)
    tk.Button(frame, text="View Attendance by Date", command=view_by_date, **btn_params).pack(pady=10)
    tk.Button(frame, text="Edit Courses/Subjects", command=edit_courses_subjects, **btn_params).pack(pady=10)
    tk.Button(frame, text="Exit", command=root.destroy, bg="#cc0000", fg="white", width=30).pack(pady=10)

    root.mainloop()

# Launch the application
show_login_window()
