import sqlite3
import json
from datetime import date, datetime, timedelta
from typing import Annotated, Literal
from pathlib import Path
import os

_default_db = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "silver"
    / "database"
    / "field_service.db"
)
DB_PATH = Path(os.getenv("DB_PATH", str(_default_db)))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def search_work_orders(
    status: Annotated[
        Literal["open", "assigned", "in_progress", "completed", "cancelled"] | None,
        "Filter by work order status.",
    ] = None,
    priority: Annotated[
        Literal["low", "medium", "high", "emergency"] | None,
        "Filter by priority level.",
    ] = None,
    customer_name: Annotated[
        str | None,
        "Filter by customer name (partial match).",
    ] = None,
) -> str:
    """Search and filter work orders by status, priority, or customer name.
    Returns a list of matching work orders.
    Use this to find multiple work orders — not for fetching a single WO by ID."""

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


def get_work_order_details(
    work_order_id: Annotated[int, "The ID of the work order to retrieve."],
) -> str:
    """Get the full details of a specific work order by its ID,
    including equipment, technician, job notes, and parts used.
    Use this when you already know the work order ID."""

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


def get_available_technicians(
    specialization: Annotated[
        str | None,
        "Filter by skill area (e.g. 'hvac', 'electrical', 'plumbing', 'refrigeration').",
    ] = None,
) -> str:
    """Find technicians who are currently available for dispatch.
    Optionally filter by specialization to match the right skills to the job."""

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


def search_parts(
    query: Annotated[
        str | None,
        "Free text search across part names and part numbers.",
    ] = None,
    category: Annotated[
        Literal["hvac", "refrigeration", "electrical", "plumbing"] | None,
        "Filter by parts category.",
    ] = None,
) -> str:
    """Search the parts inventory by keyword or category.
    Returns part numbers, stock levels, pricing, and flags low/out-of-stock items."""

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


def get_customer_details(
    customer_id: Annotated[int, "The ID of the customer to retrieve."],
) -> str:
    """Get the full customer record by ID,
    including contact info, contract status, priority level, and site notes."""

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


def get_customer_equipment(
    customer_id: Annotated[int, "The ID of the customer whose equipment to list."],
) -> str:
    """List all equipment installed at a customer site,
    including service history, warranty status, and location notes."""

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


def get_equipment_details(
    equipment_id: Annotated[int, "The ID of the equipment to retrieve."],
) -> str:
    """Get full details for a single piece of equipment by its ID,
    including warranty expiry, service status, and overdue flags."""

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


def get_technician_details(
    technician_id: Annotated[int, "The ID of the technician to retrieve."],
) -> str:
    """Get the full profile of a technician by ID,
    including specializations, service area, status, and hourly rate."""

    conn = get_db()
    row = conn.execute(
        "SELECT * FROM technicians WHERE id = ?", (technician_id,)
    ).fetchone()
    conn.close()

    if not row:
        return f"Technician {technician_id} not found."

    specs = ", ".join(json.loads(row["specializations"]))

    lines = [
        f"Technician: {row['name']}",
        f"Phone: {row['phone']}",
        f"Email: {row['email']}",
        f"Specializations: {specs}",
        f"Service area: {row['service_area']}",
        f"Status: {row['status']}",
        f"Hourly rate: ${row['hourly_rate']:.2f}",
    ]

    return "\n".join(lines)


def get_technician_schedule(
    technician_id: Annotated[int, "The ID of the technician."],
    start_date: Annotated[str, "Start date in YYYY-MM-DD format."],
    end_date: Annotated[str, "End date in YYYY-MM-DD format."],
) -> str:
    """Get a technician's schedule entries within a date range.
    Shows time blocks, schedule type, linked work orders, and notes."""

    conn = get_db()

    tech = conn.execute(
        "SELECT name FROM technicians WHERE id = ?", (technician_id,)
    ).fetchone()
    if not tech:
        conn.close()
        return f"Technician {technician_id} not found."

    rows = conn.execute(
        """SELECT s.*, wo.title as wo_title
           FROM schedules s
           LEFT JOIN work_orders wo ON s.work_order_id = wo.id
           WHERE s.technician_id = ? AND s.date BETWEEN ? AND ?
           ORDER BY s.date, s.start_time""",
        (technician_id, start_date, end_date),
    ).fetchall()
    conn.close()

    if not rows:
        return f"No schedule entries for {tech['name']} between {start_date} and {end_date}."

    lines = [f"Schedule for {tech['name']} ({start_date} to {end_date}):"]
    for row in rows:
        parts = [f"  {row['date']}"]
        if row["start_time"] and row["end_time"]:
            parts.append(f"{row['start_time']}-{row['end_time']}")
        parts.append(f"({row['schedule_type']})")
        if row["wo_title"]:
            parts.append(f"WO: {row['wo_title']}")
        if row["notes"]:
            parts.append(f"— {row['notes']}")
        lines.append(" | ".join(parts))

    return "\n".join(lines)


