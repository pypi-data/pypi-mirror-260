"""Assonant Component abstract class."""
from typing import Dict, List, Optional

from ..assonant_data_class import AssonantDataClass
from ..data_handlers import Axis, DataHandler
from ..subcomponents import Subcomponent


# TODO: Make this class abstract
class Component(AssonantDataClass):
    """Abstract class that creates the base common requirements to define an Assonant Component.

    Components are more generic definitions which may be composed by many subcomponents if more detailing in its
    composition is desired.
    """

    name: str
    subcomponents: Optional[List[Subcomponent]] = []
    positions: Optional[List[Axis]] = []
    fields: Optional[Dict[str, DataHandler]] = {}
