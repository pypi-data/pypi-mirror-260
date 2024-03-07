import pandas as pd
import pytest

from stockdex.ticker import Ticker


@pytest.mark.parametrize(
    "ticker, expected_response",
    [
        ("AAPL", 200),
        ("GOOGL", 200),
        ("MSFT", 200),
    ],
)
def test_get_response(ticker, expected_response):
    # Create a Ticker object
    ticker = Ticker(ticker)

    # Send an HTTP GET request to the website
    response = ticker.get_response(f"https://finance.yahoo.com/quote/{ticker.ticker}")

    # Check if the response is as expected
    assert response.status_code == expected_response


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_cashflow_web(ticker):
    ticker = Ticker(ticker)
    cashflow_web_df = ticker.cashflow_web

    # Check if the response is as expected
    assert isinstance(cashflow_web_df, pd.DataFrame)
    assert cashflow_web_df.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_balance_sheet_web(ticker):
    ticker = Ticker(ticker)
    balance_sheet_web_df = ticker.balance_sheet_web

    # Check if the response is as expected
    assert isinstance(balance_sheet_web_df, pd.DataFrame)
    assert balance_sheet_web_df.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_analysis(ticker):
    ticker = Ticker(ticker)
    analysis_df = ticker.analysis

    # Check if the response is as expected
    assert isinstance(analysis_df, pd.DataFrame)
    assert analysis_df.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_summary(ticker):
    ticker = Ticker(ticker)
    summary_df = ticker.summary

    # Check if the response is as expected
    assert isinstance(summary_df, pd.DataFrame)
    assert summary_df.shape[0] > 0


@pytest.mark.skip(
    reason="This test is skipped because github actions is not able to access the yahoo finance page"  # noqa E501
)
@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_statistics(ticker):
    ticker = Ticker(ticker)
    statistics_df = ticker.statistics()

    # Check if the response is as expected
    assert isinstance(statistics_df, pd.DataFrame)
    assert statistics_df.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_income_stmt(ticker):
    ticker = Ticker(ticker)
    income_stmt_df = ticker.income_stmt

    # Check if the response is as expected
    assert isinstance(income_stmt_df, pd.DataFrame)
    assert income_stmt_df.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_calls(ticker):
    ticker = Ticker(ticker)
    calls = ticker.calls

    # Check if the response is as expected
    assert isinstance(calls, pd.DataFrame)
    assert calls.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
    ],
)
def test_puts(ticker):
    ticker = Ticker(ticker)
    puts = ticker.puts

    # Check if the response is as expected
    assert isinstance(puts, pd.DataFrame)
    assert puts.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("ASML"),
    ],
)
def test_key_executives(ticker):
    ticker = Ticker(ticker)
    key_executives = ticker.key_executives

    # Check if the response is as expected
    assert isinstance(key_executives, pd.DataFrame)
    assert key_executives.shape[0] > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("ASML"),
        ("TSLA"),
    ],
)
def test_description(ticker):
    ticker = Ticker(ticker)
    description = ticker.description

    # Check if the response is as expected
    assert isinstance(description, str)
    assert len(description) > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("ASML"),
        ("TSLA"),
    ],
)
def test_corporate_governance(ticker):
    ticker = Ticker(ticker)
    corporate_governance = ticker.corporate_governance

    # Check if the response is as expected
    assert isinstance(corporate_governance, str)
    assert len(corporate_governance) > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("ASML"),
        ("TSLA"),
    ],
)
def test_major_holders(ticker):
    ticker = Ticker(ticker)
    major_holders = ticker.major_holders

    # Check if the response is as expected
    assert isinstance(major_holders, pd.DataFrame)
    assert major_holders.shape[0] > 0
    assert major_holders.shape[1] == 2


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("ASML"),
        ("TSLA"),
    ],
)
def test_top_institutional_holders(ticker):
    ticker = Ticker(ticker)
    top_institutional_holders = ticker.top_institutional_holders

    # Check if the response is as expected
    assert isinstance(top_institutional_holders, pd.DataFrame)
    assert top_institutional_holders.shape[0] > 0
    assert top_institutional_holders.shape[1] == 5


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("ASML"),
        ("TSLA"),
    ],
)
def test_top_mutual_fund_holders(ticker):
    ticker = Ticker(ticker)
    top_mutual_fund_holders = ticker.top_mutual_fund_holders

    # Check if the response is as expected
    assert isinstance(top_mutual_fund_holders, pd.DataFrame)
    assert top_mutual_fund_holders.shape[0] > 0
    assert top_mutual_fund_holders.shape[1] == 5


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("ASML"),
        ("CAT"),
        ("BAC"),
    ],
)
def test_dividend(ticker):
    ticker = Ticker(ticker)
    dividend = ticker.dividend

    # Check if the response is as expected
    assert isinstance(dividend, pd.DataFrame)
    assert dividend.shape[0] > 0
    assert dividend.shape[1] == 5