def get_technician_certifications(
    technician_id: Annotated[int, "The ID of the technician."],
) -> str:
    """List all certifications held by a technician,
    with expiry dates and flags for expired or soon-to-expire certs."""

    conn = get_db()

    tech = conn.execute(
        "SELECT name FROM technicians WHERE id = ?", (technician_id,)
    ).fetchone()
    if not tech:
        conn.close()
        return f"Technician {technician_id} not found."

    rows = conn.execute(
        """SELECT * FROM technician_certifications
           WHERE technician_id = ?
           ORDER BY cert_type""",
        (technician_id,),
    ).fetchall()
    conn.close()

    if not rows:
        return f"No certifications on record for {tech['name']}."

    today_str = str(date.today())
    thirty_days_str = str(date.today() + timedelta(days=30))

    lines = [f"Certifications for {tech['name']}:"]
    for row in rows:
        flags = []
        if row["expiry_date"] < today_str:
            flags.append("[EXPIRED]")
        elif row["expiry_date"] <= thirty_days_str:
            flags.append("[EXPIRING SOON]")

        flag_str = " ".join(flags) + " " if flags else ""
        lines.append(
            f"  {flag_str}{row['cert_type']} | #{row['licence_number']} | "
            f"Issued: {row['issued_date']} | Expires: {row['expiry_date']}"
        )

    return "\n".join(lines)


def check_certification_compliance(
    technician_id: Annotated[int, "The ID of the technician to check."],
    work_order_id: Annotated[int, "The ID of the work order to check against."],
) -> str:
    """Check if a technician holds all certifications required for a work order.
    Determines required certs from equipment type and customer site notes.
    Returns COMPLIANT or NON-COMPLIANT with details."""

    conn = get_db()

    tech = conn.execute(
        "SELECT name FROM technicians WHERE id = ?", (technician_id,)
    ).fetchone()
    if not tech:
        conn.close()
        return f"Technician {technician_id} not found."

    wo = conn.execute(
        """SELECT wo.*, c.site_notes, e.equipment_type
           FROM work_orders wo
           JOIN customers c ON wo.customer_id = c.id
           LEFT JOIN equipment e ON wo.equipment_id = e.id
           WHERE wo.id = ?""",
        (work_order_id,),
    ).fetchone()
    if not wo:
        conn.close()
        return f"Work order {work_order_id} not found."

    # Determine required certifications
    required = {}
    equipment_type = (wo["equipment_type"] or "").lower()
    site_notes = (wo["site_notes"] or "").lower()
    description = (wo["description"] or "").lower()
    title = (wo["title"] or "").lower()
    combined_text = f"{description} {title} {site_notes}"

    if equipment_type in ("refrigeration", "cold_storage"):
        required["arctick"] = f"equipment type is {equipment_type}"
    if "blue card" in site_notes:
        required["blue_card"] = "customer site requires blue card"
    if equipment_type == "electrical":
        required["electrical_licence"] = f"equipment type is {equipment_type}"
    if equipment_type in ("gas", "gas_fitting"):
        required["gas_fitting"] = f"equipment type is {equipment_type}"
    if any(kw in combined_text for kw in ("roof", "elevated", "height")):
        required["working_at_heights"] = "work involves heights"
    if any(kw in combined_text for kw in ("confined", "tank", "pit")):
        required["confined_space"] = "work involves confined space"

    if not required:
        conn.close()
        return (
            f"COMPLIANT — No specific certifications required for WO-{work_order_id:03d}. "
            f"{tech['name']} can proceed."
        )

    # Check tech's certs
    certs = conn.execute(
        """SELECT cert_type, expiry_date FROM technician_certifications
           WHERE technician_id = ?""",
        (technician_id,),
    ).fetchall()
    conn.close()

    today_str = str(date.today())
    cert_map = {c["cert_type"]: c["expiry_date"] for c in certs}

    results = []
    all_pass = True
    for cert_type, reason in required.items():
        expiry = cert_map.get(cert_type)
        if not expiry:
            results.append(f"  MISSING: {cert_type} — required because {reason}")
            all_pass = False
        elif expiry < today_str:
            results.append(
                f"  EXPIRED: {cert_type} (expired {expiry}) — required because {reason}"
            )
            all_pass = False
        else:
            results.append(f"  VALID: {cert_type} (expires {expiry})")

    header = "COMPLIANT" if all_pass else "NON-COMPLIANT"
    lines = [
        f"{header} — {tech['name']} for WO-{work_order_id:03d}:",
        *results,
    ]

    if not all_pass:
        lines.append(
            f"\n  Recommendation: Do not assign {tech['name']} to this work order. "
            f"Find an alternative technician with valid certifications."
        )

    return "\n".join(lines)


