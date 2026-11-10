from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "0.2.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'rapidcp',
     'default_range': 'string',
     'description': 'Schema for RAPID computable phenotype (CP) logic files, named '
                    '`<disease-id>_<level>_v<major>.<minor>.yaml`. '
                    'Data-model-independent. Says WHAT counts as evidence '
                    '(features, coded in source vocabularies: ICD10CM, SNOMED, '
                    'LOINC, RxNorm, ...) and HOW the evidence combines (Level 1 '
                    'disjuncts, Level 2a rules, Level 2b score). Every disjunct / '
                    'rule / score item carries a stable id (`d1`, `r2`, `s3`) that '
                    'is reported back as the flag reason.',
     'id': 'https://mendelian.co/schemas/rapid-cp-logic',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'name': 'rapid_cp_schema',
     'prefixes': {'HP': {'prefix_prefix': 'HP',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/HP_'},
                  'MONDO': {'prefix_prefix': 'MONDO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/MONDO_'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'rapidcp': {'prefix_prefix': 'rapidcp',
                              'prefix_reference': 'https://mendelian.co/schemas/rapid-cp-logic/'}},
     'source_file': 'src/rapid_cp_schema/schema/rapid_cp_schema.yaml'} )

class CPLevel(str, Enum):
    """
    How a CP's features combine into a flag. The level decides which logic block the CP carries: `disjuncts` (L1), `rules` (L2A) or `score` (L2B); L3 has none yet.
    """
    L1 = "L1"
    """
    Safe Alone - union of S1 (highly specific) disjuncts.
    """
    L2A = "L2A"
    """
    Deterministic rules - Boolean gates.
    """
    L2B = "L2B"
    """
    Deterministic score - weighted points vs threshold.
    """
    L3 = "L3"
    """
    Profile match - declared here, not in scope.
    """


class SearchMode(str, Enum):
    """
    Which patients a CP searches: the whole dataset, or only those with an umbrella code.
    """
    population = "population"
    """
    Search the whole dataset for the target disease.
    """
    cluster = "cluster"
    """
    Search only persons carrying an umbrella code (see `cluster`).
    """


class FlagRateBasis(str, Enum):
    """
    Where the numbers in an expected flag rate come from.
    """
    measured = "measured"
    """
    From measured prevalence data.
    """
    class_band = "class_band"
    """
    From Orphanet's prevalence class only (no point figure).
    """
    none = "none"
    """
    No usable epidemiology - a normal outcome for many rare diseases.
    """


class ReviewDecision(str, Enum):
    """
    The outcome of a clinical review of a CP.
    """
    proceed = "proceed"
    """
    Criteria are sound; the CP can go to sites.
    """
    revise = "revise"
    """
    Send back for revision.
    """


class Module(str, Enum):
    """
    The evidence domain a feature belongs to. Drives which OMOP tables are searched and which vocabularies are allowed.
    """
    diagnostic_code = "diagnostic_code"
    """
    ICD10CM or SNOMED diagnosis; presence ever.
    """
    genetic_finding = "genetic_finding"
    """
    Reported pathogenic / likely pathogenic variant in a causal gene.
    """
    diagnostic_test = "diagnostic_test"
    """
    Confirmatory test or biomarker RESULT (not the order).
    """
    medication = "medication"
    """
    Disease-specific drug, used as evidence of the diagnosis.
    """
    procedure = "procedure"
    """
    Diagnostic procedure, or disease-specific therapeutic procedure.
    """
    phenotype = "phenotype"
    """
    Clinical/phenotypic feature: SNOMED, ICD10CM, or LOINC with a result.
    """


class CodeSystem(str, Enum):
    """
    CP-side vocabulary names.
    """
    ICD10CM = "ICD10CM"
    """
    Athena `vocabulary_id` `ICD10CM`. Dotted codes (`E83.31`).
    """
    SNOMED = "SNOMED"
    """
    Athena `SNOMED`.
    """
    LOINC = "LOINC"
    """
    Athena `LOINC` (includes LA answer codes).
    """
    RXNORM = "RXNORM"
    """
    Athena `RxNorm`.
    """
    UCUM = "UCUM"
    """
    Athena `UCUM`. Result units only.
    """


class ResultKind(str, Enum):
    """
    Whether a result is compared with a threshold or matched against a set of accepted answers.
    """
    numeric = "numeric"
    """
    `value_as_number` compared to a threshold.
    """
    qualitative = "qualitative"
    """
    `value_as_concept_id` in a set of answer concepts.
    """


