# Historical Inspiration

The Kepler Cross-staff draws inspiration from the historical Jacob's staff used by astronomers, navigators, and surveyors from the late medieval and early modern periods.

The historical instrument demonstrated that careful observers could convert visual alignments into quantitative angular measurements using only simple geometry.

The Kepler Cross-staff does **not** seek to reproduce any specific historical design.

Instead, it preserves the underlying geometric principle while adapting the mechanical implementation to improve accessibility, repeatability, ease of construction, and iterative refinement.

Historical authenticity is therefore considered secondary to scientific utility and educational value.

------------------------------------------------------------------------

# Reference Implementation (Prototype 0.2)

The current reference implementation consists of:

- a wooden yardstick serving as the longitudinal staff;
- a wooden paint stir stick serving as the movable crosspiece;
- a lightweight cardboard sleeve providing a sliding carriage;
- permanently mounted cardboard fiducials defining multiple measurement ranges;
- a measurement index aligned with the fiducial plane.

The prototype currently supports three fiducial separations:

| Fiducial | Separation | Intended Scale               |
|----------|-----------:|------------------------------|
| Outer    |      14 in | Large angular separations    |
| Middle   |       4 in | Moderate angular separations |
| Center   |    0.25 in | Small angular separations    |

The center fiducial consists of a single V-notched element whose inward-facing points define the measurement span.

These dimensions are considered provisional pending calibration and field testing.

------------------------------------------------------------------------

# Engineering Decisions

Several design decisions distinguish the Kepler Cross-staff from many historical implementations.

## Sliding Sleeve

Prototype 0.1 used binder clips as the sliding mechanism.

Testing demonstrated excessive friction and poor usability.

Prototype 0.2 replaces this mechanism with a folded cardboard sleeve that:

- slides smoothly;
- resists rotation;
- is inexpensive to construct;
- is easily replaced if worn.

The sleeve is regarded as a consumable precision component rather than a permanent structural element.

## Fixed Fiducials

Rather than interchangeable crosspieces, the reference implementation employs permanently mounted fiducials providing multiple measurement ranges on a single crosspiece.

This design:

- reduces setup time;
- eliminates loose components during field observations;
- simplifies construction;
- permits rapid selection of measurement range.

## Fiducial Geometry

Triangular cardboard fiducials define measurement endpoints using sharp inward-facing points.

The center measurement range is implemented using a single V-notched component whose opposing points define a narrow measurement span.

This geometry was adopted because preliminary testing suggested that pointed fiducials provide more consistent visual alignment than broad edges.

Further evaluation is planned during calibration.

## Design Philosophy

Mechanical simplicity is preferred whenever it does not compromise scientific usefulness.

Components should be:

- inexpensive;
- easily fabricated;
- replaceable;
- understandable by inspection.

Engineering improvements should clarify the measurement process rather than obscure it.

The reference implementation is expected to evolve through repeated observation, calibration, and field experience.

## Further Reading

Readers interested in the historical development of the cross-staff may wish to consult:

- **The Mariners' Museum and Park** — [Cross-Staff](https://exploration.marinersmuseum.org/object/cross-staff/)
- **Museo Galileo** — [Cross-staff (Bacolo / Jacob's Staff)](https://catalogue.museogalileo.it/indepth/Crossstaff.html)
- **Mathematical Association of America** — [Bridging the Gap Between Theory and Practice: Astronomical Instruments](https://old.maa.org/press/periodicals/convergence/bridging-the-gap-between-theory-and-practice-astronomical-instruments-design-and-construction-of)
- **NASA, archived** — [The Cross Staff](https://pwg.gsfc.nasa.gov/stargaze/Scrostaf.htm)
