from typing import Literal

from pydantic import BaseModel, Field


class NormalisationTools(BaseModel):
    expanded_name: str = Field(
        ..., description="The expanded version of a given assets name."
    )


class InformationTools(BaseModel):
    asset_name: str = Field(
        ..., description="The expanded version of a given assets name."
    )
    asset_type: Literal["stock", "bond", "crypto", "real estate"] = Field(
        ...,
        description='The type of asset being discussed. One of the following options ["stock", "bond", "crypto", "real estate"]',
    )
    exchange: str = Field(
        ...,
        description="The registered exchange the asset is traded on. e.g. NYSE, NASDAQ, NZX, AX, etc.",
    )


class TickerTools(BaseModel):
    ticker: str = Field(
        ...,
        description="A ticker symbol for an exchange traded asset as it would appear on yahoo finance - or an empty string where no ticker is found.",
    )
