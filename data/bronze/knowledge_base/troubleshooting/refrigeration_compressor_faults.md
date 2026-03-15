# The Good Trades Co. — Refrigeration Troubleshooting: Compressor Faults

## Safety Precautions

- **ARCtick licence required.** All refrigerant handling on commercial refrigeration systems requires a current ARCtick licence under the Ozone Protection and Synthetic Greenhouse Gas Management Act 1989.
- **Ammonia systems (R717) = specialist only.** Do not attempt any work on ammonia refrigeration systems without specific ammonia endorsement and training. Evacuate the area and contact The Good Trades Co. supervisor immediately if an ammonia leak is suspected.
- **LOTO mandatory.** Isolate and lock out all electrical supplies before opening compressor terminal boxes or working on electrical components per AS/NZS 4836:2011.
- Wear **hearing protection** near operating compressors — noise levels regularly exceed 85 dB(A).
- Wear **safety glasses and gloves** when working with refrigerant systems. Liquid refrigerant causes frostbite on skin contact.
- Check for **oil on fittings** before starting work — oil residue at joints often indicates a refrigerant leak.

## High Pressure Faults

High pressure (HP) cutout is a safety device — do not bypass or reset repeatedly without diagnosing the cause.

1. **Check condenser airflow:** Inspect the condenser coil for dirt, grease, or debris. In kitchen environments, grease fouling is the primary cause. Clean with alkaline degreaser for grease-fouled coils or low-pressure water for standard dirt.
2. **Check condenser fan:** Verify the fan is running. A seized condenser fan motor is a common HP fault cause. WO-3 (Bitzer CSH8573-140Y) confirmed a seized condenser fan motor due to bearing failure — the compressor was cycling on HP cutout every 4 minutes.
3. **Check for overcharge:** Compare discharge pressure to expected value for the refrigerant type and current ambient temperature. Significantly elevated discharge pressure with normal condenser airflow indicates possible overcharge or non-condensable gases.
4. **Check ambient conditions:** Extreme ambient temperatures (>40C in Queensland summers) can push discharge pressure above cutout. Verify cutout setpoint is appropriate for the installation location.

## Low Pressure Faults

1. **Check for undercharge (leak):** Low suction pressure with high superheat indicates refrigerant undercharge. Perform a leak check with an electronic leak detector before adding refrigerant. WO-3 confirmed the refrigerant charge was holding at 18 kg with no leak detected.
2. **Check expansion device:** TXV or EEV restriction causes low suction pressure with low or no superheat at the valve outlet. Check the bulb position and insulation on TXV systems.
3. **Check filter drier:** A blocked filter drier causes a temperature drop across the drier body. Replace if temperature differential exceeds 2C.
4. **Check evaporator:** Iced-up evaporator coils indicate defrost failure. Check defrost timer/controller, heater elements, and drain pan.

## Compressor Not Starting

1. **Check contactor:** Inspect contactor contacts for pitting or welding. WO-36 (Bitzer CSH8573-140Y) found contactor CONT-40A with pitted contacts — replaced preventively alongside the condenser fan motor.
2. **Check capacitor:** Test run capacitor — reading should be within 10% of rated value. WO-29 tested a capacitor at 42.8 uF (rated 45 uF) — within 10% tolerance, acceptable.
3. **Check thermal overload:** If the overload has tripped, allow the compressor to cool before resetting. Investigate the cause — repeated tripping indicates an underlying problem (high head pressure, locked rotor, winding fault).
4. **Check windings:** Measure winding resistance R-S, S-T, and R-T. Readings should be balanced (within 5% of each other). WO-29 measured R-S 2.1 ohm, S-T 2.1 ohm, R-T 4.2 ohm — balanced, confirming the compressor windings were healthy.
5. **Locked rotor:** If the compressor hums but does not start and amp draw is very high (6-8x RLA), the compressor may be mechanically seized. Do not attempt repeated starts — this damages windings.

## Vibration Diagnostics

1. Measure vibration velocity at the compressor bearing housing using a vibration meter. Compare to ISO 10816 zones: Zone A (< 2.8 mm/s), Zone B (< 7.1 mm/s), Zone C (< 11 mm/s), Zone D (> 11 mm/s — stop immediately).
2. Compare to baseline readings from commissioning or previous service. A doubling from baseline warrants investigation.
3. Check all mounting bolt torque — Bitzer semi-hermetics require **45 Nm**.
4. Check anti-vibration mount condition with a Shore A durometer. Replace if hardness exceeds **Shore A 80** (original spec typically Shore A 65).

## Oil Management

