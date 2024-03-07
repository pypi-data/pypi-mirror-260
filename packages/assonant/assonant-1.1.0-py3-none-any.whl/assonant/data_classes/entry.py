"""Assonant Entry data class."""
from typing import Dict, List, Optional

from .assonant_data_class import AssonantDataClass
from .components import Component
from .data_handlers import DataHandler
from .types import ScopeType


class Entry(AssonantDataClass):
    """Data classes that wraps data into a logical/temporal scope related to the experiment.

    Entries are used to group and represent data in a defined temporal/logical scope of the
    experiment, which is directly define by the field "scope_type". e.g: calibration,
    pre-exposition.
    """

    scope_type: ScopeType
    components: Optional[List[Component]] = []
    fields: Optional[Dict[str, DataHandler]] = {}
