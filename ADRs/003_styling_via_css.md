# Styling plots via CSS
ADR state: **valid**

## Description
The main method to style plot elements is assigning classes and styling them in CSS.

## Context
Since SVG is a W3C standard based on XML, similar to HTML, it also allows to apply style choices via CSS.
This includes line weights, colors, fonts, etc.

## Justification
By assigning classes to SVG elements and styling them via CSS,
styles can be applied in a consistent way to all plot elements.
Since many developers are familiar with CSS notation, this also allows for a more intuitive user experience.

## Consequences
- where possible, style is defined and CSS and applied via classes to the SVG elements
- plot properties that cannot be defined in CSS (such as canvas size) will require a different mechanism to set them
