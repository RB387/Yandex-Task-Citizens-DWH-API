from enum import Enum
from typing import List, Dict, Any, Set, Iterable

from more_itertools import one
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from citizens_dwh_api.constants import PERCENTILES
from citizens_dwh_api.dao.citizens_abstract import AbstractCitizensDao
from citizens_dwh_api.dao.exceptions import CitizenNotFound
from citizens_dwh_api.dao.mongo.percentile_aggregation import PercentileAggregation
from citizens_dwh_api.dao.mongo.presents_aggregation import PresentsAggregation
from citizens_dwh_api.entities.schemas import Citizen, OptionalCitizen


class RelativeActions(Enum):
    PUSH = "$push"
    REMOVE = "$pop"


class MongoCitizensDao(AbstractCitizensDao):
    def __init__(self, mongo_client: AsyncIOMotorClient, db_name: str, collection_name: str):
        self.client = mongo_client
        self.db_name = db_name
        self.collection_name = collection_name

    async def insert_many(self, citizens: Iterable[Citizen]):
        await self.client[self.db_name][self.collection_name].insert_many(citizens)

    async def get_citizens_by_import_id(self, import_id: str) -> List[Citizen]:
        cursor = self.client[self.db_name][self.collection_name].find(
            {"import_id": import_id}, {"_id": 0, "import_id": 0}
        )
        return [citizen async for citizen in cursor]

    async def find_citizen(self, import_id: str, citizen_id: int) -> Citizen:
        citizen = await self.client[self.db_name][self.collection_name].find_one(
            {"import_id": import_id, "citizen_id": citizen_id}
        )
        return citizen

    async def patch_citizen(self, new_citizen_fields: OptionalCitizen, import_id: str, citizen_id: int) -> Citizen:
        citizen = await self.find_citizen(import_id, citizen_id)

        if not citizen:
            raise CitizenNotFound

        updated_relatives = set(new_citizen_fields["relatives"] or [])
        current_relatives = set(citizen.get("relatives"))

        import_id = citizen["import_id"]
        citizen_id = citizen["citizen_id"]

        async with await self.client.start_session() as session:
            async with session.start_transaction():
                if updated_relatives:
                    await self._update_relatives(
                        updated_relatives,
                        current_relatives,
                        import_id,
                        citizen_id,
                        session,
                    )

                return await self.client[self.db_name][self.collection_name].find_one_and_update(
                    {"import_id": import_id, "citizen_id": citizen_id},
                    {"$set": new_citizen_fields},
                    {"_id": 0, "import_id": 0},
                    session=session,
                    return_document=ReturnDocument.AFTER,
                )

    async def get_presents_stat(self, import_id: str) -> Dict[str, Any]:
        aggregation = PresentsAggregation(import_id)
        cursor = self.client[self.db_name][self.collection_name].aggregate(aggregation.get())

        return one([presents_stat async for presents_stat in cursor])

    async def get_percentile_stats(self, import_id: str) -> List[Dict[str, Any]]:
        aggregation = PercentileAggregation(PERCENTILES, import_id)
        cursor = self.client[self.db_name][self.collection_name].aggregate(aggregation.get())
        return [city_stat async for city_stat in cursor]

    async def _update_relatives(
            self,
            updated_relatives: Set[int],
            current_relatives: Set[int],
            import_id: str,
            citizen_id: int,
            session,
    ):
        new_relatives = (RelativeActions.PUSH, updated_relatives - current_relatives)
        outdated_relatives = (
            RelativeActions.REMOVE,
            current_relatives - updated_relatives,
        )

        for action, relatives in [new_relatives, outdated_relatives]:
            for citizen_id_relative in relatives:
                await self.client[self.db_name][self.collection_name].update_one(
                    {"import_id": import_id, "citizen_id": int(citizen_id_relative)},
                    {action.value: {"relatives": citizen_id}},
                    session=session,
                )
