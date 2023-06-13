from pydantic import BaseModel, Field, validator
from datetime import datetime


class DepositInputSchema(BaseModel):
    date: str = Field(default='31.01.2021')
    periods: int = Field(default=3, ge=1, le=60)
    amount: int = Field(default=10000, ge=10000, le=3000000)
    rate: float = Field(default=6, ge=1, le=8)

    @validator('date')
    def valid_date(cls, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return value.title()
        except ValueError:
            raise ValueError("String format must be %d.%m.%Y")