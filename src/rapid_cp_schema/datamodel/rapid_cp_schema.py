# Auto generated from rapid_cp_schema.yaml by pythongen.py version: 0.0.1
# Schema: rapid_cp_schema
#
# id: https://mendelian.co/schemas/rapid-cp-logic
# description: Schema for the two files that make up a deployable RAPID computable phenotype (CP):
#
#     1. The CP logic file  <disease-id>_<level>_v<major>.<minor>.yaml
#        Data-model-independent. Says WHAT counts as evidence (features, coded in
#        source vocabularies: ICD10CM, SNOMED, LOINC, RxNorm, ...) and HOW the
#        evidence combines (Level 1 disjuncts, Level 2a rules, Level 2b score).
#        Every disjunct / rule / score item carries a stable id (d1, r2, s3) that
#        is reported back as the flag reason.
#
#     2. The build file  <cp-id>_<datamodel>.b<build>.sql
#        The generated SQL for one data model (e.g. OMOP 5.4), shared by every
#        site on it, with a YAML comment header that conforms to CPBuild.
#
#     3. Site files  sites/<site>_v<version>.yaml
#        Everything about one site (schemas, vocabulary release, history
#        concepts), applied at run time.
#
#   This schema is deliberately separate from the curation-record schema. The curation record holds the full evidence base and review trail; the CP logic file is the executable subset selected from it. Diseases are identified by Mondo ids only.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Float, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, XSDDate, XSDDateTime

metamodel_version = "1.12.0"
version = "0.1.0"

# Namespaces
HP = CurieNamespace('HP', 'http://purl.obolibrary.org/obo/HP_')
MONDO = CurieNamespace('MONDO', 'http://purl.obolibrary.org/obo/MONDO_')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RAPIDCP = CurieNamespace('rapidcp', 'https://mendelian.co/schemas/rapid-cp-logic/')
DEFAULT_ = RAPIDCP


# Types

# Class references
class ComputablePhenotypeCpId(extended_str):
    pass


class FeatureId(extended_str):
    pass


class DisjunctId(extended_str):
    pass


class RuleId(extended_str):
    pass


class ScoreItemId(extended_str):
    pass


class CPBuildBuildId(extended_str):
    pass


