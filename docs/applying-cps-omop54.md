# Applying RAPID CP files in OMOP 5.4

What a computable phenotype (CP) file contains, and how a site applies it to OMOP CDM 5.4 data.
Written by Mendelian for the sites that run RAPID CPs; follows schema 0.2.0.

## 1. About this document

Mendelian shares each computable phenotype (CP) as a YAML file. Each site turns it into queries
on its own OMOP CDM 5.4 data, runs them, and returns counts in the format set by the
[Results-File Specification](results-file-spec.md).

- **What a site receives.** One CP file per CP version. The files follow this repository's LinkML
  schema, `rapid_cp_schema.yaml`, currently version 0.2.0.
- **What is fixed.** What a CP file means: which evidence each feature describes and how features
  combine into a flag (sections 3 to 5).
- **What each site decides.** How it searches its data for that evidence. Section 7 gives
  Mendelian's recommendations for OMOP 5.4. They reflect how Mendelian applies the files, but
  each site knows its own data best. A site that departs from them should tell Mendelian how, so
  results can be compared across sites.
- **What a site returns.** One results file per execution, as the
  [Results-File Specification](results-file-spec.md) describes. Section 8 shows how a CP's logic
  maps onto its rows.

A CP file never contains OMOP concept ids. Every code is written in its source vocabulary
(ICD-10-CM, SNOMED CT, LOINC, RxNorm) and is looked up in the site's own vocabulary tables.

## 2. The files

Each CP version is one YAML file named after its `cp_id`, for example
`mondo0010619-xlh_L2A_v2.0.yaml`.

| `mondo0010619-xlh_L2A_v2.0` | Meaning |
| --- | --- |
| `mondo0010619` | The disease's Mondo id (`MONDO:0010619`) in lowercase, without the colon |
| `-xlh` | A short name for the disease (`disease.slug`) |
| `_L2A` | The level: `L1`, `L2A`, `L2B` or `L3` (section 5) |
| `_v2` | Major version: goes up when the CP's structure changes, such as a criterion added or removed or the level changed |
| `.0` | Minor version: goes up when details inside the structure change, such as codes, thresholds or points |

Everything in the name is lowercase except the level, so two names can't differ only in case and
collide on a case-insensitive file system. Names starting `cluster-` are reserved for future
cluster CPs. They will be named `cluster-<umbrella-code>_<level>_v<major>.<minor>`, with the
umbrella code lowercase, prefixed with its vocabulary and without dots, e.g.
`cluster-icd10e833_L2A_v1.0`.

- **Versions are separate files.** A new version never overwrites an old one. Mendelian tracks
  which versions are published; sites run only published versions.
- **The schema.** `rapid_cp_schema.yaml` defines every field and allowed value. The
  [schema documentation](elements/index.md) describes each class and field.
- **Reading the YAML.** Codes, dates and version numbers are quoted (`"82236004"`,
  `"2026-09-24"`), so they should be read as text, not numbers or dates. A code can otherwise lose
  a leading zero.

Which part of the version goes up depends on what changed:

- **Major** (`v1.3` → `v2.0`): the structure changes. A disjunct, rule or score item is added or
  removed, the level changes, the search mode or cluster changes, or a feature's module changes.
  Major numbers are never reused.
- **Minor** (`v1.0` → `v1.1`): the structure stays the same but details inside it change. For
  example, codes are added to or removed from a feature, a threshold or `min_distinct_dates`
  changes, or score points are re-weighted. Minor goes back to 0 on a major bump.
- **Neither**: only fields that don't affect which patients are flagged change: `title`,
  `review`, `sites_tested`, `provenance`, `expected_flag_rate`, `notes` and `absorbed_into`.

## 3. Top-level fields

Only the fields marked **query** change which patients are flagged. The rest describe the CP and
its history; they can be read but aren't needed to build queries.

