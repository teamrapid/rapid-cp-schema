# RAPID results-file specification v1.0

The file each site returns to Mendelian after running RAPID computable phenotypes (CPs), and how
Mendelian checks it. Written by Mendelian for the RAPID Tracking Database.

## 1. About this specification

This document is for the site team that runs RAPID CPs on its own data. It defines the one file a
site sends back to Mendelian after each run: what goes in it, how it is delivered, and the reasons
a file or a result can be rejected. How a CP's logic maps onto the file is described in
[Applying RAPID CP files in OMOP 5.4](applying-cps-omop54.md), section 8.

- **A results file** reports the counts from running one or more CPs at a site. It contains counts
  only, never patient-level data.
- **A result** is one CP version run at a site on one date. One file can hold many results,
  across many disease entities.
- **Each result is checked on its own.** A problem with one result never blocks the others in the
  same file.
- **Versions.** This is version 1.0. Every file states the version it follows
  (`result_spec_version` = `1.0`). Mendelian will announce any new version, and will keep
  accepting the previous one for a transition period.
- **Questions** about this specification go to the Mendelian RAPID team.

## 2. Delivery

Each site sends its results files to Mendelian through the channel agreed with Mendelian.

1. **A CSV file.** UTF-8, comma-separated, with one header row, as laid out in section 3. The file
   must arrive as a CSV, not converted to a spreadsheet format.
2. **One file per execution.** Everything run in one go goes into one file, however many CP
   versions and disease entities that covers.
3. **A name that is easy to find again.** For example `rapid-results_<site>_<YYYY-MM-DD>.csv`.
   Mendelian doesn't read the name, but it helps when a file is discussed.
4. **A file once sent is never replaced or withdrawn.** A correction is sent as a new file
   (section 7). The files sent are the record of what the site reported.

Mendelian sends the site the reasons for anything rejected (section 6).

## 3. File layout

Each result is written as **one `summary` row** followed by **one `count` row for every criterion
in the CP**: `d1`, `d2`… for an L1 CP, or `r1`, `r2`… for an L2A CP. Every criterion is included,
even one that flagged nobody (count 0). The rows of one result share the same `cp_name` and
`run_date`. Results can appear in any order.

| Column | Format | Filled on | Meaning |
| --- | --- | --- | --- |
| `site_code` | text | every row | The site code, as given by Mendelian. The same on every row. |
| `result_spec_version` | text | every row | `1.0` for this specification. The same on every row. |
| `generated_at` | date and time with timezone, ISO 8601 | every row | When this file was produced, for example `2026-10-15T09:30:00Z`. The same on every row. |
| `cp_name` | text | every row | The CP version's `cp_id`, exactly as published, for example `mondo9999999-test-disease-a_L1_v1.0`. |
| `run_date` | date, YYYY-MM-DD | every row | The date the site ran this CP version. |
| `data_snapshot_date` | date, YYYY-MM-DD | every row | The date the site's data was last refreshed before the run. |
| `row_type` | `summary` or `count` | every row | Which kind of row this is. |
| `criterion_id` | text | `count` rows | The criterion ID from the CP: `d1`, `d2`… or `r1`, `r2`… Empty on `summary` rows. |
| `population_n` | whole number | `summary` rows | The number of people the CP was run against (section 4.1). Never hidden. |
| `population_basis` | `observation_time`, `all_persons` or `other` | `summary` rows | How the site defined the population (section 4.1). |
| `population_basis_note` | text | `summary` rows when the basis is `other` | A short description of the site's definition. |
| `count_value` | whole number, or empty | every row | On a `summary` row, the number of patients the CP flagged. On a `count` row, the number of patients matching that criterion. Empty when the count is hidden. |
| `count_status` | `exact` or `suppressed` | every row | `suppressed` when the site hides a count from 1 to 10 (section 4.3), otherwise `exact`. |

A column stays empty where the table says it isn't filled. Extra columns are not allowed.

