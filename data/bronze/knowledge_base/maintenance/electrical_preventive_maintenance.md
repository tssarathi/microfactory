# The Good Trades Co. — Electrical Preventive Maintenance Schedule

Preventive maintenance checklists for UPS systems, emergency lighting, and solar installations. All electrical work requires a current electrical licence verified with QBCC. Lockout/tagout (LOTO) procedures must be followed per AS/NZS 4836:2011 before working on any electrical equipment.

## UPS Preventive Maintenance

### Quarterly UPS Checklist

Complete every 3 months. Allow 1 hour per unit.

- [ ] Visual inspection of UPS cabinet. Check for warning indicators, unusual odours (overheating), or audible alarms.
- [ ] Clean or replace intake filters. Dust accumulation reduces cooling airflow and shortens component life.
- [ ] Inspect battery terminals for corrosion, swelling, or electrolyte leakage. Clean terminals with appropriate battery terminal cleaner if corrosion is present.
- [ ] Review UPS event log. Download or photograph the last 90 days of events. Note any transfer events, overload warnings, or battery discharge events. Report anomalies to the customer.

### Annual UPS Checklist

Complete every 12 months. Includes all quarterly items plus. Allow 3-4 hours per unit.

- [ ] Full battery string test. Measure and record for every cell:
  - Individual cell voltage (acceptable range: 13.2-13.4V per 12V block — ref. WO-16).
  - Specific gravity (acceptable range: 1.260-1.280 — ref. WO-16 measured 1.265-1.275).
  - Internal resistance. Compare to manufacturer baseline. Cells exceeding 25% above baseline indicate end-of-life approaching — flag for monitoring.
- [ ] Transfer test. Simulate mains failure and measure switchover time. Must be less than 10ms (ref. WO-16 — measured 6ms, within spec). Record exact switchover time.
- [ ] Input/output power measurement. Measure voltage, current, and power factor on input and output. Confirm within 2% of rated values (ref. WO-16).
- [ ] Torque-check all bus bar connections to 25Nm (ref. WO-16 resolution — all bus bars torqued to 25Nm).
- [ ] Clean fan assemblies and internal components. Use compressed air or vacuum. Do not use liquid cleaners inside the cabinet.
- [ ] Review firmware version. Check against manufacturer release notes for updates. Record current version in service report.
- [ ] Battery life estimation. Based on cell test results and age, estimate remaining battery life. Recommend replacement timeline to customer (ref. WO-16 — estimated 18 months remaining life, battery replacement recommended Q3 2027).

**Battery replacement cycle:** VRLA batteries typically last 3-5 years. Monitor internal resistance trend at each annual service. Plan replacement when any cell exceeds 30% above baseline internal resistance or when estimated remaining life falls below 12 months.

### Equipment-Specific: Eaton UPS 20kVA

- Battery configuration: 40 cells in series string. All cells must be tested individually during annual service.
- Transfer test procedure: use the front-panel test function or simulate mains failure at the upstream isolator. Confirm UPS transfers to battery and back without interruption to the load.
- Firmware: check current version on the LCD display under System > Information. Current known version: v3.2. Contact Eaton support for update files if a newer version is available.

### Equipment-Specific: Eaton 93PM 30kW

- Modular design allows hot-swap of power modules. During annual service, visually inspect module connections and locking mechanisms.
- Battery configuration may differ from 20kVA model. Confirm string configuration from the installation manual on-site before commencing cell testing.
- Internal bypass: verify automatic bypass operates correctly during transfer test. Monitor output voltage on an oscilloscope or power quality analyser during transfer to confirm clean switchover.

## Emergency Lighting Preventive Maintenance

Testing requirements per AS/NZS 2293.2 — Emergency escape lighting and exit signs.

### Monthly Function Test

- [ ] Simulate mains failure (press test button or switch off supply at the distribution board for the emergency lighting circuit).
- [ ] Confirm all emergency and exit lamps illuminate within 2 seconds of mains loss.
- [ ] Record any lamps that fail to illuminate or show dim output. Replace batteries or fittings as needed.
- [ ] Duration: brief test only — restore mains after confirming all lamps light. No duration measurement required at monthly interval.

### Six-Monthly Duration Test (Sample — 25% of Fittings)

- [ ] Select 25% of all emergency lighting fittings for 90-minute discharge test.
- [ ] Rotate the sample group so that all fittings are tested over a 2-year cycle.
- [ ] Disconnect mains supply to selected fittings and time the illumination duration.
- [ ] Any fitting achieving less than 90 minutes = fail. Replace battery immediately.
- [ ] Record results in the emergency lighting test register.

