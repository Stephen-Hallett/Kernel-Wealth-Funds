from typing import Literal

from pydantic import BaseModel, Field


class NormalisationTools(BaseModel):
    """Normalise an assets name to its most expanded version."""

    expanded_name: str = Field(
        ..., description="The expanded version of a given assets name."
    )


class InformationTools(BaseModel):
    """Locate information about a given asset including asset name, type and the exchange it is listed on"""

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
    """Detect the ticker for a specified asset as it appears on Yahoo Finance."""

    ticker: str = Field(
        ...,
        description="A ticker symbol for an exchange traded asset as it would appear on yahoo finance - or an empty string where no ticker is found.",
    )
