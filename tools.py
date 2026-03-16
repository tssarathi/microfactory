import sqlite3
import json
from datetime import date, datetime

DB_PATH = "data/silver/database/field_service.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def search_work_orders(
    status: str = None, priority: str = None, customer_name: str = None
) -> str:
    conn = get_db()
    query = """
        SELECT wo.id, wo.title, wo.priority, wo.status, wo.scheduled_date,
                c.name as customer, t.name as technician
        FROM work_orders wo
        JOIN customers c ON wo.customer_id = c.id
        LEFT JOIN technicians t ON wo.technician_id = t.id
        WHERE 1=1
    """
    params = []
    if status:
        query += " AND wo.status = ?"
        params.append(status)
    if priority:
        query += " AND wo.priority = ?"
        params.append(priority)
    if customer_name:
        query += " AND c.name LIKE ?"
        params.append(f"%{customer_name}%")

    query += " ORDER BY wo.created_date DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    if not rows:
        return "No work orders found matching those filters."

    results = []
    for row in rows:
        parts = [
            f"WO-{row['id']:03d}",
            row["customer"],
            row["title"],
            row["priority"],
            row["status"],
        ]
        if row["technician"]:
            parts.append(f"Assigned: {row['technician']}")
        if row["scheduled_date"]:
            parts.append(row["scheduled_date"])
        results.append(" | ".join(parts))

    return "\n".join(results)


def get_work_order_details(work_order_id: int) -> str:
    conn = get_db()
    row = conn.execute(
        """SELECT wo.*, c.name as customer_name,
                  e.make as equipment_make, e.model as equipment_model, e.equipment_type,
                  t.name as technician_name
           FROM work_orders wo
           JOIN customers c ON wo.customer_id = c.id
           LEFT JOIN equipment e ON wo.equipment_id = e.id
           LEFT JOIN technicians t ON wo.technician_id = t.id
           WHERE wo.id = ?""",
        (work_order_id,),
    ).fetchone()

    if not row:
        conn.close()
        return f"Work order {work_order_id} not found."

    notes = conn.execute(
        "SELECT created_at, note_type, content FROM job_notes WHERE work_order_id = ? ORDER BY created_at",
        (work_order_id,),
    ).fetchall()

    parts = conn.execute(
        """SELECT pi.part_number, pi.part_name, wop.quantity_used
           FROM work_order_parts wop
           JOIN parts_inventory pi ON wop.part_id = pi.id
           WHERE wop.work_order_id = ?""",
        (work_order_id,),
    ).fetchall()

    conn.close()

    equipment_str = (
        f"{row['equipment_make']} {row['equipment_model']} ({row['equipment_type']})"
        if row["equipment_make"]
        else "N/A"
    )
    technician_str = row["technician_name"] if row["technician_name"] else "Unassigned"

    lines = [
        f"Work Order: WO-{row['id']:03d}",
        f"Customer: {row['customer_name']}",
        f"Equipment: {equipment_str}",
        f"Title: {row['title']}",
        f"Description: {row['description']}",
        f"Priority: {row['priority']}",
        f"Status: {row['status']}",
        f"Technician: {technician_str}",
        f"Created: {row['created_date']}",
    ]
    if row["scheduled_date"]:
        lines.append(f"Scheduled: {row['scheduled_date']}")
    if row["completed_date"]:
        lines.append(f"Completed: {row['completed_date']}")
    if row["estimated_hours"]:
        lines.append(f"Estimated hours: {row['estimated_hours']}")
    if row["actual_hours"]:
        lines.append(f"Actual hours: {row['actual_hours']}")
    if row["diagnosis"]:
        lines.append(f"Diagnosis: {row['diagnosis']}")
    if row["resolution"]:
        lines.append(f"Resolution: {row['resolution']}")

    if parts:
        lines.append(
            "Parts used: "
            + ", ".join(
                f"{p['part_number']} ({p['part_name']}) x{p['quantity_used']}"
                for p in parts
            )
        )

    if notes:
        lines.append("Job notes:")
        for n in notes:
            lines.append(f"  [{n['created_at']}] ({n['note_type']}) {n['content']}")

    return "\n".join(lines)


def get_available_technicians(specialization: str = None) -> str:
    """
    Find available technicians, optionally filtered by specialization.

    Args:
        specialization: Filter by skill (e.g., "hvac", "electrical", "plumbing")

    Returns:
        List of available technicians with their skills and areas.
    """
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM technicians WHERE status = 'available'"
    ).fetchall()
    conn.close()

    if specialization:
        rows = [
            r
            for r in rows
            if specialization.lower() in json.loads(r["specializations"])
        ]

    if not rows:
        spec_msg = f" with specialization '{specialization}'" if specialization else ""
        return f"No available technicians found{spec_msg}."

    results = []
    for row in rows:
        specs = ", ".join(json.loads(row["specializations"]))
        results.append(
            f"{row['name']} | Phone: {row['phone']} | Skills: {specs} | Area: {row['service_area']}"
        )

    return "\n".join(results)


