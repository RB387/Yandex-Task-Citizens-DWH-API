from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any

from citizens_dwh_api.entities.aggregation_pipeline import AbstractAggregation


@dataclass
class PercentileAggregation(AbstractAggregation):
    percentiles: List[int]
    import_id: str
    age_decimal_places: int = 2

    def get(self) -> List[Dict[str, Any]]:
        return [
            {"$match": {"import_id": self.import_id}},
            {"$addFields": {"age": self._get_age_calculate_aggregation()}},
            {"$sort": {"age": 1}},
            {"$group": self._get_ages_grouped_by_city_aggregation()},
            {
                "$project": {
                    **{"town": "$_id", "_id": 0},
                    **self._get_percentile_fields_aggregation(),
                }
            },
            {"$sort": {"town": 1}},
        ]

    @staticmethod
    def _get_age_calculate_aggregation() -> Dict[str, Any]:
        return {
            "$divide": [
                {"$subtract": [datetime.now(), "$birth_date"]},
                (365 * 24 * 60 * 60 * 1000),
            ]
        }

    @staticmethod
    def _get_ages_grouped_by_city_aggregation() -> Dict[str, Any]:
        return {
            "_id": "$town",
            "count": {"$sum": 1},
            "ages": {"$push": "$$ROOT.age"},
        }

    def _get_percentile_fields_aggregation(self) -> Dict[str, Any]:
        fields = {}

        for percentile in self.percentiles:
            fields[f"p{percentile}"] = self._get_percentile_calculate_aggregation(
                percentile
            )

        return fields

    def _get_percentile_calculate_aggregation(self, percentile: int) -> Dict[str, Any]:
        return {
            "$round": [
                {
                    "$max": {
                        "$slice": [
                            "$ages",
                            {"$ceil": {"$multiply": ["$count", percentile / 100]}},
                        ]
                    }
                },
                self.age_decimal_places,
            ]
        }
