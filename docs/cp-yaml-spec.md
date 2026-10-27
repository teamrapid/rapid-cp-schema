# RAPID CP YAML specification, v0.1.0

The formal schema is `rapid_cp_logic.linkml.yaml`, in the `schema/` folder of the cp-deployment repo. This document explains it, and
is the reference for how each field turns into OMOP SQL.

## 1. The files

"The CP workstream" separates *logic* from *translation*, so a mapping fix and a logic
change are different kinds of edit. Settings that belong to a site rather than a disease
live in their own file. That gives three kinds of file:

| File | Name | Holds | New version when |
|---|---|---|---|
| CP logic | `<disease-id>_<level>_v<major>.<minor>.yaml` | Features (coded evidence) and how they combine | The clinical logic changes |
| Build | `<cp-id>_<datamodel>.b<build>.sql` | The generated SQL for one data model, shared by every site on it | Only the translation changes |
| Site | `<site>_v<version>.yaml` | Everything about running at one site: schemas, vocabulary release, history concepts (§7) | Anything about the site changes |

`<disease-id>` is the lowercase Mondo id without the colon, a hyphen, and the disease's
`slug` (`mondo0010619-xlh`). `<level>` is `L1`, `L2A`, `L2B`, or `L3`. Example:
`mondo0010619-xlh_L1_v1.0.yaml` and `mondo0010619-xlh_L1_v1.0_omop54.b1.sql`.

Everything in a file name is lowercase except the level. This keeps names safe on
case-insensitive checkouts, where two names differing only in case would collide.

Names starting `cluster-` are reserved for cluster CPs, which are not supported yet. They
will be named `cluster-<umbrella-code>_<level>_v<major>.<minor>`, with the umbrella code
lowercase, prefixed with its vocabulary and without dots (e.g. `cluster-icd10e833_L2A_v1.0`).
For now each candidate disease gets its own CP (§5.4).

**Version numbers.** Which part of `v<major>.<minor>` to bump depends on what changed:

- **Major** (`v1.3` → `v2.0`): the CP's structure changes. That means a disjunct, rule or
  score item is added or removed, the level changes, the search mode or cluster changes, or
  a feature's module changes. Major numbers are never reused.
- **Minor** (`v1.0` → `v1.1`): the structure stays the same but details inside it change.
  For example, codes are added to or removed from an existing feature, a threshold or
  `min_distinct_dates` changes, or score points are re-weighted. Minor resets to 0 on a
  major bump.
- **No bump**: only lifecycle or documentation fields change (`status`, `review`, `notes`
  and the others listed in §6). These don't affect which patients are flagged.

Either bump starts the build numbering again at `b1`. **cpsql** doesn't check which part
you bumped; it only checks that a logic change came with a new version (§6).

The CP logic file is not the curation record, which
holds the whole evidence base and review trail.

The CP file never contains OMOP `concept_id`s. Codes are written in their source
vocabularies (ICD-10-CM `E83.31`, SNOMED CT `82236004`, LOINC `2777-1`, RxNorm `2043855`),
and the generated SQL resolves them against each site's own `CONCEPT` table at run time.
That keeps the logic portable across sites and vocabulary releases.

**cpsql** is the command-line tool in the same repo that works with these files. It checks a CP file against this spec and
turns it into the SQL that sites run against their OMOP database. Its commands are:

| Command | What it does |
|---|---|
| `validate CP.yaml` | Checks the CP file against the schema |
| `explain CP.yaml` | Prints, for each feature, which OMOP tables and columns will be searched and how the logic combines them |
| `build CP.yaml` | Writes the build file: the SQL for one data model (§6) |
| `check BUILD.sql CP.yaml` | Confirms a committed build file still matches its CP file and hasn't been hand-edited |
| `render BUILD.sql --site SITE.yaml` | Applies a site file (§7), producing the SQL that site runs |
| `refresh cps/<disease-id>/` | Updates the disease folder's `translation-status.md` and `CHANGELOG.md` (§9) |

