from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_openai import ChatOpenAI

from .Prompts.Prompts import information_prompt, normalisation_prompt, ticker_prompt
from .Tools.Tools import InformationTools, NormalisationTools, TickerTools


class TickerDetector:
    def __init__(self, openai_key: str) -> None:
        self.normalisation_chain = (
            normalisation_prompt
            | ChatOpenAI(api_key=openai_key, temperature=0).bind_tools(
                [NormalisationTools], strict=True, tool_choice="NormalisationTools"
            )
            | PydanticToolsParser(tools=[NormalisationTools])
        )

        self.information_chain = (
            information_prompt
            | ChatOpenAI(api_key=openai_key, temperature=0).bind_tools(
                [InformationTools], strict=True, tool_choice="InformationTools"
            )
            | PydanticToolsParser(tools=[InformationTools])
        )

        self.ticker_chain = (
            ticker_prompt
            | ChatOpenAI(
                api_key=openai_key, model="gpt-4-turbo", temperature=0
            ).bind_tools([TickerTools], strict=True, tool_choice="TickerTools")
            | PydanticToolsParser(tools=[TickerTools])
        )

    def detect(self, asset_name: str, country_name: str) -> str:
        """Detect the appropriate ticker symbol for a given asset as it appears on yahoo finance.

        :param asset_name: Name of the asset you want a ticker for
        :param country_name: Country location of the asset
        :return: A ticker symbol e.g. AAPL, MSFT, etc.
        """
        normalisation_results = self.normalisation_chain.invoke(
            {"input_name": asset_name}
        )
        information_results = self.information_chain.invoke(
            {
                "country_name": country_name,
                "expanded_name": normalisation_results[0].expanded_name,
            }
        )
        if information_results[0].asset_type not in ["stock", "crypto"]:
            return ""

        ticker_results = self.ticker_chain.invoke(
            {
                "country_name": country_name,
                "asset_type": information_results[0].asset_type,
                "asset_name": information_results[0].asset_name,
                "exchange": information_results[0].exchange,
            }
        )
        return ticker_results[0].ticker
