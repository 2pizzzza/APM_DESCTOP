import tkinter as tk
from tkinter import simpledialog, ttk
from database import Database

class EmployeesTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.database = Database()
        self.create_widgets()

    def create_widgets(self):
        self.database = Database()
        # Frame for search
        frame_search = ttk.Frame(self)
        frame_search.grid(row=0, column=0, columnspan=5, pady=10)

        # Search by name label and entry
        lbl_search_name = ttk.Label(frame_search, text="Поиск по имени:")
        lbl_search_name.grid(row=0, column=0, padx=5, pady=5)

        self.entry_search_name = ttk.Entry(frame_search)
        self.entry_search_name.grid(row=0, column=1, padx=5, pady=5)

        # Search by position label and combobox
        lbl_search_position = ttk.Label(frame_search, text="Поиск по должности:")
        lbl_search_position.grid(row=0, column=2, padx=5, pady=5)

        positions = ["", "Менеджер", "Бухгалтер", "Инженер", "Программист", "Другое"]
        self.position_var = tk.StringVar(frame_search)
        self.position_var.set(positions[0])
        dropdown_search_position = ttk.Combobox(frame_search, textvariable=self.position_var, values=positions)
        dropdown_search_position.grid(row=0, column=3, padx=5, pady=5)

        # Search button
        btn_search = ttk.Button(frame_search, text="Поиск", command=self.search_employees)
        btn_search.grid(row=0, column=4, padx=5, pady=5)

        # Frame for employees
        frame_employees = ttk.Frame(self)
        frame_employees.grid(row=1, column=0, columnspan=5, pady=10)

        columns = ("ID", "Имя", "Должность")
        self.tree_employees = ttk.Treeview(frame_employees, columns=columns, show="headings")

        for col in columns:
            self.tree_employees.heading(col, text=col)
            self.tree_employees.column(col, width=100)

        self.tree_employees.grid(row=0, column=0, padx=10, pady=10)

        # Refresh and add employee buttons
        btn_refresh = ttk.Button(self, text="Обновить список", command=self.refresh_employees)
        btn_refresh.grid(row=2, column=0, pady=10)

        btn_add_employee = ttk.Button(self, text="Добавить сотрудника", command=self.add_employee)
        btn_add_employee.grid(row=2, column=1, pady=10)

        # Frame for info
        frame_info = ttk.Frame(self)
        frame_info.grid(row=3, column=0, columnspan=5, pady=10)

        self.lbl_info = ttk.Label(frame_info, text="Общая информация о предприятии")
        self.lbl_info.grid(row=0, column=0, pady=10)

        # Double-click binding for editing
        self.tree_employees.bind("<Double-1>", lambda event: self.edit_employee())

    def refresh_employees(self):
        for row in self.tree_employees.get_children():
            self.tree_employees.delete(row)

        employees = self.database.fetch_all("SELECT * FROM employees")

        for employee in employees:
            self.tree_employees.insert("", "end", values=employee)

    def add_employee(self):
        add_employee_window = tk.Toplevel(self)
        add_employee_window.title("Добавить сотрудника")

        lbl_name = ttk.Label(add_employee_window, text="Имя:")
        lbl_name.grid(row=0, column=0, padx=10, pady=10)

        entry_name = ttk.Entry(add_employee_window)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        lbl_position = ttk.Label(add_employee_window, text="Должность:")
        lbl_position.grid(row=1, column=0, padx=10, pady=10)

        positions = ["Менеджер", "Бухгалтер", "Инженер", "Программист", "Другое"]
        position_var = tk.StringVar(add_employee_window)
        position_var.set(positions[0])
        dropdown_position = ttk.Combobox(add_employee_window, textvariable=position_var, values=positions)
        dropdown_position.grid(row=1, column=1, padx=10, pady=10)

        btn_save = ttk.Button(add_employee_window, text="Сохранить", command=lambda: self.save_employee(
            entry_name.get(), position_var.get(), add_employee_window))
        btn_save.grid(row=2, columnspan=2, pady=10)

    def save_employee(self, name, position, add_employee_window):
        self.database.execute_query("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))
        self.refresh_employees()

        add_employee_window.destroy()

    def edit_employee(self):
        selected_item = self.tree_employees.selection()
        if selected_item:
            employee_id = self.tree_employees.item(selected_item, "values")[0]
            employee_name = self.tree_employees.item(selected_item, "values")[1]
            employee_position = self.tree_employees.item(selected_item, "values")[2]

            edit_employee_window = tk.Toplevel(self)
            edit_employee_window.title("Редактировать сотрудника")

            lbl_name = ttk.Label(edit_employee_window, text="Имя:")
            lbl_name.grid(row=0, column=0, padx=10, pady=10)

            entry_name = ttk.Entry(edit_employee_window)
            entry_name.insert(0, employee_name)
            entry_name.grid(row=0, column=1, padx=10, pady=10)

            lbl_position = ttk.Label(edit_employee_window, text="Должность:")
            lbl_position.grid(row=1, column=0, padx=10, pady=10)

            positions = ["Менеджер", "Бухгалтер", "Инженер", "Программист", "Другое"]
            position_var = tk.StringVar(edit_employee_window)
            position_var.set(employee_position)
            dropdown_position = ttk.Combobox(edit_employee_window, textvariable=position_var, values=positions)
            dropdown_position.grid(row=1, column=1, padx=10, pady=10)

            btn_save = ttk.Button(edit_employee_window, text="Сохранить",
                                  command=lambda: self.update_employee(employee_id, entry_name.get(),
                                                                       position_var.get(), edit_employee_window))
            btn_save.grid(row=2, column=0, padx=10, pady=10)

            btn_delete = ttk.Button(edit_employee_window, text="Удалить",
                                    command=lambda: self.delete_employee(employee_id, edit_employee_window))
            btn_delete.grid(row=2, column=1, padx=10, pady=10)

    def update_employee(self, employee_id, name, position, edit_employee_window):
        self.database.execute_query("UPDATE employees SET name=?, position=? WHERE id=?", (name, position, employee_id))
        self.refresh_employees()
        edit_employee_window.destroy()

    def delete_employee(self, employee_id, edit_employee_window):
        result = simpledialog.askstring("Подтверждение", "Вы уверены, что хотите удалить сотрудника? (да/нет)")

        if result.lower() == "да":
            self.database.execute_query("DELETE FROM employees WHERE id=?", (employee_id,))
            self.refresh_employees()
            edit_employee_window.destroy()

    def search_employees(self):
        search_name = self.entry_search_name.get()
        search_position = self.position_var.get()

        if not search_name and not search_position:
            return

        query = "SELECT * FROM employees WHERE name LIKE ? AND position LIKE ?"
        params = (f"%{search_name}%", f"%{search_position}%")
        search_result = self.database.fetch_all(query, params)

        for row in self.tree_employees.get_children():
            self.tree_employees.delete(row)

        for employee in search_result:
            self.tree_employees.insert("", "end", values=employee)
