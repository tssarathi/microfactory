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

if __name__ == "__main__":
    mcp.run(transport="stdio")
