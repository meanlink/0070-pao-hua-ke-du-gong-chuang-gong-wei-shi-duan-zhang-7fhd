from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, model_validator

class Span(BaseModel):
    code: str = Field(pattern=r"^[A-Z0-9-]{3,24}$")
    machine: str = Field(pattern=r"^[A-Z0-9-]{3,24}$")
    service_day: date
    open_minute: int = Field(ge=0, lt=1440)
    end_minute: int = Field(gt=0, le=1440)

    @model_validator(mode="after")
    def positive_length(self):
        if self.end_minute <= self.open_minute:
            raise ValueError("结束时间必须晚于起始时间")
        return self

class Session(Span):
    crew: str = Field(min_length=2,max_length=60)

class Block(Span):
    reason: str = Field(min_length=3,max_length=100)

class Decide(BaseModel):
    decision: Literal["counted","void"]
