from langchain_core.prompts import ChatPromptTemplate

normalisation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a very detailed AI. You take simplistic names or items and focus in on the fine details, returning an expanded version.",
        ),
        (
            "human",
            "Standardize the following company, bond, or fund name to its canonical, expanded, and unambiguous form: 'SPDR Portfolio Emerging Markets ETF'",
        ),
        (
            "ai",
            "{{'expanded_name': 'SPDR Portfolio Emerging Markets Exchange Traded Fund'}}",
        ),
        (
            "human",
            "Standardize the following company or fund name to its canonical and unambiguous form: '{input_name}'.",
        ),
    ]
)

information_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You have a world class talent for pulling information together. You take in information from multiple sources and create a digestible output of the relevant information in dictionary format.",
        ),
        (
            "human",
            "A managed fund has a holding of an asset from 'United States' with a holding description of 'SPDR Portfolio Emerging Markets ETF'. \
            Create a dictionary containing the asset_name, asset_type (One of stock, real estate, bond, crypto) and the exchange the asset is listed on if applicapble. \
            If there is no exchange for that asset, the exchange should be an empty string ''.",
        ),
        (
            "ai",
            "{{'asset_name': 'SPDR Portfolio Emerging Markets Exchange Traded Fund',\
                'asset_type': 'stock',\
                'exchange': 'NYSE Arca'}}",
        ),
        (
            "human",
            "A managed fund has a holding of an asset from '{country_name}' with a holding description of '{expanded_name}'. \
            Create a dictionary containing the asset_name, asset_type (One of stock, real estate, bond, crypto) and the exchange the asset is listed on if applicapble. \
            If there is no exchange for that asset, the exchange should be an empty string ''.",
        ),
    ]
)

ticker_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are extremely knowledgeable about stocks and assets. If there is a stock listed on any exchange you can find its ticker symbol. You are praised for your honesty and your ability to not make up tickers.",
        ),
        (
            "system",
            "If there is no ticker for the asset you should return an empty string '' as the detected ticker.",
        ),
        (
            "human",
            "Given the United States stock asset 'SPDR Portfolio Emerging Markets Exchange Traded Fund' listed on the NYSE Arca exchange,\
            please locate and return the ticker symbol as it appears on Yahoo Finance - or as it would appear in the python package yfinance. \
            Return the ticker in JSON format.",
        ),
        ("ai", "{{'ticker': 'SPEM'}}"),
        (
            "human",
            "Given the {country_name} {asset_type} asset '{asset_name}' listed on the {exchange} exchange,\
            Please locate and return the ticker symbol as it appears on Yahoo Finance - as it would appear in the python package yfinance. \
            Return the ticker in JSON format.",
        ),
    ]
)
