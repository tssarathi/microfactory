# The Good Trades Co. — Electrical Troubleshooting: UPS, Emergency Lighting, and Solar

## Safety Precautions

- **LOTO mandatory.** Isolate and lock out all electrical supplies before working on any electrical equipment per AS/NZS 4836:2011. Follow The Good Trades Co. LOTO procedure.
- Use only **CAT III or CAT IV rated** test equipment for all measurements. CAT III for distribution-level work, CAT IV for origin/supply-level work.
- **Verify your voltage tester** on a known live source before and after testing a circuit believed to be dead. A tester that gives a false reading can kill.
- Never work alone on high-energy systems (UPS, switchboards). A second person must be present and aware of the rescue procedure.
- **UPS systems remain live** even when mains power is isolated — the battery provides a secondary energy source. Both mains and battery must be isolated before working inside a UPS.
- Wear insulated gloves and safety glasses when working on battery systems. Battery acid is corrosive and batteries can produce hydrogen gas in confined spaces.

## UPS Fault Diagnosis

Core scenarios include WO-7 (UPS battery replacement — Eaton) and WO-5 (emergency lighting quarterly test and remediation — Legrand).

### Battery Testing

1. **Cell voltage:** Measure individual cell voltages across the battery string. All cells should read within the manufacturer's specified range. WO-16 (Eaton UPS 20kVA) measured cells at 13.2-13.4V — acceptable. Any cell more than 0.5V below the string average is failing.
2. **Specific gravity:** For flooded lead-acid batteries, measure specific gravity with a hydrometer. Normal range is 1.260-1.280. WO-16 measured 1.265-1.275 — nominal.
3. **Internal resistance:** Measure with a battery analyser. Compare to manufacturer baseline. Internal resistance increasing by more than 25% from baseline indicates end-of-life approaching. WO-16 noted estimated remaining battery life of 18 months — budget for replacement.
4. **Visual inspection:** Check for swelling, leaking, corrosion on terminals, or white residue (sulphation). Any of these require immediate battery replacement.

### Transfer Test

1. Simulate a mains power failure by operating the UPS input breaker (with customer approval and after notifying all affected parties).
2. Measure the transfer time — the gap between mains loss and UPS output stabilising. Must be **less than 10 ms** for critical loads. WO-16 recorded 6 ms — within spec.
3. Verify the UPS output voltage and frequency remain within specification during and after transfer.
4. Test return transfer when mains is restored.

### Eaton UPS 20kVA / 93PM 30kW

- **Error codes:** Eaton UPS units display fault codes on the front panel LCD. Common codes include battery fault, overload, over-temperature, and bypass active. Record the error code number and description before clearing.
- **Battery string configuration:** The Eaton UPS 20kVA uses a series string of VRLA batteries. When replacing, all batteries in the string must be replaced simultaneously — never mix old and new batteries.
- **Intake filter cleaning:** Dust accumulation on intake filters causes over-temperature faults. Clean filters at quarterly service. WO-16 found minor dust accumulation on intake filters — cleaned during annual service.
- **Bus bar torque:** Check all bus bar connections at annual service. Torque to **25 Nm**. WO-16 torque-checked all bus bar connections as part of the annual procedure.
- **Firmware:** Check firmware version at annual service. WO-16 confirmed firmware v3.2 was current with no updates available.

## Emergency Lighting Fault Diagnosis

### AS/NZS 2293.2 Compliance

Emergency lighting must comply with AS/NZS 2293.2 testing requirements:

- **Monthly:** Brief functional test — simulate mains failure and verify all lamps illuminate.
- **Six-monthly:** 90-minute duration discharge test on a sample of 25% of fittings.
- **Annual:** 90-minute duration discharge test on **ALL** fittings. Record results in the test register. Replace any units that fall below the **90-minute** requirement. Issue a compliance certificate upon completion.

### Identifying Failing Units

1. During the discharge test, start a timer when mains power is removed.
2. Observe each fitting at the 90-minute mark. Any fitting that has dimmed significantly or extinguished has failed.
3. WO-18 tested all 24 emergency lighting units and found 6 units (corridors 2, 4, 7; stairwells B, D; reception) showing battery duration under 60 minutes — well below the 90-minute requirement. Battery packs were 4 years old (original 2022 install, expected 3-5 year life).

### Battery Replacement

