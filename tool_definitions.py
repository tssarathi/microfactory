READ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_work_orders",
            "description": "Search and filter work orders by status, priority, or customer name. Returns a list of matching work orders. Use this to find multiple work orders — not for fetching a single WO by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": [
                            "open",
                            "assigned",
                            "in_progress",
                            "completed",
                            "cancelled",
                        ],
                        "description": "Filter by work order status.",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "emergency"],
                        "description": "Filter by priority level.",
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Filter by customer name (partial match).",
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_work_order_details",
            "description": "Get the full details of a specific work order by its ID, including equipment, technician, job notes, and parts used. Use this when you already know the work order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "work_order_id": {
                        "type": "integer",
                        "description": "The ID of the work order to retrieve.",
                    },
                },
                "required": ["work_order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_available_technicians",
            "description": "Find technicians who are currently available for dispatch. Optionally filter by specialization to match the right skills to the job.",
            "parameters": {
                "type": "object",
                "properties": {
                    "specialization": {
                        "type": "string",
                        "description": "Filter by skill area (e.g. 'hvac', 'electrical', 'plumbing', 'refrigeration').",
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_parts",
            "description": "Search the parts inventory by keyword or category. Returns part numbers, stock levels, pricing, and flags low/out-of-stock items.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Free text search across part names and part numbers.",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["hvac", "refrigeration", "electrical", "plumbing"],
                        "description": "Filter by parts category.",
                    },
                },
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_details",
            "description": "Get the full customer record by ID, including contact info, contract status, priority level, and site notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The ID of the customer to retrieve.",
                    },
                },
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_equipment",
            "description": "List all equipment installed at a customer site, including service history, warranty status, and location notes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The ID of the customer whose equipment to list.",
                    },
                },
                "required": ["customer_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_equipment_details",
            "description": "Get full details for a single piece of equipment by its ID, including warranty expiry, service status, and overdue flags.",
            "parameters": {
                "type": "object",
                "properties": {
                    "equipment_id": {
                        "type": "integer",
                        "description": "The ID of the equipment to retrieve.",
                    },
                },
                "required": ["equipment_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search technical manuals, troubleshooting procedures, safety protocols, and company documentation. Use this when the user asks HOW to do something, asks about procedures, safety requirements, maintenance schedules, or best practices. This searches real company documentation, not general knowledge.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for (e.g., 'AC troubleshooting steps', 'lockout tagout procedure', 'gas leak response')",
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return (default 3)",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

WRITE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_work_order",
            "description": "Create a new work order in the database for a customer. This inserts a new record with status 'open'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The customer this work order is for.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Short title summarising the job.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue or work required.",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "emergency"],
                        "description": "Priority level for the work order.",
                    },
                    "equipment_id": {
                        "type": "integer",
                        "description": "Optional. The ID of the equipment this work order relates to.",
                    },
                },
                "required": ["customer_id", "title", "description", "priority"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_work_order",
            "description": "Modify an existing work order. Use this to change status, reassign a technician, set a scheduled date, record diagnosis/resolution, or log hours.",
            "parameters": {
                "type": "object",
                "properties": {
                    "work_order_id": {
                        "type": "integer",
                        "description": "The ID of the work order to update.",
                    },
                    "status": {
                        "type": "string",
                        "enum": [
                            "open",
                            "assigned",
                            "in_progress",
                            "completed",
                            "cancelled",
                        ],
                        "description": "New status for the work order.",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "emergency"],
                        "description": "New priority level.",
                    },
                    "technician_id": {
                        "type": "integer",
                        "description": "ID of the technician to assign.",
                    },
                    "scheduled_date": {
                        "type": "string",
                        "description": "Date to schedule the job (YYYY-MM-DD).",
                    },
                    "diagnosis": {
                        "type": "string",
                        "description": "Technician's diagnosis of the issue.",
                    },
                    "resolution": {
                        "type": "string",
                        "description": "How the issue was resolved.",
                    },
                    "estimated_hours": {
                        "type": "number",
                        "description": "Estimated hours to complete the job.",
                    },
                    "actual_hours": {
                        "type": "number",
                        "description": "Actual hours spent on the job.",
                    },
                },
                "required": ["work_order_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_job_note",
            "description": "Add a timestamped note to a work order. Use this to log arrival, diagnosis, updates, departure, parts requests, or customer contact.",
            "parameters": {
                "type": "object",
                "properties": {
                    "work_order_id": {
                        "type": "integer",
                        "description": "The ID of the work order to add the note to.",
                    },
                    "note_type": {
                        "type": "string",
                        "enum": [
                            "arrival",
                            "diagnosis",
                            "update",
                            "departure",
                            "parts_request",
                            "customer_contact",
                        ],
                        "description": "The type of note being added.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The note content.",
                    },
                },
                "required": ["work_order_id", "note_type", "content"],
                "additionalProperties": False,
            },
        },
    },
]