class ResultOperator(str, Enum):
    """
    How a `numeric` result is compared: with a fixed threshold, a fixed range, or the normal range recorded with the result.
    """
    gt = "gt"
    """
    `x > value`
    """
    gte = "gte"
    """
    `x >= value`
    """
    lt = "lt"
    """
    `x < value`
    """
    lte = "lte"
    """
    `x <= value`
    """
    between = "between"
    """
    `value <= x <= value_high`
    """
    above_ref_high = "above_ref_high"
    """
    `x > range_high`, the upper limit recorded on the same row (`measurement` only).
    """
    below_ref_low = "below_ref_low"
    """
    `x < range_low`, the lower limit recorded on the same row (`measurement` only).
    """



class ComputablePhenotype(ConfiguredBaseModel):
    """
    One versioned CP. File name must equal `cp_id` + `.yaml`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic',
         'tree_root': True})

    cp_id: str = Field(default=..., description="""Name of the CP version, built from the disease, level and version. Format: `<disease-id>_<level>_v<major>.<minor>`, where `<disease-id>` is the lowercase Mondo id + '-' + disease.slug, e.g. `mondo0010619-xlh_L1_v1.0`""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    schema_version: str = Field(default=..., description="""Version of THIS schema the file conforms to, e.g. `0.2.0`""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    title: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    disease: DiseaseRef = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    level: CPLevel = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    search_mode: SearchMode = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    cluster: Optional[ClusterScope] = Field(default=None, description="""Required if and only if `search_mode` is `cluster`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    provenance: CPProvenance = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    review: Optional[ClinicalReview] = Field(default=None, description="""Clinical sign-off. Recorded only; not enforced.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    expected_flag_rate: Optional[ExpectedFlagRate] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    features: list[Feature] = Field(default=..., description="""Atomic evidence items. Logic blocks reference them by id.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    disjuncts: Optional[list[Disjunct]] = Field(default=None, description="""Level 1 only.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    rules: Optional[list[Rule]] = Field(default=None, description="""Level 2a only. CP fires if ANY rule fires.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    score: Optional[ScoreModel] = Field(default=None, description="""Level 2b only.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    absorbed_into: Optional[str] = Field(default=None, description="""The cluster CP that currently handles this disease, e.g. `cluster-icd10n18x_L2A_v1.0`. Empty once the disease stands alone. Cluster CPs themselves are not supported yet; the field and the `cluster-` naming are reserved so nothing needs renaming later.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })
    notes: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ComputablePhenotype']} })

    @field_validator('cp_id')
    def pattern_cp_id(cls, v):
        pattern=re.compile(r"^mondo[0-9]{7}-[a-z0-9]+(-[a-z0-9]+)*_(L1|L2A|L2B|L3)_v[0-9]+\.[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid cp_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid cp_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('absorbed_into')
    def pattern_absorbed_into(cls, v):
        pattern=re.compile(r"^cluster-[a-z0-9]+_(L1|L2A|L2B|L3)_v[0-9]+\.[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid absorbed_into format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid absorbed_into format: {v}"
            raise ValueError(err_msg)
        return v


class DiseaseRef(ConfiguredBaseModel):
    """
    The disease a CP is for, identified by an anchor Mondo id.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    mondo_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['DiseaseRef']} })
    slug: str = Field(default=..., description="""Short lowercase hyphenated disease name used in file names, e.g. `xlh`, `fabry`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiseaseRef']} })
    name: str = Field(default=..., description="""Human-readable disease name, for reviewers. Not queried.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiseaseRef', 'Feature']} })
    included_mondo_ids: Optional[list[str]] = Field(default=None, description="""Every Mondo id that constitutes this disease entity, `mondo_id` included. Defaults to `[mondo_id]`. Recorded, not queried.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiseaseRef']} })
    curation_record_version: Optional[str] = Field(default=None, description="""Version of the curation record (keyed by `mondo_id`) this CP was built from. Recorded, not queried.""", json_schema_extra = { "linkml_meta": {'domain_of': ['DiseaseRef']} })

    @field_validator('mondo_id')
    def pattern_mondo_id(cls, v):
        pattern=re.compile(r"^MONDO:[0-9]{7}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid mondo_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid mondo_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('slug')
    def pattern_slug(cls, v):
        pattern=re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid slug format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid slug format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('included_mondo_ids')
    def pattern_included_mondo_ids(cls, v):
        pattern=re.compile(r"^MONDO:[0-9]{7}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid included_mondo_ids format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid included_mondo_ids format: {v}"
            raise ValueError(err_msg)
        return v


class ClusterScope(ConfiguredBaseModel):
    """
    Limits the search to patients who have at least one of the umbrella codes. Every criterion is then evaluated only for those patients.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    umbrella_codes: list[CodeRef] = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ClusterScope']} })
    candidate_mondo_ids: Optional[list[str]] = Field(default=None, description="""Documentation only: the diseases under the umbrella. Not queried; each candidate gets its own CP.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClusterScope']} })


class CPProvenance(ConfiguredBaseModel):
    """
    Who wrote this CP version and when.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    authored_by: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['CPProvenance']} })
    authored_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['CPProvenance']} })
    kg_extracted_at: Optional[datetime ] = Field(default=None, description="""When Mendelian extracted the source data behind the features (ISO 8601, e.g. `2026-09-24T14:05:00Z`).""", json_schema_extra = { "linkml_meta": {'domain_of': ['CPProvenance']} })
    change_note: Optional[str] = Field(default=None, description="""Why this version exists (PR description summary).""", json_schema_extra = { "linkml_meta": {'domain_of': ['CPProvenance']} })
    supersedes: Optional[str] = Field(default=None, description="""Previous `cp_id`, if any.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CPProvenance']} })


class ClinicalReview(ConfiguredBaseModel):
    """
    Expert sign-off on the disease and its criteria, before the CP is tested at a site.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    reviewer: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalReview']} })
    date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalReview']} })
    decision: ReviewDecision = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalReview']} })
    comments: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalReview']} })


class ExpectedFlagRate(ConfiguredBaseModel):
    """
    Range of patients per 100,000 a correct CP should flag at a site.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    low_per_100k: Optional[float] = Field(default=None, description="""May be omitted for an open-ended range.""", ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ExpectedFlagRate']} })
    high_per_100k: Optional[float] = Field(default=None, description="""Required unless `basis` is `none`.""", ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ExpectedFlagRate']} })
    basis: FlagRateBasis = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ExpectedFlagRate']} })
    source: str = Field(default=..., description="""Which pipeline run or reference produced the range.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ExpectedFlagRate']} })


class Feature(ConfiguredBaseModel):
    """
    One piece of evidence: a set of codes for one module, plus the result or genetic finding that must be found where the module needs one. Logic blocks refer to features by id.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Feature', 'Disjunct', 'Rule', 'ScoreItem']} })
    module: Module = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })
    name: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['DiseaseRef', 'Feature']} })
    specificity_grade: int = Field(default=..., description="""Specificity grade, written S1 to S5 in prose (1 = confirmatory/pathognomonic ... 5 = incidental). L1 disjuncts may only use S1 features.""", ge=1, le=5, json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })
    hpo_id: Optional[str] = Field(default=None, description="""Phenotype features: the HPO term this realises (annotation only, not queried).""", json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })
    codes: list[CodeRef] = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })
    result: Optional[ResultCriterion] = Field(default=None, description="""Required for `diagnostic_test` features and for LOINC-coded `phenotype` features.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })
    genetic: Optional[GeneticCriterion] = Field(default=None, description="""Required for `genetic_finding` features.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })
    include_personal_history: Optional[bool] = Field(default=None, description="""`diagnostic_code` and coded `phenotype` features only. Default `true`: also count `observation` rows recording the patient's own history of the condition. Set `false` to count only direct records.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })
    text_terms: Optional[list[str]] = Field(default=None, description="""Names and synonyms for what the feature describes (a disease, a finding, a test or a drug), for a future text-search (NLP) step.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Feature']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^f[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class CodeRef(ConfiguredBaseModel):
    """
    A code written as it appears in its source vocabulary, never as an OMOP `concept_id`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    vocabulary: CodeSystem = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['CodeRef']} })
    code: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['CodeRef']} })
    label: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['CodeRef', 'Disjunct', 'Rule']} })
    include_descendants: Optional[bool] = Field(default=None, description="""Default `true` for a feature's main codes, `false` for result value and unit codes. SNOMED/LOINC/RxNorm expand via `CONCEPT_ANCESTOR`; ICD10CM expands by code prefix.""", json_schema_extra = { "linkml_meta": {'domain_of': ['CodeRef']} })


class ResultCriterion(ConfiguredBaseModel):
    """
    The result a test or measurement record must have to count: a numeric comparison or a set of accepted answers.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    kind: ResultKind = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ResultCriterion']} })
    operator: Optional[ResultOperator] = Field(default=None, description="""`numeric` only""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResultCriterion']} })
    value: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResultCriterion']} })
    value_high: Optional[float] = Field(default=None, description="""`between` only""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResultCriterion']} })
    units: Optional[list[CodeRef]] = Field(default=None, description="""UCUM units the threshold applies to. Strongly recommended for `numeric`.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResultCriterion']} })
    value_concepts: Optional[list[CodeRef]] = Field(default=None, description="""`qualitative` only: accepted answers (e.g. LOINC `LA6576-8` Positive).""", json_schema_extra = { "linkml_meta": {'domain_of': ['ResultCriterion']} })


class GeneticCriterion(ConfiguredBaseModel):
    """
    The variant result a `genetic_finding` feature looks for: a causal gene and the interpretations that count, such as pathogenic or likely pathogenic. A record matches when it carries one of the feature's codes, its interpretation is one of those listed (if any are), and, when `require_gene_text_match` is `true`, the gene symbol appears in the record's text.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    gene_symbol: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['GeneticCriterion']} })
    hgnc_id: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['GeneticCriterion']} })
    interpretations: Optional[list[CodeRef]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['GeneticCriterion']} })
    require_gene_text_match: Optional[bool] = Field(default=None, description="""Default `true` when codes are generic LOINC panels.""", json_schema_extra = { "linkml_meta": {'domain_of': ['GeneticCriterion']} })

    @field_validator('hgnc_id')
    def pattern_hgnc_id(cls, v):
        pattern=re.compile(r"^HGNC:[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid hgnc_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid hgnc_id format: {v}"
            raise ValueError(err_msg)
        return v


class Disjunct(ConfiguredBaseModel):
    """
    A Level 1 criterion: one S1 feature that is enough on its own to flag a patient. Its id is reported with the counts.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Feature', 'Disjunct', 'Rule', 'ScoreItem']} })
    feature: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    min_distinct_dates: Optional[int] = Field(default=None, ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    min_span_days: Optional[int] = Field(default=None, description="""Records must stretch across at least this many days, first to last.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    label: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['CodeRef', 'Disjunct', 'Rule']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^d[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Rule(ConfiguredBaseModel):
    """
    A Level 2A criterion: a Boolean condition over features. A patient is flagged if any rule holds; each rule's id is reported with the counts.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Feature', 'Disjunct', 'Rule', 'ScoreItem']} })
    label: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['CodeRef', 'Disjunct', 'Rule']} })
    expr: Expr = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Rule']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^r[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Expr(ConfiguredBaseModel):
    """
    One condition in a Level 2A rule. Each node uses exactly one form: `feature`, `all_of`, `any_of`, `none_of` (none of the listed conditions holds), `at_least` with `of`, or `within`. A rule must contain at least one feature that isn't under `none_of`. `min_distinct_dates` and `min_span_days` apply only to a `feature` node.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    feature: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    min_distinct_dates: Optional[int] = Field(default=None, ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    min_span_days: Optional[int] = Field(default=None, description="""Records must stretch across at least this many days, first to last.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    all_of: Optional[list[Expr]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Expr']} })
    any_of: Optional[list[Expr]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Expr']} })
    none_of: Optional[list[Expr]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Expr']} })
    at_least: Optional[int] = Field(default=None, ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['Expr']} })
    of: Optional[list[Expr]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Expr', 'Within']} })
    within: Optional[Within] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Expr']} })


class Within(ConfiguredBaseModel):
    """
    A record of each listed feature, all falling within `days` of each other. With `in_order`, the records must also occur in the listed order (the same day counts as in order).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    days: int = Field(default=..., ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Within']} })
    in_order: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Within']} })
    of: list[str] = Field(default=..., description="""Feature ids, at least two.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Expr', 'Within']} })


class ScoreModel(ConfiguredBaseModel):
    """
    The Level 2B logic: a patient is flagged when the points of the items that apply add up to the threshold.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    threshold: float = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ScoreModel']} })
    items: list[ScoreItem] = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ScoreModel']} })


class ScoreItem(ConfiguredBaseModel):
    """
    A Level 2B score item: points added when its feature is present. Its id is reported with the counts.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://mendelian.co/schemas/rapid-cp-logic'})

    id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Feature', 'Disjunct', 'Rule', 'ScoreItem']} })
    feature: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    points: float = Field(default=..., description="""May be negative.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ScoreItem']} })
    min_distinct_dates: Optional[int] = Field(default=None, ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })
    min_span_days: Optional[int] = Field(default=None, description="""Records must stretch across at least this many days, first to last.""", ge=1, json_schema_extra = { "linkml_meta": {'domain_of': ['Disjunct', 'Expr', 'ScoreItem']} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^s[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
ComputablePhenotype.model_rebuild()
DiseaseRef.model_rebuild()
ClusterScope.model_rebuild()
CPProvenance.model_rebuild()
ClinicalReview.model_rebuild()
ExpectedFlagRate.model_rebuild()
Feature.model_rebuild()
CodeRef.model_rebuild()
ResultCriterion.model_rebuild()
GeneticCriterion.model_rebuild()
Disjunct.model_rebuild()
Rule.model_rebuild()
Expr.model_rebuild()
Within.model_rebuild()
ScoreModel.model_rebuild()
ScoreItem.model_rebuild()
