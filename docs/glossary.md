# Celestial Coordinate Systems

## Purpose

To make scientific observations, we must be able to describe where an object appears in the sky.

Celestial coordinate systems provide a common language for recording those positions.

Understanding these systems is essential because astronomical instruments do not measure "coordinates." They measure observable quantities that can be used to infer coordinates.

---

# The Problem

Suppose someone points to a bright star and says:

> "It's over there."

The description is meaningful only to someone standing in the same place at the same time.

Scientific observations require a description that can be communicated, reproduced, and compared across observers.

A coordinate system solves this problem.

---

# The Celestial Sphere

The celestial sphere is an imaginary sphere of arbitrarily large radius centered on the observer.

Every visible celestial object is projected onto this sphere.

Although stars lie at vastly different distances, they appear as points on the celestial sphere when describing their directions.

The celestial sphere is therefore a geometric model rather than a physical object.

---

# The Horizontal Coordinate System

The most intuitive coordinate system is based on the observer.

Two coordinates describe every visible object.

## Altitude

Altitude is the angle above the local horizon.

- Horizon = 0°
- Zenith (directly overhead) = 90°

Altitude answers:

> How high above the horizon is the object?

---

## Azimuth

Azimuth measures direction around the horizon.

It answers:

> Which direction should I face?

The exact convention varies, but Kepler will adopt a single published convention for all observations.

---

## Advantages

- Easy to understand.
- Directly related to observation.
- Natural for many simple instruments.

---

## Limitations

The horizontal coordinate system depends on:

- observer location;
- observation time.

As the Earth rotates, the coordinates of every celestial object continually change.

The same star therefore has different horizontal coordinates throughout the night.

---

# The Equatorial Coordinate System

Astronomers often require a coordinate system that does not depend on the observer's local horizon.

Instead, they project Earth's rotation axis and equator onto the celestial sphere.

This produces the equatorial coordinate system.

---

## Declination

Declination is analogous to geographic latitude.

It measures how far north or south of the celestial equator an object lies.

Declination is measured in degrees.

---

## Right Ascension

Right ascension is analogous to geographic longitude.

Instead of degrees, it is traditionally measured in hours, minutes, and seconds.

Twenty-four hours of right ascension correspond to one complete rotation around the celestial equator.

---

## Advantages

Unlike horizontal coordinates, equatorial coordinates remain essentially fixed for celestial objects over ordinary observing times.

They provide a common reference system for astronomical catalogs and maps.

---

# Instruments and Coordinates

Different astronomical instruments measure different physical quantities.

For example:

| Instrument | Direct measurement |
|------------|--------------------|
| Cross-staff | Angular separation |
| Quadrant | Altitude |
| Gnomon | Solar altitude from shadow geometry |
| Telescope | Direction of pointing |

These measurements are not themselves celestial coordinates.

Instead, they provide information from which celestial coordinates may be inferred.

---

# Kepler

Kepler is interested in the complete scientific process.

Rather than beginning with celestial coordinates, the project begins with observations.

```text
Sky
    ↓
Instrument
    ↓
Measurement
    ↓
Coordinate inference
    ↓
Scientific inference
```

Understanding how measurements become coordinates is one of the central themes of the project.

Future documents describe the geometry, calibration procedures, and inference methods that connect raw observations to the celestial coordinate system.