## 4. Filling in the values

### 4.1 Population

Each result reports one population count: the number of people the CP was run against.

- **Default:** everyone with any recorded observation time in the site's data, with
  `population_basis` = `observation_time`.
- **A site that can only count everyone in its person table** uses `all_persons`.
- **Any other definition** uses `other`, described in `population_basis_note`.

The population must be a whole number greater than 0, and at least as large as the number of
patients flagged. RAPID may decide to unify this definition across sites.

### 4.2 Dates

- `run_date` is the day the site ran the CP version. It can't be later than `generated_at`, or
  earlier than the date the CP version was published.
- `data_snapshot_date` is the day the site's data was last refreshed. It can't be later than
  `run_date`.
- `generated_at` is the date and time the file was produced, with timezone. A resent correction
  must have a later `generated_at` than the file it corrects.

### 4.3 Counts and small numbers

- On the `summary` row, `count_value` is the number of **distinct patients** the CP flagged.
- On each `count` row, `count_value` is the number of patients matching that criterion. A patient
  who matches several criteria is counted under each of them, so the criterion counts can add up
  to more than the flagged total. That is expected.
- For an L1 CP, the flagged total can't be smaller than the largest criterion count, or larger
  than the sum of all criterion counts.
- **Hiding small numbers.** Where a site's rules require it, the site may hide any count from 1 to
  10: `count_value` is left empty and `count_status` is set to `suppressed`.
  - **Zero is never hidden:** it is written as `0` with `count_status` = `exact`.
  - **"<=10", "≤10", "-1" or "10" never go in `count_value`.** A hidden count is shown only by
    `count_status`.
- **Complementary suppression is the site's responsibility.** If a hidden count could be worked
  out from the others, for example from the flagged total minus the other criterion counts, the
  site applies its own rules to hide what else is needed.

## 5. Worked example

Test Site 1 ran two L1 CP versions on 14 October 2026, against data refreshed on 1 October, and
produced the file at 09:30 UTC on 15 October. The disease entities and sites are fictitious.

```csv
site_code,result_spec_version,generated_at,cp_name,run_date,data_snapshot_date,row_type,criterion_id,population_n,population_basis,population_basis_note,count_value,count_status
test_site_1,1.0,2026-10-15T09:30:00Z,mondo9999999-test-disease-a_L1_v1.0,2026-10-14,2026-10-01,summary,,520000,observation_time,,213,exact
test_site_1,1.0,2026-10-15T09:30:00Z,mondo9999999-test-disease-a_L1_v1.0,2026-10-14,2026-10-01,count,d1,,,,40,exact
test_site_1,1.0,2026-10-15T09:30:00Z,mondo9999999-test-disease-a_L1_v1.0,2026-10-14,2026-10-01,count,d2,,,,173,exact
test_site_1,1.0,2026-10-15T09:30:00Z,mondo9999998-test-disease-b_L1_v1.0,2026-10-14,2026-10-01,summary,,520000,observation_time,,25,exact
test_site_1,1.0,2026-10-15T09:30:00Z,mondo9999998-test-disease-b_L1_v1.0,2026-10-14,2026-10-01,count,d1,,,,22,exact
test_site_1,1.0,2026-10-15T09:30:00Z,mondo9999998-test-disease-b_L1_v1.0,2026-10-14,2026-10-01,count,d2,,,,,suppressed
test_site_1,1.0,2026-10-15T09:30:00Z,mondo9999998-test-disease-b_L1_v1.0,2026-10-14,2026-10-01,count,d3,,,,0,exact
```

- **Test Disease A:** 213 patients flagged out of 520,000. Criterion `d1` matched 40 and `d2`
  matched 173. Both results pass the checks in section 6.
- **Test Disease B:** 25 flagged. `d1` matched 22, `d2` matched between 1 and 10 and is hidden,
  and `d3` matched nobody. Zero is written as 0, not hidden. The check that the flagged total is
  at least the largest criterion count (22) still runs; the check against the sum of criteria is
  skipped, because one value is hidden.