def search_available_slots(
    target_date: Annotated[str, "Date to search in YYYY-MM-DD format."],
    specialization: Annotated[
        str | None,
        "Filter by skill area (e.g. 'hvac', 'electrical').",
    ] = None,
    min_hours: Annotated[
        int,
        "Minimum free hours required in the slot.",
    ] = 2,
) -> str:
    """Find technicians with free time blocks on a given date.
    Excludes techs on leave. Optionally filters by specialization."""

    conn = get_db()

    techs = conn.execute(
        "SELECT * FROM technicians WHERE status != 'on_leave'"
    ).fetchall()

    if specialization:
        techs = [
            t
            for t in techs
            if specialization.lower() in json.loads(t["specializations"])
        ]

    if not techs:
        conn.close()
        spec_msg = f" with specialization '{specialization}'" if specialization else ""
        return f"No technicians found{spec_msg}."

    results = []
    for tech in techs:
        # Check if tech has leave on this date
        leave = conn.execute(
            """SELECT 1 FROM schedules
               WHERE technician_id = ? AND date = ? AND schedule_type = 'leave'""",
            (tech["id"], target_date),
        ).fetchone()
        if leave:
            continue

        # Get scheduled blocks for this date
        blocks = conn.execute(
            """SELECT start_time, end_time FROM schedules
               WHERE technician_id = ? AND date = ?
               AND schedule_type != 'leave'
               ORDER BY start_time""",
            (tech["id"], target_date),
        ).fetchall()

        # Calculate gaps in a 07:00-18:00 workday
        workday_start = 7
        workday_end = 18
        free_slots = []
        current = workday_start

        for block in blocks:
            block_start = int(block["start_time"].split(":")[0])
            block_end = int(block["end_time"].split(":")[0])
            if block_start > current:
                gap = block_start - current
                if gap >= min_hours:
                    free_slots.append(f"{current:02d}:00-{block_start:02d}:00 ({gap}h)")
            current = max(current, block_end)

        if current < workday_end:
            gap = workday_end - current
            if gap >= min_hours:
                free_slots.append(f"{current:02d}:00-{workday_end:02d}:00 ({gap}h)")

        if free_slots:
            specs = ", ".join(json.loads(tech["specializations"]))
            slots_str = ", ".join(free_slots)
            results.append(
                f"{tech['name']} | {specs} | {tech['service_area']} | "
                f"Available: {slots_str}"
            )

    conn.close()

    if not results:
        return f"No technicians with {min_hours}+ hour free slots on {target_date}."

    lines = [f"Available slots on {target_date} (min {min_hours}h):"] + results
    return "\n".join(lines)


def create_work_order(
    customer_id: Annotated[int, "The ID of the customer to create the work order for."],
    title: Annotated[str, "Short title describing the job."],
    description: Annotated[str, "Detailed description of the work to be done."],
    priority: Annotated[
        Literal["low", "medium", "high", "emergency"],
        "Priority level for the work order.",
    ],
    equipment_id: Annotated[
        int | None,
        "Optional equipment ID to associate with the work order. Must belong to the specified customer.",
    ] = None,
) -> str:
    """Create a new work order for a customer.
    Validates the customer and equipment exist, then creates the order with 'open' status."""
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
    work_order_id: Annotated[int, "The ID of the work order to update."],
    status: Annotated[
        Literal["open", "assigned", "in_progress", "completed", "cancelled"] | None,
        "New status for the work order.",
    ] = None,
    priority: Annotated[
        Literal["low", "medium", "high", "emergency"] | None,
        "New priority level.",
    ] = None,
    technician_id: Annotated[int | None, "ID of the technician to assign."] = None,
    scheduled_date: Annotated[
        str | None, "Scheduled date in YYYY-MM-DD format."
    ] = None,
    diagnosis: Annotated[str | None, "Technician's diagnosis of the issue."] = None,
    resolution: Annotated[
        str | None, "Description of how the issue was resolved."
    ] = None,
    estimated_hours: Annotated[
        float | None, "Estimated hours to complete the job."
    ] = None,
    actual_hours: Annotated[float | None, "Actual hours spent on the job."] = None,
) -> str:
    """Update fields on an existing work order.
    Completed work orders cannot be modified. Setting status to 'completed' auto-fills the completed date."""
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


def add_job_note(
    work_order_id: Annotated[int, "The ID of the work order to add the note to."],
    note_type: Annotated[
        Literal[
            "arrival",
            "diagnosis",
            "update",
            "departure",
            "parts_request",
            "customer_contact",
        ],
        "The type of job note.",
    ],
    content: Annotated[str, "The note content."],
) -> str:
    """Add a timestamped job note to a work order.
    The note is automatically associated with the work order's assigned technician."""
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


