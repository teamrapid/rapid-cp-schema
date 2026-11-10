# rapid-cp-schema: specification and working context

Status: **draft**, 2026-10-27. Seeded from Mendelian's `rapid-cp-logic` v0.1.0.

This document says what the schema is for, where it came from, what has been agreed about
changing it, and what is still open. The field-by-field reading of the schema, and how a site
applies a CP to OMOP 5.4 data, is in [docs/applying-cps-omop54.md](docs/applying-cps-omop54.md).
This file sits above it.

## 1. What this repository is

The LinkML schema for **RAPID TA1 computable phenotypes (CPs)**. ARPA-H RAPID TA1 (the Rare
Collaborative Network) has to find rare disease patients at a set of clinical sites. A CP is the
versioned, reviewable definition of how to find the patients for one disease. This schema is the
format such a CP is written in.

**The schema is the only public contract for a CP.** Sites receive CPs as YAML files and build
their own queries from them, with whatever tools suit their data. Validation tools come and go,
and no single one is shared by everyone who writes, reviews or runs a CP; the schema is. So
**every rule about the data that can be stated in LinkML belongs here**, not in a tool.

## 2. Background

### 2.1 What a CP is in RAPID

Two related terms help explain what a CP is:

- A **mapping** links a disease to a code that represents that disease. Mappings belong in Mondo.
- A **value set** is a list of codes to search for when looking for patients. It is built from
  mappings.

A **computable phenotype (CP)** is made of features, and each feature is a value set. A feature
for a test or measurement also says which result counts. The CP's level decides how the features
combine: any one feature is enough (L1), Boolean rules (L2A), or a weighted score (L2B). See §2.2.

RAPID uses CPs for **cohort extraction**: a CP tells a site which patients' records to extract
for a disease. Sites run CPs on **unconsented EHR data**, not on registry data. A CP looks for
**patients who have already been diagnosed**. A CP is knowingly below 100% precise.

### 2.2 Levels

| Level | Name | In the schema |
|---|---|---|
| L1 | Safe alone | `disjuncts`: any one highly specific feature flags the patient |
| L2A | Deterministic rules | `rules`: Boolean gates (`all_of`, `any_of`, `none_of`, `at_least`, `within`) |
| L2B | Deterministic score | `score`: weighted points against a threshold |
| L3 | Profile match | It ranks candidate diseases against each other |
| beyond | Trained models | Out of scope |

In the first year, the priority is to get the pipeline working end to end, not to write complex
logic. Most CPs will be L1, where one specific marker is enough to flag a patient, and most of
those markers will be ICD-10-CM codes. About 400 diseases are expected to get a CP of this kind;
the target over five years is about 2,700 diseases.

### 2.3 Deployment modes

- **Population**: search the whole dataset for one disease.
- **Cluster**: start from patients carrying a shared, non-specific umbrella code such as
  ICD-10-CM `E83.3`, and sort them into candidate diseases (declustering). Each patient gets
  **a score for each candidate disease**. The score says how well the patient's records fit that
  disease compared with the other candidates; **it is not the probability** that the patient has
  it. For now, each candidate disease gets its own CP with the same `umbrella_codes`, and cluster
  CPs (`cluster-…`) are reserved but not yet supported.

### 2.4 How CPs are run and checked

- CPs are published in a GitHub repository.
- Each site runs them in its own research data warehouse. Most sites are on OMOP; Truveta is the
  exception.
- **Automated QC:** each CP carries an `expected_flag_rate`. A result far too high, or zero,
  sends the CP back.
- **Clinical QC** by reviewing a sample of patients. How much and where is decided per site.
- **Every criterion has a stable id** (`d1`, `r2`, `s3`) that is reported as the flag reason. That
  lets over-flagging be traced back to the rule that caused it.

## 3. Provenance of the schema

- **Author:** Mendelian, as `rapid-cp-logic` v0.1.0, id
  `https://mendelian.co/schemas/rapid-cp-logic`. The prose explanation of the schema is
  [docs/applying-cps-omop54.md](docs/applying-cps-omop54.md).
- **Imported here** as `src/rapid_cp_schema/schema/rapid_cp_schema.yaml`. Version 0.2.0 differs
  from v0.1.0 as follows:
  - `name` is `rapid_cp_schema` instead of `rapid-cp-logic`, because the project template needs
    it for the generated Python module;
  - the `rapidcp` prefix is declared, as `https://mendelian.co/schemas/rapid-cp-logic/`, because
    LinkML's generators don't run without it. This is a placeholder (§5.3);
  - references to Mendelian's in-house tools for validation and query generation are removed;
  - the build and site classes needed by those tools are removed;
  - the `status` slot and the `CPStatus` enum are removed. CPs are published on GitHub only when
    they are ready for deployment, so a lifecycle status in the file carries no information.
