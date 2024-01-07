import tkinter as tk
from tkinter import ttk

from database import Database
from employees_tab import EmployeesTab
from finance_tab import FinanceTab
from statistics_tab import StatisticsTab


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("АРМ Главного Менеджера")
        self.geometry("1000x500")

        self.create_widgets()
        self.config(background="black")

    def create_widgets(self):
        #Connect BD and Faker
        self.database = Database()
        self.database.populate_fake_data()
        # Создание вкладок
        self.tabs = ttk.Notebook(self)
        self.tab_employees = EmployeesTab(self.tabs)
        self.tab_statistics = StatisticsTab(self.tabs)
        self.tabs.add(self.tab_employees, text="Сотрудники")
        self.tabs.add(self.tab_statistics, text="Статистика")
        self.tab_finance = FinanceTab(self.tabs, self.database)
        self.tabs.add(self.tab_finance, text="Финансы")

        self.tabs.pack(expand=1, fill="both")

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
