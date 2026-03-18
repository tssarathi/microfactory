from fastmcp import FastMCP

from src.tools import (
    search_work_orders,
    get_work_order_details,
    get_available_technicians,
    search_parts,
    get_customer_details,
    get_customer_equipment,
    get_equipment_details,
    create_work_order,
    update_work_order,
    add_job_note,
    get_technician_details,
    get_technician_schedule,
    get_technician_certifications,
    check_certification_compliance,
    search_available_slots,
    schedule_job,
    assign_technician,
    update_schedule,
)

mcp = FastMCP("database")

mcp.tool()(search_work_orders)
mcp.tool()(get_work_order_details)
mcp.tool()(get_available_technicians)
mcp.tool()(search_parts)
mcp.tool()(get_customer_details)
mcp.tool()(get_customer_equipment)
mcp.tool()(get_equipment_details)
mcp.tool()(create_work_order)
mcp.tool()(update_work_order)
mcp.tool()(add_job_note)
mcp.tool()(get_technician_details)
mcp.tool()(get_technician_schedule)
mcp.tool()(get_technician_certifications)
mcp.tool()(check_certification_compliance)
mcp.tool()(search_available_slots)
mcp.tool()(schedule_job)
mcp.tool()(assign_technician)
mcp.tool()(update_schedule)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=5001)
