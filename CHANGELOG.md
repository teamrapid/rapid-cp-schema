# Changelog

All notable changes to the schema and its documentation are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions are those of the schema
(`version` in `rapid_cp_schema.yaml`). While the schema is 0.x, a minor version can break CP
files and a patch version cannot. Breaking changes are marked **Breaking**.

Each pull request that changes the schema, the documentation or the examples adds a line under
"Unreleased". A release moves those lines under the new version (see
[CONTRIBUTING.md](CONTRIBUTING.md#releases)).

## [Unreleased]

### Added

- This changelog, and a written release process in `CONTRIBUTING.md`.
- **Breaking:** `disease.disease_entity_id`, required: the disease entity's opaque RAPID id,
  `RAPID` + six digits (#4).
- Results-file specification v1.1, with its Frictionless schema and example file (#4).

### Changed

- The OMOP 5.4 guide no longer names the current schema version; it links to this changelog.
- **Breaking:** `cp_id` renamed `cp_name`. The name starts with the disease entity id instead of
  the lowercase Mondo id, e.g. `RAPID000123-xlh_L1_v1.0`, so it doesn't change when a Mondo id is
  obsoleted or merged (#4).
- Results file: `cp_name` follows the new CP name format in specification v1.1. Version 1.0 is
  no longer accepted and it has been used only for testing purposes (#4).
- **Breaking:** `specificity_grade` is now the enum `SpecificityGrade`, written `S1` to `S5`
  instead of the integers 1 to 5, with a definition for each grade. The OMOP 5.4 guide lists the
  grades with examples in §4.4 (#11).

## [0.2.0] - 2026-11-10

First release of the schema as the public contract for RAPID computable phenotypes (#5).

### Added

- Guide: [Applying RAPID CP files in OMOP 5.4](https://teamrapid.github.io/rapid-cp-schema/applying-cps-omop54/),
  including the rules a valid CP file follows.
- [Results-file specification v1.0](https://teamrapid.github.io/rapid-cp-schema/results-file-spec/),
  with a Frictionless schema and an example file.
- A description for every class and enum in the schema.

### Changed

- **Breaking:** `specificity_tier` renamed to `specificity_grade` (values unchanged, 1 to 5;
  written S1 to S5 in prose).

### Removed

- **Breaking:** `status` and `CPStatus`.
- **Breaking:** `sites_tested` and `SiteTest`.
- **Breaking:** `CPBuild`, `SiteProfile`, `HistoryConcept`, `DataModel` and `SqlDialect`. Build
  and site files are no longer part of the public schema.

[Unreleased]: https://github.com/teamrapid/rapid-cp-schema/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/teamrapid/rapid-cp-schema/releases/tag/v0.2.0
