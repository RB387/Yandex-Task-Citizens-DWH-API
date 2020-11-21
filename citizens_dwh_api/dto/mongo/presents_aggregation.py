from dataclasses import dataclass
from typing import Any, Dict, List

from citizens_dwh_api.entities.aggregation_pipeline import AbstractAggregation


@dataclass
class PresentsAggregation(AbstractAggregation):
    import_id: str

    def get(self) -> List[Dict[str, Any]]:
        return [
            {"$match": {"import_id": self.import_id}},
            {"$facet": self._get_months_facets()},
        ]

    def _get_months_facets(self) -> Dict[str, Any]:
        facets = {}

        for month_number in range(1, 13):
            facets[str(month_number)] = self._get_facet_for_month(month_number)

        return facets

    def _get_facet_for_month(self, month_number: int) -> List[Dict[str, Any]]:
        return [
            {
                "$lookup": {
                    "from": "citizens",
                    "let": {"relatives": "$relatives"},
                    "pipeline": self._get_lookup_pipeline(month_number),
                    "as": "relatives_presents",
                },
            },
            {"$match": {"relatives_presents.0": {"$exists": True}}},
            {
                "$project": {
                    "_id": 0,
                    "citizen_id": 1,
                    "presents": {"$size": "$relatives_presents"},
                }
            },
        ]

    def _get_lookup_pipeline(self, month_number: int) -> List[Dict[str, Any]]:
        return [
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": ["$import_id", self.import_id]},
                            {"$in": ["$citizen_id", "$$relatives"]},
                        ]
                    }
                }
            },
            {"$project": {"birthday_month": {"$month": "$birth_date"},}},
            {"$match": {"birthday_month": month_number}},
        ]