@pytest.mark.parametrize(
    "ticker, range, dataGranularity",
    [
        ("AAPL", "1d", "1h"),
        ("GOOGL", "1d", "1h"),
        ("MSFT", "1d", "1d"),
        ("AAPL", "1h", "1m"),
        ("GOOGL", "5d", "1d"),
        ("MSFT", "1d", "1d"),
        ("NVDA", "max", "3mo"),
        ("SAP", "1y", "1mo"),
    ],
)
def test_price(ticker, range, dataGranularity):
    """
    Test the price property of the TickerAPI class
    """

    ticker = Ticker(ticker)
    price = ticker.price(range=range, dataGranularity=dataGranularity)

    assert price.columns.tolist() == [
        "timestamp",
        "volume",
        "close",
        "open",
        "high",
        "low",
        "currency",
        "timezone",
        "exchangeTimezoneName",
        "exchangeName",
        "instrumentType",
    ]
    assert len(price) > 0


@pytest.mark.parametrize(
    "ticker",
    [
        ("AAPL"),
        ("GOOGL"),
        ("MSFT"),
        ("NVDA"),
        ("FMC"),
    ],
)
def test_current_trading_period(ticker):
    """
    Test the price property of the TickerAPI class
    """

    ticker = Ticker(ticker)
    current_trading_period = ticker.current_trading_period

    assert current_trading_period.columns.tolist() == [
        "pre",
        "regular",
        "post",
    ]
    assert len(current_trading_period) == 4
    assert current_trading_period.index.tolist() == [
        "timezone",
        "start",
        "end",
        "gmtoffset",
    ]


@pytest.mark.parametrize(
    "ticker, frequency, format",
    [
        ("AAPL", "quarterly", "fmt"),
        ("GOOGL", "quarterly", "fmt"),
        ("MSFT", "quarterly", "fmt"),
        ("NVDA", "quarterly", "raw"),
        ("FMC", "quarterly", "raw"),
    ],
)
def test_income_statement(ticker, frequency, format):
    ticker = Ticker(ticker)
    income_statement = ticker.income_statement(frequency=frequency, format=format)

    assert isinstance(income_statement, pd.DataFrame)
    assert income_statement.shape[0] > 0
    assert income_statement.shape[1] > 0


@pytest.mark.parametrize(
    "ticker, frequency, format",
    [
        ("AAPL", "quarterly", "fmt"),
        ("GOOGL", "quarterly", "fmt"),
        ("MSFT", "quarterly", "fmt"),
        ("NVDA", "quarterly", "raw"),
        ("FMC", "quarterly", "raw"),
    ],
)
def test_cash_flow(ticker, frequency, format):
    ticker = Ticker(ticker)
    cash_flow = ticker.cash_flow(frequency=frequency, format=format)

    assert isinstance(cash_flow, pd.DataFrame)
    assert cash_flow.shape[0] > 0
    assert cash_flow.shape[1] > 0


@pytest.mark.parametrize(
    "ticker, frequency, format",
    [
        ("AAPL", "quarterly", "fmt"),
        ("GOOGL", "quarterly", "fmt"),
        ("MSFT", "quarterly", "fmt"),
        ("NVDA", "quarterly", "raw"),
        ("FMC", "quarterly", "raw"),
    ],
)
def test_balance_sheet(ticker, frequency, format):
    ticker = Ticker(ticker)
    balance_sheet = ticker.balance_sheet(frequency=frequency, format=format)

    assert isinstance(balance_sheet, pd.DataFrame)
    assert balance_sheet.shape[0] > 0
    assert balance_sheet.shape[1] > 0


@pytest.mark.parametrize(
    "ticker, frequency, format",
    [
        ("AAPL", "quarterly", "fmt"),
        ("GOOGL", "quarterly", "fmt"),
        ("MSFT", "quarterly", "fmt"),
        ("NVDA", "quarterly", "raw"),
        ("FMC", "quarterly", "raw"),
    ],
)
def test_financials(ticker, frequency, format):
    ticker = Ticker(ticker)
    financials = ticker.financials(frequency=frequency, format=format)

    assert isinstance(financials, pd.DataFrame)
    assert financials.shape[0] > 0
    assert financials.shape[1] > 0
