# Data

9 tables and 222 seed records in SQLite, plus 25 technical knowledge documents embedded in ChromaDB. Raw source files live in `bronze/`, processed outputs in `silver/` — a simple bronze-to-silver data pipeline.

## Database

Entity relationships:

- `customers` → `equipment`, `work_orders`
- `technicians` → `technician_certifications`, `work_orders`, `schedules`, `job_notes`
- `equipment` → `work_orders`
- `work_orders` → `work_order_parts`, `job_notes`, `schedules`
- `parts_inventory` → `work_order_parts`

### customers (20 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| name | TEXT | |
| phone | TEXT | |
| email | TEXT | |
| address | TEXT | |
| suburb | TEXT | Brisbane metro area |
| customer_type | TEXT | e.g. commercial, residential |
| priority | TEXT | |
| contract_start | TEXT | ISO date |
| contract_end | TEXT | ISO date |
| site_notes | TEXT | |

### technicians (10 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| name | TEXT | |
| phone | TEXT | |
| email | TEXT | |
| specializations | TEXT | Trade specialisations |
| service_area | TEXT | Brisbane metro suburb/region |
| status | TEXT | e.g. active, on_leave |
| vehicle | TEXT | |
| hourly_rate | REAL | |

### technician_certifications (28 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| technician_id | INTEGER | FK → technicians.id |
| cert_type | TEXT | ARCtick, blue card, electrical licence, gas fitting, working at heights, confined space |
| licence_number | TEXT | |
| issued_date | TEXT | ISO date |
| expiry_date | TEXT | ISO date |
| issuing_body | TEXT | |

### equipment (28 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| customer_id | INTEGER | FK → customers.id |
| equipment_type | TEXT | HVAC, electrical, plumbing, refrigeration |
| make | TEXT | |
| model | TEXT | |
| serial_number | TEXT | |
| install_date | TEXT | ISO date |
| warranty_expiry | TEXT | ISO date |
| last_service_date | TEXT | ISO date |
| next_service_due | TEXT | ISO date |
| location_notes | TEXT | |
| status | TEXT | e.g. operational, needs_repair |

### work_orders (40 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| customer_id | INTEGER | FK → customers.id |
| equipment_id | INTEGER | FK → equipment.id |
| title | TEXT | |
| description | TEXT | |
| priority | TEXT | e.g. emergency, high, medium, low |
| status | TEXT | e.g. open, in_progress, completed |
| technician_id | INTEGER | FK → technicians.id |
| created_date | TEXT | ISO date |
| scheduled_date | TEXT | ISO date |
| completed_date | TEXT | ISO date, nullable |
| estimated_hours | REAL | |
| actual_hours | REAL | Nullable |
| diagnosis | TEXT | Nullable |
| resolution | TEXT | Nullable |

### job_notes (32 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| work_order_id | INTEGER | FK → work_orders.id |
| technician_id | INTEGER | FK → technicians.id |
| created_at | TEXT | ISO datetime |
| note_type | TEXT | e.g. arrival, diagnosis, update, completion |
| content | TEXT | |

### schedules (26 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| technician_id | INTEGER | FK → technicians.id |
| work_order_id | INTEGER | FK → work_orders.id |
| date | TEXT | ISO date |
| start_time | TEXT | |
| end_time | TEXT | |
| schedule_type | TEXT | |
| notes | TEXT | |

### work_order_parts (16 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| work_order_id | INTEGER | FK → work_orders.id |
| part_id | INTEGER | FK → parts_inventory.id |
| quantity_used | INTEGER | |

### parts_inventory (22 records)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| part_number | TEXT | |
| part_name | TEXT | |
| category | TEXT | |
| quantity | INTEGER | Current stock level |
| minimum_stock | INTEGER | Reorder threshold |
| unit_cost | REAL | |
| supplier | TEXT | |

## Knowledge Base

25 markdown documents embedded via `nomic-embed-text` into ChromaDB. Collection: `knowledge_base`, cosine similarity, 400-character chunks with no overlap. Not yet connected to an agent — standalone infrastructure.

### Documents by category

**Troubleshooting (7)**

| Document | Topic |
|----------|-------|
| hvac_not_cooling.md | Unit running but not cooling |
| hvac_airflow_balancing.md | Airflow and zone balancing |
| hvac_noise_vibration.md | Noise and vibration diagnosis |
| electrical_fault_diagnosis.md | UPS, emergency lighting, and solar faults |
| plumbing_hot_water_systems.md | Hot water system diagnosis |
| plumbing_drainage_grease_traps.md | Drainage and grease trap issues |
| refrigeration_compressor_faults.md | Compressor fault diagnosis |

**Safety (6)**

| Document | Topic |
|----------|-------|
| site_safety_induction.md | Site induction and PPE requirements |
| electrical_lockout_tagout.md | Electrical lockout/tagout (LOTO) procedure |
| gas_leak_emergency_response.md | Emergency gas leak response |
| refrigerant_handling_arctick.md | Refrigerant handling and ARCtick compliance |
| confined_space_entry.md | Confined space entry procedure |
| working_at_heights.md | Working at heights procedure |

**Company (5)**

| Document | Topic |
|----------|-------|
| customer_communication.md | Customer communication standards |
| dispatch_and_escalation.md | Dispatch priorities and escalation procedures |
| job_documentation_standards.md | Job documentation and note type standards |
| vehicle_and_equipment_standards.md | Vehicle and equipment loadout standards |
| warranty_and_compliance.md | Warranty and compliance procedures |

**Maintenance (4)**

| Document | Topic |
|----------|-------|
| hvac_preventive_maintenance.md | HVAC preventive maintenance checklists |
| electrical_preventive_maintenance.md | Electrical preventive maintenance checklists |
| plumbing_preventive_maintenance.md | Plumbing preventive maintenance checklists |
| refrigeration_preventive_maintenance.md | Refrigeration preventive maintenance checklists |

**Standards (3)**

| Document | Topic |
|----------|-------|
| as_hvac_refrigeration_standards.md | Australian HVAC and refrigeration standards reference |
| as_electrical_standards.md | Australian electrical standards reference |
| as_plumbing_gas_standards.md | Australian plumbing and gas standards reference |

## Folder Structure

```
data/
├── bronze/                     # Raw source files
│   ├── records/                # 9 CSV files (database seed data)
│   └── knowledge_base/         # 25 markdown documents
│       ├── troubleshooting/
│       ├── safety/
│       ├── company/
│       ├── maintenance/
│       └── standards/
└── silver/                     # Processed outputs
    ├── database/
    │   └── field_service.db    # SQLite database
    └── vectors/
        └── chroma.sqlite3      # ChromaDB vector store
```
