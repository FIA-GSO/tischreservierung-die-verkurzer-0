from datetime import datetime

from pydantic import BaseModel, field_validator

from api.utils.dateformat import db_date_format


class Reservation(BaseModel):
    table_number: int
    duration_minutes: int
    pin: int
    reservation_number: int
    timestamp: str

    @field_validator('timestamp')
    def valid_timestamp(cls, v):
        try:
            datetime.strptime(v, db_date_format)
            return v
        except ValueError:
            raise ValueError(f"Incorrect date format, should be {db_date_format}")
