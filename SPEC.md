# rapid-cp-schema: specification and working context

Status: **draft**, 2026-10-27. Seeded from Mendelian's `rapid-cp-logic` v0.1.0.

This document says what the schema is for, where it came from, what has been agreed about
changing it, and what is still open. The field-by-field reading of the schema, and how each field
turns into OMOP SQL, is Mendelian's [CP YAML specification](docs/cp-yaml-spec.md) (v0.1.0, kept
verbatim). This file sits above it.

## 1. What this repository is

The LinkML schema for **RAPID TA1 computable phenotypes (CPs)**. ARPA-H RAPID TA1 (the Rare
Collaborative Network) has to find rare disease patients at a set of clinical sites. A CP is the
versioned, reviewable definition of how to find the patients for one disease. This schema is the
format such a CP is written in.

**The schema is the only public contract for a CP.** UNC, the first site, will receive CPs as
YAML files, not as generated SQL. Mendelian's `cpsql` tool, which validates CPs and compiles
them to SQL today, stays in-house. Anyone outside Mendelian who writes, reviews or runs a CP can
check it only against this schema. So **every rule about the data that can be stated in LinkML
belongs here**, not in a tool.

## 2. Background

### 2.1 What a CP is in RAPID

There are three different things, and they get conflated:

- A **mapping** says how a disease relates to a code. It is a claim about *meaning*, and it
  belongs in Mondo.
- A **value set** is the set of codes you query to find patients. It is a claim about
  *retrieval*, and it is derived from mappings.
- A **computable phenotype** is a value set **plus filter rules**, which are sometimes empty.

A RAPID CP is a **screening instruction, not a diagnosis**: an executable definition of which
patient records a site should extract for a disease. It is knowingly below 100% precise. Mendelian
listed three uses:

1. **Cohort extraction**: whom to extract. This is the current focus.
2. **Diagnosis corroboration**: do the extracted records actually have the disease? This is done
   after extraction for now.
3. **Feature annotation**: which features come before and after diagnosis. This is deferred.

CPs run on **unconsented EHR data at the sites**, to find **patients who have already been
diagnosed**. They do not run against registry data.

### 2.2 Levels

| Level | Name | In the schema |
|---|---|---|
| L1 | Safe alone | `disjuncts`: any one Tier 1 feature flags the patient |
| L2A | Deterministic rules | `rules`: Boolean gates (`all_of`, `any_of`, `none_of`, `at_least`, `within`) |
| L2B | Deterministic score | `score`: weighted points against a threshold |
| L3 | Profile match | Declared only. It ranks candidate diseases against each other |
| beyond | Trained models | Out of scope. Such a CP is marked `status: exemplar-candidate` |

Year one is deliberately engineering-first: mostly L1 CPs built from single specific markers,
largely ICD-10-CM codes. The first batch is about 400 diseases, and the five-year target is about
2,700.

### 2.3 Deployment modes

- **Population**: search the whole dataset for one disease.
- **Cluster (declustering)**: start from patients carrying a shared, non-specific umbrella code
  such as ICD-10-CM `E83.3`, and sort them into candidate diseases. Mendelian described the result
  as **a score per candidate disease, which is an index, not a probability**. In v0.1.0 each
  candidate gets its own CP with the same `umbrella_codes`, and cluster CPs (`cluster-…`) are
  reserved but not yet supported.

### 2.4 How CPs are run and checked

- CPs are published in a GitHub repository, following the pattern of Emily Pfaff's team at UNC.
- Each site runs them in its own research data warehouse. Most sites are on OMOP; Truveta is the
  exception.
- **Automated QC:** each CP carries an `expected_flag_rate`. A result far too high, or zero,
  sends the CP back.
- **Clinical QC** by reviewing a sample of patients. How much and where is decided per site.
- **Every criterion has a stable id** (`d1`, `r2`, `s3`) that is reported as the flag reason. That
  lets over-flagging be traced back to the rule that caused it.

## 3. Provenance of the schema

- **Author:** Mendelian (Elena Marchini and colleagues), as `rapid-cp-logic` v0.1.0, id
  `https://mendelian.co/schemas/rapid-cp-logic`, CC0. It came with the prose spec
  `CP_YAML_SPEC.md`, now at [docs/cp-yaml-spec.md](docs/cp-yaml-spec.md).
- **Imported here** as `src/rapid_cp_schema/schema/rapid_cp_schema.yaml`, with **two changes**,
  both needed by the tooling. Everything else, including the `id`, is still v0.1.0 as received:
  - `name: rapid-cp-logic` → `name: rapid_cp_schema`, because the project template needs it for
    the generated Python module;
  - the `rapidcp` prefix (the `default_prefix`) is declared as
    `https://mendelian.co/schemas/rapid-cp-logic/`. v0.1.0 used it without declaring it, and
    LinkML's generators refuse to run. This is a placeholder; see §5.3.
