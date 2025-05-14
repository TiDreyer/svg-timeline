# CSS Class Name Convention
ADR state: **valid**

## Description
When creating its SVG representation, every timeline element sets the following classes on the SVG elements:
- A class representing the type of timeline element, e.g. `event`
- An (optional) class `cXX`, where `XX` refers to the configured color number in the current palette
- An (optional) class classifying the svg element as `colored` or `top_text`
- The custom classes set by the user (if any)

## Context
[ADR 003](./003_styling_via_css.md) defined that the main method to style plot elements
is assigning classes and styling them in CSS.
This ADR is meant to allow for a standardized way to define color palettes.

## Justification
This approach allows for a central definition of color palettes that can be
interchanged without modifying other parts of the code.
Elements set their color based on its index within the current palette.
Some elements (like `TimeSpan`) contain text above colored elements,
these elements can set the SVG class `top_text` on this text to style
it in a legible way.

## Consequences
- A new class `ColorPalette` is defined, holding color definitions
- One `ColorPalette` can be used per timeline
- All subclasses of `TimeLineElement`:
  - need to store the index of their color in the used `ColorPalette`
  - need to assign the CSS classes `cXX` and `colored` or `top_text`
