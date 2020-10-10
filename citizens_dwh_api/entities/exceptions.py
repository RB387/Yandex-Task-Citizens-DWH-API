from enum import Enum


class InputExceptions(Enum):
    VALUE_ERROR = "citizen_id is not valid integer"
    INCORRECT_IDS = "such citizen does not exist"