@dataclass(repr=False)
class ComputablePhenotype(YAMLRoot):
    """
    One versioned CP. File name must equal cp_id + ".yaml".
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["ComputablePhenotype"]
    class_class_curie: ClassVar[str] = "rapidcp:ComputablePhenotype"
    class_name: ClassVar[str] = "ComputablePhenotype"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.ComputablePhenotype

    cp_id: Union[str, ComputablePhenotypeCpId] = None
    schema_version: str = None
    title: str = None
    disease: Union[dict, "DiseaseRef"] = None
    level: Union[str, "CPLevel"] = None
    search_mode: Union[str, "SearchMode"] = None
    status: Union[str, "CPStatus"] = None
    provenance: Union[dict, "CPProvenance"] = None
    features: Union[dict[Union[str, FeatureId], Union[dict, "Feature"]], list[Union[dict, "Feature"]]] = empty_dict()
    cluster: Optional[Union[dict, "ClusterScope"]] = None
    review: Optional[Union[dict, "ClinicalReview"]] = None
    sites_tested: Optional[Union[Union[dict, "SiteTest"], list[Union[dict, "SiteTest"]]]] = empty_list()
    expected_flag_rate: Optional[Union[dict, "ExpectedFlagRate"]] = None
    disjuncts: Optional[Union[dict[Union[str, DisjunctId], Union[dict, "Disjunct"]], list[Union[dict, "Disjunct"]]]] = empty_dict()
    rules: Optional[Union[dict[Union[str, RuleId], Union[dict, "Rule"]], list[Union[dict, "Rule"]]]] = empty_dict()
    score: Optional[Union[dict, "ScoreModel"]] = None
    absorbed_into: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.cp_id):
            self.MissingRequiredField("cp_id")
        if not isinstance(self.cp_id, ComputablePhenotypeCpId):
            self.cp_id = ComputablePhenotypeCpId(self.cp_id)

        if self._is_empty(self.schema_version):
            self.MissingRequiredField("schema_version")
        if not isinstance(self.schema_version, str):
            self.schema_version = str(self.schema_version)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.disease):
            self.MissingRequiredField("disease")
        if not isinstance(self.disease, DiseaseRef):
            self.disease = DiseaseRef(**as_dict(self.disease))

        if self._is_empty(self.level):
            self.MissingRequiredField("level")
        if not isinstance(self.level, CPLevel):
            self.level = CPLevel(self.level)

        if self._is_empty(self.search_mode):
            self.MissingRequiredField("search_mode")
        if not isinstance(self.search_mode, SearchMode):
            self.search_mode = SearchMode(self.search_mode)

        if self._is_empty(self.status):
            self.MissingRequiredField("status")
        if not isinstance(self.status, CPStatus):
            self.status = CPStatus(self.status)

        if self._is_empty(self.provenance):
            self.MissingRequiredField("provenance")
        if not isinstance(self.provenance, CPProvenance):
            self.provenance = CPProvenance(**as_dict(self.provenance))

        if self._is_empty(self.features):
            self.MissingRequiredField("features")
        self._normalize_inlined_as_list(slot_name="features", slot_type=Feature, key_name="id", keyed=True)

        if self.cluster is not None and not isinstance(self.cluster, ClusterScope):
            self.cluster = ClusterScope(**as_dict(self.cluster))

        if self.review is not None and not isinstance(self.review, ClinicalReview):
            self.review = ClinicalReview(**as_dict(self.review))

        self._normalize_inlined_as_list(slot_name="sites_tested", slot_type=SiteTest, key_name="site", keyed=False)

        if self.expected_flag_rate is not None and not isinstance(self.expected_flag_rate, ExpectedFlagRate):
            self.expected_flag_rate = ExpectedFlagRate(**as_dict(self.expected_flag_rate))

        self._normalize_inlined_as_list(slot_name="disjuncts", slot_type=Disjunct, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="rules", slot_type=Rule, key_name="id", keyed=True)

        if self.score is not None and not isinstance(self.score, ScoreModel):
            self.score = ScoreModel(**as_dict(self.score))

        if self.absorbed_into is not None and not isinstance(self.absorbed_into, str):
            self.absorbed_into = str(self.absorbed_into)

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DiseaseRef(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["DiseaseRef"]
    class_class_curie: ClassVar[str] = "rapidcp:DiseaseRef"
    class_name: ClassVar[str] = "DiseaseRef"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.DiseaseRef

    mondo_id: Union[str, URIorCURIE] = None
    slug: str = None
    name: str = None
    included_mondo_ids: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()
    curation_record_version: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.mondo_id):
            self.MissingRequiredField("mondo_id")
        if not isinstance(self.mondo_id, URIorCURIE):
            self.mondo_id = URIorCURIE(self.mondo_id)

        if self._is_empty(self.slug):
            self.MissingRequiredField("slug")
        if not isinstance(self.slug, str):
            self.slug = str(self.slug)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.included_mondo_ids, list):
            self.included_mondo_ids = [self.included_mondo_ids] if self.included_mondo_ids is not None else []
        self.included_mondo_ids = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.included_mondo_ids]

        if self.curation_record_version is not None and not isinstance(self.curation_record_version, str):
            self.curation_record_version = str(self.curation_record_version)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClusterScope(YAMLRoot):
    """
    Cluster-filtered search. The universe is persons with any of these umbrella codes (searched like a diagnostic_code
    feature); every criterion is then restricted to that universe.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["ClusterScope"]
    class_class_curie: ClassVar[str] = "rapidcp:ClusterScope"
    class_name: ClassVar[str] = "ClusterScope"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.ClusterScope

    umbrella_codes: Union[Union[dict, "CodeRef"], list[Union[dict, "CodeRef"]]] = None
    candidate_mondo_ids: Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.umbrella_codes):
            self.MissingRequiredField("umbrella_codes")
        self._normalize_inlined_as_list(slot_name="umbrella_codes", slot_type=CodeRef, key_name="vocabulary", keyed=False)

        if not isinstance(self.candidate_mondo_ids, list):
            self.candidate_mondo_ids = [self.candidate_mondo_ids] if self.candidate_mondo_ids is not None else []
        self.candidate_mondo_ids = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.candidate_mondo_ids]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CPProvenance(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["CPProvenance"]
    class_class_curie: ClassVar[str] = "rapidcp:CPProvenance"
    class_name: ClassVar[str] = "CPProvenance"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.CPProvenance

    authored_by: str = None
    authored_date: Union[str, XSDDate] = None
    kg_extracted_at: Optional[Union[str, XSDDateTime]] = None
    change_note: Optional[str] = None
    supersedes: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.authored_by):
            self.MissingRequiredField("authored_by")
        if not isinstance(self.authored_by, str):
            self.authored_by = str(self.authored_by)

        if self._is_empty(self.authored_date):
            self.MissingRequiredField("authored_date")
        if not isinstance(self.authored_date, XSDDate):
            self.authored_date = XSDDate(self.authored_date)

        if self.kg_extracted_at is not None and not isinstance(self.kg_extracted_at, XSDDateTime):
            self.kg_extracted_at = XSDDateTime(self.kg_extracted_at)

        if self.change_note is not None and not isinstance(self.change_note, str):
            self.change_note = str(self.change_note)

        if self.supersedes is not None and not isinstance(self.supersedes, str):
            self.supersedes = str(self.supersedes)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HistoryConcept(YAMLRoot):
    """
    Either a SNOMED CT code (vocabulary + code), looked up at the site with its descendants unless include_descendants
    is false, or a raw OMOP concept_id used as is, e.g. a site-local concept.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["HistoryConcept"]
    class_class_curie: ClassVar[str] = "rapidcp:HistoryConcept"
    class_name: ClassVar[str] = "HistoryConcept"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.HistoryConcept

    vocabulary: Optional[str] = None
    code: Optional[str] = None
    concept_id: Optional[int] = None
    label: Optional[str] = None
    include_descendants: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.vocabulary is not None and not isinstance(self.vocabulary, str):
            self.vocabulary = str(self.vocabulary)

        if self.code is not None and not isinstance(self.code, str):
            self.code = str(self.code)

        if self.concept_id is not None and not isinstance(self.concept_id, int):
            self.concept_id = int(self.concept_id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.include_descendants is not None and not isinstance(self.include_descendants, Bool):
            self.include_descendants = Bool(self.include_descendants)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SiteTest(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["SiteTest"]
    class_class_curie: ClassVar[str] = "rapidcp:SiteTest"
    class_name: ClassVar[str] = "SiteTest"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.SiteTest

    site: str = None
    site_version: int = None
    build: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.site):
            self.MissingRequiredField("site")
        if not isinstance(self.site, str):
            self.site = str(self.site)

        if self._is_empty(self.site_version):
            self.MissingRequiredField("site_version")
        if not isinstance(self.site_version, int):
            self.site_version = int(self.site_version)

        if self._is_empty(self.build):
            self.MissingRequiredField("build")
        if not isinstance(self.build, str):
            self.build = str(self.build)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClinicalReview(YAMLRoot):
    """
    Expert sign-off on the disease and its criteria, before the CP is tested at a site.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["ClinicalReview"]
    class_class_curie: ClassVar[str] = "rapidcp:ClinicalReview"
    class_name: ClassVar[str] = "ClinicalReview"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.ClinicalReview

    reviewer: str = None
    date: Union[str, XSDDate] = None
    decision: Union[str, "ReviewDecision"] = None
    comments: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.reviewer):
            self.MissingRequiredField("reviewer")
        if not isinstance(self.reviewer, str):
            self.reviewer = str(self.reviewer)

        if self._is_empty(self.date):
            self.MissingRequiredField("date")
        if not isinstance(self.date, XSDDate):
            self.date = XSDDate(self.date)

        if self._is_empty(self.decision):
            self.MissingRequiredField("decision")
        if not isinstance(self.decision, ReviewDecision):
            self.decision = ReviewDecision(self.decision)

        if self.comments is not None and not isinstance(self.comments, str):
            self.comments = str(self.comments)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExpectedFlagRate(YAMLRoot):
    """
    Range of patients per 100,000 a correct CP should flag at a site (prevalence x ascertainment), from the Expected
    Flag Rate Pipeline. A wide range, not a target; feeds the flag-rate gauge.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["ExpectedFlagRate"]
    class_class_curie: ClassVar[str] = "rapidcp:ExpectedFlagRate"
    class_name: ClassVar[str] = "ExpectedFlagRate"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.ExpectedFlagRate

    basis: Union[str, "FlagRateBasis"] = None
    source: str = None
    low_per_100k: Optional[float] = None
    high_per_100k: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.basis):
            self.MissingRequiredField("basis")
        if not isinstance(self.basis, FlagRateBasis):
            self.basis = FlagRateBasis(self.basis)

        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, str):
            self.source = str(self.source)

        if self.low_per_100k is not None and not isinstance(self.low_per_100k, float):
            self.low_per_100k = float(self.low_per_100k)

        if self.high_per_100k is not None and not isinstance(self.high_per_100k, float):
            self.high_per_100k = float(self.high_per_100k)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Feature(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["Feature"]
    class_class_curie: ClassVar[str] = "rapidcp:Feature"
    class_name: ClassVar[str] = "Feature"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.Feature

    id: Union[str, FeatureId] = None
    module: Union[str, "Module"] = None
    name: str = None
    specificity_tier: int = None
    codes: Union[Union[dict, "CodeRef"], list[Union[dict, "CodeRef"]]] = None
    hpo_id: Optional[Union[str, URIorCURIE]] = None
    result: Optional[Union[dict, "ResultCriterion"]] = None
    genetic: Optional[Union[dict, "GeneticCriterion"]] = None
    include_personal_history: Optional[Union[bool, Bool]] = None
    text_terms: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FeatureId):
            self.id = FeatureId(self.id)

        if self._is_empty(self.module):
            self.MissingRequiredField("module")
        if not isinstance(self.module, Module):
            self.module = Module(self.module)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self._is_empty(self.specificity_tier):
            self.MissingRequiredField("specificity_tier")
        if not isinstance(self.specificity_tier, int):
            self.specificity_tier = int(self.specificity_tier)

        if self._is_empty(self.codes):
            self.MissingRequiredField("codes")
        self._normalize_inlined_as_list(slot_name="codes", slot_type=CodeRef, key_name="vocabulary", keyed=False)

        if self.hpo_id is not None and not isinstance(self.hpo_id, URIorCURIE):
            self.hpo_id = URIorCURIE(self.hpo_id)

        if self.result is not None and not isinstance(self.result, ResultCriterion):
            self.result = ResultCriterion(**as_dict(self.result))

        if self.genetic is not None and not isinstance(self.genetic, GeneticCriterion):
            self.genetic = GeneticCriterion(**as_dict(self.genetic))

        if self.include_personal_history is not None and not isinstance(self.include_personal_history, Bool):
            self.include_personal_history = Bool(self.include_personal_history)

        if not isinstance(self.text_terms, list):
            self.text_terms = [self.text_terms] if self.text_terms is not None else []
        self.text_terms = [v if isinstance(v, str) else str(v) for v in self.text_terms]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CodeRef(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["CodeRef"]
    class_class_curie: ClassVar[str] = "rapidcp:CodeRef"
    class_name: ClassVar[str] = "CodeRef"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.CodeRef

    vocabulary: Union[str, "CodeSystem"] = None
    code: str = None
    label: Optional[str] = None
    include_descendants: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.vocabulary):
            self.MissingRequiredField("vocabulary")
        if not isinstance(self.vocabulary, CodeSystem):
            self.vocabulary = CodeSystem(self.vocabulary)

        if self._is_empty(self.code):
            self.MissingRequiredField("code")
        if not isinstance(self.code, str):
            self.code = str(self.code)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.include_descendants is not None and not isinstance(self.include_descendants, Bool):
            self.include_descendants = Bool(self.include_descendants)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ResultCriterion(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["ResultCriterion"]
    class_class_curie: ClassVar[str] = "rapidcp:ResultCriterion"
    class_name: ClassVar[str] = "ResultCriterion"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.ResultCriterion

    kind: Union[str, "ResultKind"] = None
    operator: Optional[Union[str, "ResultOperator"]] = None
    value: Optional[float] = None
    value_high: Optional[float] = None
    units: Optional[Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]]] = empty_list()
    value_concepts: Optional[Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.kind):
            self.MissingRequiredField("kind")
        if not isinstance(self.kind, ResultKind):
            self.kind = ResultKind(self.kind)

        if self.operator is not None and not isinstance(self.operator, ResultOperator):
            self.operator = ResultOperator(self.operator)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        if self.value_high is not None and not isinstance(self.value_high, float):
            self.value_high = float(self.value_high)

        self._normalize_inlined_as_list(slot_name="units", slot_type=CodeRef, key_name="vocabulary", keyed=False)

        self._normalize_inlined_as_list(slot_name="value_concepts", slot_type=CodeRef, key_name="vocabulary", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeneticCriterion(YAMLRoot):
    """
    A row qualifies if its concept is in the feature's codes AND (when given) its value_as_concept_id is an accepted
    interpretation AND (when require_gene_text_match) the gene symbol appears in the row's source text.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["GeneticCriterion"]
    class_class_curie: ClassVar[str] = "rapidcp:GeneticCriterion"
    class_name: ClassVar[str] = "GeneticCriterion"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.GeneticCriterion

    gene_symbol: str = None
    hgnc_id: Optional[str] = None
    interpretations: Optional[Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]]] = empty_list()
    require_gene_text_match: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.gene_symbol):
            self.MissingRequiredField("gene_symbol")
        if not isinstance(self.gene_symbol, str):
            self.gene_symbol = str(self.gene_symbol)

        if self.hgnc_id is not None and not isinstance(self.hgnc_id, str):
            self.hgnc_id = str(self.hgnc_id)

        self._normalize_inlined_as_list(slot_name="interpretations", slot_type=CodeRef, key_name="vocabulary", keyed=False)

        if self.require_gene_text_match is not None and not isinstance(self.require_gene_text_match, Bool):
            self.require_gene_text_match = Bool(self.require_gene_text_match)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Disjunct(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["Disjunct"]
    class_class_curie: ClassVar[str] = "rapidcp:Disjunct"
    class_name: ClassVar[str] = "Disjunct"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.Disjunct

    id: Union[str, DisjunctId] = None
    feature: str = None
    min_distinct_dates: Optional[int] = None
    min_span_days: Optional[int] = None
    label: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DisjunctId):
            self.id = DisjunctId(self.id)

        if self._is_empty(self.feature):
            self.MissingRequiredField("feature")
        if not isinstance(self.feature, str):
            self.feature = str(self.feature)

        if self.min_distinct_dates is not None and not isinstance(self.min_distinct_dates, int):
            self.min_distinct_dates = int(self.min_distinct_dates)

        if self.min_span_days is not None and not isinstance(self.min_span_days, int):
            self.min_span_days = int(self.min_span_days)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Rule(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["Rule"]
    class_class_curie: ClassVar[str] = "rapidcp:Rule"
    class_name: ClassVar[str] = "Rule"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.Rule

    id: Union[str, RuleId] = None
    expr: Union[dict, "Expr"] = None
    label: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RuleId):
            self.id = RuleId(self.id)

        if self._is_empty(self.expr):
            self.MissingRequiredField("expr")
        if not isinstance(self.expr, Expr):
            self.expr = Expr(**as_dict(self.expr))

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Expr(YAMLRoot):
    """
    Exactly one of: feature | all_of | any_of | none_of | at_least+of | within. none_of = NOT(any of). A rule must
    contain at least one positive feature. min_distinct_dates / min_span_days apply to a feature leaf.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["Expr"]
    class_class_curie: ClassVar[str] = "rapidcp:Expr"
    class_name: ClassVar[str] = "Expr"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.Expr

    feature: Optional[str] = None
    min_distinct_dates: Optional[int] = None
    min_span_days: Optional[int] = None
    all_of: Optional[Union[Union[dict, "Expr"], list[Union[dict, "Expr"]]]] = empty_list()
    any_of: Optional[Union[Union[dict, "Expr"], list[Union[dict, "Expr"]]]] = empty_list()
    none_of: Optional[Union[Union[dict, "Expr"], list[Union[dict, "Expr"]]]] = empty_list()
    at_least: Optional[int] = None
    of: Optional[Union[Union[dict, "Expr"], list[Union[dict, "Expr"]]]] = empty_list()
    within: Optional[Union[dict, "Within"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.feature is not None and not isinstance(self.feature, str):
            self.feature = str(self.feature)

        if self.min_distinct_dates is not None and not isinstance(self.min_distinct_dates, int):
            self.min_distinct_dates = int(self.min_distinct_dates)

        if self.min_span_days is not None and not isinstance(self.min_span_days, int):
            self.min_span_days = int(self.min_span_days)

        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [v if isinstance(v, Expr) else Expr(**as_dict(v)) for v in self.all_of]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [v if isinstance(v, Expr) else Expr(**as_dict(v)) for v in self.any_of]

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [v if isinstance(v, Expr) else Expr(**as_dict(v)) for v in self.none_of]

        if self.at_least is not None and not isinstance(self.at_least, int):
            self.at_least = int(self.at_least)

        if not isinstance(self.of, list):
            self.of = [self.of] if self.of is not None else []
        self.of = [v if isinstance(v, Expr) else Expr(**as_dict(v)) for v in self.of]

        if self.within is not None and not isinstance(self.within, Within):
            self.within = Within(**as_dict(self.within))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Within(YAMLRoot):
    """
    A record of each listed feature, all falling within `days` of each other. With in_order, the records must also
    occur in the listed order (the same day counts as in order).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["Within"]
    class_class_curie: ClassVar[str] = "rapidcp:Within"
    class_name: ClassVar[str] = "Within"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.Within

    days: int = None
    of: Union[str, list[str]] = None
    in_order: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.days):
            self.MissingRequiredField("days")
        if not isinstance(self.days, int):
            self.days = int(self.days)

        if self._is_empty(self.of):
            self.MissingRequiredField("of")
        if not isinstance(self.of, list):
            self.of = [self.of] if self.of is not None else []
        self.of = [v if isinstance(v, str) else str(v) for v in self.of]

        if self.in_order is not None and not isinstance(self.in_order, Bool):
            self.in_order = Bool(self.in_order)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ScoreModel(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["ScoreModel"]
    class_class_curie: ClassVar[str] = "rapidcp:ScoreModel"
    class_name: ClassVar[str] = "ScoreModel"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.ScoreModel

    threshold: float = None
    items: Union[dict[Union[str, ScoreItemId], Union[dict, "ScoreItem"]], list[Union[dict, "ScoreItem"]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.threshold):
            self.MissingRequiredField("threshold")
        if not isinstance(self.threshold, float):
            self.threshold = float(self.threshold)

        if self._is_empty(self.items):
            self.MissingRequiredField("items")
        self._normalize_inlined_as_list(slot_name="items", slot_type=ScoreItem, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ScoreItem(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["ScoreItem"]
    class_class_curie: ClassVar[str] = "rapidcp:ScoreItem"
    class_name: ClassVar[str] = "ScoreItem"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.ScoreItem

    id: Union[str, ScoreItemId] = None
    feature: str = None
    points: float = None
    min_distinct_dates: Optional[int] = None
    min_span_days: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ScoreItemId):
            self.id = ScoreItemId(self.id)

        if self._is_empty(self.feature):
            self.MissingRequiredField("feature")
        if not isinstance(self.feature, str):
            self.feature = str(self.feature)

        if self._is_empty(self.points):
            self.MissingRequiredField("points")
        if not isinstance(self.points, float):
            self.points = float(self.points)

        if self.min_distinct_dates is not None and not isinstance(self.min_distinct_dates, int):
            self.min_distinct_dates = int(self.min_distinct_dates)

        if self.min_span_days is not None and not isinstance(self.min_span_days, int):
            self.min_span_days = int(self.min_span_days)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CPBuild(YAMLRoot):
    """
    Header of a build SQL file (<build_id>.sql): the YAML between "-- cpsql-build" and "-- end-cpsql-build", with the
    "-- " prefixes removed. Only CP-dependent fields; site settings are in site files.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["CPBuild"]
    class_class_curie: ClassVar[str] = "rapidcp:CPBuild"
    class_name: ClassVar[str] = "CPBuild"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.CPBuild

    build_id: Union[str, CPBuildBuildId] = None
    cp_id: str = None
    datamodel: Union[str, "DataModel"] = None
    build: int = None
    generator: Optional[str] = None
    cp_logic_sha256: Optional[str] = None
    change_note: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.build_id):
            self.MissingRequiredField("build_id")
        if not isinstance(self.build_id, CPBuildBuildId):
            self.build_id = CPBuildBuildId(self.build_id)

        if self._is_empty(self.cp_id):
            self.MissingRequiredField("cp_id")
        if not isinstance(self.cp_id, str):
            self.cp_id = str(self.cp_id)

        if self._is_empty(self.datamodel):
            self.MissingRequiredField("datamodel")
        if not isinstance(self.datamodel, DataModel):
            self.datamodel = DataModel(self.datamodel)

        if self._is_empty(self.build):
            self.MissingRequiredField("build")
        if not isinstance(self.build, int):
            self.build = int(self.build)

        if self.generator is not None and not isinstance(self.generator, str):
            self.generator = str(self.generator)

        if self.cp_logic_sha256 is not None and not isinstance(self.cp_logic_sha256, str):
            self.cp_logic_sha256 = str(self.cp_logic_sha256)

        if self.change_note is not None and not isinstance(self.change_note, str):
            self.change_note = str(self.change_note)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SiteProfile(YAMLRoot):
    """
    Site file, sites/<site>_v<version>.yaml: everything about running builds at one site. Applied at run time by
    `cpsql render --site`, so one build serves every site on a data model. Any change is a new version (new file); old
    versions are kept so past runs can be reproduced.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RAPIDCP["SiteProfile"]
    class_class_curie: ClassVar[str] = "rapidcp:SiteProfile"
    class_name: ClassVar[str] = "SiteProfile"
    class_model_uri: ClassVar[URIRef] = RAPIDCP.SiteProfile

    site: str = None
    version: int = None
    datamodel: Union[str, "DataModel"] = None
    vocabulary_version: str = None
    cdm_schema: str = None
    vocab_schema: str = None
    updated: Union[str, XSDDate] = None
    cdm_version: Optional[str] = None
    dialect: Optional[Union[str, "SqlDialect"]] = None
    source_value_fallback: Optional[Union[bool, Bool]] = None
    personal_history_concepts: Optional[Union[Union[dict, HistoryConcept], list[Union[dict, HistoryConcept]]]] = empty_list()
    change_note: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.site):
            self.MissingRequiredField("site")
        if not isinstance(self.site, str):
            self.site = str(self.site)

        if self._is_empty(self.version):
            self.MissingRequiredField("version")
        if not isinstance(self.version, int):
            self.version = int(self.version)

        if self._is_empty(self.datamodel):
            self.MissingRequiredField("datamodel")
        if not isinstance(self.datamodel, DataModel):
            self.datamodel = DataModel(self.datamodel)

        if self._is_empty(self.vocabulary_version):
            self.MissingRequiredField("vocabulary_version")
        if not isinstance(self.vocabulary_version, str):
            self.vocabulary_version = str(self.vocabulary_version)

        if self._is_empty(self.cdm_schema):
            self.MissingRequiredField("cdm_schema")
        if not isinstance(self.cdm_schema, str):
            self.cdm_schema = str(self.cdm_schema)

        if self._is_empty(self.vocab_schema):
            self.MissingRequiredField("vocab_schema")
        if not isinstance(self.vocab_schema, str):
            self.vocab_schema = str(self.vocab_schema)

        if self._is_empty(self.updated):
            self.MissingRequiredField("updated")
        if not isinstance(self.updated, XSDDate):
            self.updated = XSDDate(self.updated)

        if self.cdm_version is not None and not isinstance(self.cdm_version, str):
            self.cdm_version = str(self.cdm_version)

        if self.dialect is not None and not isinstance(self.dialect, SqlDialect):
            self.dialect = SqlDialect(self.dialect)

        if self.source_value_fallback is not None and not isinstance(self.source_value_fallback, Bool):
            self.source_value_fallback = Bool(self.source_value_fallback)

        if not isinstance(self.personal_history_concepts, list):
            self.personal_history_concepts = [self.personal_history_concepts] if self.personal_history_concepts is not None else []
        self.personal_history_concepts = [v if isinstance(v, HistoryConcept) else HistoryConcept(**as_dict(v)) for v in self.personal_history_concepts]

        if self.change_note is not None and not isinstance(self.change_note, str):
            self.change_note = str(self.change_note)

        super().__post_init__(**kwargs)


# Enumerations
class CPLevel(EnumDefinitionImpl):

    L1 = PermissibleValue(
        text="L1",
        description="Safe Alone - union of Tier-1 (highly-specific) disjuncts.")
    L2A = PermissibleValue(
        text="L2A",
        description="Deterministic rules - Boolean gates.")
    L2B = PermissibleValue(
        text="L2B",
        description="Deterministic score - weighted points vs threshold.")
    L3 = PermissibleValue(
        text="L3",
        description="Profile match - declared here, not generated by cpsql.")

    _defn = EnumDefinition(
        name="CPLevel",
    )

class SearchMode(EnumDefinitionImpl):

    population = PermissibleValue(
        text="population",
        description="Search the whole dataset for the target disease.")
    cluster = PermissibleValue(
        text="cluster",
        description="Search only persons carrying an umbrella code (see cluster).")

    _defn = EnumDefinition(
        name="SearchMode",
    )

class FlagRateBasis(EnumDefinitionImpl):

    measured = PermissibleValue(
        text="measured",
        description="From measured prevalence data.")
    class_band = PermissibleValue(
        text="class_band",
        description="From Orphanet's prevalence class only (no point figure).")
    none = PermissibleValue(
        text="none",
        description="No usable epidemiology - a normal outcome for many rare diseases.")

    _defn = EnumDefinition(
        name="FlagRateBasis",
    )

class ReviewDecision(EnumDefinitionImpl):

    proceed = PermissibleValue(
        text="proceed",
        description="Criteria are sound; the CP can go to sites.")
    revise = PermissibleValue(
        text="revise",
        description="Send back for revision.")

    _defn = EnumDefinition(
        name="ReviewDecision",
    )

class CPStatus(EnumDefinitionImpl):

    draft = PermissibleValue(
        text="draft",
        description="Being written; not yet tested at any site.")
    testing = PermissibleValue(
        text="testing",
        description="Being tested at one or more sites.")
    accepted = PermissibleValue(
        text="accepted",
        description="Accepted at all seed sites.")
    refining = PermissibleValue(
        text="refining",
        description="Accepted, but showed an underperformance signature and is being revised.")
    deprecated = PermissibleValue(
        text="deprecated",
        description="Superseded or withdrawn; kept for the record.")

    _defn = EnumDefinition(
        name="CPStatus",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "exemplar-candidate",
            PermissibleValue(
                text="exemplar-candidate",
                description="""Complex logic required; held for a future trained model. cpsql refuses to build SQL for it."""))

class Module(EnumDefinitionImpl):
    """
    The evidence domain a feature belongs to. Drives which OMOP tables are searched and which vocabularies are allowed
    (see docs/CP_YAML_SPEC.md §3.2).
    """
    diagnostic_code = PermissibleValue(
        text="diagnostic_code",
        description="ICD10CM or SNOMED diagnosis; presence ever.")
    genetic_finding = PermissibleValue(
        text="genetic_finding",
        description="Reported pathogenic / likely pathogenic variant in a causal gene.")
    diagnostic_test = PermissibleValue(
        text="diagnostic_test",
        description="Confirmatory test or biomarker RESULT (not the order).")
    medication = PermissibleValue(
        text="medication",
        description="Disease-specific drug, used as evidence of the diagnosis.")
    procedure = PermissibleValue(
        text="procedure",
        description="Diagnostic procedure, or disease-specific therapeutic procedure.")
    phenotype = PermissibleValue(
        text="phenotype",
        description="Clinical/phenotypic feature: SNOMED, ICD10CM, or LOINC with a result.")

    _defn = EnumDefinition(
        name="Module",
        description="""The evidence domain a feature belongs to. Drives which OMOP tables are searched and which vocabularies are allowed (see docs/CP_YAML_SPEC.md §3.2).""",
    )

class CodeSystem(EnumDefinitionImpl):
    """
    CP-side vocabulary names; cpsql maps each to its Athena vocabulary_id.
    """
    ICD10CM = PermissibleValue(
        text="ICD10CM",
        description="Athena vocabulary_id 'ICD10CM'. Dotted codes (E83.31).")
    SNOMED = PermissibleValue(
        text="SNOMED",
        description="Athena 'SNOMED'.")
    LOINC = PermissibleValue(
        text="LOINC",
        description="Athena 'LOINC' (includes LA answer codes).")
    RXNORM = PermissibleValue(
        text="RXNORM",
        description="Athena 'RxNorm'.")
    UCUM = PermissibleValue(
        text="UCUM",
        description="Athena 'UCUM'. Result units only.")

    _defn = EnumDefinition(
        name="CodeSystem",
        description="CP-side vocabulary names; cpsql maps each to its Athena vocabulary_id.",
    )

class ResultKind(EnumDefinitionImpl):

    numeric = PermissibleValue(
        text="numeric",
        description="value_as_number compared to a threshold.")
    qualitative = PermissibleValue(
        text="qualitative",
        description="value_as_concept_id in a set of answer concepts.")

    _defn = EnumDefinition(
        name="ResultKind",
    )

class ResultOperator(EnumDefinitionImpl):

    gt = PermissibleValue(
        text="gt",
        description="x > value")
    gte = PermissibleValue(
        text="gte",
        description="x >= value")
    lt = PermissibleValue(
        text="lt",
        description="x < value")
    lte = PermissibleValue(
        text="lte",
        description="x <= value")
    between = PermissibleValue(
        text="between",
        description="value <= x <= value_high")
    above_ref_high = PermissibleValue(
        text="above_ref_high",
        description="x > range_high recorded on the row (MEASUREMENT only).")
    below_ref_low = PermissibleValue(
        text="below_ref_low",
        description="x < range_low recorded on the row (MEASUREMENT only).")

    _defn = EnumDefinition(
        name="ResultOperator",
    )

class DataModel(EnumDefinitionImpl):

    omop54 = PermissibleValue(
        text="omop54",
        description="OMOP CDM v5.4")
    truveta = PermissibleValue(
        text="truveta",
        description="Truveta native model (not generated by cpsql yet).")

    _defn = EnumDefinition(
        name="DataModel",
    )

class SqlDialect(EnumDefinitionImpl):

    postgresql = PermissibleValue(
        text="postgresql",
        description="PostgreSQL (default). The tests check the generated SQL parses as PostgreSQL.")
    duckdb = PermissibleValue(
        text="duckdb",
        description="DuckDB. The generated SQL runs on it; the synthetic test database uses it.")

    _defn = EnumDefinition(
        name="SqlDialect",
    )

# Slots
class slots:
    pass

slots.computablePhenotype__cp_id = Slot(uri=RAPIDCP.cp_id, name="computablePhenotype__cp_id", curie=RAPIDCP.curie('cp_id'),
                   model_uri=RAPIDCP.computablePhenotype__cp_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^mondo[0-9]{7}-[a-z0-9]+(-[a-z0-9]+)*_(L1|L2A|L2B|L3)_v[0-9]+\.[0-9]+$'))

slots.computablePhenotype__schema_version = Slot(uri=RAPIDCP.schema_version, name="computablePhenotype__schema_version", curie=RAPIDCP.curie('schema_version'),
                   model_uri=RAPIDCP.computablePhenotype__schema_version, domain=None, range=str)

slots.computablePhenotype__title = Slot(uri=RAPIDCP.title, name="computablePhenotype__title", curie=RAPIDCP.curie('title'),
                   model_uri=RAPIDCP.computablePhenotype__title, domain=None, range=str)

slots.computablePhenotype__disease = Slot(uri=RAPIDCP.disease, name="computablePhenotype__disease", curie=RAPIDCP.curie('disease'),
                   model_uri=RAPIDCP.computablePhenotype__disease, domain=None, range=Union[dict, DiseaseRef])

slots.computablePhenotype__level = Slot(uri=RAPIDCP.level, name="computablePhenotype__level", curie=RAPIDCP.curie('level'),
                   model_uri=RAPIDCP.computablePhenotype__level, domain=None, range=Union[str, "CPLevel"])

slots.computablePhenotype__search_mode = Slot(uri=RAPIDCP.search_mode, name="computablePhenotype__search_mode", curie=RAPIDCP.curie('search_mode'),
                   model_uri=RAPIDCP.computablePhenotype__search_mode, domain=None, range=Union[str, "SearchMode"])

slots.computablePhenotype__cluster = Slot(uri=RAPIDCP.cluster, name="computablePhenotype__cluster", curie=RAPIDCP.curie('cluster'),
                   model_uri=RAPIDCP.computablePhenotype__cluster, domain=None, range=Optional[Union[dict, ClusterScope]])

slots.computablePhenotype__status = Slot(uri=RAPIDCP.status, name="computablePhenotype__status", curie=RAPIDCP.curie('status'),
                   model_uri=RAPIDCP.computablePhenotype__status, domain=None, range=Union[str, "CPStatus"])

slots.computablePhenotype__provenance = Slot(uri=RAPIDCP.provenance, name="computablePhenotype__provenance", curie=RAPIDCP.curie('provenance'),
                   model_uri=RAPIDCP.computablePhenotype__provenance, domain=None, range=Union[dict, CPProvenance])

slots.computablePhenotype__review = Slot(uri=RAPIDCP.review, name="computablePhenotype__review", curie=RAPIDCP.curie('review'),
                   model_uri=RAPIDCP.computablePhenotype__review, domain=None, range=Optional[Union[dict, ClinicalReview]])

slots.computablePhenotype__sites_tested = Slot(uri=RAPIDCP.sites_tested, name="computablePhenotype__sites_tested", curie=RAPIDCP.curie('sites_tested'),
                   model_uri=RAPIDCP.computablePhenotype__sites_tested, domain=None, range=Optional[Union[Union[dict, SiteTest], list[Union[dict, SiteTest]]]])

slots.computablePhenotype__expected_flag_rate = Slot(uri=RAPIDCP.expected_flag_rate, name="computablePhenotype__expected_flag_rate", curie=RAPIDCP.curie('expected_flag_rate'),
                   model_uri=RAPIDCP.computablePhenotype__expected_flag_rate, domain=None, range=Optional[Union[dict, ExpectedFlagRate]])

slots.computablePhenotype__features = Slot(uri=RAPIDCP.features, name="computablePhenotype__features", curie=RAPIDCP.curie('features'),
                   model_uri=RAPIDCP.computablePhenotype__features, domain=None, range=Union[dict[Union[str, FeatureId], Union[dict, Feature]], list[Union[dict, Feature]]])

slots.computablePhenotype__disjuncts = Slot(uri=RAPIDCP.disjuncts, name="computablePhenotype__disjuncts", curie=RAPIDCP.curie('disjuncts'),
                   model_uri=RAPIDCP.computablePhenotype__disjuncts, domain=None, range=Optional[Union[dict[Union[str, DisjunctId], Union[dict, Disjunct]], list[Union[dict, Disjunct]]]])

slots.computablePhenotype__rules = Slot(uri=RAPIDCP.rules, name="computablePhenotype__rules", curie=RAPIDCP.curie('rules'),
                   model_uri=RAPIDCP.computablePhenotype__rules, domain=None, range=Optional[Union[dict[Union[str, RuleId], Union[dict, Rule]], list[Union[dict, Rule]]]])

slots.computablePhenotype__score = Slot(uri=RAPIDCP.score, name="computablePhenotype__score", curie=RAPIDCP.curie('score'),
                   model_uri=RAPIDCP.computablePhenotype__score, domain=None, range=Optional[Union[dict, ScoreModel]])

slots.computablePhenotype__absorbed_into = Slot(uri=RAPIDCP.absorbed_into, name="computablePhenotype__absorbed_into", curie=RAPIDCP.curie('absorbed_into'),
                   model_uri=RAPIDCP.computablePhenotype__absorbed_into, domain=None, range=Optional[str],
                   pattern=re.compile(r'^cluster-[a-z0-9]+_(L1|L2A|L2B|L3)_v[0-9]+\.[0-9]+$'))

slots.computablePhenotype__notes = Slot(uri=RAPIDCP.notes, name="computablePhenotype__notes", curie=RAPIDCP.curie('notes'),
                   model_uri=RAPIDCP.computablePhenotype__notes, domain=None, range=Optional[str])

slots.diseaseRef__mondo_id = Slot(uri=RAPIDCP.mondo_id, name="diseaseRef__mondo_id", curie=RAPIDCP.curie('mondo_id'),
                   model_uri=RAPIDCP.diseaseRef__mondo_id, domain=None, range=Union[str, URIorCURIE],
                   pattern=re.compile(r'^MONDO:[0-9]{7}$'))

slots.diseaseRef__slug = Slot(uri=RAPIDCP.slug, name="diseaseRef__slug", curie=RAPIDCP.curie('slug'),
                   model_uri=RAPIDCP.diseaseRef__slug, domain=None, range=str,
                   pattern=re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$'))

slots.diseaseRef__name = Slot(uri=RAPIDCP.name, name="diseaseRef__name", curie=RAPIDCP.curie('name'),
                   model_uri=RAPIDCP.diseaseRef__name, domain=None, range=str)

slots.diseaseRef__included_mondo_ids = Slot(uri=RAPIDCP.included_mondo_ids, name="diseaseRef__included_mondo_ids", curie=RAPIDCP.curie('included_mondo_ids'),
                   model_uri=RAPIDCP.diseaseRef__included_mondo_ids, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]],
                   pattern=re.compile(r'^MONDO:[0-9]{7}$'))

slots.diseaseRef__curation_record_version = Slot(uri=RAPIDCP.curation_record_version, name="diseaseRef__curation_record_version", curie=RAPIDCP.curie('curation_record_version'),
                   model_uri=RAPIDCP.diseaseRef__curation_record_version, domain=None, range=Optional[str])

slots.clusterScope__umbrella_codes = Slot(uri=RAPIDCP.umbrella_codes, name="clusterScope__umbrella_codes", curie=RAPIDCP.curie('umbrella_codes'),
                   model_uri=RAPIDCP.clusterScope__umbrella_codes, domain=None, range=Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]])

