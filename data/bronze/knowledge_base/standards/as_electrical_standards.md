# The Good Trades Co. — Australian Electrical Standards Quick Reference

**For field use only. Not a substitute for the full standard.**
**Queensland | Updated March 2026**

---

## AS/NZS 4836:2011 — Safe Working on or Near Low-Voltage Electrical Installations

**Scope:** All electrical work on installations operating below 1000V AC or 1500V DC.

### Key Requirements

- **Risk assessment** must be completed before any electrical work begins. Document the hazards, controls, and residual risk.
- **Isolation and LOTO (Lock Out / Tag Out):**
  - Identify all sources of supply.
  - Isolate at the point of supply.
  - Apply personal lock and danger tag. Each worker applies their own — no sharing.
  - Prove dead at the point of work before touching anything.
- **Testing for dead:**
  - Use a voltage tester rated to the correct CAT rating for the location.
  - Test the tester on a known live source BEFORE and AFTER proving dead (prove-test-prove method).
- **Test instrument CAT ratings:**
  - CAT III — distribution boards, sub-mains.
  - CAT IV — main switchboard, point of supply, metering.
  - Never use a CAT II instrument at a switchboard. It is not rated for the fault energy present.
- **Live work** is only permitted when de-energisation would create a greater risk. Requires a specific risk assessment and authorisation.

---

## AS/NZS 3000:2018 — Wiring Rules

**Scope:** Design, construction, and verification of electrical installations in Australia and New Zealand.

### Key Field Service Requirements

- **Circuit identification:** Every circuit must be labelled at the switchboard. Labels must match what the circuit actually feeds — verify during service.
- **Cable sizing:** Determined by current-carrying capacity, voltage drop (max 5% from point of supply to final subcircuit), and fault loop impedance. Refer to Tables in Section 3 for derating factors (grouping, ambient temperature, thermal insulation).
- **Earthing and bonding:**
  - MEN (Multiple Earthed Neutral) system is standard in QLD.
  - Main earth conductor connects the main neutral bar to the main earthing terminal.
  - All exposed conductive parts must be bonded to earth.
  - Earth electrode resistance: aim for <10 ohms; maximum acceptable depends on fault loop impedance.
- **RCD requirements (Clause 2.6):**
  - 30mA RCDs mandatory for: all socket outlets up to 20A, lighting circuits in domestic, circuits supplying outdoor equipment.
  - RCDs must be tested by the user via the push-button every 3 months. Test and tag at service intervals.
- **Maximum demand:** Calculate per AS/NZS 3000 Section 2 — needed when adding circuits or assessing capacity for new loads.

---

## AS/NZS 2293.2 — Emergency Escape Lighting — Inspection and Maintenance

### Testing Schedule

| Frequency | Test | Duration | Scope |
|-----------|------|----------|-------|
| Monthly | Function test | Brief switch to battery | All fittings — confirm they illuminate |
| 6-monthly | Sample discharge | 90 minutes | 25% of fittings (rotating sample) |
| Annual | Full discharge | 90 minutes | ALL fittings simultaneously |

### Documentation

- **Test register** must record: date, tester name, fitting ID/location, test type, result (pass/fail), and any corrective action.
- **Compliance certificate** required after installation or alteration. Issued to the building owner/manager.

### Failure Criteria

- Any fitting that does not maintain illumination for the full **90 minutes** during discharge = **FAIL**.
- Failed fitting = replace the battery (or the fitting if the battery is non-replaceable).
- Re-test the individual fitting after battery replacement to confirm 90-minute hold.

---

## AS/NZS 4777.2 — Grid Connection of Energy Systems via Inverters (Solar)

### Key Service Checks

- **Anti-islanding verification:** The inverter must disconnect from the grid within 2 seconds of grid supply loss. Confirm anti-islanding protection is enabled and functional during commissioning and service.
- **Power quality:** Inverter output must comply with voltage and frequency limits. If the grid voltage at the point of connection is out of range, the inverter must trip — do not adjust protection settings without network approval.
- **Insulation resistance testing:** Minimum **1 megohm per string** (DC side), measured between positive and earth, then negative and earth. Values below 1 megohm indicate insulation breakdown — investigate before re-energising.
- **Shutdown procedure for service:** DC isolator at array first, then AC isolator at inverter, then AC isolator at switchboard. Reverse order for re-energisation.