1. **Sight glass check:** Oil level should be visible in the lower third to middle of the sight glass during normal operation. No oil visible = investigate return path.
2. **Oil quality:** For large systems, take an oil sample for lab analysis. Check for acidity (high acid = moisture ingress), metal particles (bearing wear), and discolouration (overheating).
3. **Oil return:** In systems with long suction lines or vertical risers, verify oil is returning to the compressor. Oil traps may be required on vertical risers.

## Equipment-Specific Procedures

### Bitzer CSH8573-140Y (Screw Compressor)

This is a screw-type compressor used in low-temperature freezer applications (R507A refrigerant).

- **HP cutout:** WO-3 diagnosed an HP fault on this unit. Root cause was a seized condenser fan motor (bearing failure) causing the compressor to cycle on HP cutout every 4 minutes. Condenser coil was also fouled with dust/debris. Refrigerant charge held at 18 kg — no leak. Resolution required condenser fan motor replacement (300W 3-phase 415V 50Hz, replacement model FM-300W per WO-36).
- **Oil differential pressure:** Monitor oil differential pressure at each service. Low oil differential indicates oil pump wear or low oil level. The CSH8573 has a built-in oil pressure monitoring system.
- **Slide valve position:** The capacity control slide valve should move smoothly through its full range. If capacity control is erratic, check the slide valve actuator and solenoid. Abnormal vibration can also indicate slide valve issues.
- **Contactor replacement:** WO-36 replaced the 40A contactor preventively due to pitted contacts. Always replace contactors at the first sign of contact pitting — a welded contactor can prevent the compressor from stopping on a safety cutout.

### Bitzer 4FES-5Y (Semi-Hermetic Reciprocating)

This is a semi-hermetic reciprocating compressor used in medium-temperature coolroom applications.

- **Valve plate inspection:** The 4FES-5Y has accessible valve plates. If the compressor runs but cooling capacity is reduced (suction pressure higher than expected, discharge pressure lower than expected), suspect leaking valve plates. Access requires removing the cylinder head — gasket replacement is mandatory on reassembly.
- **Crankcase heater:** Verify the crankcase heater is operating during compressor off-cycles. The heater prevents refrigerant migration into the oil during standby. A failed crankcase heater leads to liquid slugging on startup, which damages valve plates and bearings. Check heater element resistance and supply voltage.
- **WO-2 reference:** WO-2 (kitchen coolroom temp rising) involved this compressor model. Temperature rising in a coolroom is an urgent call — product may be at risk.

### Bitzer 4NES-20Y / 4TES-12Y (Semi-Hermetic Reciprocating)

- **Fault codes:** These models with the Bitzer IQ module display fault codes on the controller screen. Common codes include HP cutout, LP cutout, oil pressure fault, and motor temperature fault. Record the fault code and timestamp before resetting.
- **Parallel oil management:** When 4NES-20Y or 4TES-12Y compressors run in parallel rack systems, oil equalisation between compressors is critical. Check oil equalisation line connections and sight glass levels on all compressors in the rack. Uneven oil levels indicate a blocked equalisation line or check valve fault.
- **WO-25 reference (4TES-12Y):** Vibration check found mounting bolts loosened and anti-vibration mounts deteriorated (Shore A 85 vs spec Shore A 65). After retorquing to 45 Nm and replacing 2 mounts, vibration returned to near-baseline: axial 1.4 mm/s, radial 2.2 mm/s.

## Emergency Response — Product at Risk

When a compressor fault threatens stored product (coolrooms, freezers):

1. **Deploy portable cooling** immediately if available. Position portable units to maintain the cold chain while the primary system is being repaired.
2. **Temperature monitoring:** Place a data logger in the affected cold room. Record the temperature at the time of arrival and every 30 minutes during the repair.
3. **Food safety notification:** For commercial kitchens and cold storage facilities, advise the site manager of the temperature breach. Food safety regulations require documentation of any break in the cold chain.
4. **Time limits:** Chilled product (0-5C) — if temperature exceeds 5C for more than 4 hours, product may need to be disposed. Frozen product (-18C) — if temperature exceeds -12C, assess product condition and advise the customer.
5. **Communicate clearly** with the customer about repair timeframes and product risk. Do not make promises about timeline if parts are required.

## When to Escalate

- **Ammonia (R717) systems** — specialist contractor with ammonia endorsement required.
- **Compressor internal failure** — seized compressor, broken valve reeds, bearing failure requiring compressor replacement.
- **Parallel rack systems** — multi-compressor systems with shared oil and refrigerant circuits require specialist commissioning.
- **Warranty claims** — compressors under manufacturer warranty must be assessed by the manufacturer's authorised service agent before any invasive work.
