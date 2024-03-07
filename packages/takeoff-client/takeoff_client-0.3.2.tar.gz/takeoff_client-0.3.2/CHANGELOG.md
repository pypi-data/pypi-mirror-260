# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

## [0.3.2] - 2024-03-01

### Added

- Support for management api endpoints

## [0.2.0] - 2024-02-19

### Added

- add support for image to text models, by adding an `image_path` keyword argument to the `generate` method. 

### Changed
- Changed default value for embedding endpoint from `'embed'` to `'primary'` to match takeoff defaults.

## [0.1.0] - 2024-02-07

### Added

- add classify to the takeoff client to match the new endpoint

## [0.0.4] - 2024-01-06

### Added

- add sseclient-py dependency into pyproject.toml 


## [0.0.3] - 2024-01-05

- initial release
- add takeoff python client, publishing on [PyPI](https://pypi.org/project/takeoff-client/)

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