## 6. What Mendelian checks

A problem with the **whole file** rejects every result in it. A problem with **one result** rejects
only that result, and the rest of the file still loads. Mendelian sends the site every reason,
worded as below.

| Applies to | Reason given | What to do |
| --- | --- | --- |
| Whole file | File can't be read: not a CSV, or columns missing or extra | Use the layout in section 3, saved as a CSV. |
| Whole file | Unknown specification version | Set `result_spec_version` to `1.0`. |
| Whole file | `site_code`, `result_spec_version` or `generated_at` differs between rows | Use the same value on every row. |
| Whole file | Site code does not match the site that sent the file | Put the site's own code in `site_code`. |
| One result | CP version not registered | Check the `cp_name` spelling against the published `cp_id`. If it's right, tell Mendelian. |
| One result | CP version is a draft | Run only published CP versions. |
| One result | CP version appears more than once in the file for the same run date | Report each CP version and run date once. |
| One result | Missing summary row, or more than one | Give exactly one `summary` row per result. |
| One result | Population missing or zero | Give the population as a whole number greater than 0. |
| One result | Population basis "other" without a description | Fill in `population_basis_note`. |
| One result | Flagged count larger than the population | Check both numbers. |
| One result | Flagged count below the largest criterion count (L1 only) | Check the counts: everyone matching a criterion is flagged. |
| One result | Flagged count above the sum of the criterion counts (L1 only) | Check the counts: every flagged patient matches at least one criterion. |
| One result | Run date later than the file date, or earlier than the CP version's publication | Check `run_date` and `generated_at`. |
| One result | Data snapshot date missing or later than the run date | Give the date the site's data was last refreshed. |
| One result | Hidden count written as a number, or a count marked `suppressed` with a value | Leave `count_value` empty for hidden counts, and write zero as 0 `exact`. |
| One result | Older than current data | This file was produced before, or at the same moment as, the one that gave the current result. Send a correction as a new file with a later `generated_at` (section 7). |

Results for a CP version that Mendelian has since superseded or withdrawn are still accepted.
Mendelian may follow up with the site about them.

## 7. Resending and re-running

| Situation | What to send | What Mendelian does |
| --- | --- | --- |
| A result was rejected, or the site found a mistake | A new file with the corrected result, the **same** `run_date`, and a later `generated_at`. It only needs the results being corrected. | The corrected result replaces the earlier one, which stays on record. |
| The site ran a CP version again on refreshed data | A new file with the **new** `run_date` and `data_snapshot_date`. | Both results are kept. The new one is a separate run. |
| The site sent exactly the same file twice | Nothing. | The copy is recognised and ignored. |

A correction is always sent as a **new file**. The original is never replaced or edited, because
it is part of the record. A resent file must be regenerated, so it carries a new
`generated_at`. An exact copy of a file Mendelian already received, even one that was rejected, is
recorded as a duplicate and loads nothing, with the reason "identical to a file already rejected:
regenerate the file before resending".

## 8. Checking a file before sending

The layout in section 3 is also available as a machine-readable Frictionless Table Schema,
[`results-file-schema-v1.0.json`](results-file/results-file-schema-v1.0.json), with the
worked example from section 5 as
[`results-example-v1.0.csv`](results-file/results-example-v1.0.csv). A file can be checked
against the schema with the free [Frictionless](https://framework.frictionlessdata.io/)
command-line tool:

```bash
frictionless validate rapid-results_test_site_1_2026-10-15.csv --schema results-file-schema-v1.0.json
```

This catches layout and format problems: column names, dates, number formats and allowed values.
It doesn't check the rules that compare rows or need Mendelian's records, such as the
flagged-count limits, duplicate results, or whether a CP version is registered. Those are checked
when Mendelian loads the file (section 6).
