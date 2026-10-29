# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

LinkML schema for RAPID TA1 computable phenotypes (CPs), generated from the
[linkml-project-copier](https://github.com/linkml/linkml-project-copier) template.
**Read `SPEC.md` before changing the schema** — it holds the purpose, provenance, agreed
changes (§5), open questions (§6), rejected directions (§7) and working conventions (§8).
`docs/cp-yaml-spec.md` is Mendelian's field-by-field prose spec (v0.1.0), kept verbatim — do not
edit it.

## Commands

All recipes run through `just` (config is loaded from `config.public.mk`); `just` alone lists them.

- `just install` — `uv sync --group dev`
- `just test` — runs three things: schema generation into `tmp/`, pytest (after regenerating the
  Python datamodel), and `linkml-run-examples` over `tests/data/valid` and the counter-examples in
  `tests/data/invalid` (output to `examples/output/`, git-ignored)
- `just lint` — `linkml-lint` on the schema directory
- `just gen-project` — regenerate `project/` artifacts and the Python datamodel
- `just gen-python` — regenerate only `src/rapid_cp_schema/datamodel/` (dataclasses + pydantic)
- `just gen-doc` / `just testdoc` — build docs into `docs/elements/` (and serve with mkdocs)

Single test / single file:

```sh
uv run pytest tests/test_data.py -k CPBuild
uv run linkml-validate -s src/rapid_cp_schema/schema/rapid_cp_schema.yaml -C ComputablePhenotype tests/data/valid/ComputablePhenotype-001.yaml
```

pytest imports the generated datamodel, so run `just gen-python` first after any schema edit.

## Architecture

- **The single source of truth is `src/rapid_cp_schema/schema/rapid_cp_schema.yaml`.** Everything
  in `project/`, `src/rapid_cp_schema/datamodel/*.py`, `docs/elements/*.md` and
  `docs/schema/` is generated from it — never hand-edit those.
- The schema describes three separately versioned file kinds: `ComputablePhenotype` (the CP logic
  file, `tree_root`), `CPBuild` (a compiled build header) and `SiteProfile` (site config).
  A CP is a list of `features` (coded evidence items with stable ids) plus a logic block chosen by
  `level`: `disjuncts` (L1), `rules` built from recursive `Expr` nodes (L2A), or `score` (L2B).
  Logic blocks reference features by id.
- **The schema is the only public contract for a CP** (Mendelian's `cpsql` validator/compiler is
  in-house). Any data rule expressible in LinkML belongs in the schema, not in a tool. Repository
  concerns (file name = `cp_id`, fingerprints, build immutability) stay out of it.
- v0.1.0 enforces few of the spec's rules; `SPEC.md` §5.1 lists the constraint layer to add.

## Test data conventions

- `tests/data/{valid,invalid}/<ClassName>-<id>.yaml` — the prefix before `-` is the target class
  (pytest and `linkml-run-examples` both rely on it). Any class works, so class-local rules are
  tested on fragments (`Feature-…`, `HistoryConcept-…`).
- `tests/test_data.py` runs the LinkML validator on every file. `invalid/` files need one or more
  `# expect: <regex>` header lines, each of which must match an error, so a file can't fail for
  the wrong reason.
- `tests/data/problem/invalid/` — files that *should* fail but currently pass (strict xfail).
  When a schema change makes one fail, pytest reports an XPASS failure: move the file to
  `tests/data/invalid/` and add its `# expect:` line.
- `tests/data/problem/valid/` — files that *should* validate but are rejected; their `# expect:`
  lines record the current rejection.
- Each invalid/problem file differs from a valid CP in exactly one respect.
- Every new schema rule comes with an invalid example it rejects.
- Example CPs are illustrative, not clinically reviewed.

## Constraints on changes

- **Do not break v0.1.0 CP files** until UNC's feedback on the test CPs is in — additive changes
  only (e.g. `curie` *alongside* `vocabulary` + `code`, not replacing it).
- Bump the schema `version` for every released change.
- Do not invent a RAPID prefix, PURL or schema `id`; the current `rapidcp` expansion is a
  placeholder pending agreement with the TA1 group (`SPEC.md` §5.3).
- Codes stay in source vocabularies (ICD10CM, SNOMED, LOINC, RxNorm), never OMOP `concept_id`s.
