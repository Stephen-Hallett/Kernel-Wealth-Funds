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

ticker_prompt = ChatPromptTemplate.from_template(
    """You are a financial assistant that identifies Yahoo Finance ticker symbols.

Given the {country_name} {asset_type} asset '{asset_name}' listed on the {exchange} exchange:

→ Locate and return the *exact* Yahoo Finance ticker symbol (e.g., 'AAPL', 'VTI', '4568.T').  
→ Do **not** return a company name or description.  
→ If you are uncertain or no symbol is available, return an empty string.

Your output must be a JSON object with the field 'ticker'.

### Examples:
Input: 'SPDR S&P 500 ETF Trust' → Output: {{ "ticker": "SPY" }}
Input: 'Toyota Motor Corp' → Output: {{ "ticker": "TM" }}
Input: 'Daiichi Sankyo Co Ltd' → Output: {{ "ticker": "4568.T" }}
Input: 'Private real estate in Iceland' → Output: {{ "ticker": "" }}
Input: 'Westpac Banking Corporation (AU Register)'  → Output: {{ "ticker": "WBC.AX" }}
Input: 'The Warehouse Group Limited'  → Output: {{ "ticker": "WHS.NZ" }}

Now return the output for this asset only:
"""
)
