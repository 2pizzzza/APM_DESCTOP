import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatisticsTab(tk.Frame):
    def __init__(self, master=None, database=None):
        super().__init__(master)
        self.database = database
        self.create_widgets()
        self.schedule_update()

    def create_widgets(self):
        frame_statistics = ttk.Frame(self)
        frame_statistics.pack(pady=10)

        # График с сотрудниками
        self.fig_employees, self.ax_employees = plt.subplots()
        self.canvas_employees = FigureCanvasTkAgg(self.fig_employees, master=self)
        self.canvas_employees_widget = self.canvas_employees.get_tk_widget()
        self.canvas_employees_widget.pack(side=tk.LEFT, padx=10)

        # График с финансами
        self.fig_finances, self.ax_finances = plt.subplots()
        self.canvas_finances = FigureCanvasTkAgg(self.fig_finances, master=self)
        self.canvas_finances_widget = self.canvas_finances.get_tk_widget()
        self.canvas_finances_widget.pack(side=tk.RIGHT, padx=10)

    def schedule_update(self):
        self.update_statistics()
        self.after(10000, self.schedule_update)  # Обновление каждые 10 секунд (в миллисекундах)

    def update_statistics(self):
        self.show_employees_statistics()
        self.show_finances_statistics()

    def show_employees_statistics(self):
        query = "SELECT position, COUNT(position) FROM employees GROUP BY position"
        position_stats = self.database.fetch_all(query)

        positions = []
        counts = []

        for position, count in position_stats:
            positions.append(position)
            counts.append(count)

        self.ax_employees.clear()
        self.ax_employees.pie(counts, labels=positions, autopct='%1.1f%%', startangle=90)
        self.ax_employees.set_title("Статистика по сотрудникам")

        self.canvas_employees.draw()

    def show_finances_statistics(self):
        query = "SELECT budget, income, expense FROM finances"
        finances = self.database.fetch_all(query)

        budgets = [finance[0] for finance in finances]
        incomes = [finance[1] for finance in finances]
        expenses = [finance[2] for finance in finances]

        self.ax_finances.clear()
        self.ax_finances.plot(budgets, label='Бюджет')
        self.ax_finances.plot(incomes, label='Доход')
        self.ax_finances.plot(expenses, label='Расход')
        self.ax_finances.set_title("Статистика по финансам")
        self.ax_finances.set_xlabel("Запись в базе данных")
        self.ax_finances.set_ylabel("Сумма")
        self.ax_finances.legend()

        self.canvas_finances.draw()
