# The Good Trades Co. — HVAC Troubleshooting: Noise and Vibration

## Safety Precautions

- **Isolate power** and apply LOTO before opening any panels or inspecting rotating components. Follow The Good Trades Co. LOTO procedure per AS/NZS 4836:2011.
- Wear **hearing protection** in plant rooms and near operating compressors — sound levels commonly exceed 85 dB(A).
- Never reach into operating equipment to check for vibration by touch while running. Use a vibration meter or mechanical stethoscope.
- On rooftop plant, complete a working at heights permit before access.
- Some faults require the unit to be running during diagnosis. If the unit must run with panels removed, maintain a safe distance from rotating parts and re-fit panels immediately after testing.

## Noise Classification

Identify the noise type first — this narrows the diagnosis significantly. WO-6 (AC making grinding noise) is a typical presentation — the customer description pointed directly to a bearing or fan contact fault.

| Noise Type | Likely Source | Urgency |
|---|---|---|
| **Rattling** | Loose panels, screws, ductwork | Low — tighten and check |
| **Grinding** | Bearing failure, fan blade contact | High — stop and inspect |
| **Humming** | Electrical — capacitor, contactor, transformer | Medium — diagnose cause |
| **Squealing** | Belt slip, dry bearing | Medium — lubricate or replace |
| **Clicking** | Relay cycling, thermal protection tripping | Medium — investigate root cause |

## Vibration Assessment — ISO 10816

Use a vibration meter to measure velocity (mm/s RMS) at the bearing housing or mounting point.

| Zone | Velocity (mm/s) | Condition | Action |
|---|---|---|---|
| A | < 2.8 | New or excellent | Record as baseline |
| B | < 7.1 | Acceptable for long-term operation | Monitor at next service |
| C | < 11.0 | Short-term operation only | Schedule repair within 2 weeks |
| D | > 11.0 | Damage imminent | **Stop equipment immediately** |

Always compare current readings to the baseline recorded at commissioning or last service. A doubling of vibration velocity from baseline warrants investigation even if still within Zone B.

## Diagnosis by Component

### Indoor Fan Barrel (Cross-Flow Fan)

- **Dust/lint accumulation** on blades causes rotational imbalance. This is the most common cause of indoor unit noise, especially in residential settings with pets.
- Noise is often worse in heating mode because the fan runs at higher RPM for heat distribution.
- Inspect by removing the front panel and filter. Look for uneven dust buildup across the barrel length.
- Clean with coil cleaner and water rinse. For heavy buildup, remove the barrel for cleaning.

### Outdoor Fan Motor

- **Bearing wear** produces a grinding or squealing noise that worsens over time.
- Use a mechanical stethoscope on the motor housing to isolate bearing noise from other sources.
- Check for axial play by gently pushing the shaft — any perceptible movement indicates bearing wear.
- Replace threshold: bearing play > 0.1 mm = replace motor.

### Compressor

- **Mounting bolts:** Check torque on all compressor mounting bolts. Loose bolts allow the compressor to walk on its mounts, transmitting vibration to the chassis and connected pipework.
- **Anti-vibration mounts:** Check rubber mount condition. Use a Shore A durometer if available — original spec is typically Shore A 60-70. Hardened rubber (Shore A > 80) no longer absorbs vibration effectively and must be replaced.
- **Internal noise:** A metallic knocking from within the compressor shell indicates internal damage (broken valve reed, piston slap, or bearing failure). This is not field-repairable — escalate.

### VSD-Driven Fans (Variable Speed Drive)

- VSDs can excite natural resonance frequencies in fan assemblies, typically in the **25-35 Hz** range.
- If vibration occurs only at certain speeds and disappears at higher or lower speeds, resonance is the likely cause.
- Solution: program skip frequencies in the VSD to avoid the resonant range.

## Equipment-Specific Procedures

### Daikin Ducted (RZQS250, ACAS140, FDYAN100, FDYAN140)

- **Fan barrel cleaning:** Access the indoor fan barrel by removing the return air grille and filter, then the bottom access panel. The barrel slides out after disconnecting the motor coupling. Clean with coil cleaner spray, rinse with water, and dry before reinstalling.
- **Bearing lubrication:** Daikin ducted indoor fan motors have sealed bearings — they are not field-lubricated. If the bearing is noisy, the motor must be replaced.
- **Ductwork rattle:** Ducted systems transmit vibration through ductwork. Check for flex duct rubbing against framing, loose duct clamps, and unsupported rigid duct sections. Duct supports should be at maximum 1.5 m intervals per AS/NZS 4254.1.

