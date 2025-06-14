from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.output_parsers.string import StrOutputParser
from langchain_openai import ChatOpenAI

from .Prompts.Prompts import information_prompt, ticker_prompt
from .Tools.Tools import InformationTools


class TickerDetector:
    def __init__(self, openai_key: str) -> None:
        self.information_chain = (
            information_prompt
            | ChatOpenAI(
                api_key=openai_key, model="gpt-4.1-nano", temperature=0
            ).bind_tools(
                [InformationTools], strict=True, tool_choice="InformationTools"
            )
            | PydanticToolsParser(tools=[InformationTools])
        )

        self.ticker_chain = (
            ticker_prompt
            | ChatOpenAI(
                api_key=openai_key,
                model="ft:gpt-4.1-nano-2025-04-14:personal::BYS5as8d",
                temperature=0,
            )
            | StrOutputParser()
        )

    def detect(self, asset_name: str, country_name: str) -> str:
        """Detect the appropriate ticker symbol for a given asset as it appears on yahoo finance.

        :param asset_name: Name of the asset you want a ticker for
        :param country_name: Country location of the asset
        :return: A ticker symbol e.g. AAPL, MSFT, etc.
        """

        information_results = self.information_chain.invoke(
            {"country_name": country_name, "expanded_name": asset_name}
        )
        if information_results[0].asset_type not in ("stock", "crypto"):
            return ""

        return self.ticker_chain.invoke(
            {
                "country_name": country_name,
                "asset_name": information_results[0].asset_name,
            }
        )
