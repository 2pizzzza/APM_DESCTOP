# projects_tab.py
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk


class ProjectsTab(tk.Frame):
    def __init__(self, master=None, database=None):
        super().__init__(master)
        self.database = database
        self.create_widgets()

    def create_widgets(self):
        # Кнопка для добавления проекта
        btn_add_project = ttk.Button(self, text="Добавить проект", command=self.add_project)
        btn_add_project.pack(pady=10)

        # Таблица с проектами
        columns = ("ID", "Название", "Ответственный сотрудник")
        self.tree_projects = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree_projects.heading(col, text=col, anchor="center")
            self.tree_projects.column(col, width=450, anchor="center")

        self.tree_projects.pack(pady=10)

        # Обновить список проектов
        btn_refresh_projects = ttk.Button(self, text="Обновить список проектов", command=self.refresh_projects)
        btn_refresh_projects.pack(pady=10)

        # Привязка функции для обработки двойного клика по проекту
        self.tree_projects.bind("<Double-1>", lambda event: self.edit_project())
        self.refresh_projects()

    def refresh_projects(self):
        for row in self.tree_projects.get_children():
            self.tree_projects.delete(row)

        projects = self.database.fetch_all("SELECT projects.id, projects.name, employees.name FROM projects "
                                           "LEFT JOIN employees ON projects.responsible_employee_id = employees.id")

        for project in projects:
            self.tree_projects.insert("", "end", values=project)

    def add_project(self):
        add_project_window = tk.Toplevel(self)
        add_project_window.title("Добавить проект")

        lbl_name = ttk.Label(add_project_window, text="Название:")
        lbl_name.grid(row=0, column=0, padx=10, pady=10)

        entry_name = ttk.Entry(add_project_window)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        # Выпадающий список для выбора ответственного сотрудника
        lbl_responsible = ttk.Label(add_project_window, text="Ответственный сотрудник:")
        lbl_responsible.grid(row=1, column=0, padx=10, pady=10)

        employees = self.database.fetch_all("SELECT * FROM employees")
        employee_names = [employee[1] for employee in employees]
        responsible_var = tk.StringVar(add_project_window)
        responsible_var.set(employee_names[0])
        dropdown_responsible = ttk.Combobox(add_project_window, textvariable=responsible_var, values=employee_names)
        dropdown_responsible.grid(row=1, column=1, padx=10, pady=10)

        btn_save = ttk.Button(add_project_window, text="Сохранить", command=lambda: self.save_project(
            entry_name.get(), responsible_var.get(), add_project_window))
        btn_save.grid(row=2, columnspan=2, pady=10)

    def save_project(self, name, responsible_name, add_project_window):
        responsible_id = self.database.fetch_one("SELECT id FROM employees WHERE name=?", (responsible_name,))

        if responsible_id:
            self.database.execute_query("INSERT INTO projects (name, responsible_employee_id) VALUES (?, ?)",
                                        (name, responsible_id[0]))
            self.refresh_projects()
            add_project_window.destroy()
        else:
            simpledialog.messagebox.showerror("Ошибка", "Выберите существующего ответственного сотрудника")

    def edit_project(self):
        selected_item = self.tree_projects.selection()
        if selected_item:
            project_id = self.tree_projects.item(selected_item, "values")[0]
            project_name = self.tree_projects.item(selected_item, "values")[1]
            responsible_name = self.tree_projects.item(selected_item, "values")[2]

            edit_project_window = tk.Toplevel(self)
            edit_project_window.title("Редактировать проект")

            lbl_name = ttk.Label(edit_project_window, text="Название:")
            lbl_name.grid(row=0, column=0, padx=10, pady=10)

            entry_name = ttk.Entry(edit_project_window)
            entry_name.insert(0, project_name)
            entry_name.grid(row=0, column=1, padx=10, pady=10)

            # Выпадающий список для выбора ответственного сотрудника
            lbl_responsible = ttk.Label(edit_project_window, text="Ответственный сотрудник:")
            lbl_responsible.grid(row=1, column=0, padx=10, pady=10)

            employees = self.database.fetch_all("SELECT * FROM employees")
            employee_names = [employee[1] for employee in employees]
            responsible_var = tk.StringVar(edit_project_window)
            responsible_var.set(responsible_name)
            dropdown_responsible = ttk.Combobox(edit_project_window, textvariable=responsible_var,
                                                values=employee_names)
            dropdown_responsible.grid(row=1, column=1, padx=10, pady=10)

            btn_save = ttk.Button(edit_project_window, text="Сохранить", command=lambda: self.update_project(
                project_id, entry_name.get(), responsible_var.get(), edit_project_window))
            btn_save.grid(row=2, columnspan=2, pady=10)

    def update_project(self, project_id, name, responsible_name, edit_project_window):
        responsible_id = self.database.fetch_one("SELECT id FROM employees WHERE name=?", (responsible_name,))

        if responsible_id:
            self.database.execute_query("UPDATE projects SET name=?, responsible_employee_id=? WHERE id=?",
                                        (name, responsible_id[0], project_id))
            self.refresh_projects()
            edit_project_window.destroy()
        else:
            simpledialog.messagebox.showerror("Ошибка", "Выберите существующего ответственного сотрудника")
