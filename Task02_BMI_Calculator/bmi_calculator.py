import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

def initialize_database():
    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not initialize the database:\n{error}"
        )


initialize_database()

# Create main window
window = tk.Tk()
window.title("BMI Calculator")
window.geometry("400x430")
window.resizable(False, False)


# Title
title_label = tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=20)


# User name
name_label = tk.Label(
    window,
    text="User Name:"
)
name_label.pack()

name_entry = tk.Entry(window, width=30)
name_entry.pack(pady=5)


# Weight
weight_label = tk.Label(
    window,
    text="Weight (kg):"
)
weight_label.pack()

weight_entry = tk.Entry(window, width=30)
weight_entry.pack(pady=5)


# Height
height_label = tk.Label(
    window,
    text="Height (m):"
)
height_label.pack()

height_entry = tk.Entry(window, width=30)
height_entry.pack(pady=5)

def calculate_bmi():
    try:
        name = name_entry.get().strip()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if not name:
            messagebox.showerror("Input Error", "Please enter a user name.")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Input Error",
                "Weight and height must be greater than zero."
            )
            return

        bmi = weight / (height ** 2)

        if bmi < 18.5:
            category = "Underweight"
            color = "blue"

        elif bmi < 25:
            category = "Normal"
            color = "green"

        elif bmi < 30:
            category = "Overweight"
            color = "orange"

        else:
            category = "Obese"
            color = "red"


        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=color
        )

        try:
            connection = sqlite3.connect("bmi_records.db")
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO bmi_records
                (user_name, weight, height, bmi, category, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                weight,
                height,
                bmi,
                category,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not save the BMI record:\n{error}"
            )



    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values for weight and height."
        )

def view_bmi_trend():
    try:
        name = name_entry.get().strip()

        if not name:
            messagebox.showerror(
                "Input Error",
                "Please enter a user name first."
            )
            return

        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT recorded_at, bmi
            FROM bmi_records
            WHERE user_name = ?
            ORDER BY recorded_at
        """, (name,))

        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo(
                "BMI Trend",
                f"No BMI records found for {name}."
            )
            return

        dates = [record[0] for record in records]
        bmi_values = [record[1] for record in records]

        plt.figure(figsize=(8, 5))
        plt.plot(dates, bmi_values, marker="o")

        plt.title(f"BMI Trend for {name}")
        plt.xlabel("Date and Time")
        plt.ylabel("BMI")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        plt.show()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not read BMI records:\n{error}"
        )

def view_history():
    try:
        connection = sqlite3.connect("bmi_records.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_name, weight, height, bmi, category, recorded_at
            FROM bmi_records
            ORDER BY recorded_at DESC
        """)

        records = cursor.fetchall()
        connection.close()

        if not records:
            messagebox.showinfo(
                "BMI History",
                "No BMI records found."
            )
            return

        history_window = tk.Toplevel(window)
        history_window.title("BMI History")
        history_window.geometry("650x400")

        history_text = tk.Text(
            history_window,
            width=75,
            height=20
        )
        history_text.pack(padx=10, pady=10)

        for record in records:
            user_name, weight, height, bmi, category, recorded_at = record

            history_text.insert(
                tk.END,
                f"User: {user_name}\n"
                f"Weight: {weight} kg | Height: {height} m\n"
                f"BMI: {bmi:.2f} | Category: {category}\n"
                f"Recorded: {recorded_at}\n"
                f"{'-' * 60}\n"
            )

        history_text.config(state="disabled")

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not read BMI history:\n{error}"
        )

# Result
result_label = tk.Label(
    window,
    text="",
    font=("Arial", 12, "bold")
)
result_label.pack(pady=20)

calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    command=calculate_bmi,
    width=20
)
calculate_button.pack(pady=10)

history_button = tk.Button(
    window,
    text="View History",
    command=view_history,
    width=20
)
history_button.pack(pady=5)

trend_button = tk.Button(
    window,
    text="View BMI Trend",
    command=view_bmi_trend,
    width=20
)
trend_button.pack(pady=5)


# Start GUI
window.mainloop()
