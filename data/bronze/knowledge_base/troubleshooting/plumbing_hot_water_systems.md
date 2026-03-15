# The Good Trades Co. — Plumbing Troubleshooting: Hot Water Systems

## Safety Precautions

- **Gas isolation:** Before working on any gas hot water system, isolate the gas supply at the appliance isolation valve. Verify gas is off by checking the flame indicator or pilot light.
- **LOTO for electric HWS:** Isolate and lock out the electrical supply before working on electric hot water systems per AS/NZS 4836:2011.
- **PTR valve hazard:** The pressure and temperature relief (PTR) valve discharges scalding water at up to 99C and system pressure. Never block, cap, or redirect the PTR valve discharge pipe. Stand clear of the discharge outlet when testing.
- **Burn risk:** Hot water system components (heat exchangers, flues, casings) can cause severe burns. Allow the system to cool before handling internal components. Wear gloves when testing PTR valves.
- **Gas leak check:** After any work involving gas connections, perform a leak test using leak detection solution on all joints. Never use a flame to check for gas leaks.

## Temperature Issues

### Not Hot Enough

1. **Gas HWS — check thermostat setting.** Verify the thermostat is set to the correct temperature (60C minimum for storage systems to prevent Legionella, as required by AS/NZS 3500.4).
2. **Gas HWS — check gas valve.** Verify the gas valve is in the full ON position and the pilot light is lit (storage systems). For instantaneous units, verify the unit fires when a hot tap is opened.
3. **Electric HWS — check element.** Measure element resistance with a multimeter. An open circuit reading indicates a failed element. Check both upper and lower elements on dual-element systems.
4. **Check for crossover.** A faulty mixer valve or tap can allow cold water to flow back into the hot line, diluting the hot water supply.

### Too Hot

1. **Failed thermostat.** A thermostat stuck in the closed position will keep heating past the setpoint. Test by measuring the outlet temperature — if it exceeds the thermostat setting by more than 5C, the thermostat has failed. Replace immediately — this is a scald and PTR discharge risk.
2. **Failed TMV.** If the tempering valve (TMV) is not reducing temperature at the fixtures, the thermostatic element may have failed. See TMV Diagnosis below.

### Fluctuating Temperature

1. **Minimum flow rate not met.** Instantaneous (continuous flow) systems require a minimum flow rate to maintain stable combustion. If the user partially opens the mixer tap, flow may drop below the minimum threshold, causing temperature fluctuation. WO-19 (Rinnai Infinity 26) identified this exact issue — flow measured at 2.8 L/min, which is borderline against the unit minimum of 2.4 L/min.
2. **Crossover through mixer valves.** Check all mixer taps and thermostatic mixing valves for backflow from cold to hot side.

## PTR Valve Faults

The PTR valve is a critical safety device. It must discharge freely if over-temperature or over-pressure occurs. WO-4 (hot water system leaking) was initially reported as a leak but diagnosed as PTR valve discharge — a common misidentification by customers.

- **Weeping (> 50 mL per heat cycle) = replace.** A small amount of discharge during heating is normal due to thermal expansion. If discharge exceeds 50 mL per heat cycle, the valve seat is worn or damaged. WO-31 (Rheem Stellar 330) found approximately 200 mL discharge per heat cycle — valve seat showed minor pitting, likely caused by debris during original installation.
- **Continuous discharge:** Indicates thermostat failure (over-temperature) or excessive mains pressure (over-pressure). Check mains pressure — should be under 500 kPa for most systems. Check thermostat operation.
- **Missing expansion control valve:** Thermal expansion during heating causes a pressure spike in mains-pressure systems. An expansion control valve (also called a pressure-limiting valve or cold water expansion valve) is **required per AS/NZS 3500.4 Clause 8.8** for mains pressure systems. WO-31 found no expansion control valve fitted — this was a builder defect.

## TMV (Tempering Valve) Diagnosis

TMVs reduce hot water temperature at sanitary fixtures to prevent scalding. Maximum outlet temperature is 50C per AS 3498.

- **Temperature fluctuation > 3C = replace.** WO-24 (Rheem Stellar 360) found the TMV outlet temperature fluctuating between 42C and 58C — exceeding the AS 3498 maximum of 50C at sanitary fixtures. The thermostatic element was sluggish and not responding to temperature changes within the required 3 seconds.
- **Response time > 3 seconds = sluggish element.** The TMV should respond to temperature changes within 3 seconds. WO-24 confirmed the valve was not meeting this requirement.
- **Scaling in hard water areas.** Water hardness above 200 mg/L CaCO3 accelerates TMV element degradation. WO-24 measured water hardness at **280 mg/L CaCO3** — premature TMV failure at only 3 years old (installed 2023) was attributed to the high water hardness. In hard water areas, recommend:
  - TMV replacement cycle shortened to 3-4 years (vs 5 years in soft water areas).
  - Quarterly TMV outlet temperature testing per AS 3498.
  - Consider water softener installation for the hot water system.
- **Post-replacement verification:** After TMV replacement, test outlet temperature at multiple fixtures across the flow range. WO-24 tested at 3 fixtures on Level 2 — all within 45-50C across flow range 4-15 L/min.

## Gas Hot Water Specifics

### Gas Pressure Testing

