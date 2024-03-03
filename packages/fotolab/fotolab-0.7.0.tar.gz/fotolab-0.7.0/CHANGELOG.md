# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [0-based versioning](https://0ver.org/).

## [Unreleased]

## v0.7.0 (2024-03-03)

### Added

- Add `sharpen` subcommand to sharpen image
- Set sharpen parameters through `-r` or `--radius` option
- Set sharpen parameters through `-p` or `--percent` option
- Set sharpen parameters through `-t` or `--threshold` option

## v0.6.1 (2024-02-18)

### Added

- Allow setting of different border width through `-wt`, `-wr`, `-wb`, and `wl`
  option

### Fixed

- Remove extra lines in help message in README.md

## v0.6.0 (2024-02-18)

### Added

- Add `resize` subcommand to resize image

## v0.5.0 (2024-02-11)

### Added

- Add `-od` or `--output-dir` global option to set default output directory
- Add missing types in doc
- Log when saving image

## v0.4.0 (2024-02-04)

### Added

- Add `-o` or `--overwrite` global flag to overwrite modified image

## v0.3.1 (2024-01-28)

### Added

- Add `-w` or `--width` option to `fotolab border` subcommand
- Add `-c` or `--color` option to `fotolab border` subcommand

### Fixed

- Fix border not added to image

## v0.3.0 (2024-01-21)

### Fixed

- Fix incorrect subcommand wording

### Changed

- Ignore `__repr__` in code coverage
- Ignore duplicate code linting rule

### Added

- Add `fotolab border` subcommand to add border for an image
- Test `quiet` flag

## v0.2.0 (2024-01-14)

### Added

- Add `fotolab env` subcommand for debugging and bug reporting purpose

### Fixed

- Fix incorrect metavar for `--font-color`

## v0.1.1 (2024-01-07)

### Added

- Generate project documentation using `sphinx`

### Changes

- Bump project and pre-commit hooks deps

## v0.1.0 (2024-01-01)

### Added

- Initial public release
