# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

* Incident.py - dropping all of the 'stage' search bits from tktFilter() because 
  that field doesn't exist in SNOW (it's left over from Remedy-land)

## [1.2.3] - 2019-03-20

### Added

* CHANGELOG.md - standardizing on a single changelog file

### Changed

* Makefile.local - now includes Pypi (pip) bindings
* setup.py, omdclient.spec - re-worked for setuptools instead of distutils.core
* README.md - lots of updates on the path towards real distribution

