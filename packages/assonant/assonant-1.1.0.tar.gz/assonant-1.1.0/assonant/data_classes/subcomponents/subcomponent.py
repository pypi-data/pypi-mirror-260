"""Assonant Component abstract class."""
from typing import Dict, List, Optional

from ..assonant_data_class import AssonantDataClass
from ..data_handlers import Axis, DataHandler


# TODO: Make this class abstract
class Subcomponent(AssonantDataClass):
    """Abstract class that creates the base common requirements to define an Assonant Subcomponent.

    Subcomponents are less generic definitions which may compose and detail components. Usually,
    subcomponents existance doesn't make sense without being related to a Component.
    """

    name: str
    positions: Optional[List[Axis]] = []
    fields: Optional[Dict[str, DataHandler]] = {}