def schedule_job(
    technician_id: Annotated[int, "The ID of the technician."],
    work_order_id: Annotated[int, "The ID of the work order."],
    scheduled_date: Annotated[str, "Date in YYYY-MM-DD format."],
    start_time: Annotated[str, "Start time in HH:MM format."],
    end_time: Annotated[str, "End time in HH:MM format."],
    notes: Annotated[str | None, "Optional notes for the schedule entry."] = None,
) -> str:
    """Create a schedule entry linking a technician to a work order on a specific date and time.
    Sets schedule_type to 'job'. Validates tech and WO exist. Checks for time conflicts."""

    conn = get_db()

    tech = conn.execute(
        "SELECT name FROM technicians WHERE id = ?", (technician_id,)
    ).fetchone()
    if not tech:
        conn.close()
        return f"Technician {technician_id} not found."

    wo = conn.execute(
        "SELECT id, title FROM work_orders WHERE id = ?", (work_order_id,)
    ).fetchone()
    if not wo:
        conn.close()
        return f"Work order {work_order_id} not found."

    # Check for time conflicts
    conflict = conn.execute(
        """SELECT * FROM schedules
           WHERE technician_id = ? AND date = ?
           AND start_time < ? AND end_time > ?""",
        (technician_id, scheduled_date, end_time, start_time),
    ).fetchone()
    if conflict:
        conn.close()
        return (
            f"Scheduling conflict: {tech['name']} already has "
            f"{conflict['schedule_type']} scheduled {conflict['start_time']}-{conflict['end_time']} "
            f"on {scheduled_date}."
        )

    conn.execute(
        """INSERT INTO schedules (technician_id, work_order_id, date, start_time, end_time,
           schedule_type, notes)
           VALUES (?, ?, ?, ?, ?, 'job', ?)""",
        (technician_id, work_order_id, scheduled_date, start_time, end_time, notes),
    )
    conn.commit()
    conn.close()

    return (
        f"Scheduled {tech['name']} for WO-{work_order_id:03d} on {scheduled_date} "
        f"{start_time}-{end_time}."
    )


def assign_technician(
    work_order_id: Annotated[int, "The ID of the work order."],
    technician_id: Annotated[int, "The ID of the technician to assign."],
) -> str:
    """Assign a technician to a work order by updating the technician_id field.
    Does NOT validate certifications — the agent must check compliance before calling this."""

    conn = get_db()

    wo = conn.execute(
        "SELECT id, title, status FROM work_orders WHERE id = ?", (work_order_id,)
    ).fetchone()
    if not wo:
        conn.close()
        return f"Work order {work_order_id} not found."

    if wo["status"] == "completed":
        conn.close()
        return "Cannot modify completed work orders."

    tech = conn.execute(
        "SELECT name FROM technicians WHERE id = ?", (technician_id,)
    ).fetchone()
    if not tech:
        conn.close()
        return f"Technician {technician_id} not found."

    conn.execute(
        "UPDATE work_orders SET technician_id = ?, status = 'assigned' WHERE id = ?",
        (technician_id, work_order_id),
    )
    conn.commit()
    conn.close()

    return (
        f"Assigned {tech['name']} to WO-{work_order_id:03d} ({wo['title']}). "
        f"Status updated to 'assigned'."
    )


def update_schedule(
    schedule_id: Annotated[int, "The ID of the schedule entry to update."],
    scheduled_date: Annotated[str | None, "New date in YYYY-MM-DD format."] = None,
    start_time: Annotated[str | None, "New start time in HH:MM format."] = None,
    end_time: Annotated[str | None, "New end time in HH:MM format."] = None,
    notes: Annotated[str | None, "Updated notes."] = None,
) -> str:
    """Update an existing schedule entry. Only provided fields are modified."""

    conn = get_db()

    row = conn.execute(
        "SELECT * FROM schedules WHERE id = ?", (schedule_id,)
    ).fetchone()
    if not row:
        conn.close()
        return f"Schedule entry {schedule_id} not found."

    updates = {}
    if scheduled_date is not None:
        updates["date"] = scheduled_date
    if start_time is not None:
        updates["start_time"] = start_time
    if end_time is not None:
        updates["end_time"] = end_time
    if notes is not None:
        updates["notes"] = notes

    if not updates:
        conn.close()
        return "No fields provided to update."

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values())
    values.append(schedule_id)

    conn.execute(f"UPDATE schedules SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()

    changes = [f"  {k}: {row[k]} -> {v}" for k, v in updates.items()]
    lines = [f"Updated schedule entry {schedule_id}:"] + changes
    return "\n".join(lines)
