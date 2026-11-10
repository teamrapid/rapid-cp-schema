# Example data for rapid_cp_schema

This folder contains example data for testing and demonstrating the datamodel,
sorted in subfolders:

- `valid` for data conforming to the datamodel. Used to verify the datamodel.
- `invalid` for data not conforming to the datamodel. Used to verify the validation.
- `problem` for data which are not yet handled correctly in the current schema version,
   again separated into valid/invalid.

The filenames of all example data must conform to the scheme `classname-###.yaml`
where classname must be a the name of a class from the schema. "###" can be a number
or one or more other characters allowed in filenames. The classname is derived by
splitting at the first "-" and taking the part before the "-". Any class can be the
target, so a rule local to one class can be tested on a fragment (`Feature-…`)
rather than a whole CP.

`tests/test_data.py` validates every file with the LinkML validator:

| Folder | Test passes when |
|---|---|
| `valid/` | the file validates and loads into the generated dataclasses |
| `invalid/` | the file fails, and every `# expect: <regex>` header line matches an error message |
| `problem/invalid/` | the file still validates (strict xfail). When the schema starts rejecting it, the test fails: move it to `invalid/` and add an `# expect:` line |
| `problem/valid/` | the file is still rejected with exactly the errors its `# expect:` lines record (strict xfail). When it validates, move it to `valid/` |

Each file starts with a comment saying what it tests. The rules come from
[`docs/applying-cps-omop54.md`](../../docs/applying-cps-omop54.md), mostly its section 5.6. Each `invalid` and `problem` file differs from a
valid CP in one respect only, so it fails (or should fail) for one reason.

## Running the tests

`just test` runs three steps:

1. `gen-project` into `tmp/` (git-ignored): every LinkML generator must accept the schema.
2. `gen-python`, then pytest: regenerates `src/rapid_cp_schema/datamodel/` and runs
   `tests/test_data.py` as described above.
3. `linkml-run-examples` over `valid/` and the counter-examples in `invalid/`, writing
   converted copies to `examples/output/` (git-ignored).

CI (`.github/workflows/main.yaml`) runs `just test` on Python 3.10–3.14 for every push to
`main` and every pull request. To check a single file:

```sh
uv run pytest tests/test_data.py -k Feature-medication
uv run linkml-validate -s src/rapid_cp_schema/schema/rapid_cp_schema.yaml -C Feature tests/data/valid/Feature-procedure-snomed.yaml
```