| Field | Required | Used by queries | Meaning |
| --- | --- | --- | --- |
| `cp_id` | yes | no | The CP version's name (section 2). |
| `schema_version` | yes | no | Version of the LinkML schema the file follows, currently `0.2.0`. |
| `title` | yes | no | A readable name for the CP. |
| `disease` | yes | no | The disease entity: `mondo_id` (primary Mondo id), `slug`, `name`, `included_mondo_ids` (every Mondo id for the entity, primary included), `curation_record_version`. |
| `level` | yes | query | `L1`, `L2A`, `L2B` or `L3`. Decides which logic block the file carries (section 5). |
| `search_mode` | yes | query | `population`: search everyone. `cluster`: search only patients with an umbrella code (section 5.5). |
| `cluster` | in cluster mode | query | `umbrella_codes`: the codes that define the group searched. `candidate_mondo_ids`: documentation only. |
| `features` | yes | query | The evidence (section 4). |
| `disjuncts`, `rules` or `score` | one, by level | query | The logic (section 5). A file carries only its own level's block. |
| `provenance` | yes | no | `authored_by`, `authored_date`, `kg_extracted_at`, `change_note`, `supersedes` (the version this one replaces). |
| `review` | no | no | Clinical sign-off: `reviewer`, `date`, `decision` (`proceed` or `revise`), `comments`. |
| `expected_flag_rate` | no | no | The range of patients per 100,000 a correct CP should flag: `low_per_100k`, `high_per_100k`, `basis`, `source`. Mendelian compares each site's results against it. |
| `sites_tested` | no | no | Mendelian's record of where this version has run. |
| `absorbed_into` | no | no | Reserved for future cluster CPs. |
| `notes` | no | no | Free text. |

## 4. Features

A feature is one piece of evidence: a set of codes, plus, for tests and measurements, the result
that must be found. A feature listed under `features` but not used by the logic is carried for
the record only and needs no query.

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | `f1`, `f2`, … Referenced by the logic. |
| `module` | yes | The kind of evidence (table below). |
| `name` | yes | A readable name, e.g. "Low serum phosphate". |
| `specificity_grade` | yes | 1 (confirmatory) to 5 (incidental), written S1 to S5 in prose. Level 1 uses only S1 features. |
| `codes` | yes | One or more code references. A record matching any one of them counts. |
| `result` | tests and measured phenotypes | The result that must be found (4.2). |
| `genetic` | genetic findings | The gene and accepted interpretations (4.3). |
| `include_personal_history` | no | Diagnoses and coded phenotypes only. Default `true`: a record of the patient's own history of the condition also counts (section 7.3). |
| `hpo_id` | no | The HPO term a phenotype represents. Annotation only. |
| `text_terms` | no | Names and synonyms for a future text search. Not used for structured queries. |

| Module | Vocabularies | Needs |
| --- | --- | --- |
| `diagnostic_code` | ICD-10-CM, SNOMED CT | — |
| `phenotype` (coded) | ICD-10-CM, SNOMED CT | — |
| `phenotype` (measured) | LOINC | `result` |
| `diagnostic_test` | LOINC, SNOMED CT | `result`; an order alone never counts |
| `genetic_finding` | LOINC, SNOMED CT | `genetic` |
| `medication` | RxNorm | — |
| `procedure` | SNOMED CT | — |

### 4.1 Code references

Each entry under `codes` is written like
`{vocabulary: SNOMED, code: "82236004", label: ..., include_descendants: true}`.

| Field | Meaning |
| --- | --- |
| `vocabulary` | `ICD10CM`, `SNOMED`, `LOINC` or `RXNORM`, plus `UCUM` for result units only. In OMOP these are the `vocabulary_id` values `ICD10CM`, `SNOMED`, `LOINC`, `RxNorm` and `UCUM`. |
| `code` | The code as written in that vocabulary, e.g. `E83.31`. Matches OMOP's `concept_code`. ICD-10-CM codes are dotted; one written without the dot, such as `E8331`, is read as `E83.31`. |
| `label` | Optional, for readers. |
| `include_descendants` | Also match the more specific codes beneath it. Default `true` for a feature's codes, `false` for result values and units. |

### 4.2 Results

A `numeric` result compares the record's value with a threshold; a `qualitative` one accepts
listed answers.

| Operator | Matches when the value is… | Needs |
| --- | --- | --- |
| `gt` / `gte` | above (or equal to) `value` | `value` |
| `lt` / `lte` | below (or equal to) `value` | `value` |
| `between` | from `value` to `value_high`, both included | both |
| `above_ref_high` | above the upper limit of the normal range recorded with that result | — |
| `below_ref_low` | below the lower limit of the normal range recorded with that result | — |

- `units`: UCUM units the threshold applies to, e.g. `{vocabulary: UCUM, code: mg/dL}`. With none
  given, values in any unit are compared. The reference-range operators are usually the safer
  choice: they need no units and are age-appropriate wherever the lab supplies ranges.
- `value_concepts` (qualitative only): the accepted answers, e.g. LOINC `LA6576-8` (Positive).

### 4.3 Genetic findings

