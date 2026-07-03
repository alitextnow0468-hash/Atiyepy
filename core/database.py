# core/database.py
# Atiyepy - Database layer (sqlite3 - stdlib). Upgradeable independently.
# Handles employees and settings persistence.

import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
        self.db_path = os.path.join(base_dir, "data", "hrm.db")
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                code TEXT PRIMARY KEY,
                last_name TEXT NOT NULL,
                national_id TEXT,
                id_number TEXT,
                marital TEXT,
                children INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)

        columns_to_add = [
            ("position", "TEXT"),
            ("base_salary", "INTEGER DEFAULT 166255500"),
            ("employment_year", "INTEGER"),
            ("employment_month", "INTEGER"),
            ("employment_day", "INTEGER")
        ]
        for col_name, col_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE employees ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError:
                pass  # column exists

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        conn.commit()
        conn.close()

    def load_settings(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings")
        settings = {key: value for key, value in cursor.fetchall()}
        conn.close()
        return settings

    def save_setting(self, key, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()

    def load_employees(self):
        employees = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT code, last_name, national_id, id_number, position, base_salary, 
                   marital, children, employment_year, employment_month, employment_day 
            FROM employees
        """)
        for row in cursor.fetchall():
            emp = {
                "code": row[0],
                "last_name": row[1],
                "national_id": row[2],
                "id_number": row[3] or "",
                "position": row[4] or "",
                "base_salary": row[5] or 166255500,
                "marital": row[6],
                "children": row[7] or 0,
                "employment_year": row[8],
                "employment_month": row[9] or 1,
                "employment_day": row[10] or 1
            }
            employees.append(emp)
        conn.close()
        return employees

    def save_employee(self, emp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employees 
            (code, last_name, national_id, id_number, position, base_salary, marital, children,
             employment_year, employment_month, employment_day, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            emp["code"], emp["last_name"], emp["national_id"], emp.get("id_number", ""),
            emp.get("position", ""), emp.get("base_salary", 166255500),
            emp.get("marital", ""), emp.get("children", 0),
            emp.get("employment_year"), emp.get("employment_month"), emp.get("employment_day"),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

    def update_employee(self, emp):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE employees SET 
                last_name = ?, national_id = ?, id_number = ?, position = ?, 
                base_salary = ?, marital = ?, children = ?, 
                employment_year = ?, employment_month = ?, employment_day = ?
            WHERE code = ?
        """, (
            emp["last_name"], emp["national_id"], emp.get("id_number", ""),
            emp.get("position", ""), emp.get("base_salary", 166255500),
            emp.get("marital", ""), emp.get("children", 0),
            emp.get("employment_year"), emp.get("employment_month"), emp.get("employment_day"),
            emp["code"]
        ))
        conn.commit()
        conn.close()

    def delete_employee(self, code):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE code = ?", (code,))
        conn.commit()
        conn.close()

    def employee_exists(self, national_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM employees WHERE national_id = ?", (national_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists