# The Good Trades Co. — HVAC Troubleshooting: Airflow and Zone Balancing

## Safety Precautions

- **Ceiling space access:** If accessing ductwork in ceiling spaces, assess working at heights risk. Any work where a fall of 2 metres or more is possible requires a working at heights permit per Work Health and Safety Regulation 2011 (QLD) Chapter 6 Part 1.
- **Asbestos check:** Before entering any ceiling space, check the building's asbestos register. Older buildings in Queensland may contain asbestos-backed ductwork or insulation. If suspected asbestos-containing material is found, stop work immediately, isolate the area, and notify the site contact and The Good Trades Co. supervisor.
- **LOTO:** Isolate power to the HVAC system before working on any electrical components (damper actuators, zone controllers, fan motors) per AS/NZS 4836:2011.
- Use a head torch and knee pads in ceiling spaces. Walk on ceiling joists only — never step on plasterboard.

## Symptoms

WO-10 (ducted AC uneven cooling) is a typical example of the symptoms below — one zone significantly warmer than others despite the system running normally.

- Hot or cold spots — some rooms comfortable, others not.
- One room not cooling or heating at all while rest of the building is fine.
- System runs continuously but rooms never reach setpoint.
- Airflow strong at some registers, weak or absent at others.

## Generic Diagnostic Procedure

### Step 1 — Inspect Ductwork

1. Access the ceiling space or duct riser and visually inspect all ductwork runs from the indoor unit to each supply register.
2. Look for:
   - **Disconnected flex duct** — pushed off the collar or torn. This is one of the most common causes. WO-23 found a 2.5 m section of flex duct disconnected from the living room supply collar on a Daikin FDYAN100.
   - **Crushed or kinked flex duct** — restricts airflow. Flex duct must maintain a smooth curve with no sharp bends.
   - **Insulation damage** — torn or missing insulation causes condensation and energy loss.
   - **Duct supports** — flex duct should be supported at maximum 1.5 m intervals per AS/NZS 4254.1. Sagging duct creates low points that trap condensate.
3. Repair disconnected flex duct by reattaching to the collar and securing with a **hose clamp + foil tape** per AS/NZS 4254.1. Do not rely on tape alone — the hose clamp provides the mechanical connection.

### Step 2 — Check Zone Dampers

1. Verify each zone damper position matches the expected setting. Main living areas are typically set to **80% open**. WO-23 found a living room damper at only 40% — adjusting to 80% restored proper airflow.
2. Test actuator response time. The damper should move from fully closed to the set position in **less than 15 seconds**. If response time exceeds 15 seconds, the actuator is sluggish and may need replacement. WO-28 found an actuator taking 45 seconds to respond.
3. Manually override each zone to 100% open, then 0%, to verify full range of movement. Listen for mechanical binding or grinding.

### Step 3 — Measure Airflow

1. Use an anemometer at each supply register.
2. Calculate total measured airflow and compare to the system rated capacity.
3. Identify underperforming zones — any register delivering less than 70% of its expected share warrants investigation.
4. Measure supply air temperature at each register. All zones should deliver within 1-2C of each other. A large variation (e.g. WO-23 where the living room was 19C vs bedrooms at 14.2C) indicates a ductwork or damper problem in that zone.

### Step 4 — Check Return Air

1. Inspect the return air filter. A heavily clogged filter restricts total system airflow and affects all zones. WO-23 found a filter heavily clogged with pet hair in a home with two cats — recommended cleaning every 6 weeks for homes with pets.
2. Check return air grille sizing — undersized return air grilles create a pressure drop that reduces total system capacity.
3. Verify return air paths to each room. Sealed rooms (no gap under the door) create positive pressure that resists supply air delivery. A minimum 10 mm gap under the door or a transfer grille is required.

## Duct Repair Procedures

### Flex Duct Reconnection (per AS/NZS 4254.1)

1. Slide the flex duct inner liner over the collar (minimum 50 mm overlap).
2. Secure with a **stainless steel hose clamp** — tighten firmly but do not crush the collar.
3. Wrap the joint with **aluminium foil tape** (not cloth duct tape, which degrades over time).
4. Pull the insulation and outer vapour barrier over the joint and tape the vapour barrier to maintain the moisture seal.

### Rigid Duct Sealing

1. Clean the joint area of dust and debris.
2. Apply mastic sealant to all joints and seams.
3. For joints with gaps greater than 3 mm, use fibreglass mesh tape bedded into mastic.

