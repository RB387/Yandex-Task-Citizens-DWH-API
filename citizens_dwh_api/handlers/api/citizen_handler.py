from enum import Enum
from typing import Dict, Any, Set

import trafaret as t
from aiohttp.web_response import Response
from pymongo import ReturnDocument

from lib.handler.utils import (
    validate_request_schema,
    get_request_args,
    get_bad_request_exception,
)
from citizens_dwh_api.constants import MONGO_COLLECTION_NAME
from citizens_dwh_api.handlers.base_mongo_handler import MongoApiHandler
from citizens_dwh_api.entities.exceptions import InputExceptions
from citizens_dwh_api.handlers.utils import get_json_response, cast_citizen_id
from citizens_dwh_api.entities.schemas import OptionalCitizen, Citizen


class RelativeActions(Enum):
    PUSH = "$push"
    REMOVE = "$pop"


class CitizenHandler(MongoApiHandler):
    request_schema: t.Trafaret = OptionalCitizen

    @validate_request_schema(request_schema)
    @get_request_args(match_list=["import_id", "citizen_id"])
    async def patch(
        self, request_json: OptionalCitizen, import_id: str, citizen_id: str
    ) -> Response:
        citizen_id = cast_citizen_id(citizen_id)

        citizen = await self._find_citizen(import_id, citizen_id)

        patched_citizen = await self._patch_citizen(request_json, citizen)
        return get_json_response(patched_citizen)

    async def _find_citizen(self, import_id: str, citizen_id: int) -> Citizen:
        citizen = await self.mongo[MONGO_COLLECTION_NAME].find_one(
            {"import_id": import_id, "citizen_id": citizen_id}
        )

        if not citizen:
            raise get_bad_request_exception(InputExceptions.INCORRECT_IDS.value)

        return citizen

    async def _patch_citizen(
        self, updated_fields: Dict[str, Any], citizen: Citizen
    ) -> Citizen:
        updated_relatives = set(updated_fields.get("relatives", []))
        current_relatives = set(citizen["relatives"])

        import_id = citizen["import_id"]
        citizen_id = citizen["citizen_id"]

        async with await self.mongo.start_session() as session:
            async with session.start_transaction():
                if updated_relatives:
                    await self._update_relatives(
                        updated_relatives,
                        current_relatives,
                        import_id,
                        citizen_id,
                        session,
                    )

                return await self.mongo[MONGO_COLLECTION_NAME].find_one_and_update(
                    {"import_id": import_id, "citizen_id": citizen_id},
                    {"$set": updated_fields},
                    {"_id": 0, "import_id": 0},
                    session=session,
                    return_document=ReturnDocument.AFTER,
                )

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
                await self.mongo[MONGO_COLLECTION_NAME].update_one(
                    {"import_id": import_id, "citizen_id": int(citizen_id_relative)},
                    {action.value: {"relatives": citizen_id}},
                    session=session,
                )
