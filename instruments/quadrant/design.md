# Quadrant Design

## Purpose

The quadrant is the second reference instrument developed for the Kepler project.

Its purpose is not merely to measure angles, but to introduce a fundamentally different measurement principle from that used by the cross-staff. Together, the two instruments allow participants to compare independent approaches to astronomical observation, understand the strengths and limitations of each design, and investigate how different measurement systems influence scientific inference.

The quadrant also serves as the first test of Kepler's instrument-independent data architecture. While the physical instrument differs substantially from the cross-staff, the surrounding workflow—calibration, observation, validation, and data submission—should remain largely unchanged.

------------------------------------------------------------------------

# Historical Background

Quadrants have been used for astronomical and navigational measurement for more than two millennia.

Their widespread adoption arose from a simple observation: gravity provides a remarkably stable reference direction. By combining a graduated arc with a freely hanging plumb line, a quadrant converts the direction of an observed object into an angular measurement.

Numerous forms of quadrant were developed throughout history, including:

- astronomical quadrants
- mural quadrants
- mariner's quadrants
- Davis quadrants
- surveying quadrants

Although these instruments differ in construction and intended application, they all rely upon the same underlying measurement principle.

The Kepler quadrant is inspired by these historical instruments but is designed for modern educational use using inexpensive, easily obtained materials.

The objective is not historical reconstruction, but faithful reproduction of the underlying scientific ideas.

------------------------------------------------------------------------

# Measurement Principle

Unlike the cross-staff, which infers an angle from a measured linear displacement, the quadrant measures an angle directly.

The instrument consists of:

- a rigid quarter-circle
- a graduated angular scale
- a sighting mechanism
- a plumb line suspended from the center of the arc

When the observer sights an object, gravity causes the plumb line to remain vertical while the instrument rotates with the observer.

The intersection of the plumb line with the graduated scale provides a direct measurement of the object's elevation angle above the horizon.

This distinction has important consequences.

## Cross-Staff

Measures:

- linear displacement

Angle obtained through:

- geometric reconstruction

Primary reference:

- instrument geometry

## Quadrant

Measures:

- angular position

Angle obtained through:

- direct reading

Primary reference:

- gravity

These complementary approaches provide an opportunity to compare systematic error, random error, calibration procedures, and measurement uncertainty.

------------------------------------------------------------------------

# Design Philosophy

The Kepler quadrant follows the same design philosophy as the cross-staff.

The instrument should be:

- inexpensive
- easy to construct
- mechanically understandable
- easily repairable
- sufficiently accurate for scientific investigation

Construction decisions favor simplicity over historical authenticity whenever those goals conflict.

Historical inspiration informs the design but does not constrain it.

------------------------------------------------------------------------

# Expected Accuracy

The attainable accuracy of a quadrant depends upon numerous factors including:

- scale resolution
- plumb-line stability
- observer technique
- sighting precision
- construction quality
- environmental conditions

Rather than assuming a theoretical accuracy, Kepler characterizes each instrument empirically through calibration.

Calibration therefore measures the combined performance of the complete observer–instrument system.

------------------------------------------------------------------------

# Sources of Uncertainty

Important contributors include:

- scale reading error
- plumb-line oscillation
- imperfect sight alignment
- instrument flexure
- graduation accuracy
- observer repeatability
- atmospheric conditions

These uncertainties are expected to differ from those encountered with the cross-staff, providing an opportunity to compare two fundamentally different measurement systems.

------------------------------------------------------------------------

# Relationship to the Kepler Data Model

The quadrant is expected to require a new observation specification while remaining compatible with the existing survey metadata, validation workflow, and repository organization.

If successful, this demonstrates that the Kepler data architecture separates instrument-specific measurements from the common scientific workflow.

------------------------------------------------------------------------

# Future Work

Subsequent documents will describe:

- detailed construction
- bill of materials
- calibration procedures
- calibration campaign
- observation specification

# Further Reading

Readers interested in the history and development of quadrants may find the following resources useful.

## Historical Astronomical Instruments

- Jim Bennett, *The Divided Circle: A History of Instruments for Astronomy, Navigation and Surveying.*
- Derek J. de Solla Price, *Precision Instruments: To 1500.*

## Online Resources

- **Smithsonian National Museum of American History – Astronomical Quadrant**\
  A detailed description of an eighteenth-century astronomical quadrant used for measuring stellar altitudes. Includes photographs and historical context.\
  <https://americanhistory.si.edu/collections/object/nmah_1132007> :contentReference[oaicite:0]{index="0"}

- **Smithsonian National Museum of American History – Tycho Brahe Quadrant Replica**\
  A replica of one of Tycho Brahe's astronomical quadrants together with historical notes on its construction and use.\
  <https://americanhistory.si.edu/collections/object/nmah_1455781> :contentReference[oaicite:1]{index="1"}

- **National Park Service – The Quadrant**\
  A concise introduction to the navigational quadrant, its operation, and its relationship to later instruments such as the sextant.\
  <https://www.nps.gov/articles/000/quadrant.htm> :contentReference[oaicite:2]{index="2"}

- **Smithsonian – Surveying and Navigational Instruments**\
  An overview of historical astronomical and surveying instruments, including Gunter quadrants and related trigonometric devices.\
  <https://www.si.edu/spotlight/trigonometry-in-the-plane/planine-trigonometry-surveying> :contentReference[oaicite:3]{index="3"}

## History of Scientific Observation

- J. L. Heilbron, *The Sun in the Church.*
- David S. Landes, *Revolution in Time.*
