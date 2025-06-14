from typing import Literal

from pydantic import BaseModel, Field


class InformationTools(BaseModel):
    """Locate information about a given asset including asset name, and asset type."""

    asset_name: str = Field(
        ..., description="The most expanded version of a given assets name."
    )
    asset_type: Literal["stock", "bond", "crypto", "real estate"] = Field(
        ...,
        description='The type of asset being discussed. One of the following options ["stock", "bond", "crypto", "real estate"]',
    )
