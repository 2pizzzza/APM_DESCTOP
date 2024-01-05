import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database import Database


class StatisticsTab(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.database = Database()
        self.create_widgets()

    def create_widgets(self):
        self.database = Database()
        frame_statistics = ttk.Frame(self)
        frame_statistics.pack(pady=10)

        btn_show_statistics = ttk.Button(frame_statistics, text="Показать статистику", command=self.show_statistics)
        btn_show_statistics.pack(pady=10)

    def show_statistics(self):
        total_employees = self.database.fetch_all("SELECT COUNT(*) FROM employees")[0][0]

        position_stats = self.database.fetch_all("SELECT position, COUNT(position) FROM employees GROUP BY position")

        self.show_statistics_window(total_employees, position_stats)

    def show_statistics_window(self, total_employees, position_stats):
        statistics_window = tk.Toplevel(self)
        statistics_window.title("Статистика")

        lbl_total_employees = ttk.Label(statistics_window, text=f"Общее количество сотрудников: {total_employees}")
        lbl_total_employees.pack(pady=10)

        lbl_position_stats = ttk.Label(statistics_window, text="Количество сотрудников по должностям:")
        lbl_position_stats.pack(pady=5)

        positions = []
        counts = []

        for position, count in position_stats:
            positions.append(position)
            counts.append(count)

        fig, ax = plt.subplots()
        ax.pie(counts, labels=positions, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        canvas = FigureCanvasTkAgg(fig, master=statistics_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
