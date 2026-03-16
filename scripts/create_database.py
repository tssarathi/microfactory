import sqlite3
import csv
import os
from typing import Dict

db_path = "data/silver/database/field_service.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def create_table(table_name: str, columns: Dict[str, str]):

    with open(f"data/bronze/records/{table_name}.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{column} {columns[column]}' for column in columns])})"
        )
        cursor.executemany(
            f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in columns])})",
            [tuple(row[col] for col in columns) for row in rows],
        )
        conn.commit()


create_table(
    "customers",
    {
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT",
        "phone": "TEXT",
        "email": "TEXT",
        "address": "TEXT",
        "suburb": "TEXT",
        "customer_type": "TEXT",
        "priority": "TEXT",
        "contract_start": "TEXT",
        "contract_end": "TEXT",
        "site_notes": "TEXT",
    },
)

create_table(
    "technicians",
    {
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT",
        "phone": "TEXT",
        "email": "TEXT",
        "specializations": "TEXT",
        "service_area": "TEXT",
        "status": "TEXT",
        "vehicle": "TEXT",
        "hourly_rate": "REAL",
    },
)

create_table(
    "technician_certifications",
    {
        "id": "INTEGER PRIMARY KEY",
        "technician_id": "INTEGER",
        "cert_type": "TEXT",
        "licence_number": "TEXT",
        "issued_date": "TEXT",
        "expiry_date": "TEXT",
        "issuing_body": "TEXT",
    },
)

create_table(
    "equipment",
    {
        "id": "INTEGER PRIMARY KEY",
        "customer_id": "INTEGER",
        "equipment_type": "TEXT",
        "make": "TEXT",
        "model": "TEXT",
        "serial_number": "TEXT",
        "install_date": "TEXT",
        "warranty_expiry": "TEXT",
        "last_service_date": "TEXT",
        "next_service_due": "TEXT",
        "location_notes": "TEXT",
        "status": "TEXT",
    },
)

create_table(
    "work_orders",
    {
        "id": "INTEGER PRIMARY KEY",
        "customer_id": "INTEGER",
        "equipment_id": "INTEGER",
        "title": "TEXT",
        "description": "TEXT",
        "priority": "TEXT",
        "status": "TEXT",
        "technician_id": "INTEGER",
        "created_date": "TEXT",
        "scheduled_date": "TEXT",
        "completed_date": "TEXT",
        "estimated_hours": "REAL",
        "actual_hours": "REAL",
        "diagnosis": "TEXT",
        "resolution": "TEXT",
    },
)

create_table(
    "work_order_parts",
    {
        "id": "INTEGER PRIMARY KEY",
        "work_order_id": "INTEGER",
        "part_id": "INTEGER",
        "quantity_used": "INTEGER",
    },
)

create_table(
    "parts_inventory",
    {
        "id": "INTEGER PRIMARY KEY",
        "part_number": "TEXT",
        "part_name": "TEXT",
        "category": "TEXT",
        "quantity": "INTEGER",
        "minimum_stock": "INTEGER",
        "unit_cost": "REAL",
        "supplier": "TEXT",
    },
)

create_table(
    "schedules",
    {
        "id": "INTEGER PRIMARY KEY",
        "technician_id": "INTEGER",
        "work_order_id": "INTEGER",
        "date": "TEXT",
        "start_time": "TEXT",
        "end_time": "TEXT",
        "schedule_type": "TEXT",
        "notes": "TEXT",
    },
)

create_table(
    "job_notes",
    {
        "id": "INTEGER PRIMARY KEY",
        "work_order_id": "INTEGER",
        "technician_id": "INTEGER",
        "created_at": "TEXT",
        "note_type": "TEXT",
        "content": "TEXT",
    },
)

conn.close()
print("Database created at data/silver/database/field_service.db")