1. Connect a manometer to the test point on the gas valve.
2. Natural gas operating pressure: **2.5-3.0 kPa**. WO-19 (Rinnai Infinity 26) measured 2.75 kPa — within spec.
3. LPG operating pressure: 2.75 kPa (varies by appliance — check the data plate).
4. If pressure is outside the specified range, do not adjust the appliance regulator. The upstream supply pressure needs investigation — contact the gas retailer or check the cylinder regulator for LPG.

### Combustion Analysis

1. Use a calibrated flue gas analyser to measure combustion products.
2. Acceptable ranges for natural gas:
   - CO: **< 200 ppm** (air-free). WO-19 measured 28 ppm — well within limits.
   - CO2: 7-9%. WO-19 measured 8.2%.
   - O2: 5-9%. WO-19 measured 7.1%.
3. If CO exceeds 200 ppm, do not leave the appliance in service. Isolate the gas supply, tag the appliance as unsafe, and notify the customer. Common causes include blocked flue, damaged burner, or cracked heat exchanger.

### Flame Appearance

- Natural gas: blue flame with a small yellow tip is acceptable. A lazy yellow or orange flame indicates incomplete combustion — check air supply, burner condition, and flue draught.
- If the flame lifts off the burner (too much air) or impinges on the heat exchanger (too little air), the air shutter needs adjustment.

## Equipment-Specific Procedures

### Rheem Stellar 360 / Stellar 330 (Gas Storage)

- **Thermocouple faults:** The Rheem Stellar uses a thermocouple to sense the pilot flame. If the pilot won't stay lit after releasing the button, the thermocouple has likely failed. Test by measuring the millivolt output — should be 25-35 mV with the pilot lit. Below 20 mV = replace.
- **Anode rod inspection:** The sacrificial anode rod protects the tank from corrosion. Inspect every 2 years. If the rod is less than 10 mm diameter or heavily corroded, replace it. A corroded anode rod that is not replaced leads to tank perforation and water damage.
- **WO-31 reference (Stellar 330):** PTR valve weeping approximately 200 mL per heat cycle. Valve seat showed minor pitting. Replaced PTR valve (Reliance PTR-15) and installed a thermal expansion control valve (Reliance Model 309) on the cold water inlet. The missing expansion control valve was a **builder defect** — documented and photographed for the customer's warranty claim with **Metricon**. Post-fix: no discharge during 3 heat cycles, system pressure stable at 600 kPa hot, 580 kPa cold.
- **WO-24 reference (Stellar 360):** TMV replacement due to temperature fluctuation. Replaced with an upgraded TMV rated for high-hardness water. Outlet temperature stable at 48C across flow range.

### Rinnai Infinity 26 (Instantaneous Gas)

- **Error codes:** The Rinnai Infinity 26 displays error codes on the temperature controller. Common codes:
  - **11:** No ignition — check gas supply, igniter, flame rod.
  - **12:** Flame failure — check flame rod, gas pressure, flue.
  - **14:** Thermal fuse activated — overheating, check for blocked heat exchanger or flue.
  - **16:** Over-temperature — thermostat failure or insufficient water flow.
  - **32:** Outlet thermistor fault — check wiring and thermistor resistance.
- **Minimum flow rate:** The Rinnai Infinity 26 requires a minimum flow rate of **2.4 L/min** to activate. If the customer reports fluctuating temperatures, measure the flow rate at the point of fluctuation. WO-19 measured 2.8 L/min — borderline. Advise the customer to open the mixer tap fully before adjusting temperature.
- **Heat exchanger flush:** Flush the heat exchanger with descaler at annual service. WO-19 found minimal scale — this is typical in soft water areas. In hard water areas (>200 mg/L CaCO3), flush every 6 months.
- **Inlet water filter:** Clean the inlet water filter at every service. WO-19 found minor sediment — normal.
- **PCB diagnostics:** If error codes are persistent or erratic, inspect the PCB for signs of moisture damage, corrosion, or burnt components. Moisture ingress through the flue or casing is a common cause of PCB failure in outdoor-installed units exposed to Queensland weather.

## Builder Defect Identification

When a hot water system fault is caused by a non-compliant installation, document it as a potential builder defect:

1. **Missing expansion control valve** — required per AS/NZS 3500.4 Clause 8.8 for mains pressure systems. WO-31 documented this defect on a Metricon-built property.
2. **Incorrect PTR valve rating** — the PTR valve must match the system's maximum working pressure and temperature.
3. **Non-compliant installation** — incorrect flue termination, inadequate clearances, missing drip trays.
4. **Documentation process:**
   - Photograph the non-compliant installation.
   - Note the defect in your work order diagnosis.
   - Advise the customer of their rights under the builder's warranty (typically 6 years for structural/major defects in Queensland under the Queensland Building and Construction Commission Act 1991).
   - Provide a written report that the customer can use for their warranty claim.

## When to Escalate

- **Gas leak detected** — follow The Good Trades Co. gas leak emergency response procedure. Do not attempt repair until the area is safe.
- **CO reading above 200 ppm** — isolate immediately, tag as unsafe, notify customer.
- **Tank perforation or major water damage** — coordinate with plumber and property owner for emergency response.
- **Tempering valve at a healthcare or aged care facility** — these are critical installations with additional compliance requirements under AS 3498. Escalate to The Good Trades Co. supervisor.
