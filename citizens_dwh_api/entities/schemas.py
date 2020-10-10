import trafaret as t

from citizens_dwh_api.constants import DATE_FORMAT


def _build_trafaret(schema, optional=False):
    return t.Dict({t.Key(key, optional=optional): item for key, item in schema.items()})


OptionalCitizenSchema = {
    "town": t.String(min_length=1),
    "street": t.String(min_length=1),
    "building": t.String(min_length=1),
    "apartment": t.ToInt(gte=0),
    "name": t.String(min_length=1),
    "birth_date": t.ToDateTime(
        format=DATE_FORMAT  # datetime, because pymongo cannot insert date
    ),
    "gender": t.Enum("male", "female"),
    "relatives": t.List(t.ToInt(gte=0)),
}

CitizenSchema = {**OptionalCitizenSchema, **{"citizen_id": t.ToInt(gte=0)}}

OptionalCitizen = _build_trafaret(OptionalCitizenSchema, optional=True)
Citizen = _build_trafaret(CitizenSchema, optional=False)