### Mitsubishi MSZ-AP25VG / MSZ-AP50VG / MSZ-AP35VG (Split)

**NOTE:** WO-20 (grinding noise investigation) is a **Mitsubishi MSZ-AP25VG**, not a Fujitsu unit.

- **Indoor fan barrel removal:** On the MSZ-AP series, the barrel is accessed by removing the front panel, filters, left-side cover, and disconnecting the drain tray. The barrel slides out to the left after removing the retaining screw on the right bearing.
- **Grinding in heating mode:** The MSZ-AP series runs the indoor fan at higher RPM in heating mode. Dust/lint accumulation that causes minor imbalance at low speed becomes a significant grinding noise at high speed. WO-20 confirmed this pattern — significant dust/lint on the MSZ-AP25VG barrel caused rotational imbalance, resolved by cleaning. Evaporator coil was also cleaned with coil cleaner and water rinse.
- **Fan motor bearing:** If cleaning resolves the noise but it returns within 6 months, the fan motor bearing is worn and the fan motor assembly needs replacement (approximate part cost ~$180 + labour).
- **R32 compressor noise:** R32 compressors in the MSZ-AP series operate at slightly higher pressures than R410A equivalents. A light hum is normal. Excessive vibration warrants checking mounting bolts and suction/discharge line supports.

### ABB ACS580 VSD

The ABB ACS580 VSD is used on exhaust fan systems in commercial installations (e.g. WO-11, food court exhaust fan vibration).

- **Resonance parameter programming:**
  1. Access parameter group 22 (Critical Speeds).
  2. Set parameter **22.51** (Critical Speed 1 Low) to the lower bound of the resonant range (e.g. 25 Hz).
  3. Set parameter **22.52** (Critical Speed 1 High) to the upper bound (e.g. 35 Hz).
  4. The VSD will ramp through this range without dwelling, preventing sustained resonance.
- **Vibration at fixed speed:** If vibration occurs at a fixed speed setting, check motor coupling alignment, motor mounting bolts, and fan blade condition. The VSD is not the cause if vibration is speed-independent.
- **Electrical hum from VSD enclosure:** A low hum from the enclosure itself is normal (inductor/transformer noise). If the hum changes character or becomes loud, check for loose mounting hardware inside the enclosure and verify input power quality.

### Bitzer Compressors (4TES-12Y, 4FES-5Y, CSH8573-140Y, 4NES-20Y)

- **Mounting bolt torque:** Bitzer semi-hermetic compressors require mounting bolt torque of **45 Nm**. Check all bolts at every service. WO-25 (Bitzer 4TES-12Y) found 2 of 4 bolts loosened — vibration had doubled from baseline (axial 1.2 to 2.8 mm/s, radial 2.0 to 4.2 mm/s, ISO 10816 Zone B). Retorquing and replacing deteriorated mounts restored readings to near baseline (axial 1.4 mm/s, radial 2.2 mm/s).
- **Anti-vibration mounts:** Replace if rubber has hardened beyond **Shore A 80** (original spec Shore A 65). WO-25 confirmed mounts measured at Shore A 85 were no longer effective — replacement brought vibration back to acceptable levels.
- **Screw compressor (CSH8573-140Y):** Vibration in screw compressors can indicate slide valve issues or rotor bearing wear. These require specialist diagnosis — record vibration readings and escalate if Zone C or above.
- **Quarterly monitoring:** Record vibration readings at every quarterly service to build a trend baseline. If radial readings exceed 4.5 mm/s, bearing investigation is warranted.

## Replace vs Repair Decision Thresholds

| Component | Threshold | Action |
|---|---|---|
| Fan bearing | Play > 0.1 mm | Replace motor |
| Anti-vibration mount | Shore A > 80 | Replace mount |
| Fan barrel | Any crack or deformation | Replace barrel |
| Fan barrel | Dust buildup only | Clean and reuse |
| Compressor bearing | Internal knocking noise | Escalate — not field-repairable |

## When to Escalate

- Compressor internal noise (knocking, metallic grinding from within the shell).
- Vibration readings in ISO 10816 Zone D (> 11 mm/s) — stop equipment and escalate immediately.
- VSD-related vibration that cannot be resolved by skip frequency programming.
- Any noise accompanied by unusual smell (burning insulation, overheating).
- Repeated failures after repair — indicates a systemic issue requiring engineering assessment.
