# Output timelines as SVG files
ADR status: **valid**

## Description
The timeline plots generated with this library will be saved as SVG files.

## Context
The goal of this library is to create timeline plots,
i.e. graphics where data points (e.g. text, images, etc.) are positioned on the drawing plain
depending on their associated dates.
This requires the abilities to:
- draw simple lines and shapes on the graphic
- place text in the graphic
- include images in the graphic
- control visual properties of these elements, such as line widths, colors, font families, etc.

## Justification
SVG is a text-based (XML-)file format that gets rendered by the opening software (e.g. web browsers or image viewers).

### Positives
- SVG is an open and well documented standard
- the XML-based file format allows for file creation via simple string manipulations
- the SVG standard defines primitives like `path`, `circle`, `rect` etc. that can be combined to form the desired elements
- as vector graphics, SVG files are scalable without loss of image quality

### Negatives
- different renderers might interpret the same file differently
- some older software can not work directly with SVG (e.g. old PowerPoint versions)

## Consequences
- this library can create simple plots without any dependencies on image manipulation libraries
- for some applications, the plots might need to be converted to other formats using third party software

## References
- [W3C standard for SVG](https://www.w3.org/TR/SVG2/)
- [MDN documentation for SVG](https://developer.mozilla.org/en-US/docs/Web/SVG)
