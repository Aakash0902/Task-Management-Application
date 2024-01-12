"""
file: main.py
language: python 3
author: Aakash Jaideva
purpose: To Do list with GUI
"""


# Import necessary modules from the Tkinter library
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from datetime import datetime, timedelta


# Function to generate time options in 15-minute intervals
def generate_time_options():
    base_time = datetime.strptime("00:00", "%H:%M")
    time_options = []
    for _ in range(96):
        time_options.append(base_time.strftime("%I:%M %p"))
        base_time += timedelta(minutes=15)
    return time_options


# Function to handle adding a new task
def new_task():
    task = my_entry.get()
    priority = priority_var.get()
    due_date = cal.get_date()
    due_time = time_var.get()

    if task != "":
        # Format the task details
        task_with_details = f"{task} - Priority: {priority} - Due: {due_date} {due_time}"

        # Insert the formatted task into the listbox
        lb.insert(END, task_with_details)

        # Save the task details in a list
        tasks.append({"task": task, "priority": priority, "due_date": due_date, "due_time": due_time})

        # Clear input fields
        my_entry.delete(0, "end")
        priority_var.set("Low")
        cal.set_date("")
        time_combobox.set("")

        # Save the tasks to a file
        save_tasks()
    else:
        # Show a warning if no task is entered
        messagebox.showwarning("Warning", "Please enter some task")


# Function to delete a selected task
def delete_task():
    selected_task_index = lb.curselection()
    if selected_task_index:
        # Remove the task from the listbox and tasks list
        lb.delete(selected_task_index)
        tasks.pop(selected_task_index[0])
        # Save the updated tasks to a file
        save_tasks()


# Function to save tasks to a text file
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(f"{task['task']} - Priority: {task['priority']} - Due: {task['due_date']} {task['due_time']}\n")


# Function to load tasks from a text file
def load_tasks():
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                # Insert each task from the file into the listbox
                lb.insert(END, line.strip())
                task_info = line.split(" - Priority: ")
                if len(task_info) > 1:
                    task_details = task_info[1].split(" - Due: ")
                    if len(task_details) > 1:
                        tasks.append(
                            {"task": task_info[0], "priority": task_details[0], "due_date": task_details[1][:10],
                             "due_time": task_details[1][11:]})
    except FileNotFoundError:
        pass


# Create the main Tkinter window
ws = Tk()
ws.geometry('650x600+500+200')
ws.title('To-Do List')
ws.config(bg='#7f8c8d')
ws.resizable(width=False, height=False)

# Create a frame for the listbox
frame = Frame(ws, bg='#7f8c8d')
frame.pack(pady=10)

# Create a listbox to display tasks
lb = Listbox(
    frame,
    width=55,
    height=12,
    font=('Arial', 14),
    bd=0,
    fg='#2c3e50',
    selectbackground='#95a5a6',
    activestyle='none'
)
lb.pack(side=LEFT, fill=BOTH)

# Initialize a list to store tasks
tasks = []

# Load tasks from the file
load_tasks()

# Create a scrollbar for the listbox
sb = Scrollbar(frame)
sb.pack(side=RIGHT, fill=BOTH)
lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)

# Create an entry widget for task input
my_entry = Entry(
    ws,
    font=('Arial', 18),
    width=30,
    bd=3,
    relief=GROOVE
)
my_entry.pack(pady=10)

# Create a dropdown menu for selecting task priority
priority_var = StringVar(ws)
priority_var.set("Low")

priority_label = Label(ws, text="Select Priority:", font=('Arial', 14), bg='#7f8c8d', fg='#2c3e50')
priority_label.pack()

priority_options = ["Low", "Medium", "High"]
priority_menu = OptionMenu(ws, priority_var, *priority_options)
priority_menu.config(font=('Arial', 12), bg='#bdc3c7', fg='#2c3e50', bd=2)
priority_menu.pack(pady=10)

# Create a calendar widget for selecting due date
cal_label = Label(ws, text="Select Due Date:", font=('Arial', 14), bg='#7f8c8d', fg='#2c3e50')
cal_label.pack()

cal = DateEntry(ws, width=12, background='#3498db', foreground='white', borderwidth=2, font=('Arial', 12),
                selectmode='day', locale='en_US')
cal.pack(pady=10)

# Create a combobox for selecting due time
time_label = Label(ws, text="Select Due Time:", font=('Arial', 14), bg='#7f8c8d', fg='#2c3e50')
time_label.pack()

time_options = generate_time_options()
time_var = StringVar(ws)
time_combobox = ttk.Combobox(ws, textvariable=time_var, values=time_options, font=('Arial', 12), state="readonly")
time_combobox.set("")  # Set default value to an empty string
time_combobox.pack(pady=10)

# Create a frame for buttons
button_frame = Frame(ws, bg='#7f8c8d')
button_frame.pack(pady=20)

# Create a button to add a new task
addTask_btn = Button(
    button_frame,
    text='Add Task',
    font=('Arial', 14),
    bg='#2ecc71',
    padx=20,
    pady=10,
    command=new_task
)
addTask_btn.pack(fill=BOTH, expand=True, side=LEFT)

# Create a button to delete a selected task
delTask_btn = Button(
    button_frame,
    text='Delete Task',
    font=('Arial', 14),
    bg='#e74c3c',
    padx=20,
    pady=10,
    command=delete_task
)
delTask_btn.pack(fill=BOTH, expand=True, side=LEFT)


# Function to be called when the window is closed
def on_closing():
    save_tasks()
    ws.destroy()


# Bind the function to the window's close button
ws.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
ws.mainloop()
