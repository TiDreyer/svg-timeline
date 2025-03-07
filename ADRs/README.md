# Architectural Decision Records
This directory contains the Architectural Decision Records (ADRs) for this project.

## What is an ADR?
The purpose of an ADR is to document architectural decisions that are important for a software project
in a lightweight, approachable way.
They help developers to understand (and remember) decisions that guide the structure of this project
along with the **contex** of the decision process and **reasoning** behind them.

An ADR should:
- be short (max ~1 page if printed)
- clearly describe **one** structural decision
- give context and justify the decision

See also [adr.github.io](https://adr.github.io/) for more general information on the concept.

## Which decisions need to be documented?
This is subjective to some degree, but in general aim to document decisions that:
- Every developer should be aware of
- Whose consequences are not immediately obvious
- Whose justification is not immediately obvious
- Have long term consequences
- Differentiate the project from similar ones

## Which form do ADRs take?
The focus of ADRs is to have a lightweight approach to documentation,
therefore too much formal overhead would be counterproductive.

The following conventions should be followed in this project:
- Every ADR should be contained in a single Markdown file
  - (figures might be linked from other files if necessary)
- The file is named with a running number and a short title
- The file should roughly be structured like this:
  - A short, expressive title 
  - The state of the document, e.g. `valid`, `invalid`, `superseeded by XXX`, `refined by XXX`, ...
  - A 1-2 sentence description of the decision
  - A section with relevant context information
  - A section justifying the decision
  - A section describing consequences of the decision

Also take a look at the already existing ADRs for examples.

All of these are **guidelines** and can be broken, if there is a reasonable need for another format.