- `gene_symbol` (required): the causal gene, e.g. `PHEX`. `hgnc_id`: optional reference.
- `interpretations`: accepted answers, e.g. LOINC `LA6668-3` (Pathogenic), `LA26332-9` (Likely
  pathogenic).
- `require_gene_text_match`: the gene symbol must appear in the record's text. Default `true`
  when the codes are generic LOINC panels.

Any variant in the gene with an accepted interpretation counts; a CP can't name specific variants.

## 5. Logic

The level decides how features combine. Each part of the logic has an id (`d1`, `r2`, `s3`…);
these are the criteria a site reports counts for. Level 3 can be declared but has no logic block
yet, so sites don't receive L3 files to run.

### 5.1 Level 1: disjuncts

A patient is flagged if **any** disjunct is met. Each disjunct names one S1 feature.

```yaml
disjuncts:
  - {id: d1, feature: f1}
  - {id: d2, feature: f2, min_distinct_dates: 2}
```

### 5.2 Level 2A: rules

A patient is flagged if **any** rule's condition holds. Each rule has an `id` (`r1`…), an optional
`label`, and an `expr`. Conditions nest as deeply as needed, and every rule contains at least one
feature that isn't negated, because a rule made only of `none_of` would match almost everyone.

| Form | True when | Example |
| --- | --- | --- |
| `feature` | The feature is present, meeting any date options (5.4) | `{feature: f3, min_distinct_dates: 2}` |
| `all_of` | Every listed condition holds | `{all_of: [{feature: f2}, {feature: f5}]}` |
| `any_of` | At least one listed condition holds | `{any_of: [{feature: f3}, {feature: f4}]}` |
| `none_of` | None of the listed conditions holds | `{none_of: [{feature: f9}]}` |
| `at_least` + `of` | At least N of the listed conditions hold | `{at_least: 2, of: [{feature: f2}, {feature: f3}, {feature: f4}]}` |
| `within` | A record of each listed feature, all within `days` of each other | `{within: {days: 365, of: [f2, f5]}}` |

With `within: {..., in_order: true}`, the records must also fall in the listed order: the first
feature's record on or before the second's, and so on. Records on the same day count as in order,
and `days` is measured from the first listed feature to the last. `of` lists feature ids only.

### 5.3 Level 2B: score

```yaml
score:
  threshold: 4
  items:
    - {id: s1, feature: f2, points: 2}
    - {id: s2, feature: f3, points: 2, min_distinct_dates: 2}
    - {id: s3, feature: f9, points: -3}
```

Each item adds its `points` when its feature is present (meeting any date options); points can be
negative. A patient is flagged when their total reaches `threshold`.

### 5.4 Date options