- **Licence:** CC0 1.0, as declared in the original schema.
- **Ownership:** Mendelian agreed to move the schema to this programme-neutral home in the
  `teamrapid` GitHub org. **Mendelian remain the owners and maintainers**, and others contribute
  by pull request.

## 4. Design choices to keep

The v0.1.0 design gets these right, and changes should preserve them:

- **The CP file holds only the logic**, versioned for its own reason. How a site runs it is the
  site's business (see [docs/applying-cps-omop54.md](docs/applying-cps-omop54.md)).
- **Codes stay in their source vocabularies** (ICD10CM, SNOMED, LOINC, RxNorm), never as OMOP
  `concept_id`s. A CP then carries across sites and vocabulary releases.
- **Versions are defined by their effect on the logic.** Structural changes bump the major
  version, detail changes bump the minor, and lifecycle or documentation edits don't bump it.
- **Stable criterion ids** come back as flag reasons.
- **Counts are never suppressed, and zero is a result.** That is right for rare disease.
- **Personal history counts and family history doesn't.** The handling of this in OMOP
  `observation` is careful.
- **`expected_flag_rate` is a range with an explicit `basis`**, and `none` is allowed.

## 5. Agreed changes

Agreed with Mendelian in October 2026 after a first review. They are in rough PR order.

### 5.1 Constraint layer (first PR)

v0.1.0 enforces almost none of the rules in
[docs/applying-cps-omop54.md](docs/applying-cps-omop54.md) §5.6. The file
`tests/data/problem/invalid/ComputablePhenotype-nine-violations.yaml` breaks nine of them and
still passes `linkml-validate` with "No issues found" (checked 2026-10-23):

| # | Broken rule |
|---|---|
| 1 | `search_mode: cluster` with no `cluster` block |
| 2 | `medication` feature coded in LOINC |
| 3 | `diagnostic_test` with no `result` |
| 4 | Two features with the same id |
| 5 | L1 disjunct on a non-specific (S3) feature |
| 6 | Disjunct referencing a feature that doesn't exist (`f99`) |
| 7 | L2A `rules` block on an L1 CP |
| 8 | One `expr` node that is both `feature` and `all_of` |
| 9 | Rule made only of `none_of` |

How to fix them:

- **`exactly_one_of` on `Expr`** fixes 8. It was tested on a patched copy and works.
- **Class `rules`** (pre- and postconditions) fix 1, and if `search_mode` is `cluster` then
  `cluster` is required. Also tested and working.
- **`module` as a type designator** fixes 2 and 3. That gives subclasses `DiagnosticCodeFeature`,
  `PhenotypeFeature`, `DiagnosticTestFeature`, `GeneticFindingFeature`, `MedicationFeature` and
  `ProcedureFeature`, each with its own required slots and allowed vocabularies.
- **Level as a type designator** fixes 7: `L1Phenotype` has `disjuncts`, `L2APhenotype` has
  `rules`, and `L2BPhenotype` has `score`. Forbidding the other levels' blocks with
  `maximum_cardinality: 0` was tried and gave a misleading error, which is why the subclass route
  is preferred. **But** a type designator changes what a CP file must contain, so it is a
  breaking change (see §8, Compatibility).
- **Typed references** (`range: Feature`, `inlined: false`) on `Disjunct.feature`,
  `ScoreItem.feature`, `Expr.feature` and `Within.of` fix 6. The default validator did not check
  that a referenced id exists, so this needs a referential-integrity check.
- **4** (unique ids within a list) and **5** (L1 may only use S1 features) don't map onto plain
  LinkML. They may need rules, a custom validation plugin, or a small Python check in the tests.
- **9** (a rule needs at least one positive leaf) is recursive. It is likely a Python check.

**When it's done:** move the nine-violation file to `tests/data/invalid/`. Better still, split it
into one file per violation, so each rule is tested on its own.

These stay **out of the schema**: the file name matching `cp_id` and fingerprint checks. They are
about files and the repository, not the data.

### 5.2 CURIEs alongside `vocabulary` + `code`

Today a code is `{vocabulary: SNOMED, code: "82236004"}`. Mendelian agreed to **add** a `curie`
slot **alongside** `vocabulary` and `code` rather than replace them, so v0.1.0 files keep working.
They may switch to CURIEs only if UNC is happy with that.

- Use **Bioregistry prefixes**: `snomedct:82236004`, `icd10cm:E83.31`, `loinc:2777-1`,
  `rxnorm:2043855`, `ucum:mg/dL`. Declare them in the schema's `prefixes`.
