from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AbstractAggregation(ABC):
    """
    Abstract class for mongodb aggregation
    Used to keep readability of complex aggregations
    """

    @abstractmethod
    def get(self) -> List[Dict[str, Any]]:
        raise NotImplementedError