Any feature reference (a disjunct, a rule's `feature`, a score item) can add:

- `min_distinct_dates`: the feature must appear on at least this many different days (default 1).
  Days are counted, not records, so duplicate records don't count twice.
- `min_span_days`: the feature's records must stretch across at least this many days, from first
  to last. This separates a condition that keeps being recorded from a code entered once in error.

### 5.5 Cluster mode

With `search_mode: cluster`, the first step finds every patient with any of
`cluster.umbrella_codes`, searched like a diagnostic code with descendants included (e.g. `E83.3`
also covers `E83.30`, `E83.31`…), except that records of the patient's own history don't count.
The logic is then evaluated only for those patients: a patient who meets a criterion but has no
umbrella code is not flagged. Each candidate disease under an umbrella has its own CP file with
the same umbrella codes.

### 5.6 Rules a valid CP file follows

A CP file that breaks any of these rules is wrong, even where the schema doesn't reject it yet.

**The file as a whole**

- `cp_id` agrees with the file name, `level`, `disease.mondo_id` and `disease.slug` (section 2).
- `included_mondo_ids`, when given, includes `mondo_id`.
- `supersedes`, when given, is a `cp_id`.
- `schema_version` is a schema version number, e.g. `0.2.0`.
- A `cluster` block is given when `search_mode` is `cluster`, and only then. Umbrella codes are
  ICD-10-CM or SNOMED CT.
- Each level carries its own logic block and no other: `disjuncts` (at least one) for L1, `rules`
  for L2A, `score` for L2B, and none for L3.
- `expected_flag_rate`: with `basis: none`, no numbers are given. Otherwise `high_per_100k` is
  required, `low_per_100k` may be left out for an open-ended range, and `low_per_100k` is not
  above `high_per_100k`.

**Features**

- Feature ids are unique, and so are the ids of disjuncts, rules and score items, since each is
  reported as a criterion.
- Every feature has at least one code, in a vocabulary its module allows (section 4).
  `UCUM` is used for result units only, and units are always `UCUM`.
- SNOMED CT and RxNorm codes are quoted, so YAML doesn't read them as numbers.
- `result` is given where the module needs it (`diagnostic_test`, measured `phenotype`) and not
  elsewhere; `genetic` is given on `genetic_finding` features only.
- A `phenotype` feature with LOINC codes is all-LOINC. A coded (SNOMED CT or ICD-10-CM) phenotype
  goes in a separate feature.
- `include_personal_history` is set only on `diagnostic_code` and coded `phenotype` features.
- `hpo_id` is an HPO term (`HP:…`).
- A `numeric` result has an `operator` and no `value_concepts`. `gt`, `gte`, `lt` and `lte` need
  a `value`; `between` needs `value` and `value_high`, with `value` not above `value_high`;
  `above_ref_high` and `below_ref_low` take neither. `value_high` is used only with `between`.
- A `qualitative` result has `value_concepts` and no `operator`.

**Logic**

- Every disjunct, rule leaf, score item and `within.of` entry names a feature listed under
  `features`.
- Every disjunct names an S1 feature.
- Each `expr` node is exactly one of the forms in section 5.2. `at_least` and `of` come together,
  and `at_least` is not more than the number of conditions in `of`. Lists of conditions are not
  empty.
- `min_distinct_dates` and `min_span_days` are set on a feature reference only, not on a node
  that combines conditions.
- `within.of` lists at least two feature ids.
- Every rule has at least one feature that isn't under `none_of` (section 5.2).

## 6. Applying a CP in OMOP 5.4

A CP becomes counts in six steps. Steps 1 and 3 follow Mendelian's recommendations in section 7;
the others follow directly from the CP file.

1. **Resolve the codes.** For each feature, look up its codes in the site's `CONCEPT` table by
   `vocabulary_id` and `concept_code`, and add the descendants where `include_descendants`
   applies. Do the same separately for result answers (`value_concepts`, `interpretations`) and
   units, and for a cluster CP the umbrella codes. Each feature's concept lists stay separate.
2. **Apply cluster mode.** For a cluster CP, find the patients with an umbrella code first (5.5),
   and search for features only among them. The result is the same, and the searches run over far
   fewer patients.
3. **Find each feature's records.** In the tables for the feature's module, find the records whose
   concept is in that feature's list and, where the feature has a `result` or a `genetic` block,
   whose value qualifies. Each match gives a patient and a date.
4. **Summarise by patient and feature.** For each patient and feature, note the number of distinct
   dates, the first date and, where `min_span_days` is used, the days between the first and last
   record.
5. **Evaluate the logic.** For each patient, decide which disjuncts or rules are met, or add up the
   score (section 5). A patient is flagged when the level's rule says so.
6. **Count.** Count distinct flagged patients, and for each criterion the patients who meet it
   (section 8). The population is counted as the
   [Results-File Specification](results-file-spec.md) defines it.

## 7. Recommended matching rules in OMOP 5.4

These are recommendations and following them keeps
results comparable across sites.

### 7.1 Where to search

| Module | Tables to search | Date of a record |
| --- | --- | --- |
| `diagnostic_code`, `phenotype` (coded) | `condition_occurrence`, `observation` | `condition_start_date`, `observation_date` |
| `phenotype` (measured), `diagnostic_test`, `genetic_finding` | `measurement`, `observation` | `measurement_date`, `observation_date` |
| `medication` | `drug_exposure` | `drug_exposure_start_date` |
| `procedure` | `procedure_occurrence` | `procedure_date` |

Why `observation` too: OMOP files a record by its concept's domain, and many SNOMED CT findings
belong to the Observation domain. A result using `above_ref_high` or `below_ref_low` should search
`measurement` only, since only it records normal ranges.

### 7.2 Matching codes

- **Both concept columns.** A record should match when either its standard concept
  (`*_concept_id`) or its source concept (`*_source_concept_id`) is in the feature's list. This
  finds a SNOMED CT code where OMOP stores it and an ICD-10-CM code as the site recorded it.
- **Descendants of SNOMED CT, LOINC and RxNorm** should come from the site's `CONCEPT_ANCESTOR`
  table. An RxNorm ingredient then matches every product containing it.
- **ICD-10-CM by prefix.** ICD-10-CM isn't a standard vocabulary in OMOP, so its codes never
  appear in `CONCEPT_ANCESTOR`. Its hierarchy is built into the codes instead: `E83.3` should
  match every `ICD10CM` concept whose `concept_code` starts with `E83.3`.
- **Raw ICD-10-CM strings.** Some data loads leave the source concept id at 0. For ICD-10-CM
  codes, the raw `condition_source_value` and `observation_source_value` should also be compared,
  ignoring case, dots and spaces (` e8331 ` matches `E83.31`).
- **Retired concepts.** A code whose concept has an `invalid_reason` should still be matched,
  since older records may carry it. Sites should report such codes to Mendelian, so the CP can be
  updated.

### 7.3 History records

- **The patient's own history counts** (unless the feature sets
  `include_personal_history: false`). OMOP usually records "history of X" as an `observation` row
  whose `observation_concept_id` is a history concept and whose `value_as_concept_id` is X. Such
  rows should match when `value_as_concept_id` is in the feature's list and
  `observation_concept_id` is SNOMED CT `417662000` (History of clinical finding in subject) or a
  descendant. A site that uses another history concept should use it and tell Mendelian.
