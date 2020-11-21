from typing import List, Dict, Any, Iterable

from abc import ABC, abstractmethod

from citizens_dwh_api.entities.schemas import Citizen, OptionalCitizen


class AbstractCitizensDto(ABC):
    @abstractmethod
    async def insert_many(self, citizens: Iterable[Citizen]):
        ...

    @abstractmethod
    async def get_citizens_by_import_id(self, import_id: str) -> List[Citizen]:
        ...

    @abstractmethod
    async def find_citizen(self, import_id: str, citizen_id: int) -> Citizen:
        ...

    @abstractmethod
    async def patch_citizen(self, new_citizen_fields: OptionalCitizen, import_id: str, citizen_id: int) -> Citizen:
        ...

    @abstractmethod
    async def get_presents_stat(self, import_id: str) -> Dict[str, Any]:
        ...

    @abstractmethod
    async def get_percentile_stats(self, import_id: str) -> List[Dict[str, Any]]:
        ...