def search_parts(query: str = None, category: str = None) -> str:
    conn = get_db()
    sql = "SELECT * FROM parts_inventory WHERE 1=1"
    params = []

    if query:
        sql += " AND (part_name LIKE ? OR part_number LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])
    if category:
        sql += " AND category = ?"
        params.append(category)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    if not rows:
        filters = []
        if query:
            filters.append(f"'{query}'")
        if category:
            filters.append(f"category '{category}'")
        return (
            f"No parts found matching {', '.join(filters)}."
            if filters
            else "No parts found."
        )

    results = []
    for row in rows:
        if row["quantity"] == 0:
            stock_flag = "[OUT OF STOCK] "
        elif row["quantity"] < row["minimum_stock"]:
            stock_flag = "[LOW STOCK] "
        else:
            stock_flag = ""
        results.append(
            f"{stock_flag}{row['part_number']} | {row['part_name']} | {row['category']} | "
            f"Qty: {row['quantity']} (min: {row['minimum_stock']}) | ${row['unit_cost']:.2f} | {row['supplier']}"
        )

    return "\n".join(results)


def get_customer_details(customer_id: int) -> str:
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()
    conn.close()

    if not row:
        return f"Customer {customer_id} not found."

    lines = [
        f"Customer: {row['name']}",
        f"Type: {row['customer_type']} | Priority: {row['priority']}",
        f"Phone: {row['phone']}",
        f"Email: {row['email']}",
        f"Address: {row['address']} ({row['suburb']})",
    ]

    if row["contract_start"] and row["contract_end"]:
        contract_line = f"Contract: {row['contract_start']} to {row['contract_end']}"
        if row["contract_end"] < str(date.today()):
            contract_line = f"[EXPIRED] {contract_line}"
        lines.append(contract_line)
    else:
        lines.append("Contract: No contract")

    if row["site_notes"]:
        lines.append(f"Site notes: {row['site_notes']}")

    return "\n".join(lines)


def get_customer_equipment(customer_id: int) -> str:
    conn = get_db()
    rows = conn.execute(
        """SELECT e.*, c.name as customer_name
           FROM equipment e
           JOIN customers c ON e.customer_id = c.id
           WHERE e.customer_id = ?""",
        (customer_id,),
    ).fetchall()
    conn.close()

    if not rows:
        return f"No equipment found for customer {customer_id}."

    lines = [f"Equipment for {rows[0]['customer_name']}:"]
    for row in rows:
        lines.append(
            f"  [EQ-{row['id']:03d}] {row['make']} {row['model']} | {row['equipment_type']} "
            f"| Serial: {row['serial_number']} | Status: {row['status']}"
        )
        service_str = (
            row["last_service_date"] if row["last_service_date"] else "Never serviced"
        )
        detail_parts = [f"Installed: {row['install_date']}"]
        if row["warranty_expiry"]:
            detail_parts.append(f"Warranty expires: {row['warranty_expiry']}")
        detail_parts.append(f"Last service: {service_str}")
        if row["next_service_due"]:
            detail_parts.append(f"Next service: {row['next_service_due']}")
        lines.append(f"    {' | '.join(detail_parts)}")
        if row["location_notes"]:
            lines.append(f"    Location: {row['location_notes']}")

    return "\n".join(lines)


def get_equipment_details(equipment_id: int) -> str:
    conn = get_db()
    row = conn.execute(
        """SELECT e.*, c.name as customer_name
           FROM equipment e
           JOIN customers c ON e.customer_id = c.id
           WHERE e.id = ?""",
        (equipment_id,),
    ).fetchone()
    conn.close()

    if not row:
        return f"Equipment {equipment_id} not found."

    today_str = str(date.today())
    flags = []
    if row["warranty_expiry"] and row["warranty_expiry"] < today_str:
        flags.append("[WARRANTY EXPIRED]")
    if row["next_service_due"] and row["next_service_due"] < today_str:
        flags.append("[SERVICE OVERDUE]")

    header = f"Equipment: {row['make']} {row['model']}"
    if flags:
        header += " " + " ".join(flags)

    service_str = (
        row["last_service_date"] if row["last_service_date"] else "Never serviced"
    )

    lines = [
        header,
        f"Type: {row['equipment_type']} | Status: {row['status']}",
        f"Serial: {row['serial_number']}",
        f"Customer: {row['customer_name']}",
    ]
    if row["location_notes"]:
        lines.append(f"Location: {row['location_notes']}")
    lines.append(f"Installed: {row['install_date']}")
    if row["warranty_expiry"]:
        lines.append(f"Warranty expires: {row['warranty_expiry']}")
    lines.append(f"Last service: {service_str}")
    if row["next_service_due"]:
        lines.append(f"Next service due: {row['next_service_due']}")

    return "\n".join(lines)