- **Licence:** CC0 1.0, as declared in the original schema.
- **Ownership:** Mendelian agreed to move the schema to this programme-neutral home in the
  `teamrapid` GitHub org. **Mendelian remain the owners and maintainers**, and others contribute
  by pull request.
- **Timing:** Mendelian asked to wait until UNC (Emily Pfaff's team) has looked at the first test
  CPs before the repository is set up publicly and PRs start. Those test CPs were written against
  v0.1.0, so **changes must not break v0.1.0 CP files** until that feedback is in.

## 4. Design choices to keep

The v0.1.0 design gets these right, and changes should preserve them:

- **Logic, build and site are separate files**, each versioned for its own reason. A mapping fix,
  a logic change and a site change are different kinds of edit.
- **Codes stay in their source vocabularies** (ICD10CM, SNOMED, LOINC, RxNorm), never as OMOP
  `concept_id`s. A CP then carries across sites and vocabulary releases.
- **Versions are defined by their effect on the logic.** Structural changes bump the major
  version, detail changes bump the minor, and lifecycle or documentation edits don't bump it.
- **Builds are fingerprinted** against the logic fields only.
- **Stable criterion ids** come back as flag reasons.
- **Counts are never suppressed, and zero is a result.** That is right for rare disease.
- **Personal history counts and family history doesn't.** The handling of this in OMOP
  `observation` is careful.
- **`expected_flag_rate` is a range with an explicit `basis`**, and `none` is allowed.

## 5. Agreed changes

Agreed with Mendelian in October 2026 after a first review. They are in rough PR order.

### 5.1 Constraint layer (first PR)

v0.1.0 enforces almost none of the spec's rules. The file
`tests/data/problem/invalid/ComputablePhenotype-nine-violations.yaml` breaks nine of them and
still passes `linkml-validate` with "No issues found" (checked 2026-10-23):

| # | Broken rule | Spec |
|---|---|---|
| 1 | `search_mode: cluster` with no `cluster` block | §2 |
| 2 | `medication` feature coded in LOINC | §3.2 |
| 3 | `diagnostic_test` with no `result` | §3.2 |
| 4 | Two features with the same id | §3 |
| 5 | L1 disjunct on a Tier 3 feature | §5.1 |
| 6 | Disjunct referencing a feature that doesn't exist (`f99`) | §5 |
| 7 | L2A `rules` block on an L1 CP | §2 |
| 8 | One `expr` node that is both `feature` and `all_of` | §5.2 |
| 9 | Rule made only of `none_of` | §5.2 |

`cpsql validate` catches all nine today, but nobody outside Mendelian can run it.

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
  is preferred. **But** a type designator changes what a v0.1.0 file must contain, so it needs a
  plan for staying compatible with the test CPs (see §3, Timing).
- **Typed references** (`range: Feature`, `inlined: false`) on `Disjunct.feature`,
  `ScoreItem.feature`, `Expr.feature` and `Within.of` fix 6. The default validator did not check
  that a referenced id exists, so this needs a referential-integrity check.
- **4** (unique ids within a list) and **5** (L1 may only use Tier 1) don't map onto plain LinkML.
  They may need rules, a custom validation plugin, or a small Python check in the tests.
- **9** (a rule needs at least one positive leaf) is recursive. It is likely a Python check.

**When it's done:** move the nine-violation file to `tests/data/invalid/`. Better still, split it
into one file per violation, so each rule is tested on its own.

These stay **out of the schema**: the file name matching `cp_id`, fingerprint checks, and build
immutability. They are about files and the repository, not the data.

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

### 5.6 Specificity tiers as an enum

`specificity_tier` is an integer from 1 to 5, and only 1 ("confirmatory/pathognomonic") and 5
("incidental") are defined. The tier decides what counts as "safe alone" in L1. Agreed: make it
an **enum with a definition for each tier**. Examples belong in the documentation, not the
schema.

## 6. Open questions

1. **Evidence per feature.** Nothing records *why* a feature counts as evidence for the disease,
   for example why burosumab is Tier 1 for XLH. Mendelian is undecided, and is discussing
   **accompanying files per CP** that hold this detail plus a human-readable version of the CP.
   Proposals:
   - give the accompanying file its own LinkML class in this repo, so it is validated too;
   - **generate** the human-readable version from the YAML, so the two can't drift;
   - an evidence entry would be a source CURIE (a DisMech or knowledge-graph association, a PMID,
     a drug label), a predicate (e.g. indication or `has_phenotype`) and optionally a
     knowledge-graph edge id.

   Mendelian's **curation record**, the output of its per-disease curation pipeline, **will not
   be public**. So whatever reviewers need to see has to live in the CP or its accompanying file.
2. **`included_mondo_ids` and Mondo descendants.** It is a flat list, "recorded, not queried".
   Whether a Mondo subtype is actually found depends entirely on the feature codes and their
   `include_descendants`, and nothing ties the two together. Options:
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
   points on? Mendelian's "index score, not probability" rules out a calibrated reading, but it
   doesn't say what the score does mean.
4. **Build and site files.** UNC receives YAML only, and SQL generation stays with Mendelian. Do
   `CPBuild` and `SiteProfile` belong in the public schema? Who turns a CP into a query at a site
   that doesn't use cpsql?
5. **Mimics and hard exclusions.** `none_of` exists, but the spec says the mimic and
   hard-exclusion modules are "not yet specified". In rare disease, mimics are often where
   precision is won or lost. A disease's differential diagnoses are knowledge, which Mondo could
   supply, not site configuration.
6. **`first_date`** is the earliest qualifying event, not the date a rule became true. Is that
   acceptable for later time-to-diagnosis analyses?
7. **Vocabularies.** Only ICD10CM, SNOMED, LOINC and RXNORM are admitted, plus UCUM for units.
   Candidates (spec §10):
   - CPT4, HCPCS and ICD10PCS for procedures;
   - RxNorm Extension and ATC for drugs;
   - OMOP Genomic.

   WHO Drug licensing costs have been raised as a barrier to coding treatments in the registries
   work.
8. **Genetic findings.** OMOP 5.4 can't tie a gene, a variant and an interpretation together, so
   `genetic_finding` is a heuristic. Whether sites load genetics as discrete rows decides whether
   this module is usable at all.
9. **Free text.** `text_terms` is carried for a future NLP step. The clinical side expects NER on
   notes to be needed, and Mendelian has said notes are in scope "but ideally not for the first
   six months".
10. **Granularity and thresholds.** A CP needing "sweat chloride above X" can't be written
    against a term that only says "elevated". Which of SNOMED and HPO is finer depends on the
    branch of the hierarchy. Keep thresholds in `ResultCriterion`, not in a vocabulary choice.
11. **Relation to existing formats.** OHDSI Circe and the Phenotype Library, PheKB and CQL
    already exist. A paragraph saying why this format differs (it is data-model independent and
    uses source-vocabulary codes), or an export to Circe JSON, would help adoption at OHDSI
    sites. This is not a reason to replace the format.

## 7. Rejected directions

- **Replace it with Circe JSON or CQL.** Circe is tied to OMOP concept ids. Data-model
  independence and versioned, fingerprinted logic are what this design gets right.
- **Move every check into the schema.** File-name agreement, fingerprints and build immutability
  are repository concerns.
- **Make a CP an OWL class expression.** Counting, time windows and scores have no natural OWL
  reading, and the users are clinical informaticians.
- **Pick one phenotype vocabulary.** Which one is finer depends on the branch, so a
  single-vocabulary rule is wrong somewhere by construction.

## 8. Working conventions

- **Example data** goes in `tests/data/`, named `<ClassName>-<id>.yaml`:
  - `valid/`: must validate. It currently holds an L1 and an L2A XLH CP, a site file and a build
    header, all built from the spec's own snippets. **They are illustrative and not clinically
    reviewed.**
  - `invalid/`: must fail validation.
  - `problem/invalid/`: should fail but doesn't yet. This is where the nine-violation file lives
    until §5.1 lands.
- **A new rule in the schema comes with an invalid example** that it rejects.
- **Schema version:** bump `version` in the schema for every released change. CP files record the
  schema version they conform to in `schema_version`.
- **Compatibility:** until UNC's feedback on the test CPs is in, every change has to keep v0.1.0
  CP files valid.

## 9. People and context

- **Mendelian:** schema authors and owners. Elena Marchini (product lead) is the contact for the
  schema, and Peter Fish is COMPPHENO co-lead.
- **UNC:** Emily Pfaff's team is the first site to receive test CPs.
- **Nicolas Matentzoglu (Semanticly / Monarch Initiative):** reviewer and contributor, with Mondo
  and mappings as the main interest.
- **Workstream:** COMPPHENO (computable phenotypes), mainly tasks COMPPHENO.T02 (run CPs) and
  COMPPHENO.T03 (the ontology side, including Mondo lumping and splitting).

## 10. Where the background lives

These are local and not part of this repository. They are Nico's planning notes in
`~/ws/notes/rapid`:

- `background/mendelian/`: the original schema and spec as received, and Mendelian's reply to the
  review
- `brainstorms/2026-10-14-mendelian-cp-schema-review.md`: the full first-round review
- `sources/2026-10-mendelian-cp-schema-review-exchange.md`: what was agreed, point by point
- `brainstorms/2026-09-30-computable-phenotypes.md`: the mapping, value set and CP distinction,
  and SNOMED/HPO granularity
- `meetings/2026-09-28-mendelian-cp-approach.md` and `meetings/2026-10-01-comppheno-cp-approach.md`:
  Mendelian's CP strategy