## Equipment-Specific Procedures

### Actron ESP Plus / ESP Platinum (Zoning Systems)

- **Zone controller programming:** The Actron ESP zone controller manages up to 8 zones via motorised dampers. Access programming via the wall controller by holding the MODE button for 5 seconds to enter installer mode.
- **Damper motor replacement:**
  1. Isolate power to the zone controller.
  2. Disconnect the faulty motor wiring at the zone controller terminal strip (note the zone number).
  3. Remove the motor from the damper blade mounting bracket (2 screws).
  4. Install the replacement motor, reconnect wiring, and restore power.
  5. Test the zone from the wall controller — verify open and close response.
- **Commissioning:** After any damper motor replacement, run a full zone commissioning cycle from the controller. This tests each zone sequentially and confirms communication with all damper motors.

### Daikin FDYAN100 / FDYAN140 (Ducted)

- **Static pressure adjustment:** Daikin FDYAN units have adjustable static pressure settings to match duct system resistance. If ductwork is long or has many bends, increase the static pressure setting via the DIP switches on the indoor unit PCB. Settings range from low (30 Pa) to high (200 Pa) — refer to the Daikin installation manual for the DIP switch table.
- **Fan speed selection:** Fan speed should be matched to the duct system. If total measured airflow is low despite clean filters and clear ductwork, increase the fan speed setting. If noise is excessive, decrease one step and verify airflow is still adequate.
- **WO-23 reference (FDYAN100):** Disconnected flex duct and incorrect damper settings were the root cause of uneven cooling. After reconnecting ductwork and adjusting the living room damper from 40% to 80%, supply air temperatures equalised: bedrooms 14.2C, living room 14.5C (previously 19C with the duct disconnected).

### Belimo Damper Actuators

- **Replacement procedure (LF24-SR spring-return):**
  1. Isolate power to the actuator.
  2. Note the wiring configuration (2-point, 3-point, or 0-10V signal).
  3. Remove the actuator from the damper shaft clamp (Allen key).
  4. Mount the new actuator and tighten the shaft clamp.
  5. Reconnect wiring and restore power.
  6. Verify travel range — the actuator should drive the damper through its full range smoothly.
- **PID tuning for critical spaces:** For spaces with strict temperature control requirements (theatres, server rooms), supply air damper actuator PID parameters must be tuned to maintain stable temperature.
  - WO-28 (theatre HVAC calibration, Daikin FDYAN140) found the original PID parameters too sluggish: P=5, I=180s, D=0 (derivative term was disabled).
  - Adjusted to: **P=8, I=120s, D=30s**. The increased proportional gain and added derivative term provide faster response to load changes without overshoot.
  - Post-calibration, the theatre held 20.8-21.2C over a 2-hour test with simulated heat load, within the AS/NZS 1386.5 specification of 20-22C for critical spaces.

## Theatre and Critical Space Calibration

Critical spaces (theatres, server rooms, clean rooms) require tighter temperature control than standard commercial areas.

### Temperature Sensor Calibration

1. Place a calibrated reference thermometer next to the room temperature sensor.
2. Allow both to stabilise for 10 minutes.
3. Compare readings. Acceptable drift is **less than 0.5C**. WO-28 found a sensor drifted 1.6C (reading 20.5C when actual was 22.1C) — the system was under-cooling because it believed the room was cooler than it was.
4. Apply an offset correction in the controller if drift is within correctable range.
5. If drift exceeds the correctable range, replace the sensor.

### Calibration Interval

- **6 months** for critical spaces (theatres, server rooms). WO-28 set the next calibration check 6 months out.
- **12 months** for standard commercial spaces.
- Record the calibration date and next due date in the maintenance log.

### Performance Verification

After calibration, run a performance test:
1. Allow the system to reach steady state.
2. Introduce a simulated heat load equivalent to expected occupancy (WO-28 used approximately 2.5 kW additional load).
3. Monitor room temperature over a minimum 1-hour period.
4. Temperature should remain within the specified band without excessive cycling.

## When to Escalate

- Ductwork modifications requiring engineering design (resizing, rerouting, adding zones).
- Asbestos-backed ductwork or insulation discovered during inspection.
- BMS integration issues affecting zone control logic.
- Persistent imbalance after all mechanical checks — may indicate incorrect system sizing or design fault requiring engineering review.
