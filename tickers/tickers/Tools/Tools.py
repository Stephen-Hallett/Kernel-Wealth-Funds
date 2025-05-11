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
    """Detect the Yahoo Finance ticker symbol for a given asset."""

    ticker: str = Field(
        ...,
        description=(
            "A valid ticker symbol as it appears on Yahoo Finance (e.g., 'AAPL', 'VTI', '4568.T'). "
            "This must be the actual symbol used on Yahoo Finance, not the company name. "
            "If no ticker is found or you are unsure, return an empty string ('')."
        ),
    )