slots.clusterScope__candidate_mondo_ids = Slot(uri=RAPIDCP.candidate_mondo_ids, name="clusterScope__candidate_mondo_ids", curie=RAPIDCP.curie('candidate_mondo_ids'),
                   model_uri=RAPIDCP.clusterScope__candidate_mondo_ids, domain=None, range=Optional[Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]]])

slots.cPProvenance__authored_by = Slot(uri=RAPIDCP.authored_by, name="cPProvenance__authored_by", curie=RAPIDCP.curie('authored_by'),
                   model_uri=RAPIDCP.cPProvenance__authored_by, domain=None, range=str)

slots.cPProvenance__authored_date = Slot(uri=RAPIDCP.authored_date, name="cPProvenance__authored_date", curie=RAPIDCP.curie('authored_date'),
                   model_uri=RAPIDCP.cPProvenance__authored_date, domain=None, range=Union[str, XSDDate])

slots.cPProvenance__kg_extracted_at = Slot(uri=RAPIDCP.kg_extracted_at, name="cPProvenance__kg_extracted_at", curie=RAPIDCP.curie('kg_extracted_at'),
                   model_uri=RAPIDCP.cPProvenance__kg_extracted_at, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.cPProvenance__change_note = Slot(uri=RAPIDCP.change_note, name="cPProvenance__change_note", curie=RAPIDCP.curie('change_note'),
                   model_uri=RAPIDCP.cPProvenance__change_note, domain=None, range=Optional[str])

slots.cPProvenance__supersedes = Slot(uri=RAPIDCP.supersedes, name="cPProvenance__supersedes", curie=RAPIDCP.curie('supersedes'),
                   model_uri=RAPIDCP.cPProvenance__supersedes, domain=None, range=Optional[str])

slots.historyConcept__vocabulary = Slot(uri=RAPIDCP.vocabulary, name="historyConcept__vocabulary", curie=RAPIDCP.curie('vocabulary'),
                   model_uri=RAPIDCP.historyConcept__vocabulary, domain=None, range=Optional[str])

slots.historyConcept__code = Slot(uri=RAPIDCP.code, name="historyConcept__code", curie=RAPIDCP.curie('code'),
                   model_uri=RAPIDCP.historyConcept__code, domain=None, range=Optional[str])

slots.historyConcept__concept_id = Slot(uri=RAPIDCP.concept_id, name="historyConcept__concept_id", curie=RAPIDCP.curie('concept_id'),
                   model_uri=RAPIDCP.historyConcept__concept_id, domain=None, range=Optional[int])

slots.historyConcept__label = Slot(uri=RAPIDCP.label, name="historyConcept__label", curie=RAPIDCP.curie('label'),
                   model_uri=RAPIDCP.historyConcept__label, domain=None, range=Optional[str])

slots.historyConcept__include_descendants = Slot(uri=RAPIDCP.include_descendants, name="historyConcept__include_descendants", curie=RAPIDCP.curie('include_descendants'),
                   model_uri=RAPIDCP.historyConcept__include_descendants, domain=None, range=Optional[Union[bool, Bool]])

slots.siteTest__site = Slot(uri=RAPIDCP.site, name="siteTest__site", curie=RAPIDCP.curie('site'),
                   model_uri=RAPIDCP.siteTest__site, domain=None, range=str,
                   pattern=re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$'))

slots.siteTest__site_version = Slot(uri=RAPIDCP.site_version, name="siteTest__site_version", curie=RAPIDCP.curie('site_version'),
                   model_uri=RAPIDCP.siteTest__site_version, domain=None, range=int)

slots.siteTest__build = Slot(uri=RAPIDCP.build, name="siteTest__build", curie=RAPIDCP.curie('build'),
                   model_uri=RAPIDCP.siteTest__build, domain=None, range=str)

slots.clinicalReview__reviewer = Slot(uri=RAPIDCP.reviewer, name="clinicalReview__reviewer", curie=RAPIDCP.curie('reviewer'),
                   model_uri=RAPIDCP.clinicalReview__reviewer, domain=None, range=str)

slots.clinicalReview__date = Slot(uri=RAPIDCP.date, name="clinicalReview__date", curie=RAPIDCP.curie('date'),
                   model_uri=RAPIDCP.clinicalReview__date, domain=None, range=Union[str, XSDDate])

slots.clinicalReview__decision = Slot(uri=RAPIDCP.decision, name="clinicalReview__decision", curie=RAPIDCP.curie('decision'),
                   model_uri=RAPIDCP.clinicalReview__decision, domain=None, range=Union[str, "ReviewDecision"])

slots.clinicalReview__comments = Slot(uri=RAPIDCP.comments, name="clinicalReview__comments", curie=RAPIDCP.curie('comments'),
                   model_uri=RAPIDCP.clinicalReview__comments, domain=None, range=Optional[str])

slots.expectedFlagRate__low_per_100k = Slot(uri=RAPIDCP.low_per_100k, name="expectedFlagRate__low_per_100k", curie=RAPIDCP.curie('low_per_100k'),
                   model_uri=RAPIDCP.expectedFlagRate__low_per_100k, domain=None, range=Optional[float])

slots.expectedFlagRate__high_per_100k = Slot(uri=RAPIDCP.high_per_100k, name="expectedFlagRate__high_per_100k", curie=RAPIDCP.curie('high_per_100k'),
                   model_uri=RAPIDCP.expectedFlagRate__high_per_100k, domain=None, range=Optional[float])

slots.expectedFlagRate__basis = Slot(uri=RAPIDCP.basis, name="expectedFlagRate__basis", curie=RAPIDCP.curie('basis'),
                   model_uri=RAPIDCP.expectedFlagRate__basis, domain=None, range=Union[str, "FlagRateBasis"])

slots.expectedFlagRate__source = Slot(uri=RAPIDCP.source, name="expectedFlagRate__source", curie=RAPIDCP.curie('source'),
                   model_uri=RAPIDCP.expectedFlagRate__source, domain=None, range=str)

slots.feature__id = Slot(uri=RAPIDCP.id, name="feature__id", curie=RAPIDCP.curie('id'),
                   model_uri=RAPIDCP.feature__id, domain=None, range=URIRef,
                   pattern=re.compile(r'^f[0-9]+$'))

slots.feature__module = Slot(uri=RAPIDCP.module, name="feature__module", curie=RAPIDCP.curie('module'),
                   model_uri=RAPIDCP.feature__module, domain=None, range=Union[str, "Module"])

slots.feature__name = Slot(uri=RAPIDCP.name, name="feature__name", curie=RAPIDCP.curie('name'),
                   model_uri=RAPIDCP.feature__name, domain=None, range=str)

slots.feature__specificity_tier = Slot(uri=RAPIDCP.specificity_tier, name="feature__specificity_tier", curie=RAPIDCP.curie('specificity_tier'),
                   model_uri=RAPIDCP.feature__specificity_tier, domain=None, range=int)

slots.feature__hpo_id = Slot(uri=RAPIDCP.hpo_id, name="feature__hpo_id", curie=RAPIDCP.curie('hpo_id'),
                   model_uri=RAPIDCP.feature__hpo_id, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.feature__codes = Slot(uri=RAPIDCP.codes, name="feature__codes", curie=RAPIDCP.curie('codes'),
                   model_uri=RAPIDCP.feature__codes, domain=None, range=Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]])

slots.feature__result = Slot(uri=RAPIDCP.result, name="feature__result", curie=RAPIDCP.curie('result'),
                   model_uri=RAPIDCP.feature__result, domain=None, range=Optional[Union[dict, ResultCriterion]])

slots.feature__genetic = Slot(uri=RAPIDCP.genetic, name="feature__genetic", curie=RAPIDCP.curie('genetic'),
                   model_uri=RAPIDCP.feature__genetic, domain=None, range=Optional[Union[dict, GeneticCriterion]])

slots.feature__include_personal_history = Slot(uri=RAPIDCP.include_personal_history, name="feature__include_personal_history", curie=RAPIDCP.curie('include_personal_history'),
                   model_uri=RAPIDCP.feature__include_personal_history, domain=None, range=Optional[Union[bool, Bool]])

slots.feature__text_terms = Slot(uri=RAPIDCP.text_terms, name="feature__text_terms", curie=RAPIDCP.curie('text_terms'),
                   model_uri=RAPIDCP.feature__text_terms, domain=None, range=Optional[Union[str, list[str]]])

slots.codeRef__vocabulary = Slot(uri=RAPIDCP.vocabulary, name="codeRef__vocabulary", curie=RAPIDCP.curie('vocabulary'),
                   model_uri=RAPIDCP.codeRef__vocabulary, domain=None, range=Union[str, "CodeSystem"])

slots.codeRef__code = Slot(uri=RAPIDCP.code, name="codeRef__code", curie=RAPIDCP.curie('code'),
                   model_uri=RAPIDCP.codeRef__code, domain=None, range=str)

slots.codeRef__label = Slot(uri=RAPIDCP.label, name="codeRef__label", curie=RAPIDCP.curie('label'),
                   model_uri=RAPIDCP.codeRef__label, domain=None, range=Optional[str])

slots.codeRef__include_descendants = Slot(uri=RAPIDCP.include_descendants, name="codeRef__include_descendants", curie=RAPIDCP.curie('include_descendants'),
                   model_uri=RAPIDCP.codeRef__include_descendants, domain=None, range=Optional[Union[bool, Bool]])

slots.resultCriterion__kind = Slot(uri=RAPIDCP.kind, name="resultCriterion__kind", curie=RAPIDCP.curie('kind'),
                   model_uri=RAPIDCP.resultCriterion__kind, domain=None, range=Union[str, "ResultKind"])

slots.resultCriterion__operator = Slot(uri=RAPIDCP.operator, name="resultCriterion__operator", curie=RAPIDCP.curie('operator'),
                   model_uri=RAPIDCP.resultCriterion__operator, domain=None, range=Optional[Union[str, "ResultOperator"]])

slots.resultCriterion__value = Slot(uri=RAPIDCP.value, name="resultCriterion__value", curie=RAPIDCP.curie('value'),
                   model_uri=RAPIDCP.resultCriterion__value, domain=None, range=Optional[float])

slots.resultCriterion__value_high = Slot(uri=RAPIDCP.value_high, name="resultCriterion__value_high", curie=RAPIDCP.curie('value_high'),
                   model_uri=RAPIDCP.resultCriterion__value_high, domain=None, range=Optional[float])

slots.resultCriterion__units = Slot(uri=RAPIDCP.units, name="resultCriterion__units", curie=RAPIDCP.curie('units'),
                   model_uri=RAPIDCP.resultCriterion__units, domain=None, range=Optional[Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]]])