1. Isolate mains power to the fitting.
2. Open the fitting enclosure and disconnect the battery pack.
3. Install the replacement battery pack — match the voltage, capacity, and connector type exactly.
4. Restore mains power and verify the charge indicator shows charging.
5. After full charge (minimum 24 hours), conduct a discharge test to confirm the new battery achieves 90+ minutes.

### Legrand Emergency Lighting Pack

- **Battery part number:** Replacement battery is Legrand part **6901 20** (NiCd battery pack).
- **Test button:** The test button is located on the front face of the fitting. Press and hold for 3 seconds to initiate a manual discharge test. The lamp should illuminate immediately.
- **WO-18 reference:** Replaced 6x NiCd battery packs (Legrand part 6901 20). Post-replacement discharge test confirmed all units achieving 105-115 minutes duration. Compliance certificate was issued upon completion.
- **Central battery vs self-contained:** Legrand Emergency Lighting Packs in The Good Trades Co. customer sites are self-contained units (each has its own battery). Central battery systems require different testing procedures — check the system type before testing.
- **Bulk replacement planning:** When multiple units in a building are the same age and some have started failing, recommend a bulk replacement programme to the customer. WO-18 recommended bulk replacement for the remaining 18 units in 2027 to avoid piecemeal failures.

## Solar Inverter Fault Diagnosis

### Insulation Resistance Testing

1. Isolate the inverter from DC and AC supplies.
2. Measure insulation resistance on each string using a 1000V DC insulation tester.
3. Each string must measure **greater than 1 MOhm** to pass. WO-37 (Fronius Symo 15.0) found String 1 at 2.8 MOhm (pass) and String 2 at 0.3 MOhm (fail).
4. If a string fails, isolate individual panels by disconnecting connectors at each panel until the fault is located. WO-37 isolated the fault to String 2, Panel 8 of 12.

### Common Fault: Moisture Ingress

- Moisture ingress into panel junction boxes is a common cause of insulation faults in Queensland due to high humidity and severe weather.
- Signs: oxidation on DC connectors, water staining inside junction boxes, failed silicone seals around cable glands.
- WO-37 found the junction box cable gland seal had failed on the affected panel, causing oxidation on the DC connector.
- Repair: replace damaged DC connectors, reseal cable glands with UV-resistant silicone. WO-37 post-repair insulation test: String 2 recovered to 15.6 MOhm.

### Fronius Symo 15.0

- **State 509 (Insulation Fault):** This is the most common Fronius error seen in the field. The inverter detects insulation resistance to ground below its internal threshold and shuts down to prevent DC earth fault. Follow the insulation resistance testing procedure above to locate the affected string and panel.
- **Recovery after repair:** Once the fault is repaired, clear the error by cycling the inverter DC isolator. The inverter will run an internal insulation test before resuming production. WO-37 confirmed the inverter cleared the error and resumed generation at 12.3 kW (rated 15 kW, cloud cover present at the time).
- **Warranty claims:** For defective panel junction boxes or connectors within the panel warranty period, submit a warranty claim to Fronius or the panel manufacturer. WO-37 submitted a warranty claim for the defective panel junction box (warranty ref **FRO-WAR-2026-1187**). Document all faults with photos, measurements, and serial numbers.

## General Electrical Diagnostics

- **RCD testing:** Test residual current devices at each service. Press the test button — the RCD must trip. Measure trip time with an RCD tester — must trip within 300 ms at rated sensitivity (typically 30 mA for socket outlets).
- **Thermographic inspection:** Use a thermal camera to identify hot joints in switchboards and distribution boards. Any connection more than 10C above adjacent connections warrants investigation and retorquing.
- **Earth fault loop impedance:** Measure at the furthest point on each circuit. Compare to maximum values per AS 3000:2018 for the circuit protection device rating.

## When to Escalate

- **High voltage (>1000V AC or >1500V DC)** — requires high voltage authorisation.
- **Switchboard modifications** — adding circuits, changing protection devices, or modifying bus bars requires a licensed electrical contractor with appropriate notifications.
- **Fire-rated cable systems** — any work on fire-rated cables or barriers requires specialist knowledge and materials to maintain the fire rating.
- **UPS bypass failure** — if the UPS cannot transfer to bypass safely, do not attempt repairs with the load live. Coordinate a planned shutdown with the customer.