### Annual Full Discharge Test (ALL Fittings)

- [ ] Discharge test ALL emergency lighting fittings for the full 90-minute duration.
- [ ] Record start time, end time, and pass/fail for each fitting.
- [ ] Replace battery packs in any fitting that fails to maintain illumination for 90 minutes.
- [ ] Update the emergency lighting test register with all results.
- [ ] Issue compliance certificate to the building owner or facility manager.
- [ ] Identify fittings approaching end of battery life (achieving 90-95 minutes) and recommend proactive replacement.

**Battery replacement cycle:** NiCd/NiMH battery packs typically last 3-5 years. Track install date for each fitting. Plan bulk replacement programmes to avoid piecemeal failures (ref. WO-18 — recommended bulk replacement for remaining units in 2027).

### Equipment-Specific: Legrand Emergency Lighting Pack

- Battery part number: 6901 20 (NiCd pack). Keep spares on van for emergency replacements.
- Test button location: on the front face of the fitting. Press and hold for 3 seconds to initiate manual discharge test.
- Battery replacement procedure: isolate supply at the distribution board, remove fitting cover (2 screws), disconnect old battery pack (spade connectors), connect new pack, refit cover, restore supply. Confirm lamp illuminates on test within 24 hours of replacement (allows initial charge).
- Ref. WO-18: six units replaced (corridors 2, 4, 7; stairwells B, D; reception). Original 2022 install batteries reached 4 years — within expected 3-5 year life. Post-replacement discharge test: all achieving 105-115 minutes.

## Solar System Preventive Maintenance

### Annual Solar Checklist

- [ ] Visual panel inspection. Check for cracking, delamination, hot spots (discolouration), and junction box seal integrity. Inspect mounting rails and clamps for corrosion or loosening.
- [ ] DC connector check. Inspect all MC4 or equivalent connectors for oxidation, heat damage, or looseness. Re-torque if manufacturer torque specification is available. Replace connectors showing oxidation (ref. WO-37 — oxidised DC connector replaced on String 2).
- [ ] String insulation resistance test. Test each string to ground using insulation resistance tester at 1000V DC. Pass threshold: greater than 1 MOhm per string. Fail requires investigation — isolate affected string and inspect panel junction boxes for moisture ingress (ref. WO-37 — String 2 measured 0.3 MOhm, traced to moisture ingress at panel junction box).
- [ ] Review inverter event log. Download or photograph event history. Note any error codes, grid disconnection events, or power derating. Common Fronius state code: 509 = insulation resistance fault.
- [ ] Generation data review. Compare kWh generation for the past 12 months against the previous year. Decline exceeding 5% (weather-adjusted) warrants investigation. Check for new shading sources (tree growth, new construction).

**Panel cleaning:** Clean only when soiling is visually evident (bird droppings, heavy pollen, dust buildup). Use deionised water and a soft brush or squeegee only. Do not use detergents, abrasive pads, or high-pressure water. Clean early morning or late afternoon when panels are cool to avoid thermal shock.

### Equipment-Specific: Fronius Symo 15.0

- State codes: 509 (insulation fault — check string insulation), 306 (grid voltage out of range), 307 (grid frequency out of range). Consult Fronius state code reference for full list.
- Monitoring: verify WiFi or LAN connection to Fronius Solar.web portal. Confirm data is uploading. Reset datalogger connection if portal shows data gaps.
- String configuration: confirm number of strings and panels per string matches the installation record. Any changes to string configuration require recalculation of inverter MPPT settings.
- Warranty: standard 5-year warranty, extendable to 10 years. For warranty claims, contact Fronius with model, serial number, and fault description. Reference format: FRO-WAR-YYYY-XXXX (ref. WO-37).

## Reporting Requirements

All electrical maintenance reports from The Good Trades Co. must include:

1. Test results for every item on the applicable checklist.
2. Pass/fail status clearly stated for compliance-related tests (emergency lighting duration, insulation resistance, transfer time).
3. Compliance certificates issued where required (emergency lighting per AS/NZS 2293.2, electrical work per AS 3000:2018).
4. Battery condition summary with estimated remaining life for UPS and emergency lighting.
5. Recommendations and suggested follow-up timing.

Submit reports to the customer within 3 business days of the service visit.

Related completed work orders for reference: WO-5, WO-7, WO-16, WO-18, WO-33, WO-37.
