# The Good Trades Co. — HVAC Troubleshooting: Unit Running But Not Cooling

## Safety Precautions

- **Isolate power** before opening any panels or accessing electrical components. Follow The Good Trades Co. LOTO procedure per AS/NZS 4836:2011.
- Wear PPE: safety glasses, gloves, and steel cap boots at all times.
- Check for refrigerant leaks before handling components — a hissing sound or oily residue at fittings indicates a possible leak. ARCtick licence required for any refrigerant work.
- On rooftop units, complete a working at heights permit before accessing the outdoor unit.
- If the system uses R32 refrigerant (Mitsubishi MSZ-AP series), note it is mildly flammable (A2L classification) — no open flames or sparking tools near connections.

## Common Causes by Frequency

| Cause | Frequency | Typical Fix Time |
|---|---|---|
| Dirty or blocked filter | 35% | 15 min |
| Dirty condenser coil | 20% | 30-60 min |
| Failed run capacitor | 15% | 30 min |
| Low refrigerant (leak) | 12% | 1-4 hours |
| Failed contactor | 8% | 30 min |
| Faulty thermostat | 5% | 30-60 min |
| Compressor failure | 5% | Escalate |

## Generic Diagnostic Procedure

Common presentations include WO-1 (AC not cooling Level 12 — Daikin RZQS250, required full diagnostic from airflow through to refrigerant) and WO-22 (AC not working, baby in house — Mitsubishi MSZ-AP50VG, prioritised as urgent due to vulnerable occupant).

### Step 1 — Check Airflow

1. Inspect the return air filter. A clogged filter is the single most common cause. Hold it up to light — if you cannot see through it, replace or clean it.
2. Check all return air grilles for obstructions (furniture, boxes, curtains).
3. Check all supply registers are open and unobstructed.
4. Expected airflow: 57-75 L/s per kW of rated cooling capacity. If available, use an anemometer at each supply register and compare total measured airflow to the system rating.

### Step 2 — Check Thermostat/Controller

1. Verify the system is set to **cooling** mode, not heating, fan-only, or auto.
2. Check the temperature differential — setpoint should be at least 2C below current room temperature.
3. For wired controllers: check wiring connections at Y (compressor), G (fan), R (24V power), and C (common) terminals.
4. For wireless controllers: replace batteries if display is dim or unresponsive.
5. Test by setting the temperature to minimum (16C) — the outdoor unit should start within 3 minutes.

### Step 3 — Check Outdoor Unit

1. Inspect the condenser coil for dirt, debris, or vegetation. Clean with low-pressure water if fouled — never use a high-pressure washer directly on fins.
2. Verify the condenser fan is running and spinning freely. Listen for bearing noise.
3. Listen to the compressor:
   - **Humming but not starting** = likely failed run capacitor or seized compressor.
   - **Clicking on and off** = thermal overload tripping (possible low refrigerant or high head pressure).
   - **Running normally but not cooling** = possible refrigerant issue or failed reversing valve (stuck in heating).
4. Test the run capacitor with a multimeter — reading should be within 10% of the rated microfarad value on the label.
5. Measure amp draw with a clamp meter and compare to the nameplate RLA (rated load amps). Over 110% of RLA indicates a problem.

### Step 4 — Check Refrigerant

1. Connect gauge set to service valves. Compare suction and discharge pressures to manufacturer specifications for the current ambient temperature.
2. **Low suction pressure + high superheat** = undercharge (leak likely). Do not just top up — find and repair the leak first.
3. **High suction pressure + low superheat** = overcharge, restricted condenser, or failing compressor valves.
4. Perform a leak check with an electronic leak detector before adding any refrigerant.
5. ARCtick licence is mandatory for any refrigerant handling. Log all quantities added or recovered.

## Equipment-Specific Procedures

### Daikin RZQS250 / ACAS250 / ACAS140 (Ducted)

