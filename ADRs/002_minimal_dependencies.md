# Use minimal dependencies
ADR state: **valid**

## Description
This library should have minimal (ideally no) dependencies on other python libraries.

## Context
The goal of this library is to create timeline plots in a simple, yet customizable way.
The choice of SVG as the output format (see [ADR 001](001_output_as_svg.md)) allows to
do this by combining basic SVG elements like `path`s and `circle`s.

## Justification
While popular python libraries for the creation and manipulation of SVG files exist (e.g. `drawsvg`),
this project uses only a very limited subset of the available SVG features.
This subset can be implemented in a handful of classes in a very simple way,
avoiding the mental load of using a separate libraries API for creating SVGs.
At the same time, SVG is a well established web standard,
therefore no frequent major changes are to be expected.

On a less technical level, the independent implementation of basic functionalities
also makes this side project more fun to work on and provides a larger learning effect.

## Consequences
- this project contains python code that allow for the creation of simple SVG files
- if possible, the inclusion of other python libraries as dependencies will be avoided
