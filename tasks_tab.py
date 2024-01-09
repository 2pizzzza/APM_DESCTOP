# tasks_tab.py
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk


class TasksTab(tk.Frame):
    def __init__(self, master=None, database=None):
        super().__init__(master)
        self.database = database
        self.create_widgets()

    def create_widgets(self):
        # Выпадающий список для выбора проекта
        projects = self.database.fetch_all("SELECT * FROM projects")
        project_names = [project[1] for project in projects]
        self.project_var = tk.StringVar(self)
        self.project_var.set(project_names[0])
        dropdown_project = ttk.Combobox(self, textvariable=self.project_var, values=project_names)
        dropdown_project.pack(pady=10)

        # Информация о проекте
        lbl_project_info = ttk.Label(self, text="Информация о проекте:")
        lbl_project_info.pack()

        self.lbl_project_name = ttk.Label(self, text="")
        self.lbl_project_name.pack()

        self.lbl_responsible_employee = ttk.Label(self, text="")
        self.lbl_responsible_employee.pack()

        # Таблица с задачами
        columns = ("ID", "Название", "Ответственный сотрудник")
        self.tree_tasks = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree_tasks.heading(col, text=col, anchor="center")
            self.tree_tasks.column(col, width=450, anchor="center")

        self.tree_tasks.pack(pady=10)

        # Обновить список задач
        btn_refresh_tasks = ttk.Button(self, text="Обновить список задач", command=self.refresh_tasks)
        btn_refresh_tasks.pack(pady=10)

        # Кнопка для добавления задачи
        btn_add_task = ttk.Button(self, text="Добавить задачу", command=self.add_task)
        btn_add_task.pack(pady=10)

        # Привязка функции для обработки изменения выбранного проекта
        dropdown_project.bind("<<ComboboxSelected>>", lambda event: self.refresh_project_info())

    def refresh_project_info(self):
        selected_project = self.project_var.get()

        # Получаем информацию о проекте и отображаем ее
        project_info = self.database.fetch_one("SELECT * FROM projects WHERE name=?", (selected_project,))
        if project_info:
            self.lbl_project_name.config(text=f"Название проекта: {project_info[1]}")
            responsible_employee_name = self.database.fetch_one(
                "SELECT name FROM employees WHERE id=?", (project_info[2],)
            )
            self.lbl_responsible_employee.config(text=f"Ответственный сотрудник: {responsible_employee_name[0]}")
        else:
            self.lbl_project_name.config(text="Информация о проекте не найдена")
            self.lbl_responsible_employee.config(text="")

        # Обновляем список задач для выбранного проекта
        self.refresh_tasks()
        self.tree_tasks.bind("<Double-1>", lambda event: self.edit_task())

    def refresh_tasks(self):
        selected_project = self.project_var.get()

        for row in self.tree_tasks.get_children():
            self.tree_tasks.delete(row)

        project_info = self.database.fetch_one("SELECT id FROM projects WHERE name=?", (selected_project,))
        if project_info:
            tasks = self.database.fetch_all("SELECT * FROM tasks WHERE project_id=?", (project_info[0],))
            for task in tasks:
                self.tree_tasks.insert("", "end", values=task)

    def add_task(self):
        add_task_window = tk.Toplevel(self)
        add_task_window.title("Добавить задачу")

        lbl_name = ttk.Label(add_task_window, text="Название:")
        lbl_name.grid(row=0, column=0, padx=10, pady=10)

        entry_name = ttk.Entry(add_task_window)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        # Выпадающий список для выбора ответственного сотрудника
        lbl_responsible = ttk.Label(add_task_window, text="Ответственный сотрудник:")
        lbl_responsible.grid(row=1, column=0, padx=10, pady=10)

        employees = self.database.fetch_all("SELECT * FROM employees")
        employee_names = [employee[1] for employee in employees]
        responsible_var = tk.StringVar(add_task_window)
        responsible_var.set(employee_names[0])
        dropdown_responsible = ttk.Combobox(add_task_window, textvariable=responsible_var, values=employee_names)
        dropdown_responsible.grid(row=1, column=1, padx=10, pady=10)

        btn_save = ttk.Button(add_task_window, text="Сохранить", command=lambda: self.save_task(
            entry_name.get(), responsible_var.get(), add_task_window))
        btn_save.grid(row=2, columnspan=2, pady=10)

    def save_task(self, name, responsible_name, add_task_window):
        selected_project = self.project_var.get()
        project_info = self.database.fetch_one("SELECT id FROM projects WHERE name=?", (selected_project,))

        if project_info:
            responsible_id = self.database.fetch_one("SELECT id FROM employees WHERE name=?", (responsible_name,))

            if responsible_id:
                self.database.execute_query(
                    "INSERT INTO tasks (name, project_id, responsible_employee_id) VALUES (?, ?, ?)",
                    (name, project_info[0], responsible_id[0]))
                self.refresh_tasks()
                add_task_window.destroy()
            else:
                simpledialog.messagebox.showerror("Ошибка", "Выберите существующего ответственного сотрудника")
        else:
            simpledialog.messagebox.showerror("Ошибка", "Выберите существующий проект")

    def edit_task(self):
        selected_item = self.tree_tasks.selection()
        if selected_item:
            task_id = self.tree_tasks.item(selected_item, "values")[0]
            task_name = self.tree_tasks.item(selected_item, "values")[1]
            task_responsible_id = self.tree_tasks.item(selected_item, "values")[2]

            edit_task_window = tk.Toplevel(self)
            edit_task_window.title("Редактировать задачу")

            lbl_name = ttk.Label(edit_task_window, text="Название:")
            lbl_name.grid(row=0, column=0, padx=10, pady=10)

            entry_name = ttk.Entry(edit_task_window)
            entry_name.insert(0, task_name)
            entry_name.grid(row=0, column=1, padx=10, pady=10)

            # Выпадающий список для выбора ответственного сотрудника
            lbl_responsible = ttk.Label(edit_task_window, text="Ответственный сотрудник:")
            lbl_responsible.grid(row=1, column=0, padx=10, pady=10)

            employees = self.database.fetch_all("SELECT * FROM employees")
            employee_names = [employee[1] for employee in employees]
            responsible_var = tk.StringVar(edit_task_window)
            responsible_var.set(
                self.database.fetch_one("SELECT name FROM employees WHERE id=?", (task_responsible_id,))[0])
            dropdown_responsible = ttk.Combobox(edit_task_window, textvariable=responsible_var, values=employee_names)
            dropdown_responsible.grid(row=1, column=1, padx=10, pady=10)

            btn_save = ttk.Button(edit_task_window, text="Сохранить",
                                  command=lambda: self.update_task(task_id, entry_name.get(), responsible_var.get(),
                                                                   edit_task_window))
            btn_save.grid(row=2, column=0, padx=10, pady=10)

            btn_delete = ttk.Button(edit_task_window, text="Удалить",
                                    command=lambda: self.delete_task(task_id, edit_task_window))
            btn_delete.grid(row=2, column=1, padx=10, pady=10)

    def update_task(self, task_id, name, responsible_name, edit_task_window):
        responsible_id = self.database.fetch_one("SELECT id FROM employees WHERE name=?", (responsible_name,))
        if responsible_id:
            self.database.execute_query("UPDATE tasks SET name=?, responsible_employee_id=? WHERE id=?",
                                        (name, responsible_id[0], task_id))
            self.refresh_tasks()
            edit_task_window.destroy()
        else:
            simpledialog.messagebox.showerror("Ошибка", "Выберите существующего ответственного сотрудника")

    def delete_task(self, task_id, edit_task_window):
        result = simpledialog.askstring("Подтверждение", "Вы уверены, что хотите удалить задачу? (да/нет)")

        if result.lower() == "да":
            self.database.execute_query("DELETE FROM tasks WHERE id=?", (task_id,))
            self.refresh_tasks()
            edit_task_window.destroy()