- **Error codes:** Access the LED diagnostic panel on the indoor unit PCB (behind the return air filter access panel). Press and hold the self-diagnosis button for 3 seconds. Error codes display as a two-character alphanumeric sequence — cross-reference with Daikin fault code chart.
- **EEV diagnostic mode:** On the ACAS140, if superheat is erratic (e.g. EEV hunting between 15-85% open as seen in WO-15), enter EEV diagnostic mode via the PCB DIP switches. Check that the EEV stepper motor responds to controller commands across its full range. Measured subcooling should be 6-8K per Daikin spec — anything under 4K with erratic superheat indicates EEV failure or refrigerant undercharge.
- **BMS integration:** Verify BMS points are reading correctly. A BMS fault can override the thermostat setpoint or lock the unit in an unintended mode. Check the BACnet/Modbus communication LED for steady flashing (communication OK) vs solid on (fault).

### Mitsubishi MSZ-AP50VG / MSZ-AP25VG / MSZ-AP35VG (Split)

- **LED blink codes:** The operation LED on the indoor unit flashes in a pattern to indicate faults. Count the number of flashes, then the pause, then repeat. Cross-reference with the Mitsubishi MSZ-AP service manual blink code table.
- **4-way valve testing:** If the unit runs but blows warm air in cooling mode, the 4-way reversing valve may be stuck. Measure the solenoid coil resistance — should be 15-25 ohms. Open circuit (infinity) means the coil has failed (as confirmed in WO-29 on an MSZ-AP35VG). Test valve operation by switching between heating and cooling — listen for the valve click.
- **R32 pressures:** R32 operating pressures differ from R410A. In cooling mode at 35C ambient, expect suction pressure approximately 1.0-1.1 MPa and discharge pressure approximately 3.0-3.3 MPa. In heating mode at 14C ambient, suction pressure approximately 0.6 MPa.

### Fujitsu ASTG24KMCA / ARTG36LHTA

- **LED diagnostic sequences:** The operation, timer, and economy LEDs flash in combination to indicate fault codes. Record which LEDs flash and the sequence — refer to Fujitsu installer manual for the specific model.
- **Auto-restart behaviour:** After a power interruption, Fujitsu units have an auto-restart function. If the unit was in cooling mode before power loss, it will attempt to restart in the same mode. If it fails to restart, check whether the auto-restart DIP switch on the PCB is enabled.
- **Common fault on ARTG36LHTA:** The outdoor unit fan motor can overheat in extreme Queensland summer conditions (ambient >40C). The unit will shut down on thermal protection and restart automatically once cooled. If this recurs, check condenser coil cleanliness and ensure adequate clearance around the outdoor unit (minimum 200 mm sides, 700 mm front).

### Carrier 42VH024 / 42VH036

- **Diagnostic codes:** The Carrier 42VH series uses a diagnostic LED on the outdoor unit PCB. Steady green = normal operation. Flashing patterns indicate specific faults — count flashes per cycle.
- **Heritage installs:** The 42VH series is commonly found in heritage-listed buildings (e.g. WO-14, annual AC service at a heritage property). Any modifications require heritage approval before proceeding. Do not relocate units, run new pipework on visible facades, or modify existing penetrations without written approval from the building owner and heritage authority.
- **Filter access:** On the 42VH024, the filter is accessed via the front panel clips — do not force. On older installs, clips may be brittle. Replacement filters must match the original size exactly.

## When to Escalate

Escalate to The Good Trades Co. supervisor or specialist contractor in these situations:

- **Compressor internal failure** — locked rotor, open/short windings, or mechanical noise from within the compressor shell. Do not attempt field repair.
- **VRV/VRF systems** — multi-unit systems with centralised refrigerant management require manufacturer-certified technicians.
- **Inaccessible refrigerant leaks** — leaks within walls, underground, or in brazed joints inside ceiling spaces that cannot be accessed safely.
- **Units under 12 months old** — do not perform invasive diagnostics on units within warranty. Contact the manufacturer warranty line first. Document the fault and advise the customer of the warranty process.
