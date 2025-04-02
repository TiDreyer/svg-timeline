# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added

### Changed

### Fixed

### Removed


## [0.2.2] - 2025-04-02

### Added
- TimeSpacing classes based on weeks, hours, minutes and seconds (#16)
- This changelog (#17)

### Changed
- `TimeLinePlot` uses `<g>` to group related SVG elements (#17)

### Fixed
- For better compatibility, colors are no longer defined in CSS via `:root` (#19)
- For better compatibility, the background color is no longer defined in CSS via `svg` (#19)


## [0.2.1] - 2025-03-04

### Fixed
- `TimeSpacingPerDay` threw an exception when counting into the next year (#15) 


## [0.2.0] - 2025-03-04

### Added
- Connected events as a new entry type (#13)

### Changed
- CSS is used for most styling options (#12)

### Removed
- Removed support for python versions < 3.11 (#14)


## [0.1.3] - 2025-02-10
First version that was packaged and published to PyPI (#9)
