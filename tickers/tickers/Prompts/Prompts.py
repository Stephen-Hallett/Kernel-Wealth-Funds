from langchain_core.prompts import ChatPromptTemplate

information_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You have a world class talent for pulling information together. You take in information from multiple sources and create a digestible output of the relevant information in dictionary format.",
        ),
        (
            "user",
            "A managed fund has a holding of an asset from 'United States' with a holding description of 'SPDR Portfolio Emerging Markets ETF'. \
            Create a dictionary containing the asset_name and the asset_type (One of stock, real estate, bond, crypto).",
        ),
        (
            "assistant",
            "{{'asset_name': 'SPDR Portfolio Emerging Markets Exchange Traded Fund',\
                'asset_type': 'stock'}}",
        ),
        (
            "user",
            "A managed fund has a holding of an asset from '{country_name}' with a holding description of '{expanded_name}'. \
            Create a dictionary containing the asset_name and the asset_type (One of stock, real estate, bond, crypto).",
        ),
    ]
)

ticker_prompt = ChatPromptTemplate.from_messages(
    [
        {
            "role": "system",
            "content": "Given an asset listed on a stock exchange, return the associated ticker symbol as it appears on Yahoo finance. Keep in mind Yahoo Finance often adds a suffix based on the relevant exchange, such as '.NZ' for New Zealand, '.AX' for Australia, '.T' for Japan, etc.",
        },
        {"role": "user", "content": '{country_name} asset "{asset_name}"'},
    ]
)
