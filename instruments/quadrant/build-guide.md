---
title: "Quadrant Build Guide"
author: "Kepler Project"
output:
  pdf_document:
    toc: true
    number_sections: true
    fig_caption: true
---

This document describes the construction of the Kepler reference quadrant.

The objective is to produce an inexpensive, robust, and repeatable instrument suitable for astronomical observation and educational use. The reference design intentionally favors accessibility, mechanical simplicity, and measurement quality over historical authenticity.

The first Kepler quadrant is intended to be constructible using inexpensive materials available from hardware, craft, office supply, or general retail stores.

A reference schematic is provided in:

- `figures/quadrant-front.svg`

------------------------------------------------------------------------

# Design Objectives

The completed instrument should be:

- inexpensive
- easy to construct using common tools
- mechanically robust
- easy to calibrate
- comfortable to use
- sufficiently accurate for scientific investigation
- easily reproducible by independent builders

Preference is given to repeatability and simplicity over historical fidelity.

------------------------------------------------------------------------

# Reference Design

The reference quadrant consists of:

- a rigid cardboard body
- a printed protractor or printed quadrant scale
- a narrow cardboard sight shelf
- a tube sight mounted to the rear surface
- a reinforced plumb-line pivot
- a plumb line with attached weight

Unlike many educational quadrants, the structural body is **not** cut to the outline of the printed scale. Instead, the printed scale is mounted to a rigid substrate that provides stiffness and a stable reference for the sighting system.

The lower right corner of the body is chamfered to provide clearance for the plumb bob while preserving the strength of the instrument.

Figure \@ref(fig:quadrant-ref) illustrates the Kepler reference quadrant described in this guide.

![Kepler reference quadrant. Hidden features are shown with dashed lines.](images/quadrant-front.pdf){width="3.5in" height="4in"}

------------------------------------------------------------------------

# Materials

## Structure

Recommended:

- corrugated cardboard
- laminated cardboard

Additional layers may be laminated together to increase stiffness.

Whenever possible, use an existing machine-cut straight edge (for example from a cardboard box) as the **top edge** of the instrument. This edge serves as the primary alignment reference for the sighting system.

## Angular Scale

Recommended:

- printed paper protractor
- printed paper quadrant

The printed scale should be mounted so that the straight edge of the quadrant is precisely parallel to the top edge of the instrument.

The printed sheet need not be trimmed provided that the graduations remain fully visible.

## Sighting Mechanism

Recommended:

- plastic drinking straw
- metal drinking straw
- rigid plastic tube

The sight tube is mounted to the **rear face** of the instrument immediately beneath the sight shelf using a full-length glue joint.

Mounting the tube to the rear surface provides:

- improved rigidity
- increased bonding area
- reduced rotational movement
- consistent alignment with the sight shelf

## Sight Shelf

The sight shelf is a narrow strip of cardboard attached along the top edge of the instrument.

Its purpose is to provide a straight mechanical reference that aligns and supports the rear-mounted sight tube.

The shelf is not intended as a facial reference or handle.

## Pivot

Recommended:

- small metal paper eyelet

The eyelet reinforces the pivot while providing a durable bearing surface for the plumb line.

A small margin of cardboard should remain above the printed quadrant so that the eyelet is installed within the body of the instrument rather than through the joint between the body and sight shelf.

## Plumb Line

Recommended:

- braided nylon cord
- fishing line
- fine synthetic cord

The plumb line should hang freely without interference.

## Plumb Bob

Possible options include:

- steel washer
- hex nut
- small brass weight

The weight should hang below the bottom edge of the instrument throughout the intended measurement range.

------------------------------------------------------------------------

# Adhesives

Recommended:

- PVA (white glue or wood glue)

Glue should be applied over the full contact surface wherever practical.

The design intentionally avoids adhesive-dependent metal reinforcement. The paper eyelet provides the required mechanical reinforcement.

------------------------------------------------------------------------

# Required Tools

Typical tools include:

- scissors or utility knife
- ruler
- printer
- glue
- hole punch or awl
- eyelet setting tool

------------------------------------------------------------------------

# Construction Overview

1.  Prepare a rigid cardboard body with a straight machine-cut top edge.
2.  Attach the sight shelf to the top edge.
3.  Print the quadrant scale.
4.  Glue the printed scale to the front face, ensuring its straight edge is parallel to the top edge of the body.
5.  Allow the assembly to dry under weight to minimize warping.
6.  Install the paper eyelet at the vertex of the printed quadrant.
7.  Mount the sight tube to the rear face immediately beneath the sight shelf.
8.  Thread the plumb line through the eyelet.
9.  Attach the plumb bob.
10. Verify that the plumb line swings freely throughout the measurement range.
11. Perform calibration.

------------------------------------------------------------------------

# Design Rationale

## Structural Body

The body functions as the structural element of the instrument rather than as a decorative outline.

This design:

- increases stiffness
- simplifies construction
- minimizes unnecessary cutting
- provides generous mounting surfaces
- improves long-term durability

## Printed Scale

The angular scale is treated as a replaceable component rather than part of the structure.

This permits inexpensive replacement if damaged.

## Straight Top Edge

The top edge is the primary geometric reference for the instrument.

Using a factory-cut edge improves alignment of both the sight shelf and the sight tube.

## Rear-Mounted Sight

The sight tube is mounted behind the body using a full-length glue joint.

This provides greater rigidity and repeatability than edge-mounted designs.

## Sight Shelf

The sight shelf mechanically aligns the sight tube while protecting it from rotation during use.

## Eyelet Pivot

A paper eyelet provides:

- repeatable pivot geometry
- reduced wear
- improved durability
- mechanical reinforcement without relying on glued metal joints

## Clearance Chamfer

The lower right chamfer allows the plumb bob to swing freely at shallow elevation angles while preserving nearly all of the body's structural rigidity.

------------------------------------------------------------------------

# Calibration

No quadrant should be considered complete until it has undergone a documented calibration campaign.

Calibration procedures are described in:

- `calibration.md`

------------------------------------------------------------------------

# Future Revisions

Future prototypes may investigate:

- alternative body materials
- laminated versus single-layer construction
- alternative sight tube materials
- alternative plumb bobs
- precision instrument variants using machined components

The reference design should remain inexpensive and widely reproducible even as more advanced variants are developed.