def create_work_order(
    customer_id: int,
    title: str,
    description: str,
    priority: str,
    equipment_id: int = None,
) -> str:
    valid_priorities = ("low", "medium", "high", "emergency")
    if priority not in valid_priorities:
        return f"Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}."

    conn = get_db()

    customer = conn.execute(
        "SELECT id, name FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()
    if not customer:
        conn.close()
        return f"Customer {customer_id} not found."

    if equipment_id is not None:
        equip = conn.execute(
            "SELECT id, customer_id FROM equipment WHERE id = ?", (equipment_id,)
        ).fetchone()
        if not equip:
            conn.close()
            return f"Equipment {equipment_id} not found."
        if equip["customer_id"] != customer_id:
            conn.close()
            return (
                f"Equipment {equipment_id} does not belong to customer {customer_id}."
            )

    cursor = conn.execute(
        """INSERT INTO work_orders (customer_id, equipment_id, title, description, priority, status, created_date)
           VALUES (?, ?, ?, ?, ?, 'open', ?)""",
        (customer_id, equipment_id, title, description, priority, str(date.today())),
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    lines = [
        f"Work order created: WO-{new_id:03d}",
        f"Customer: {customer['name']}",
        f"Title: {title}",
        f"Priority: {priority}",
        "Status: open",
        f"Created: {date.today()}",
    ]
    return "\n".join(lines)


def update_work_order(
    work_order_id: int,
    status: str = None,
    priority: str = None,
    technician_id: int = None,
    scheduled_date: str = None,
    diagnosis: str = None,
    resolution: str = None,
    estimated_hours: float = None,
    actual_hours: float = None,
) -> str:
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM work_orders WHERE id = ?", (work_order_id,)
    ).fetchone()

    if not row:
        conn.close()
        return f"Work order {work_order_id} not found."

    if row["status"] == "completed":
        conn.close()
        return "Cannot modify completed work orders. Completed WOs are immutable historical records."

    valid_statuses = ("open", "assigned", "in_progress", "completed", "cancelled")
    if status and status not in valid_statuses:
        conn.close()
        return (
            f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}."
        )

    valid_priorities = ("low", "medium", "high", "emergency")
    if priority and priority not in valid_priorities:
        conn.close()
        return f"Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}."

    updates = {}
    if status is not None:
        updates["status"] = status
    if priority is not None:
        updates["priority"] = priority
    if technician_id is not None:
        updates["technician_id"] = technician_id
    if scheduled_date is not None:
        updates["scheduled_date"] = scheduled_date
    if diagnosis is not None:
        updates["diagnosis"] = diagnosis
    if resolution is not None:
        updates["resolution"] = resolution
    if estimated_hours is not None:
        updates["estimated_hours"] = estimated_hours
    if actual_hours is not None:
        updates["actual_hours"] = actual_hours

    if not updates:
        conn.close()
        return "No fields provided to update."

    if status == "completed":
        updates["completed_date"] = str(date.today())

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values())
    values.append(work_order_id)

    conn.execute(f"UPDATE work_orders SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()

    changes = []
    for field, new_val in updates.items():
        old_val = row[field]
        changes.append(f"  {field}: {old_val} -> {new_val}")

    lines = [f"Updated WO-{work_order_id:03d}:"] + changes
    return "\n".join(lines)


def add_job_note(work_order_id: int, note_type: str, content: str) -> str:
    valid_types = (
        "arrival",
        "diagnosis",
        "update",
        "departure",
        "parts_request",
        "customer_contact",
    )
    if note_type not in valid_types:
        return f"Invalid note type '{note_type}'. Must be one of: {', '.join(valid_types)}."

    conn = get_db()
    row = conn.execute(
        "SELECT id, technician_id FROM work_orders WHERE id = ?", (work_order_id,)
    ).fetchone()

    if not row:
        conn.close()
        return f"Work order {work_order_id} not found."

    technician_id = row["technician_id"]
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn.execute(
        """INSERT INTO job_notes (work_order_id, technician_id, created_at, note_type, content)
           VALUES (?, ?, ?, ?, ?)""",
        (work_order_id, technician_id, created_at, note_type, content),
    )
    conn.commit()
    conn.close()

    return (
        f"Note added to WO-{work_order_id:03d} [{created_at}] ({note_type}) {content}"
    )


if __name__ == "__main__":
    print('Tool: search_work_orders(status="in_progress", customer_name="Eagle")\n')
    print(search_work_orders(status="in_progress", customer_name="Eagle"))
    print()
    print("Tool: get_work_order_details(work_order_id=3)\n")
    print(get_work_order_details(3))
    print()
    print('Tool: get_available_technicians(specialization="refrigeration")\n')
    print(get_available_technicians(specialization="refrigeration"))
    print()
    print('Tool: search_parts(category="hvac")\n')
    print(search_parts(category="hvac"))
    print()
    print("Tool: get_customer_details(customer_id=1)\n")
    print(get_customer_details(1))
    print()
    print("Tool: get_customer_equipment(customer_id=1)\n")
    print(get_customer_equipment(1))
    print()
    print("Tool: get_equipment_details(equipment_id=1)\n")
    print(get_equipment_details(1))
