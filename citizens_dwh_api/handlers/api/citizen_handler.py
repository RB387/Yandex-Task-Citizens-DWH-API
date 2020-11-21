from simio.handler.utils import route, get_bad_request_exception

from citizens_dwh_api.dao.exceptions import CitizenNotFound
from citizens_dwh_api.handlers.base_mongo_handler import DtoApiHandler
from citizens_dwh_api.handlers.utils import get_json_response
from citizens_dwh_api.entities.schemas import OptionalCitizen


@route(path="/imports/{import_id}/citizens/{citizen_id}")
class CitizenHandlerDto(DtoApiHandler):
    async def patch(
        self, new_citizen_fields: OptionalCitizen, import_id: str, citizen_id: int
    ):
        try:
            patched_citizen = await self.dao.patch_citizen(new_citizen_fields, import_id, citizen_id)
        except CitizenNotFound:
            raise get_bad_request_exception("Citizen not found")

        return get_json_response(patched_citizen)