- **Units:** a CURIE's local part can contain `/`. Bioregistry's `ucum` prefix expands to
  `https://units-of-measurement.org/` and lists `m/s` and `dL/g` among its own examples. LinkML
  accepts `ucum:mg/dL`, `ucum:mm[Hg]`, `ucum:10*3/uL` and `ucum:{cells}/uL` (checked
  2026-10-27). Brackets and braces need percent-encoding only if expanded to full URIs. Since
  nobody joins units against mappings, **leaving units as `vocabulary` + `code` is acceptable.**
- Consider deriving `vocabulary` from the prefix, or validating that the two agree.
- **Why it matters:** CP features must join with Mondo mappings, SSSOM mapping sets and the RAPID
  value sets, which are the inputs CPs consume.

### 5.3 Schema id, prefix and PURL

- `default_prefix: rapidcp` was used but **not declared** in v0.1.0. It is declared here with a
  placeholder expansion under the v0.1.0 id (§3), which has to be replaced.
- The schema `id` is still `https://mendelian.co/schemas/rapid-cp-logic`. An open corpus needs a
  **stable, resolvable, programme-neutral id**, such as a w3id. Mendelian agreed. **The actual
  RAPID prefix and PURL are to be agreed with the wider TA1 group**, so don't invent one here.

### 5.4 `mondo_version`

Add a slot recording **which Mondo release** the CP was built against. Mondo ids get obsoleted
and merged, so a CP without a pinned release can't be checked later. Agreed.

### 5.5 HPO terms with mapping predicates

`Feature.hpo_id` allows one term, with no semantics beyond "annotation". Agreed: replace it with
a **list of HPO terms, each with an SSSOM-style predicate** (`skos:exactMatch`, `skos:broadMatch`,
`skos:narrowMatch`, `skos:closeMatch`). A SNOMED or LOINC feature is often broader or narrower
than the nearest HPO term, and a thresholded lab result is narrower than "abnormal X". This is
low priority for Mendelian, because the first simple CPs aren't expected to have definitional
phenotypic features. Keep `hpo_id` readable during the transition.

### 5.6 Specificity grades as an enum

`specificity_grade` is an integer from 1 to 5 (S1 to S5 in prose), and only 1
("confirmatory/pathognomonic") and 5 ("incidental") are defined. The grade decides what counts as
"safe alone" in L1. Agreed: make it an **enum with a definition for each grade**. Examples belong
in the documentation, not the schema.

### 5.7 Opaque CP identifier

Every CP gets an **internal, opaque identifier** as its `cp_id`, completely separate from its
Mondo id. Today `cp_id` is built from the Mondo id, the slug, the level and the version (e.g.
`mondo0010619-xlh_L1_v1.0`), so obsoleting or merging the Mondo id, renaming the slug or changing
the level would change the CP's identity. An opaque id stays the same through all of these; the
disease stays recorded in `disease.mondo_id`.

This is a breaking change. Still to decide:

- the format of the identifier, and who assigns it;
- whether the version stays part of `cp_id` or moves to a separate field;
- what the file name becomes, since it currently equals `cp_id`;
- the knock-on changes: the `cp_id` pattern in the schema, the naming rules in
  [docs/applying-cps-omop54.md](docs/applying-cps-omop54.md) §2 and §5.6, and the `cp_name`
  column and its pattern in the [results-file specification](docs/results-file-spec.md).

## 6. Open questions

1. **Evidence per feature.** Nothing records *why* a feature counts as evidence for the disease,
   for example why burosumab is S1 for XLH. Mendelian is undecided, and is discussing
   **accompanying files per CP** that hold this detail plus a human-readable version of the CP.
   Proposals:
   - give the accompanying file its own LinkML class in this repo, so it is validated too;
   - **generate** the human-readable version from the YAML, so the two can't drift;
   - an evidence entry would be a source CURIE (a DisMech or knowledge-graph association, a PMID,
     a drug label), a predicate (e.g. indication or `has_phenotype`) and optionally a
     knowledge-graph edge id.
   Mendelian's **curation record**, the output of its per-disease curation pipeline, **will not
   be public**. So whatever reviewers need to see has to live in the CP or its accompanying file.
2. **`included_mondo_ids` and Mondo descendants.** Whether a Mondo subtype is actually found
   depends entirely on the feature codes. Options:
   - **(a)** pin `mondo_version` and check the list against Mondo's cross-references for those
     ids;
   - **(b)** an `include_descendants`-style flag for Mondo, so the scope is "this term and
     everything under it in release Y", and work out the list from that.
   (b) follows the pattern already used for SNOMED codes. Separately, a list longer than one is a
   **lumping decision**, and it should become feedback to Mondo rather than a silent CP-side
   choice. The clinical workstream is discussing which Mondo ids make up each disease entity, and
   that is expected to produce Mondo feedback. Note also that `included_mondo_ids` is part of the
   logic fingerprint, so editing it forces a new CP version even though it doesn't change who is
   flagged.
3. **Score semantics.** Are L2B points comparable **across** the candidate CPs under one
   umbrella? Declustering needs that if patients are ranked across candidates. What scale are the
   points on?
