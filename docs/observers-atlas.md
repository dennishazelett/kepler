# Observer's Atlas

## Purpose

The purpose of this document is to explain how observations collected with Kepler instruments become positions in an Observer's Atlas.

This document is intentionally practical.

It does not attempt to teach celestial mechanics or derive the mathematics of astronomical coordinate systems. Those topics are valuable and are explored elsewhere within the project.

Instead, it describes the standard workflow used by Kepler to transform careful observations into atlas coordinates.

------------------------------------------------------------------------

# Why Coordinates?

Observations made with a cross-staff or quadrant describe what you see from one place at one particular moment.

An Observer's Atlas, however, is intended to grow over months and years.

To compare observations made on different nights—or by different observers—we require a coordinate system that remains fixed with respect to the stars rather than the observer.

For this reason, Kepler adopts the **equatorial coordinate system** using:

- Right Ascension (RA)
- Declination (Dec)

You do not need to become an expert in celestial coordinates before beginning your atlas.

Like latitude and longitude on Earth, these coordinates become familiar through use.

------------------------------------------------------------------------

# What You Measure

Kepler instruments measure observable quantities.

Examples include:

- angular separation between objects;
- altitude above the horizon;
- observation time;
- observing location.

These are your primary observations.

They remain the canonical scientific record.

------------------------------------------------------------------------

# What Goes Into the Atlas

The Observer's Atlas stores positions in an equatorial coordinate system.

These coordinates are not primary observations.

They are **derived quantities** computed from your observations.

This distinction is fundamental to the Kepler data philosophy.

Observations remain immutable.

Atlas coordinates may improve as better observations become available.

------------------------------------------------------------------------

# Two Approaches

Kepler supports two complementary approaches for determining atlas coordinates.

## Method A — Manual Coordinate Determination

Participants who wish to understand celestial geometry in greater depth may determine Right Ascension and Declination directly from their observations.

This approach may involve:

- astronomical reference tables;
- spherical geometry;
- celestial navigation methods;
- historical astronomical techniques.

It provides deeper insight into the construction of astronomical coordinate systems and closely resembles historical observational astronomy.

Future Kepler investigations will explore these methods in detail.

------------------------------------------------------------------------

## Method B — Kepler Coordinate Helper

Participants may instead use Kepler's coordinate conversion tools.

In this workflow, you still perform every scientific observation yourself.

You are responsible for:

- identifying the object;
- measuring it carefully;
- recording the observation time;
- recording the observing location;
- documenting uncertainty.

Kepler then transforms those observations into an estimated Right Ascension and Declination suitable for plotting in your Observer's Atlas.

The software performs the coordinate transformation.

The scientific observation remains entirely yours.

------------------------------------------------------------------------

# Which Method Should I Use?

Both approaches are scientifically valid.

Neither is considered more correct.

They simply emphasize different learning objectives.

If your primary goal is to learn the sky and begin constructing your Observer's Atlas, the Kepler Coordinate Helper is recommended.

If you are interested in celestial geometry or historical astronomical methods, you are encouraged to determine coordinates manually.

Many participants will naturally begin with the Kepler helper and later revisit earlier observations using manual methods.

------------------------------------------------------------------------

# Building the Atlas

Once an object's coordinates have been determined, either manually or with the Kepler Coordinate Helper, the object can be added to your Observer's Atlas.

An atlas entry should include:

- object identifier;
- estimated Right Ascension;
- estimated Declination;
- date of first observation;
- supporting observations;
- observational notes;
- uncertainty.

Whenever the object is observed again, the new observation should be added rather than replacing earlier ones.

The atlas therefore becomes richer with time.

------------------------------------------------------------------------

# A Living Atlas

The Observer's Atlas is not a reference chart.

It is a living scientific record.

Each position in the atlas is supported by observations collected by the observer.

Repeated observations improve confidence, reveal uncertainty, and document the gradual development of the observer's understanding.

The stars themselves remain essentially fixed.

Your understanding of them does not.

------------------------------------------------------------------------

# Looking Ahead

As the Kepler project evolves, participants may choose to:

- determine coordinates manually;
- compare manual and software-derived coordinates;
- combine personal observations with community observations;
- construct probabilistic representations of celestial positions;
- compare their atlas with those created by other observers.

The Observer's Atlas is therefore not simply a map.

It is the evolving representation of an observer's scientific experience.

------------------------------------------------------------------------

# Further Reading

- Celestial Coordinate Systems
- Observer's Atlas
- Measurement Model
- Foundational Investigation: Build Your Observer's Atlas

Future Kepler documentation will provide additional resources for participants interested in the mathematical foundations of astronomical coordinate systems.

## Software Ecosystem

The Observer's Atlas is intended to remain independent of any particular software implementation.

Several mature open-source astronomy libraries already provide high-quality support for celestial coordinate systems, coordinate transformations, ephemerides, and sky plotting. Rather than reimplementing these capabilities, future Kepler software will build upon established community libraries where appropriate.

The table below summarizes several libraries that may support future development.

| Library | Language | Primary Strengths | Potential Role in Kepler |
|----|----|----|----|
| **Astropy** | Python | Standard astronomy library; celestial coordinate systems; coordinate transformations; FITS/WCS support | Canonical coordinate transformations, atlas generation, coordinate helper |
| **Astroplan** | Python | Observation planning and visibility calculations | Guided observing campaigns, planning observations |
| **Skyfield** | Python | High-precision ephemerides and planetary positions | Planetary investigations, simulation, validation |
| **Matplotlib** | Python | Scientific plotting | Atlas rendering and visualization |
| **celestial** | R | Basic astronomical coordinate calculations | Exploratory analyses and teaching examples |
| **oce** | R | Spherical geometry and navigation utilities | Coordinate demonstrations and educational examples |
| **mapproj** | R | Cartographic projections | Experimental atlas projections (e.g., stereographic) |

At present, Kepler does not require any particular software library. The Observer's Atlas is defined by its underlying data model rather than by the software used to construct or visualize it.