slots.resultCriterion__value_concepts = Slot(uri=RAPIDCP.value_concepts, name="resultCriterion__value_concepts", curie=RAPIDCP.curie('value_concepts'),
                   model_uri=RAPIDCP.resultCriterion__value_concepts, domain=None, range=Optional[Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]]])

slots.geneticCriterion__gene_symbol = Slot(uri=RAPIDCP.gene_symbol, name="geneticCriterion__gene_symbol", curie=RAPIDCP.curie('gene_symbol'),
                   model_uri=RAPIDCP.geneticCriterion__gene_symbol, domain=None, range=str)

slots.geneticCriterion__hgnc_id = Slot(uri=RAPIDCP.hgnc_id, name="geneticCriterion__hgnc_id", curie=RAPIDCP.curie('hgnc_id'),
                   model_uri=RAPIDCP.geneticCriterion__hgnc_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^HGNC:[0-9]+$'))

slots.geneticCriterion__interpretations = Slot(uri=RAPIDCP.interpretations, name="geneticCriterion__interpretations", curie=RAPIDCP.curie('interpretations'),
                   model_uri=RAPIDCP.geneticCriterion__interpretations, domain=None, range=Optional[Union[Union[dict, CodeRef], list[Union[dict, CodeRef]]]])

slots.geneticCriterion__require_gene_text_match = Slot(uri=RAPIDCP.require_gene_text_match, name="geneticCriterion__require_gene_text_match", curie=RAPIDCP.curie('require_gene_text_match'),
                   model_uri=RAPIDCP.geneticCriterion__require_gene_text_match, domain=None, range=Optional[Union[bool, Bool]])

slots.disjunct__id = Slot(uri=RAPIDCP.id, name="disjunct__id", curie=RAPIDCP.curie('id'),
                   model_uri=RAPIDCP.disjunct__id, domain=None, range=URIRef,
                   pattern=re.compile(r'^d[0-9]+$'))

slots.disjunct__feature = Slot(uri=RAPIDCP.feature, name="disjunct__feature", curie=RAPIDCP.curie('feature'),
                   model_uri=RAPIDCP.disjunct__feature, domain=None, range=str)

slots.disjunct__min_distinct_dates = Slot(uri=RAPIDCP.min_distinct_dates, name="disjunct__min_distinct_dates", curie=RAPIDCP.curie('min_distinct_dates'),
                   model_uri=RAPIDCP.disjunct__min_distinct_dates, domain=None, range=Optional[int])

slots.disjunct__min_span_days = Slot(uri=RAPIDCP.min_span_days, name="disjunct__min_span_days", curie=RAPIDCP.curie('min_span_days'),
                   model_uri=RAPIDCP.disjunct__min_span_days, domain=None, range=Optional[int])

slots.disjunct__label = Slot(uri=RAPIDCP.label, name="disjunct__label", curie=RAPIDCP.curie('label'),
                   model_uri=RAPIDCP.disjunct__label, domain=None, range=Optional[str])

slots.rule__id = Slot(uri=RAPIDCP.id, name="rule__id", curie=RAPIDCP.curie('id'),
                   model_uri=RAPIDCP.rule__id, domain=None, range=URIRef,
                   pattern=re.compile(r'^r[0-9]+$'))

slots.rule__label = Slot(uri=RAPIDCP.label, name="rule__label", curie=RAPIDCP.curie('label'),
                   model_uri=RAPIDCP.rule__label, domain=None, range=Optional[str])

slots.rule__expr = Slot(uri=RAPIDCP.expr, name="rule__expr", curie=RAPIDCP.curie('expr'),
                   model_uri=RAPIDCP.rule__expr, domain=None, range=Union[dict, Expr])

slots.expr__feature = Slot(uri=RAPIDCP.feature, name="expr__feature", curie=RAPIDCP.curie('feature'),
                   model_uri=RAPIDCP.expr__feature, domain=None, range=Optional[str])

slots.expr__min_distinct_dates = Slot(uri=RAPIDCP.min_distinct_dates, name="expr__min_distinct_dates", curie=RAPIDCP.curie('min_distinct_dates'),
                   model_uri=RAPIDCP.expr__min_distinct_dates, domain=None, range=Optional[int])

slots.expr__min_span_days = Slot(uri=RAPIDCP.min_span_days, name="expr__min_span_days", curie=RAPIDCP.curie('min_span_days'),
                   model_uri=RAPIDCP.expr__min_span_days, domain=None, range=Optional[int])

slots.expr__all_of = Slot(uri=RAPIDCP.all_of, name="expr__all_of", curie=RAPIDCP.curie('all_of'),
                   model_uri=RAPIDCP.expr__all_of, domain=None, range=Optional[Union[Union[dict, Expr], list[Union[dict, Expr]]]])

slots.expr__any_of = Slot(uri=RAPIDCP.any_of, name="expr__any_of", curie=RAPIDCP.curie('any_of'),
                   model_uri=RAPIDCP.expr__any_of, domain=None, range=Optional[Union[Union[dict, Expr], list[Union[dict, Expr]]]])

slots.expr__none_of = Slot(uri=RAPIDCP.none_of, name="expr__none_of", curie=RAPIDCP.curie('none_of'),
                   model_uri=RAPIDCP.expr__none_of, domain=None, range=Optional[Union[Union[dict, Expr], list[Union[dict, Expr]]]])

slots.expr__at_least = Slot(uri=RAPIDCP.at_least, name="expr__at_least", curie=RAPIDCP.curie('at_least'),
                   model_uri=RAPIDCP.expr__at_least, domain=None, range=Optional[int])

slots.expr__of = Slot(uri=RAPIDCP.of, name="expr__of", curie=RAPIDCP.curie('of'),
                   model_uri=RAPIDCP.expr__of, domain=None, range=Optional[Union[Union[dict, Expr], list[Union[dict, Expr]]]])

slots.expr__within = Slot(uri=RAPIDCP.within, name="expr__within", curie=RAPIDCP.curie('within'),
                   model_uri=RAPIDCP.expr__within, domain=None, range=Optional[Union[dict, Within]])

slots.within__days = Slot(uri=RAPIDCP.days, name="within__days", curie=RAPIDCP.curie('days'),
                   model_uri=RAPIDCP.within__days, domain=None, range=int)

slots.within__in_order = Slot(uri=RAPIDCP.in_order, name="within__in_order", curie=RAPIDCP.curie('in_order'),
                   model_uri=RAPIDCP.within__in_order, domain=None, range=Optional[Union[bool, Bool]])

slots.within__of = Slot(uri=RAPIDCP.of, name="within__of", curie=RAPIDCP.curie('of'),
                   model_uri=RAPIDCP.within__of, domain=None, range=Union[str, list[str]])

slots.scoreModel__threshold = Slot(uri=RAPIDCP.threshold, name="scoreModel__threshold", curie=RAPIDCP.curie('threshold'),
                   model_uri=RAPIDCP.scoreModel__threshold, domain=None, range=float)

slots.scoreModel__items = Slot(uri=RAPIDCP.items, name="scoreModel__items", curie=RAPIDCP.curie('items'),
                   model_uri=RAPIDCP.scoreModel__items, domain=None, range=Union[dict[Union[str, ScoreItemId], Union[dict, ScoreItem]], list[Union[dict, ScoreItem]]])

slots.scoreItem__id = Slot(uri=RAPIDCP.id, name="scoreItem__id", curie=RAPIDCP.curie('id'),
                   model_uri=RAPIDCP.scoreItem__id, domain=None, range=URIRef,
                   pattern=re.compile(r'^s[0-9]+$'))

slots.scoreItem__feature = Slot(uri=RAPIDCP.feature, name="scoreItem__feature", curie=RAPIDCP.curie('feature'),
                   model_uri=RAPIDCP.scoreItem__feature, domain=None, range=str)

slots.scoreItem__points = Slot(uri=RAPIDCP.points, name="scoreItem__points", curie=RAPIDCP.curie('points'),
                   model_uri=RAPIDCP.scoreItem__points, domain=None, range=float)

slots.scoreItem__min_distinct_dates = Slot(uri=RAPIDCP.min_distinct_dates, name="scoreItem__min_distinct_dates", curie=RAPIDCP.curie('min_distinct_dates'),
                   model_uri=RAPIDCP.scoreItem__min_distinct_dates, domain=None, range=Optional[int])

slots.scoreItem__min_span_days = Slot(uri=RAPIDCP.min_span_days, name="scoreItem__min_span_days", curie=RAPIDCP.curie('min_span_days'),
                   model_uri=RAPIDCP.scoreItem__min_span_days, domain=None, range=Optional[int])

slots.cPBuild__generator = Slot(uri=RAPIDCP.generator, name="cPBuild__generator", curie=RAPIDCP.curie('generator'),
                   model_uri=RAPIDCP.cPBuild__generator, domain=None, range=Optional[str])

slots.cPBuild__cp_logic_sha256 = Slot(uri=RAPIDCP.cp_logic_sha256, name="cPBuild__cp_logic_sha256", curie=RAPIDCP.curie('cp_logic_sha256'),
                   model_uri=RAPIDCP.cPBuild__cp_logic_sha256, domain=None, range=Optional[str])

slots.cPBuild__build_id = Slot(uri=RAPIDCP.build_id, name="cPBuild__build_id", curie=RAPIDCP.curie('build_id'),
                   model_uri=RAPIDCP.cPBuild__build_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^.+_v[0-9]+\.[0-9]+_[a-z0-9]+\.b[0-9]+$'))

slots.cPBuild__cp_id = Slot(uri=RAPIDCP.cp_id, name="cPBuild__cp_id", curie=RAPIDCP.curie('cp_id'),
                   model_uri=RAPIDCP.cPBuild__cp_id, domain=None, range=str)

slots.cPBuild__datamodel = Slot(uri=RAPIDCP.datamodel, name="cPBuild__datamodel", curie=RAPIDCP.curie('datamodel'),
                   model_uri=RAPIDCP.cPBuild__datamodel, domain=None, range=Union[str, "DataModel"])

slots.cPBuild__build = Slot(uri=RAPIDCP.build, name="cPBuild__build", curie=RAPIDCP.curie('build'),
                   model_uri=RAPIDCP.cPBuild__build, domain=None, range=int)

slots.cPBuild__change_note = Slot(uri=RAPIDCP.change_note, name="cPBuild__change_note", curie=RAPIDCP.curie('change_note'),
                   model_uri=RAPIDCP.cPBuild__change_note, domain=None, range=Optional[str])

slots.siteProfile__site = Slot(uri=RAPIDCP.site, name="siteProfile__site", curie=RAPIDCP.curie('site'),
                   model_uri=RAPIDCP.siteProfile__site, domain=None, range=str,
                   pattern=re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$'))

slots.siteProfile__version = Slot(uri=RAPIDCP.version, name="siteProfile__version", curie=RAPIDCP.curie('version'),
                   model_uri=RAPIDCP.siteProfile__version, domain=None, range=int)

slots.siteProfile__datamodel = Slot(uri=RAPIDCP.datamodel, name="siteProfile__datamodel", curie=RAPIDCP.curie('datamodel'),
                   model_uri=RAPIDCP.siteProfile__datamodel, domain=None, range=Union[str, "DataModel"])

slots.siteProfile__cdm_version = Slot(uri=RAPIDCP.cdm_version, name="siteProfile__cdm_version", curie=RAPIDCP.curie('cdm_version'),
                   model_uri=RAPIDCP.siteProfile__cdm_version, domain=None, range=Optional[str])

slots.siteProfile__dialect = Slot(uri=RAPIDCP.dialect, name="siteProfile__dialect", curie=RAPIDCP.curie('dialect'),
                   model_uri=RAPIDCP.siteProfile__dialect, domain=None, range=Optional[Union[str, "SqlDialect"]])

slots.siteProfile__vocabulary_version = Slot(uri=RAPIDCP.vocabulary_version, name="siteProfile__vocabulary_version", curie=RAPIDCP.curie('vocabulary_version'),
                   model_uri=RAPIDCP.siteProfile__vocabulary_version, domain=None, range=str)

slots.siteProfile__cdm_schema = Slot(uri=RAPIDCP.cdm_schema, name="siteProfile__cdm_schema", curie=RAPIDCP.curie('cdm_schema'),
                   model_uri=RAPIDCP.siteProfile__cdm_schema, domain=None, range=str)

slots.siteProfile__vocab_schema = Slot(uri=RAPIDCP.vocab_schema, name="siteProfile__vocab_schema", curie=RAPIDCP.curie('vocab_schema'),
                   model_uri=RAPIDCP.siteProfile__vocab_schema, domain=None, range=str)

slots.siteProfile__source_value_fallback = Slot(uri=RAPIDCP.source_value_fallback, name="siteProfile__source_value_fallback", curie=RAPIDCP.curie('source_value_fallback'),
                   model_uri=RAPIDCP.siteProfile__source_value_fallback, domain=None, range=Optional[Union[bool, Bool]])

slots.siteProfile__personal_history_concepts = Slot(uri=RAPIDCP.personal_history_concepts, name="siteProfile__personal_history_concepts", curie=RAPIDCP.curie('personal_history_concepts'),
                   model_uri=RAPIDCP.siteProfile__personal_history_concepts, domain=None, range=Optional[Union[Union[dict, HistoryConcept], list[Union[dict, HistoryConcept]]]])

slots.siteProfile__updated = Slot(uri=RAPIDCP.updated, name="siteProfile__updated", curie=RAPIDCP.curie('updated'),
                   model_uri=RAPIDCP.siteProfile__updated, domain=None, range=Union[str, XSDDate])

slots.siteProfile__change_note = Slot(uri=RAPIDCP.change_note, name="siteProfile__change_note", curie=RAPIDCP.curie('change_note'),
                   model_uri=RAPIDCP.siteProfile__change_note, domain=None, range=Optional[str])
