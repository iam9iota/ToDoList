import customtkinter as ctk
from tkcalendar import Calendar
import util_img
from config import *
from datetime import datetime
from time import strftime
from tkinter import messagebox
import sqlite3

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ToDoList")
        self.geometry("1300x800")
        self.tasks = [] 
        self.connectToDatabase()
 
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images
        self.logo = util_img.re_img("logo.ico", (30,30))
        self.wm_iconbitmap(util_img.open_img("logo.ico"))
        self.logo_image = util_img.re_img("tasks3.png", (80,80))
        self.img_tasks = util_img.re_img("check.png", (30,30))
        self.img_importance = util_img.re_img("importance2.png", (30,30))
        self.img_calendar = util_img.re_img("calendar4.png", (30,30))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=int(0), fg_color=VIOLET)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text=" ToDoList", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=40, family=FONT, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=(20,70))

        self.tasks_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tasks", 
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   font=ctk.CTkFont(size=30, family=FONT, weight="bold"), 
                                                   image=self.img_tasks, anchor="w", command=self.home_button_event)
        self.tasks_button.grid(row=1, column=0, sticky="ew")

        self.importance_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Action Log",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      font=ctk.CTkFont(size=30, family=FONT, weight="bold"),
                                                      image=self.img_importance, anchor="w", command=self.frame_2_button_event)
        self.importance_button.grid(row=2, column=0, sticky="ew")

        self.dates_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dates",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      font=ctk.CTkFont(size=30, family=FONT, weight="bold"),
                                                      image=self.img_calendar, anchor="w", command=self.frame_3_button_event)
        self.dates_button.grid(row=3, column=0, sticky="ew")

       

        
        # create home frame
        self.tasks_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=JADE)
        self.tasks_frame.grid_columnconfigure(0, weight=1)

        self.frame_entry_task = ctk.CTkFrame(self.tasks_frame, corner_radius=25, fg_color=SEA_FOAM, width=940, height=300)
        self.frame_entry_task.grid(row=0, column=0, pady=(10,0), sticky="n")

        self.frame_for_tasks = ctk.CTkScrollableFrame(self.tasks_frame, corner_radius=25, fg_color=SEA_FOAM, width=900, height=350)
        self.frame_for_tasks.grid(row=1, column=0, pady=(20,0), sticky="n")

        #clock
        #date                                                                                 
        self.a=datetime.today().strftime('%A')                              
        self.b=(self.a.upper())
        self.c=(self.b[0:2]) 

        self.l1 = ctk.CTkLabel(self.frame_entry_task, font=ctk.CTkFont(family=FONT_CLOCK, size=50, weight="bold"), 
                               text_color=VIOLET, fg_color="transparent", bg_color="transparent")
        self.l1.place(x=400,y=15)

        self.l2 = ctk.CTkLabel(self.frame_entry_task, font=ctk.CTkFont(family=FONT_CLOCK, size=50, weight="bold"), 
                               text_color=VIOLET, fg_color="transparent", bg_color="transparent")
        self.l2.configure(text=self.c+" |")
        self.l2.place(x=280,y=15)

        self.l3 = ctk.CTkLabel(self.frame_entry_task, font=ctk.CTkFont(family=FONT_CLOCK, size=8), text_color=VIOLET,
                                text='DAY')
        self.l3.place(x=310,y=65)

        self.l4 = ctk.CTkLabel(self.frame_entry_task, font=ctk.CTkFont(family=FONT_CLOCK, size=8), text_color=VIOLET,
                                text='HOURS')
        self.l4.place(x=415,y=65)

        self.l5 = ctk.CTkLabel(self.frame_entry_task, font=ctk.CTkFont(family=FONT_CLOCK, size=8), text_color=VIOLET,
                                text='MINUTES')
        self.l5.place(x=510,y=65)

        self.l3 = ctk.CTkLabel(self.frame_entry_task, font=ctk.CTkFont(family=FONT_CLOCK, size=8),
                                text_color=VIOLET, text='SECONDS')
        self.l3.place(x=605, y=65)

        self.motivation_label = ctk.CTkLabel(self.frame_entry_task, text="Manage your time!", 
                                             font=ctk.CTkFont(family=FONT, size=40, weight="bold"), text_color=VIOLET)
        self.motivation_label.place(x=300, y=100)

        #entry form
        self.entry_task = ctk.CTkEntry(self.frame_entry_task, width=700, height=50, font=ctk.CTkFont(family=FONT),
                                       placeholder_text="Enter the task...", fg_color=VIOLET)
        self.entry_task.place(x=50, y=175)

        self.add_task_button = ctk.CTkButton(self.frame_entry_task, corner_radius=10, text="+", 
                                             font=ctk.CTkFont(family=FONT, size=30, weight="bold"), width=100, height=50, 
                                             fg_color=VIOLET, command=self.add_task)
        self.add_task_button.place(x=775, y=175)

        self.entry_importance = ctk.CTkComboBox(self.frame_entry_task, values=["LOW", "MEDIUM", "HIGH"], 
                                                dropdown_fg_color=JADE,  dropdown_hover_color=PINK, button_color=JADE,
                                                font=ctk.CTkFont(family=FONT), dropdown_font=ctk.CTkFont(family=FONT), 
                                                width=200, fg_color=VIOLET)
        self.entry_importance.place(x=50, y=250)

        self.category = ctk.CTkComboBox(self.frame_entry_task, values=["Personal", "Shopping", "Study", "Work", "Other"], 
                                        dropdown_fg_color=JADE, dropdown_hover_color=PINK, button_color=JADE,
                                        font=ctk.CTkFont(family=FONT), dropdown_font=ctk.CTkFont(family=FONT), 
                                        width=200, fg_color=VIOLET)
        self.category.place(x=300, y=250)

        self.entry_date = ctk.CTkButton(self.frame_entry_task, text="Choose Date", font=ctk.CTkFont(family=FONT),
                                         fg_color=VIOLET, width=200, command=self.open_date_picker)
        self.entry_date.place(x=550, y=250)

        self.progress_frame = ctk.CTkFrame(self.tasks_frame, corner_radius=25, fg_color="transparent", width=950, height=100)
        self.progress_frame.grid(row=2, column=0, pady=(0, 0), sticky="ns")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="0 of 0 tasks completed",
                                           fg_color="transparent", bg_color="transparent",
                                        font=ctk.CTkFont(family=FONT, size=20, weight="bold"), text_color=GREEN)
        self.progress_label.place(x=20, y=5)

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=GREEN, fg_color=VIOLET, width=900, height=20)
        self.progress_bar.place(x=20, y=35)

        # create second frame
        self.importance_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color=JADE)

        # create third frame
        self.dates_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=JADE)

        cal = Calendar(self.dates_frame, selectmode='day', locale='en_US', disabledforeground='red',
               cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
               selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        cal.pack(fill="both", expand=True, padx=10, pady=10)

        # select default frame
        self.entry_importance.set("Importance")
        self.category.set("Category")
        self.select_frame_by_name("tasks")
        self.load_tasks()
        self.time()
        
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.tasks_button.configure(fg_color=(PINK, PINK) if name == "tasks" else "transparent")
        self.importance_button.configure(fg_color=(PINK, PINK) if name == "importance" else "transparent")
        self.dates_button.configure(fg_color=(PINK, PINK) if name == "dates" else "transparent")

        # show selected frame
        if name == "tasks":
            self.tasks_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tasks_frame.grid_forget()
        if name == "importance":
            self.importance_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.importance_frame.grid_forget()
        if name == "dates":
            self.dates_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.dates_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("tasks")

    def frame_2_button_event(self):
        self.select_frame_by_name("importance")
        self.show_action_log() 

    def frame_3_button_event(self):
        self.select_frame_by_name("dates")

    def time(self):
        self.a=strftime('%H : %M : %S')
        self.l1.configure(text=self.a)
        self.l1.after(1000,self.time)

    def connectToDatabase(self):
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            importance TEXT NOT NULL
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS action_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        timestamp TEXT NOT NULL
        )''')

        connection.commit()
        connection.close()

    def load_tasks(self):
        for widget in self.frame_for_tasks.winfo_children():
            widget.destroy()

        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, task, date, completed, importance FROM tasks")
        tasks = cursor.fetchall()
        connection.close()
        self.tasks=tasks
        self.update_progress() 

        for task in tasks:
            self.create_task_frame(task[0], task[1], task[2], task[3], task[4])

    def add_task(self):
        task_text = self.entry_task.get().strip() 
        importance = self.entry_importance.get()
        category = self.category.get()
        date = self.entry_date.cget("text")
        task_format = f"{task_text} - {importance} - {category}"

        if not task_text or not importance or not category or date == "choose date":
            messagebox.showerror("ERROR", "PLS, ENTER ALL FIELDS!") 
            return

        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (task, importance, date) VALUES (?, ?,  ?)",
                       (task_format, importance,  date))
        connection.commit()
        connection.close()

        self.entry_task.delete(0, "end")  
        self.entry_importance.set("Importance")
        self.category.set("Category") 
        self.entry_date.configure(text="Choose Date")

        self.load_tasks()
        self.log_action(f"Добавлена задача: {task_format} на {date}")

    def create_task_frame(self, task_id, task_format, date, completed, importance):
        task_color = MAGENTA if importance == "HIGH" else MEDIUM

        task_frame = ctk.CTkFrame(self.frame_for_tasks, corner_radius=10, fg_color=task_color)
        task_frame.pack(fill="x", padx=10, pady=5)
       
        task_checkbox = ctk.CTkCheckBox(task_frame, text="", width=30, height=30, corner_radius=15,
                                        command=lambda:(
                                        self.update_task_status(task_id, task_checkbox),
                                        self.update_progress()
                                        ))
        task_checkbox.grid(row=0, column=0, padx=10, pady=5)
        task_checkbox.select() if completed else task_checkbox.deselect()

        task_label = ctk.CTkLabel(task_frame, text=task_format, anchor="w", 
                                font=ctk.CTkFont(size=16, family=FONT), text_color=VIOLET)
        task_label.grid(row=0, column=1, padx=(10, 5), pady=5, sticky="w")

        date_label = ctk.CTkLabel(task_frame, text=date, anchor="e", 
                                font=ctk.CTkFont(size=16, family=FONT), text_color=VIOLET)
        date_label.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="e")

        edit_button = ctk.CTkButton(task_frame, text="CHANGE", fg_color=VIOLET, 
                                    font=ctk.CTkFont(size=14, family=FONT),
                                    width=100, command=lambda: self.edit_task(task_id, task_label, date_label, edit_button, task_frame))
        edit_button.grid(row=0, column=3, padx=10, pady=5)

        delete_button = ctk.CTkButton(task_frame, text="DELETE", fg_color=RED, 
                                    font=ctk.CTkFont(size=14, family=FONT),
                                    width=100, command=lambda: self.delete_task(task_frame, task_id))
        delete_button.grid(row=0, column=4, padx=10, pady=5)

    def open_date_picker(self):
        date_window = ctk.CTkToplevel(self)
        date_window.title("CHOOSE DATE")
        date_window.geometry("250x300")
        date_window.resizable(False, False)

        date_window.attributes("-topmost", True)
        date_window.grab_set()

        label = ctk.CTkLabel(date_window, text="CHOOSE DATE:", font=ctk.CTkFont(size=16))
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        calendar = Calendar(date_window, selectmode="day", locale="en_US", 
                            background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                            selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        calendar.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")

        def confirm_date():
            selected_date = calendar.get_date()
            self.entry_date.configure(text=selected_date)
            date_window.destroy() 

        confirm_button = ctk.CTkButton(date_window, text="OK", command=confirm_date, fg_color=GREEN, width=100)
        confirm_button.grid(row=2, column=0, pady=10, sticky="n")
        cancel_button = ctk.CTkButton(date_window, text="CANCEL", command=date_window.destroy, fg_color=RED, width=100)
        cancel_button.grid(row=2, column=1, pady=10, sticky="n")

    def open_date_picker_for_edit(self, edit_date_button):
        date_window = ctk.CTkToplevel(self)
        date_window.title("CHOOSE DATE")
        date_window.geometry("250x300")
        date_window.resizable(False, False)

        date_window.attributes("-topmost", True)
        date_window.grab_set()

        label = ctk.CTkLabel(date_window, text="CHOOSE DATE:", font=ctk.CTkFont(size=16))
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        calendar = Calendar(date_window, selectmode="day", locale="en_US", 
                            background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                            selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        calendar.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")

        def set_date():
            selected_date = calendar.get_date()
            edit_date_button.configure(text=selected_date)
            date_window.destroy() 

        confirm_button = ctk.CTkButton(date_window, text="OK", command=set_date, fg_color=GREEN, width=100)
        confirm_button.grid(row=2, column=0, pady=10, sticky="n")
        cancel_button = ctk.CTkButton(date_window, text="CANCEL", command=date_window.destroy, fg_color=RED, width=100)
        cancel_button.grid(row=2, column=1, pady=10, sticky="n")

    def delete_task(self, task_frame, task_id): 
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        connection.commit()
        connection.close()  

        task_frame.destroy()

        self.tasks = [task for task in self.tasks if task[0] != task_id]

        self.update_progress()
        self.log_action(f"Удалена задача ID {task_id}")

    def edit_task(self, task_id, task_label, date_label, edit_button, task_frame):
        current_text = task_label.cget("text").split("           ")[0]
        current_date = date_label.cget("text")
        
        entry_edit = ctk.CTkEntry(task_frame, width=300, fg_color=VIOLET, font=ctk.CTkFont(family=FONT))
        entry_edit.insert(0, current_text)
        entry_edit.grid(row=0, column=1, padx=(10, 5), pady=5, sticky="w")

        edit_date_button = ctk.CTkButton(task_frame, text=current_date, fg_color=VIOLET, font=ctk.CTkFont(family=FONT),
                                         command=lambda: self.open_date_picker_for_edit(edit_date_button))
        edit_date_button.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="w")

        edit_button.configure(text="SAVE", fg_color="green", font=ctk.CTkFont(family=FONT),
                                    command=lambda: self.save_task(task_id, entry_edit, edit_date_button, task_label, date_label, edit_button, task_frame))
        
    def save_task(self, task_id, entry_edit, edit_date_button, task_label, date_label, edit_button, task_frame):
        new_task_text = entry_edit.get().strip()
        current_text = task_label.cget("text").split("           ")[0]
        new_date = edit_date_button.cget("text")

        if not new_task_text or not new_date:
            messagebox.showerror("ERROR", "PLS, ENTER ALL FIELDS!")
            return

        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET task=?, date=? WHERE id=?", (new_task_text, new_date, task_id))
        connection.commit()
        connection.close()

        task_label.configure(text=new_task_text)
        date_label.configure(text=new_date)

        entry_edit.destroy()
        edit_date_button.destroy()
        edit_button.configure(text="SAVE", fg_color=VIOLET, font=ctk.CTkFont(family=FONT),
                              command=lambda:self.edit_task(task_id, task_label, date_label, edit_button, task_frame))

        task_label.grid(row=0, column=1, padx=(10, 5), pady=5, sticky="w")
        date_label.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="e")

        self.log_action(f"Изменена задача {current_text}: на {new_task_text}  {new_date}")

    def update_progress(self):
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task[3] == 1) 

        if total_tasks > 0:
            progress = completed_tasks / total_tasks
        else:
            progress = 0

        self.progress_label.configure(text=f"{completed_tasks} of {total_tasks} tasks completed")
        self.progress_bar.set(progress)

    def update_task_status(self, task_id, checkbox):
        completed = 1 if checkbox.get() else 0

        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (completed, task_id))
        connection.commit()
        connection.close()

        self.tasks = [
            (task[0], task[1], task[2], completed if task[0] == task_id else task[3], task[4]) for task in self.tasks
        ]

        self.update_progress()

    def log_action(self, action):
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO action_log (action, timestamp) VALUES (?, ?)", (action, timestamp))
        connection.commit()
        connection.close()

    def show_action_log(self):
        for widget in self.importance_frame.winfo_children():
            widget.destroy()

        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("SELECT action, timestamp FROM action_log ORDER BY timestamp DESC")
        logs = cursor.fetchall()
        connection.close()

        for action, timestamp in logs:
            log_label = ctk.CTkLabel(self.importance_frame, text=f"{timestamp} - {action}", font=ctk.CTkFont(size=20, family=FONT), text_color=SEA_FOAM, anchor="w")
            log_label.pack(fill="x", padx=10, pady=15)

if __name__ == "__main__":
    app = App()
    app.mainloop()

    #pyinstaller --noconfirm --onefile --noconsole --add-data "assets;assets" --add-data "tasks.db;tasks.db" ToDoList.py