## 2. Top-level fields

| Field | Req | Notes |
|---|---|---|
| `cp_id` | ✓ | Must match the file name, `level`, `disease.mondo_id` and `disease.slug` |
| `schema_version` | ✓ | Version of this spec, currently `0.1.0` |
| `title` | ✓ | |
| `disease` | ✓ | `mondo_id` ✓, `slug` ✓ (short lowercase hyphenated name used in file names, e.g. `xlh`), `name` ✓, `included_mondo_ids` (every Mondo id that constitutes the disease entity, `mondo_id` included, as CURIEs; defaults to just `mondo_id`. `mondo_id` stays the primary id and, with `slug`, names the file), `curation_record_version` (version of the curation record for `mondo_id` that this CP was built from) |
| `level` | ✓ | `L1` / `L2A` / `L2B` / `L3` (L3 is declared only; **cpsql** does not generate it) |
| `search_mode` | ✓ | `population` or `cluster` |
| `cluster` | if cluster | `umbrella_codes` (ICD10CM/SNOMED), `candidate_mondo_ids` (documentation only: the other diseases under the umbrella. Each candidate gets its own CP) |
| `status` | ✓ | `draft` (being written) / `testing` (at one or more sites) / `accepted` (at all seed sites) / `refining` (accepted, but showed an underperformance signature and is being revised) / `exemplar-candidate` (no expert-set logic works; held for a future trained model, and **cpsql** won't build SQL for it) / `deprecated` (superseded or withdrawn) |
| `review` | | Clinical sign-off: `reviewer` ✓, `date` ✓, `decision` ✓ (`proceed` / `revise`), `comments`. Recorded only; **cpsql** doesn't block unreviewed CPs |
| `sites_tested` | | Where this CP version has been run: a list of `{site, site_version, build}`, e.g. `{site: unc, site_version: 1, build: mondo0010619-xlh_L1_v1.0_omop54.b1}`. `site` is a lowercase name, `site_version` the site file version used (§7), and `build` must be a build of this CP. Recorded only |
| `provenance` | ✓ | `authored_by`, `authored_date`, `kg_extracted_at` (ISO 8601 timestamp of the KG subgraph extract), `change_note`, `supersedes` |
| `expected_flag_rate` | | The range of patients per 100,000 a correct CP should flag at a site (prevalence × the share of cases diagnosed and coded), from the Expected Flag Rate Pipeline: `low_per_100k`, `high_per_100k`, `basis` ✓ (`measured` / `class_band` / `none`), `source` ✓ (which pipeline run or reference produced it). With `none`, give no numbers; otherwise `high_per_100k` is required and `low_per_100k` can be left out for an open-ended range. A wide range, not a target: feeds the flag-rate gauge |
| `features` | ✓ | Atomic evidence items (§3) |
| `disjuncts` | L1 only | §5.1 |
| `rules` | L2A only | §5.2 |
| `score` | L2B only | §5.3 |
| `absorbed_into` | | The cluster CP that currently handles this disease (e.g. `cluster-icd10e833_L2A_v1.0`); empty once the disease stands alone. Reserved for cluster CPs |
| `notes` | | Free text. |

Each level must carry its own logic block and no other level's block.

## 3. Features

A feature is one piece of evidence. Every feature has an `id` (`f1`, `f2`, …), a `module`,
a `name`, a `specificity_tier` (1 to 5), and one or more `codes`. Some
modules also need a `result` or a `genetic` block. Optional fields:
`hpo_id` (an annotation on phenotype features; it is not queried), `text_terms`
(names and synonyms for Lane 3 NLP; the OMOP generator ignores them), and
`include_personal_history` (§3.2).

A feature can be listed under `features` without being used in any disjunct, rule or score item. Such features are carried for traceability and
never queried.

### 3.1 Code references

```yaml
- {vocabulary: SNOMED, code: "82236004", label: ..., include_descendants: true}
```

`vocabulary` names the code's vocabulary: `ICD10CM`, `SNOMED`, `LOINC` or `RXNORM`. Result
units use a fifth, `UCUM` (e.g. `mg/dL`).
**cpsql** maps each to its Athena `vocabulary_id`. Always quote SNOMED and RxNorm codes, so YAML
reads them as strings rather than numbers.

`include_descendants` controls whether a code also matches the more specific codes beneath
it in its vocabulary's hierarchy. For example, a SNOMED CT disorder with
`include_descendants: true` also matches every subtype of that disorder, and the RxNorm
ingredient burosumab also matches every burosumab product (each strength and formulation).
Without it, only records carrying exactly that code match.

The default depends on where the code is used:

- **A feature's main codes default to true.** Sites often record a more specific code than
  the one you curated, so descendants are usually wanted.
- **Result values and units default to false.** An accepted answer such as `Pathogenic`, or a
  unit such as `mg/dL`, should match only itself.

Set it explicitly on any code to override the default.

How descendants are found depends on the vocabulary. For SNOMED, LOINC and RxNorm codes, **cpsql** looks them up in the site's `CONCEPT_ANCESTOR` table, which lists
every ancestor–descendant pair in the OMOP vocabularies. ICD10CM codes can't be expanded
that way: ICD-10-CM is not a standard vocabulary in OMOP (its codes are source codes that
map to SNOMED CT), so they never appear in `CONCEPT_ANCESTOR`. Instead they expand by code
prefix, which works because an ICD-10-CM code's children all start with it: `E83.3`
matches `E83.30`, `E83.31`, and so on. ICD10CM codes are also normalised to dotted form (`E8331` → `E83.31`),
as a safety net for codes typed without the dot.

### 3.2 Modules, allowed vocabularies, and OMOP routing

The same code-matching logic runs against every table: the codeset is compared with **both**
the standard `*_concept_id` and `*_source_concept_id` columns. Concept ids are unique across
vocabularies, so a standard SNOMED concept matches the standard column and a non-standard
ICD10CM concept matches the source column, with no ambiguity.

| Module | Vocabularies | Default OMOP tables | Extra requirement | What must be true of the row |
|---|---|---|---|---|
| `diagnostic_code` | ICD10CM, SNOMED | `condition_occurrence`, `observation` | none | Code present (ever) |
| `phenotype` (coded) | ICD10CM, SNOMED | `condition_occurrence`, `observation` | none | Code present |
| `phenotype` (measurement) | LOINC | `measurement`, `observation` | `result` | Result meets criterion |
| `diagnostic_test` | LOINC, SNOMED | `measurement`, `observation` | `result` | Result meets criterion (an order is not a finding) |
| `genetic_finding` | LOINC, SNOMED | `measurement`, `observation` | `genetic` | Interpretation and gene match (§3.4) |
| `medication` | RXNORM | `drug_exposure` | none | Any exposure (ingredient expands to products) |
| `procedure` | SNOMED | `procedure_occurrence` | none | Procedure recorded |

`observation` is searched alongside `condition_occurrence` because in OMOP a
concept's `domain_id` decides the table, and many SNOMED findings are Observation-domain.

Searching `observation` doesn't pick up family history. OMOP usually records "family
history of X" in two parts:

- `observation_concept_id` holds a general concept, such as "family history of clinical
  finding";
- `value_as_concept_id` holds the disease X itself.

For coded features, **cpsql** looks for the code only in `observation_concept_id` (and
`observation_source_concept_id`), never in `value_as_concept_id`. So a relative's diagnosis
doesn't flag the patient.

"History of X" records, about the patient's own past condition, are stored the same way,
but they are real evidence for a lifelong rare disease, so **cpsql** counts them. An
`observation` row counts as the patient's own history when both of these hold:

- `value_as_concept_id` is one of the feature's codes, and
- `observation_concept_id` is a personal-history concept: by default SNOMED CT `417662000`
  "History of clinical finding in subject", or any of its descendants.

This is on by default for `diagnostic_code` and coded `phenotype` features. Set
`include_personal_history: false` on a feature to count only direct records. Sites that use
different history concepts can change the list in their site file (§7).

For ICD10CM codes, the site file's `source_value_fallback` (default on) also compares the raw
`*_source_value` string, normalised for case, dots, and whitespace. This catches ETLs that
left `*_source_concept_id` at 0.

A phenotype feature with LOINC codes must be all-LOINC. Put coded (SNOMED/ICD10CM)
phenotypes in a separate feature.

Reference-range operators (`above_ref_high`, `below_ref_low`) route to `measurement` only,
because `observation` has no range columns.

### 3.3 Results

```yaml
result: {kind: numeric, operator: below_ref_low}                 # uses the row's own range_low
result: {kind: numeric, operator: gt, value: 100, units: [{vocabulary: UCUM, code: pg/mL}]}
result: {kind: qualitative, value_concepts: [{vocabulary: LOINC, code: LA6576-8}]}   # Positive
```

A numeric result compares the row's `value_as_number` using one of these operators:

| Operator | Matches when the result is… | Fields needed |
|---|---|---|
| `gt` | greater than `value` | `value` |
| `gte` | greater than or equal to `value` | `value` |
| `lt` | less than `value` | `value` |
| `lte` | less than or equal to `value` | `value` |
| `between` | from `value` to `value_high`, both included | `value`, `value_high` |
| `above_ref_high` | above the upper limit of the normal range recorded on that same row (`range_high`) | none |
| `below_ref_low` | below the lower limit of the normal range recorded on that same row (`range_low`) | none |

The last two use the normal range the lab reported with each result, not a threshold you
set. They only work in `measurement` (the only table with range columns), and a row with
no range recorded doesn't match.

When a numeric threshold has no `units`, the value is compared whatever its unit, and
`cpsql validate` warns about it. The reference-range operators are usually the safest choice,
since they are unit-free and age-appropriate wherever the lab supplies ranges.

### 3.4 Genetic findings

```yaml
codes: [{vocabulary: LOINC, code: "53037-8"}]        # Genetic variation clinical significance
genetic:
  gene_symbol: PHEX
  hgnc_id: HGNC:8918
  interpretations: [{vocabulary: LOINC, code: LA6668-3}, {vocabulary: LOINC, code: LA26332-9}]
  require_gene_text_match: true
```

A row qualifies when its concept is in `codes`, **and** its `value_as_concept_id` is an
accepted interpretation (if any are listed), **and** the gene symbol appears in the row's
source text (`*_source_value`, `value_source_value`, and `value_as_string` on
`observation`). The last condition applies only if `require_gene_text_match` is true.

Core OMOP 5.4 has no place that ties a gene, a variant, and an interpretation together, so
this matching is a heuristic. It flags any variant in the gene with an accepted
interpretation; it can't be restricted to specific variants. Before relying on this module at a site,
confirm that the site's genetics results are loaded as discrete rows at all.

## 4. Counting and persistence: `min_distinct_dates`, `min_span_days`

Disjuncts, rule leaves, and score items can require a feature on N distinct dates
(default 1). **cpsql** counts distinct dates rather than rows, so ETL duplicates don't inflate
the count.

They can also require **persistence** with `min_span_days`: the feature's records must
stretch across at least N days, from the first to the last. This separates a condition that
keeps being recorded from a code entered once in error.

```yaml
- {feature: f2, min_distinct_dates: 2, min_span_days: 90}   # 2+ dates, at least 90 days apart
```

## 5. Logic

### 5.1 Level 1: disjuncts

```yaml
disjuncts:
  - {id: d1, feature: f1}
  - {id: d2, feature: f2, min_distinct_dates: 1}
```

The CP fires if any disjunct fires. Every disjunct must reference a `specificity_tier: 1` feature,
matching the "union of every domain that reaches Tier 1" definition.

### 5.2 Level 2A: rules

```yaml
rules:
  - id: r2
    expr:
      all_of:
        - {feature: f2}
        - any_of: [{feature: f3, min_distinct_dates: 2}, {feature: f4}]
        - none_of: [{feature: f9}]
  - id: r3
    expr: {at_least: 2, of: [{feature: f2}, {feature: f3}, {feature: f5}]}
```

Each `expr` node is exactly one of: `feature`, `all_of`, `any_of`, `none_of` (NOT any),
`at_least`+`of`, or `within` (below). The CP fires if any rule fires. Every rule must contain at least one
positive (non-negated) feature, because a rule made only of `none_of` would match almost
everyone.

**Time windows.** A `within` node requires a record of each listed feature, all falling
within a set number of days of each other:

```yaml
- id: r4
  expr:
    within:
      days: 365
      of: [f2, f5]          # E83.31 and burosumab within a year of each other
```

Add `in_order: true` to require the records in the listed order as well. For example,
the drug started on or after the diagnosis:

```yaml
    within: {days: 365, in_order: true, of: [f2, f5]}    # f2 first, then f5
```

With `in_order`, records on the same day count as in order, and `days` is measured from the
first listed feature to the last. `of` lists feature ids only (at least two), and each
feature's own filters (codes, results, personal history) apply as usual. A `within` node can
be combined with the other nodes like any condition, including inside `none_of` (e.g. "the
diagnosis, but not treated within a year").

`none_of` is available as syntax, but the curated mimic and hard-exclusion modules are not
yet specified.

### 5.3 Level 2B: score

```yaml
score:
  threshold: 4
  items:
    - {id: s1, feature: f2, points: 2}
    - {id: s2, feature: f3, points: 2, min_distinct_dates: 2}
    - {id: s3, feature: f9, points: -3}
```

A person flags when the sum of the points for features they meet reaches `threshold`. The
flag reasons are the items with a non-zero contribution. Negative items appear too, which
makes it visible when an exclusion-like item was outweighed.

### 5.4 Cluster mode

Cluster mode searches only the patients who already carry a broad "umbrella" diagnosis,
instead of the whole database. It is meant for telling apart several diseases that share
an umbrella code. For example, XLH, hereditary vitamin D-dependent rickets and other
disorders all sit under ICD-10-CM `E83.3` (disorders of phosphorus metabolism).

Set `search_mode: cluster` and list the umbrella codes under `cluster.umbrella_codes`:

```yaml
search_mode: cluster
cluster:
  umbrella_codes:
    - {vocabulary: ICD10CM, code: E83.3}
```

**cpsql** then works in two steps:

1. **Build the cluster.** It finds every patient with an umbrella code, searching the same
   tables in the same way as a `diagnostic_code` feature, descendants included (so `E83.3`
   also covers `E83.30`, `E83.31`, …), except that personal-history records don't count. Internally this is handled as a hidden feature with
   the id `u0`. It never appears as a flag reason.
2. **Apply the rules inside the cluster.** Every disjunct, rule or score item is evaluated
   only for patients in the cluster. A patient who meets a rule but has no umbrella code is
   not flagged.

The `counts` statement changes to match: `__denominator__` is the number of patients in
the cluster, not the number of patients in the whole `person` table. The flag rate then
reads as "the share of the cluster that looks like this disease".

Each candidate disease under the umbrella gets its own CP file with the same
`umbrella_codes` (see `candidate_mondo_ids` in §2).

## 6. Build file

The build file is the SQL itself: one file, `<cp_id>_<datamodel>.b<build>.sql`, committed to
GitHub next to the CP file. It serves every site on that data model, because site settings
are applied only when it runs (§7). It has two parts.

**Header.** A YAML block inside SQL comments, between `-- cpsql-build` and
`-- end-cpsql-build`, recording where the SQL came from. It follows the `CPBuild` class in
the schema:

```sql
-- cpsql-build
-- generator: cpsql 0.1.0
-- cp_logic_sha256: be8d8491…        -- fingerprint of the CP logic this SQL came from
-- build_id: mondo0010619-xlh_L1_v1.0_omop54.b1
-- cp_id: mondo0010619-xlh_L1_v1.0
-- datamodel: omop54
-- build: 1
-- change_note: ...
-- end-cpsql-build
```

**Three statements**, each introduced by a `-- ======== @statement <name>` line (§8).

The statements are generated and are never edited by hand. A new build of the same CP
version is only needed when the translation itself changes, for example a new **cpsql**
release:

```bash
cpsql build CP.yaml --from cps/<disease-id>/…b1.sql --note "Regenerated with cpsql 0.2"   # -> …b2.sql
```

Build files are immutable: `cpsql build` refuses to overwrite an existing one. A new CP
version starts again at `b1`.

`cpsql check BUILD.sql CP.yaml` regenerates the statements from the CP file and fails if:

- any statement differs (someone hand-edited the SQL, or a different **cpsql** version wrote it);
- the CP logic's fingerprint no longer matches (the logic changed without a new CP version
  and rebuild).

The fingerprint covers only the fields that decide which patients are flagged: the disease
ids (`mondo_id`, `included_mondo_ids`), `level`, `search_mode`, `cluster`, `features`,
`disjuncts`, `rules` and `score`. Lifecycle and documentation fields (`status`, `review`,
`sites_tested`, `provenance`, `expected_flag_rate`, `title`, `notes`, `absorbed_into`) can be edited without a new
version or build.

Running `check` in the GitHub Action keeps the committed SQL and the YAML logic from drifting
apart.

## 7. Site files

Everything that depends on the site rather than the disease is kept in one file per site,
under `/sites/`, and applied when the SQL runs:

```yaml
site: unc
version: 1
datamodel: omop54
cdm_version: "5.4"
dialect: postgresql
vocabulary_version: v5.0 30-AUG-26      # from the site's VOCABULARY table
cdm_schema: cdm
vocab_schema: vocab
source_value_fallback: true             # also match raw ICD-10-CM strings (§3.2)
personal_history_concepts:              # what marks an observation as the patient's own history
  - {vocabulary: SNOMED, code: "417662000", label: History of clinical finding in subject}
  - {concept_id: 2000001234, label: local history concept}   # an id, used as is
updated: "2026-09-29"
change_note: ...
```

**Versioned.** Any change to a site's settings is a new file, `unc_v2.yaml`, and old versions
are kept. A run is then fully identified by the build and the site file version, which is
what `sites_tested` records. Changing a site file never invalidates a build.

**Applied at run time.** The SQL that sites run comes from `cpsql render`:

```bash
cpsql render cps/<disease-id>/…b1.sql --site sites/unc_v1.yaml                     # whole file
cpsql render cps/<disease-id>/…b1.sql --site sites/unc_v1.yaml --statement counts
```

In the committed SQL each site setting is a marker: an SQL comment followed by a safe
default (e.g. `/*@source_value_fallback*/1`). So the file still parses and runs before rendering,
with the fallback on and no personal-history concepts. Only the schema
names (`@cdm_schema`, `@vocab_schema`) must be filled in. Rendering refuses a site file whose
data model doesn't match the build.

The `codesets` statement is the check that a new site file is right: run it once per new
version to confirm the site's history concepts and vocabulary release resolve. History concepts
given as a code are looked up like any other code; those given as a `concept_id` are listed
as they are, and show `NOT_FOUND` if the id isn't in the site's `CONCEPT` table.

## 8. The three statements

| Statement | Output | Use |
|---|---|---|
| `codesets` | One row per concept each requested code matched, including descendants found through `CONCEPT_ANCESTOR` and ICD-10-CM prefix matches: matched code, concept name, domain, standard flag, invalid reason, status `OK / NOT_FOUND / INVALID / NON_STANDARD_NO_EXPANSION`. A code that matches nothing gets one row, status `NOT_FOUND`. History concepts the site file gives as a `concept_id` also get one row each (feature `ph`, the id as `requested_code`, no vocabulary), so a wrong id shows as `NOT_FOUND` | Run this first at every site. It is the portability pre-check. |
| `flags` | `cp_id, build_id, person_id, criterion_id, first_date, points`: one row per criterion that fired | Which patients the CP found, and which criterion found each one. `criterion_id` is the flag reason. |
| `counts` | Persons per criterion, `__any__`, and `__denominator__`. Every criterion gets a row, including those that flagged nobody (0), and nothing is suppressed: for rare diseases, small counts and zero are the result | How many patients each criterion found at the site. |

`first_date` is the earliest qualifying event among the positive features in the criterion.
It is not necessarily the date the rule first became true (for example, the date a
time window was completed).

## 9. Repository layout

Each disease has its own folder under `/cps/`, named after its disease id. Site files sit
in one `/sites/` folder at the top of the repository (§7).

```
/sites/
  unc_v1.yaml
/cps/
  mondo0010619-xlh/
    mondo0010619-xlh_L1_v1.0.yaml
    mondo0010619-xlh_L1_v1.0_omop54.b1.sql
    mondo0010619-xlh_L2A_v2.0.yaml
    mondo0010619-xlh_L2A_v2.0_omop54.b1.sql
    CHANGELOG.md
    translation-status.md
```

`cpsql build` writes each build next to its CP. `cpsql refresh cps/<disease-id>/` updates
the two Markdown files:

- **`translation-status.md`** is fully generated and rewritten on every refresh, so don't
  edit it by hand. For each data model it shows the newest build, which CP version it was
  built from, and whether it is `current`, `stale` (built from an older CP version than the
  newest one) or fails `cpsql check`.
- **`CHANGELOG.md`** gets one entry per CP version, newest first, with the date, level,
  author, what it supersedes, and its `provenance.change_note`. An entry is generated the
  first time **cpsql** sees that version and is never rewritten afterwards, so people can
  amend it freely. Later refreshes only add entries for new versions.

## 10. Open decisions

These were settled provisionally and need a decision from you:

1. **Genetic data.** Whether sites load variant results as discrete rows determines
   whether `genetic_finding` is a Lane 1 feature at all.
2. **Dialects.** The generated SQL runs on DuckDB and parses as PostgreSQL at the moment. SQL Server
   and Oracle sites would need a translation step, since the SQL uses `||` string
   concatenation.
3. **Vocabularies.** Only ICD10CM, SNOMED, LOINC and RXNORM are admitted for now (plus UCUM
   for units). Candidates to consider adding:
   - CPT4, HCPCS and ICD10PCS for procedures, since US sites often record procedures only in
     these;
   - RxNorm Extension and ATC for medications;
   - OMOP Genomic for genetic findings, if a site loads gene-specific variant concepts.

   Adding one means updating the admitted list in the schema, the allowed vocabularies for
   the relevant modules, and the §3.2 table.
4. **Encounter context (future work).** Only counting a record if it came from a certain
   kind of encounter: an inpatient stay, a specialist, or the problem list rather than a
   billing code. It is one of the briefing's ways to add corroboration when a CP flags too
   many patients. OMOP holds this in `visit_occurrence` (visit type), `provider`
   (specialty) and `*_type_concept_id` (record origin), but how reliably sites fill these
   in varies, so it is deferred until a real CP needs it. It would likely be an optional
   `encounter` filter on a feature.
