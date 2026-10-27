"""rapid-cp-schema.

LinkML schema for RAPID TA1 computable phenotypes (CPs): versioned, data-model-independent CP logic files.
"""

try:
    from rapid_cp_schema._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
