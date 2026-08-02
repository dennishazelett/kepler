# Quadrant

The quadrant is the second reference instrument in the Kepler project.

Unlike the cross-staff, which estimates angular separation through linear measurement and geometric reconstruction, the quadrant measures elevation angles directly using a graduated arc and a plumb line. Together, the two instruments illustrate complementary approaches to astronomical measurement and provide an opportunity to compare their precision, accuracy, calibration requirements, and error characteristics.

The quadrant is intended to support both historical investigations and modern scientific practice. While inspired by historical instruments, the goal is not historical reconstruction for its own sake. Instead, the instrument serves as a vehicle for studying how careful observation, calibration, uncertainty analysis, and statistical inference combine to produce scientific knowledge.

## Learning Objectives

Building and using the quadrant introduces participants to:

- direct angular measurement
- gravity as a measurement reference
- calibration of graduated instruments
- observational uncertainty
- instrument comparison
- reproducible data collection

These concepts complement those introduced by the cross-staff and broaden the range of observational techniques available within Kepler.

## Repository Contents

| File | Purpose |
|----|----|
| `design.md` | Measurement principles, historical context, and engineering decisions |
| `build-guide.md` | Construction instructions and required materials |
| `calibration.md` | Calibration principles, rationale, and interpretation |
| `bill-of-materials.md` | Components required to build the instrument |

Operational calibration procedures are maintained separately in protocols/quadrant/calibration/protocol.md.

## Relationship to the Kepler Data Model

The quadrant serves as the first test of the instrument-independent architecture developed for Kepler.

The survey metadata, validation workflow, and repository organization are expected to remain unchanged. Only the instrument-specific observation schema should differ from that of the cross-staff.

This provides an opportunity to evaluate whether the Kepler data model successfully separates common observational concepts from instrument-specific measurement details.

## Current Status

The Kepler reference quadrant has been designed, constructed, and evaluated through an initial calibration campaign.

Current work focuses on refining the calibration protocol, documenting instrument performance, and extending the instrument from controlled calibration measurements to astronomical field observations.