4. **Mimics and hard exclusions.** `none_of` exists, but the v0.1.0 spec said the mimic and
   hard-exclusion modules are "not yet specified". In rare disease, mimics are often where
   precision is won or lost. A disease's differential diagnoses are knowledge, which Mondo could
   supply.
5. **`first_date`** is the earliest qualifying event, not the date a rule became true. Is that
   acceptable for later time-to-diagnosis analyses?
6. **Vocabularies.** Only ICD10CM, SNOMED, LOINC and RXNORM are admitted, plus UCUM for units.
   Candidates:
   - CPT4, HCPCS and ICD10PCS for procedures;
   - RxNorm Extension and ATC for drugs;
   - OMOP Genomic.
   WHO Drug licensing costs have been raised as a barrier to coding treatments in the registries
   work.
7. **Genetic findings.** OMOP 5.4 can't tie a gene, a variant and an interpretation together, so
   `genetic_finding` is a heuristic. Whether sites load genetics as discrete rows decides whether
   this module is usable at all.
8. **Free text.** `text_terms` is carried for a future NLP step. The clinical side expects NER on
   notes to be needed, and Mendelian has said notes are in scope "but not for the first
   six months".
9. **Granularity and thresholds.** A CP needing "sweat chloride above X" can't be written
    against a term that only says "elevated". Which of SNOMED and HPO is finer depends on the
    branch of the hierarchy. Keep thresholds in `ResultCriterion`, not in a vocabulary choice.
10. **Relation to existing formats.** OHDSI Circe and the Phenotype Library, PheKB and CQL
    already exist. A paragraph saying why this format differs (it is data-model independent and
    uses source-vocabulary codes), or an export to Circe JSON, would help adoption at OHDSI
    sites. This is not a reason to replace the format.
11. **Results-file gaps.** The [results-file specification](docs/results-file-spec.md) v1.0
    covers L1 and L2A criteria only. It has no rows or checks yet for L2B score items, no place
    for the number of patients with an umbrella code in a cluster CP, and no column for the
    site's vocabulary release. Its Frictionless schema
    ([docs/results-file/](docs/results-file/)) matches: `criterion_id` allows only `d` and `r`
    ids.
12. **Encounter context.** Counting a record only if it came from a certain kind of encounter: an
    inpatient stay, a specialist, or the problem list rather than a billing code. It is one way to
    add corroboration when a CP flags too many patients. OMOP holds this in `visit_occurrence`
    (visit type), `provider` (specialty) and `*_type_concept_id` (record origin), but how reliably
    sites fill these in varies, so it is deferred until a real CP needs it. It would likely be an
    optional `encounter` filter on a feature.

## 7. Rejected directions

- **Replace it with Circe JSON or CQL.** Circe is tied to OMOP concept ids. Data-model
  independence and versioned, fingerprinted logic are what this design gets right.
- **Make a CP an OWL class expression.** Counting, time windows and scores have no natural OWL
  reading.
- **Pick one phenotype vocabulary.** Which one is finer depends on the branch, so a
  single-vocabulary rule is wrong somewhere by construction.

## 8. Working conventions

- **Example data** goes in `tests/data/`, named `<ClassName>-<id>.yaml`:
  - `valid/`: must validate. It currently holds an L1 and an L2A XLH CP and feature fragments,
    all built from the v0.1.0 spec's own snippets. **They are illustrative and not clinically
    reviewed.**
  - `invalid/`: must fail validation, for the reason stated in the file's `# expect:` lines.
  - `problem/invalid/`: should fail but doesn't yet. This is where the nine-violation file lives
    until §5.1 lands, together with one file per rule the schema doesn't enforce.
  - `problem/valid/`: should validate but is rejected.
- **A new rule in the schema comes with an invalid example** that it rejects.
- **Schema version:** bump `version` in the schema for every released change. CP files record the
  schema version they conform to in `schema_version`.
- **Compatibility:** schema 0.2.0 deliberately broke v0.1.0 CP files (§3). Breaking changes are
  allowed, but each one bumps the minor version while the schema is 0.x, is recorded in §3 with
  its reason, and updates the test data in the same change.

## 9. People and context

- **Mendelian:** schema authors and owners. Elena Marchini (product lead) is the contact for the
  schema, and Peter Fish is COMPPHENO co-lead.
- **UNC:** Emily Pfaff's team is the first site to receive test CPs.
- **Nicolas Matentzoglu (Semanticly / Monarch Initiative):** reviewer and contributor, with Mondo
  and mappings as the main interest.
- **Workstream:** COMPPHENO (computable phenotypes), mainly tasks COMPPHENO.T02 (run CPs) and
  COMPPHENO.T03 (the ontology side, including Mondo lumping and splitting).