- **Family history never counts.** It is stored the same way under a family-history concept.
  Since only `observation_concept_id` and the source column are matched for ordinary records, and
  `value_as_concept_id` only under a personal-history concept, a relative's diagnosis never flags
  the patient.

### 7.4 Results and genetic findings

- **Numeric:** compare `value_as_number`. Where `units` are given, `unit_concept_id` must also be
  one of them. `above_ref_high` and `below_ref_low` compare with the same row's `range_high` and
  `range_low`; a row with no range recorded doesn't match.
- **Qualitative:** `value_as_concept_id` must be one of the `value_concepts`.
- **Genetic:** if genetic findings are stored in OMOP, the record's concept is in the feature's
  codes, its `value_as_concept_id` is one of the `interpretations`, and, when
  `require_gene_text_match` is true, the gene symbol appears (ignoring case) in the record's text:
  `measurement_source_value` and `value_source_value` in `measurement`;
  `observation_source_value`, `value_as_string` and `value_source_value` in `observation`.

### 7.5 Counting dates

Distinct dates are counted per patient and feature, not rows, so duplicate records don't count
twice. Records found through history count like any other record.

## 8. Producing the results file

Each CP version a site runs becomes one result in the results file: one `summary` row and one
`count` row per criterion. The [Results-File Specification](results-file-spec.md) sets the
columns, formats, small-number rules and checks; this section only says which CP values go where.

| Results-file value | From the CP |
| --- | --- |
| `cp_name` | The CP's `cp_id`, exactly as written |
| `summary` row, `count_value` | Distinct patients flagged by the CP |
| `summary` row, `population_n` | The population as the specification defines it (its section 4.1). For a cluster CP this is still the site population, not the number of patients with an umbrella code. |
| `count` rows, `criterion_id` | Every disjunct (`d1`…), rule (`r1`…) or score item (`s1`…) in the CP, including any that found nobody (`0`) |
| `count` rows, `count_value` | Patients meeting that criterion (below) |

What a criterion's count means:

- **Level 1:** patients who meet that disjunct.
- **Level 2A:** patients for whom that rule holds.
- **Level 2B:** flagged patients for whom that item applied, i.e. its feature was present and met
  any date options. Negative items count too, which shows when one was outweighed.
- **Cluster CPs:** only patients with an umbrella code are counted, in every criterion and in the
  flagged total.

A patient who meets several criteria is counted under each, so criterion counts can add up to
more than the flagged total; the `summary` row counts each patient once.

## 9. Before running, and open points

Mendelian recommends two quick checks before the first run of each CP version. Neither touches
patient data.

- **Do the codes resolve?** Look up every code in the CP in the site's `CONCEPT` table. Sites
  should report any code that isn't found, is retired (`invalid_reason` set) or, where descendants
  are wanted, isn't a standard concept. These explain a lower flag rate than expected.
- **Which vocabulary release is the site on?** It's the `vocabulary_version` of the `VOCABULARY`
  row whose `vocabulary_id` is `None`. Sites should report it to Mendelian with their first
  results; the results file has no column for it yet.

Open points Mendelian is working on:

- The [Results-File Specification](results-file-spec.md) describes criteria for Level 1 and 2A
  only. Score items (`s1`…) for Level 2B CPs, and the checks that apply to them, still need adding.
- For cluster CPs, the results file has no place yet for the number of patients with an umbrella
  code.
- Genetic findings rely on variant results being stored as structured rows. Where they aren't,
  those features will find nobody, and the approach needs discussing with Mendelian.
