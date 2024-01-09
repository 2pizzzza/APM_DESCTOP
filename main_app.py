import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from database import Database
from employees_tab import EmployeesTab
from finance_tab import FinanceTab
from statistics_tab import StatisticsTab

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("АРМ Главного Менеджера")
        self.geometry("1500x700")

        self.create_widgets()
        self.configure(background="white")

    def create_widgets(self):
        # Connect BD and Faker
        self.database = Database()

        # Создание вкладок
        self.tabs = ttk.Notebook(self)

        # Load images and create PhotoImage objects
        icon_employees_1 = Image.open("media/554744.png").resize((30,30), Image.ADAPTIVE)
        icon_statistics_2 = Image.open("media/statis.png").resize((30, 30), Image.AFFINE)
        icon_finance_3 = Image.open("media/finance.png").resize((30, 30), Image.AFFINE)

        self.icon_employees = ImageTk.PhotoImage(icon_employees_1)
        self.icon_statistics = ImageTk.PhotoImage(icon_statistics_2)
        self.icon_finance = ImageTk.PhotoImage(icon_finance_3)

        # Create tab instances
        tab_employees = EmployeesTab(self.tabs)
        tab_statistics = StatisticsTab(self.tabs, self.database)
        tab_finance = FinanceTab(self, self.database)

        # Add tabs to the notebook
        self.tabs.add(tab_employees, text="Сотрудники", compound=tk.TOP, image=self.icon_employees)
        self.tabs.add(tab_statistics, text="Статистика", compound=tk.TOP, image=self.icon_statistics)
        self.tabs.add(tab_finance, text="Финансы", compound=tk.TOP, image=self.icon_finance)

        # Pack the notebook
        self.tabs.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
