import tkinter as tk
from tkinter import ttk, simpledialog
from database import Database

class FinanceTab(tk.Frame):
    def __init__(self, master=None, database=None):
        super().__init__(master)
        self.database = database
        self.create_widgets()

    def create_widgets(self):
        frame_finances = ttk.Frame(self)
        frame_finances.pack(pady=10)

        # Treeview для отображения финансовых данных
        columns = ("ID", "Бюджет", "Доход", "Расход")
        self.tree_finances = ttk.Treeview(frame_finances, columns=columns, show="headings")

        for col in columns:
            self.tree_finances.heading(col, text=col)
            self.tree_finances.column(col, width=100)

        self.tree_finances.pack()

        btn_refresh = ttk.Button(self, text="Обновить список", command=self.refresh_finances)
        btn_refresh.pack(pady=10)

        btn_add_finance = ttk.Button(self, text="Добавить финансовую информацию", command=self.add_finance)
        btn_add_finance.pack(pady=10)

        btn_edit_finance = ttk.Button(self, text="Редактировать финансовую информацию", command=self.edit_finance)
        btn_edit_finance.pack(pady=10)

        btn_delete_finance = ttk.Button(self, text="Удалить финансовую информацию", command=self.delete_finance)
        btn_delete_finance.pack(pady=10)

        self.refresh_finances()

    def refresh_finances(self):
        for row in self.tree_finances.get_children():
            self.tree_finances.delete(row)

        finances = self.database.fetch_all("SELECT * FROM finances")

        for finance in finances:
            self.tree_finances.insert("", "end", values=finance)

    def add_finance(self):
        add_finance_window = tk.Toplevel(self)
        add_finance_window.title("Добавить финансовую информацию")

        lbl_budget = ttk.Label(add_finance_window, text="Бюджет:")
        lbl_budget.grid(row=0, column=0, padx=10, pady=10)

        entry_budget = ttk.Entry(add_finance_window)
        entry_budget.grid(row=0, column=1, padx=10, pady=10)

        lbl_income = ttk.Label(add_finance_window, text="Доход:")
        lbl_income.grid(row=1, column=0, padx=10, pady=10)

        entry_income = ttk.Entry(add_finance_window)
        entry_income.grid(row=1, column=1, padx=10, pady=10)

        lbl_expense = ttk.Label(add_finance_window, text="Расход:")
        lbl_expense.grid(row=2, column=0, padx=10, pady=10)

        entry_expense = ttk.Entry(add_finance_window)
        entry_expense.grid(row=2, column=1, padx=10, pady=10)

        btn_save = ttk.Button(add_finance_window, text="Сохранить", command=lambda: self.save_finance(
            entry_budget.get(), entry_income.get(), entry_expense.get(), add_finance_window))
        btn_save.grid(row=3, columnspan=2, pady=10)

    def save_finance(self, budget, income, expense, add_finance_window):
        self.database.execute_query("INSERT INTO finances (budget, income, expense) VALUES (?, ?, ?)",
                                    (budget, income, expense))
        self.refresh_finances()
        add_finance_window.destroy()

    def edit_finance(self):
        selected_item = self.tree_finances.selection()
        if selected_item:
            finance_id = self.tree_finances.item(selected_item, "values")[0]
            budget = self.tree_finances.item(selected_item, "values")[1]
            income = self.tree_finances.item(selected_item, "values")[2]
            expense = self.tree_finances.item(selected_item, "values")[3]

            edit_finance_window = tk.Toplevel(self)
            edit_finance_window.title("Редактировать финансовую информацию")

            lbl_budget = ttk.Label(edit_finance_window, text="Бюджет:")
            lbl_budget.grid(row=0, column=0, padx=10, pady=10)

            entry_budget = ttk.Entry(edit_finance_window)
            entry_budget.insert(0, budget)
            entry_budget.grid(row=0, column=1, padx=10, pady=10)

            lbl_income = ttk.Label(edit_finance_window, text="Доход:")
            lbl_income.grid(row=1, column=0, padx=10, pady=10)

            entry_income = ttk.Entry(edit_finance_window)
            entry_income.insert(0, income)
            entry_income.grid(row=1, column=1, padx=10, pady=10)

            lbl_expense = ttk.Label(edit_finance_window, text="Расход:")
            lbl_expense.grid(row=2, column=0, padx=10, pady=10)

            entry_expense = ttk.Entry(edit_finance_window)
            entry_expense.insert(0, expense)
            entry_expense.grid(row=2, column=1, padx=10, pady=10)

            btn_save = ttk.Button(edit_finance_window, text="Сохранить",
                                  command=lambda: self.update_finance(finance_id, entry_budget.get(),
                                                                       entry_income.get(), entry_expense.get(),
                                                                       edit_finance_window))
            btn_save.grid(row=3, column=0, padx=10, pady=10)

            btn_delete = ttk.Button(edit_finance_window, text="Удалить",
                                    command=lambda: self.delete_finance(finance_id, edit_finance_window))
            btn_delete.grid(row=3, column=1, padx=10, pady=10)

    def update_finance(self, finance_id, budget, income, expense, edit_finance_window):
        self.database.execute_query("UPDATE finances SET budget=?, income=?, expense=? WHERE id=?",
                                    (budget, income, expense, finance_id))
        self.refresh_finances()
        edit_finance_window.destroy()

    def delete_finance(self, finance_id, edit_finance_window):
        result = simpledialog.askstring("Подтверждение", "Вы уверены, что хотите удалить финансовую информацию? (да/нет)")

        if result.lower() == "да":
            self.database.execute_query("DELETE FROM finances WHERE id=?", (finance_id,))
            self.refresh_finances()
            edit_finance_window.destroy()
