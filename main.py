import tkinter as tk
from tkinter import ttk
import sqlite3

verify_table = 0


def set_table(number):
    global verify_table
    verify_table = number


class TkinterApp:
    def __init__(self, master):
        self.tree = None
        self.master = master
        self.master.title("Faculty Management System")

        # Set the initial size of the window (width x height)
        self.master.geometry("1800x800")

        # Database initialization
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()

        # Create and set up GUI components
        self.create_widgets()

    def destroy_frame(self):
        if hasattr(self, 'frame2'):
            # If frame2 exists, destroy it
            self.frame2.destroy()

    def create_widgets(self):
        # Frame for the first set of buttons (students, professors)
        frame1 = tk.Frame(self.master)
        frame1.pack(side="top", padx=10, pady=5, anchor="nw")  # "nw" stands for northwest

        students_button = tk.Button(frame1, text="Students", command=self.show_students_table)
        students_button.pack(side="left", padx=5)

        grades_button = tk.Button(frame1, text="Grades", command=self.show_grades_table)
        grades_button.pack(side="left", padx=5)

        professors_button = tk.Button(frame1, text="Professors", command=self.show_professors_table)
        professors_button.pack(side="left", padx=5)

        for year in range(1, 5):
            year_button = tk.Button(frame1, text=f"Year {year}", command=lambda y=year: self.show_year_table(y))
            year_button.pack(side="left", padx=5)

        graduates_button = tk.Button(frame1, text="Graduates", command=self.show_graduates_table)
        graduates_button.pack(side="left", padx=5)

        space_label1 = tk.Label(frame1, text="    ")
        space_label1.pack(side="left")

        last_asc_button = tk.Button(frame1, text="LAST NAME ASC", command=lambda: self.show_sorted("Last_Name", "ASC"))
        last_asc_button.pack(side="left", padx=2)
        last_desc_button = tk.Button(frame1, text="LAST NAME DESC", command=lambda: self.show_sorted("Last_Name", "DESC"))
        last_desc_button.pack(side="left", padx=2)

        space_label1 = tk.Label(frame1, text="  ")
        space_label1.pack(side="left")

        first_asc_button = tk.Button(frame1, text="FIRST NAME ASC", command=lambda: self.show_sorted("First_Name", "ASC"))
        first_asc_button.pack(side="left", padx=2)
        first_desc_button = tk.Button(frame1, text="FIRST NAME DESC", command=lambda: self.show_sorted("First_Name", "DESC"))
        first_desc_button.pack(side="left", padx=2)

        space_label1 = tk.Label(frame1, text="  ")
        space_label1.pack(side="left")

        year_asc_button = tk.Button(frame1, text="YEAR ASC", command=lambda: self.show_sorted("Year", "ASC"))
        year_asc_button.pack(side="left", padx=2)
        year_desc_button = tk.Button(frame1, text="YEAR DESC", command=lambda: self.show_sorted("Year", "DESC"))
        year_desc_button.pack(side="left", padx=2)

        space_label1 = tk.Label(frame1, text="  ")
        space_label1.pack(side="left")

        mark_asc_button = tk.Button(frame1, text="MARK ASC", command=lambda: self.show_sorted("Mark", "ASC"))
        mark_asc_button.pack(side="left", padx=2)
        mark_desc_button = tk.Button(frame1, text="MARK DESC", command=lambda: self.show_sorted("Mark", "DESC"))
        mark_desc_button.pack(side="left", padx=2)

        space_label1 = tk.Label(frame1, text="  ")
        space_label1.pack(side="left")

        space_label1 = tk.Label(frame1, text="  ")
        space_label1.pack(side="left")

        graduates_button = tk.Button(frame1, text="PASS 1 YEAR", command=self.promovate)
        graduates_button.pack(side="left", padx=2)

        self.frame2 = tk.Frame(self.master)
        self.frame2.pack(side="top", padx=10, pady=10, anchor="nw")  # Place it below the first frame

    def show_students_table(self):
        set_table(1)
        self.show_table("students")

    def show_grades_table(self):
        set_table(2)
        self.show_table("grades")

    def show_professors_table(self):
        set_table(3)
        self.show_table("professors")

    def show_year_table(self, year):
        # different cases depending on the shown year
        match year:
            case 1:
                set_table(4)
            case 2:
                set_table(5)
            case 3:
                set_table(6)
            case 4:
                set_table(7)
        self.show_table(f"year{year}")

    def show_graduates_table(self):
        set_table(8)
        self.show_table("graduates")

    def show_sorted(self, criteria, typo):

        match verify_table:
            case 1:
                table_n = "students"
            case 2:
                table_n = "grades"
                criteria = "Grade"
            case 3:
                table_n = "professors"
            case 4:
                table_n = "year1"
            case 5:
                table_n = "year2"
            case 6:
                table_n = "year3"
            case 7:
                table_n = "year4"
            case 8:
                table_n = "graduates"

        self.show_sorted_table(f"{table_n}", f"{criteria}", f"{typo}")

    def promovate(self):
        query = f'INSERT INTO graduates SELECT ID FROM students WHERE "Year" = 4 AND "Mark" >= 5;'
        self.cursor.execute(query)
        query = f'DELETE FROM students WHERE "Year" = 4 AND Mark >= 5;'
        self.cursor.execute(query)
        query = f'UPDATE students SET "Year" = 4 WHERE "Year" = 3 AND Mark >=5;'
        self.cursor.execute(query)
        query = f'UPDATE students SET "Year" = 3 WHERE "Year" = 2 AND Mark >=5;'
        self.cursor.execute(query)
        query = f'UPDATE students SET "Year" = 2 WHERE "Year" = 1 AND Mark >=5;'
        self.cursor.execute(query)
        query = f'DELETE FROM year1 WHERE "Mark" >= 5;'
        self.cursor.execute(query)
        query = f'DELETE FROM year2 WHERE "Mark" >= 5;'
        self.cursor.execute(query)
        query = f'INSERT INTO year2 ("ID", "Mark") SELECT "ID", "Mark" FROM students WHERE "Year" = 2 AND Mark >=5;'
        self.cursor.execute(query)
        query = f'DELETE FROM year3 WHERE "Mark" >= 5;'
        self.cursor.execute(query)
        query = f'INSERT INTO year3 ("ID", "Mark") SELECT "ID", "Mark" FROM students WHERE "Year" = 3 AND Mark >=5;'
        self.cursor.execute(query)
        query = f'DELETE FROM year4 WHERE "Mark" >= 5;'
        self.cursor.execute(query)
        query = f'INSERT INTO year4 ("ID", "Mark") SELECT "ID", "Mark" FROM students WHERE "Year" = 4 AND Mark >= 5;'
        self.cursor.execute(query)

    def show_table(self, table_name):
        # Retrieve data from the selected table
        query = f'SELECT * FROM {table_name}'
        self.cursor.execute(query)
        table_data = self.cursor.fetchall()

        if hasattr(self, 'tree') and isinstance(self.tree, ttk.Treeview):
            self.tree.destroy()

        self.tree = ttk.Treeview(self.frame2, columns=self.get_column_names(table_name), show='headings',
                                 height=20)

        column_widths = (200, 200, 200, 200, 200, 200, 200, 200)  # Adjust these values as needed

        for i, column in enumerate(self.get_column_names(table_name)):
            self.tree.heading(column, text=column)
            self.tree.column(column, width=column_widths[i], anchor="center")

        for row in table_data:
            self.tree.insert('', 'end', values=row)

        self.tree.pack(padx=10, pady=10)

    def show_sorted_table(self, table_name, criteria, type):

        query = f'SELECT * FROM {table_name} ORDER BY {criteria} {type}'
        self.cursor.execute(query)
        table_data = self.cursor.fetchall()

        if hasattr(self, 'tree') and isinstance(self.tree, ttk.Treeview):
            self.tree.destroy()

        self.tree = ttk.Treeview(self.frame2, columns=self.get_column_names(table_name), show='headings',
                                 height=20)

        column_widths = (200, 200, 200, 200, 200, 200, 200, 200)  # Adjust these values as needed

        for i, column in enumerate(self.get_column_names(table_name)):
            self.tree.heading(column, text=column)
            self.tree.column(column, width=column_widths[i], anchor="center")

        for row in table_data:
            self.tree.insert('', 'end', values=row)

        self.tree.pack(padx=10, pady=10)

    def get_column_names(self, table_name):
        # Get the column names of a table
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]
        return columns


if __name__ == '__main__':
    root = tk.Tk()
    app = TkinterApp(root)
    root.mainloop()
