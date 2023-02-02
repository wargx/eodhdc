# EODHDC

![license](https://badgen.net/pypi/license/eodhdc)
![version](https://badgen.net/pypi/v/eodhdc)
![versions](https://badgen.net/pypi/python/eodhdc)
![coverage](https://raw.githubusercontent.com/wargx/eodhdc/main/reports/coverage.svg)
![pylint](https://raw.githubusercontent.com/wargx/eodhdc/main/reports/pylint.svg)
![docs](https://readthedocs.org/projects/eodhdc/badge/?version=stable)  
![pytest:37](https://raw.githubusercontent.com/wargx/eodhdc/main/reports/pytest-py37.svg)
![pytest:38](https://raw.githubusercontent.com/wargx/eodhdc/main/reports/pytest-py38.svg)
![pytest:39](https://raw.githubusercontent.com/wargx/eodhdc/main/reports/pytest-py39.svg)
![pytest:310](https://raw.githubusercontent.com/wargx/eodhdc/main/reports/pytest-py310.svg)
![pytest:311](https://raw.githubusercontent.com/wargx/eodhdc/main/reports/pytest-py311.svg)

Python client for the EOD Historical Data service REST / WebSockets API and provides various financial data 
including stock market, splits and dividends, fundamental and economic, exchanges and alternative data feeds.
Provides synchronous and asynchronous interfaces for HTTP API, asynchronous interface for WebSockets.   

[Documentation](https://eodhdc.readthedocs.io/)

## Installation

For normal usage you will need API key which you can get from [here](https://eodhistoricaldata.com/).  
Supported Python version >= 3.7

Package can be installed using pip or poetry:
```
pip install eodhdc
```
```
poetry add eodhdc
```
To support additional HTTP clients install with extras:
```
pip install eodhdc[httpx,aiohttp]
```

## Quickstart

Asynchronous usage
```python
import asyncio
from eodhdc import EODHDClient

eodhdc = EODHDClient("httpxa", key="demo")
async with eodhdc.session:
    results = await asyncio.gather(
        eodhdc.market.historical("MCD.US", start="2023-01-01", finish="2023-01-10", fmt="csv"),
        eodhdc.market.historical("MCD.US", start="2023-01-01", finish="2023-01-10", fmt="json")
    )
for result in results:
    print(result)
```

Synchronous usage
```python
from eodhdc import EODHDClient

eodhdc = EODHDClient("requests", key="demo")
result = eodhdc.market.historical(
    "AAPL.US", start="2023-01-01", finish="2023-01-10",
    fmt="json", output="pandas:./response.csv", writer={"header": False}
)
print(result, "\n")
```

WebSockets usage
```python
from eodhdc import EODHDWebSockets

eodhdws = EODHDWebSockets(buffer=100)
async with eodhdws.connect("us") as websocket:
    await eodhdws.subscribe(websocket, ["TSLA", "EURUSD"])
    async for message in eodhdws.receive(websocket):
        print(message)
        if len(eodhdws.buffer) > 5:
            await eodhdws.unsubscribe(websocket, ["EURUSD"])
        if len(eodhdws.buffer) > 10:
            eodhdws.deactivate()

print(eodhdws.buffer)
```

Also check `playground.py` for quickstart examples. 

## Description

### Main client modules

- EODHDClient: HTTP API client, parameters are:
  - client: http client module to use.
  - key: api token.
  - args: http client `get` args to use across requests.

- EODHDWebSockets: WebSockets API client, parameters are:
  - key: api token.
  - buffer: enable and set buffer size.
  - args: websocket client args.

EODHDClient will automatically determine sync or async http client and provide corresponding interface 
with same signature, so for example usage can easily be changed:

```python
eodhdc = EODHDClient("httpxs")
result = eodhdc.market.historical(...)
```

```python
eodhdc = EODHDClient("httpsxa")
result = await eodhdc.market.historical(...)
```

Asynchronous version of EODHDClient can be used without context manager, do not forget to call `destroy` 
method to close session in that case. 

EODHDWebSockets client provides following methods:
- connect: connect to web-socket endpoint, returns context manager.
- authorize: check authorization status, do not use directly as it will consume messages. 
- subscribe: subscribe to the tickers.
- unsubscribe: unsubscribe from the tickers.
- receive: receive messages, async generator.
- activate: activate message loop.
- deactivate: deactivate message loop.

### HTTP client modules

- requests: default, well known, synchronous module.
- httpxs: httpx library, synchronous mode, 'httpx' extra.
- httpxa: httpx library, asynchronous mode, 'httpx' extra.
- aiohttp: aiohttp library, asynchronous mode, 'aiohttp' extra.

### HTTP API groups

Main HTTP API module contains groups that corresponds to EODHD API groups, and can be accessed like:   
```eodhdc.market.<method>``` or  ```eodhdc.exchange.<method>```  
See below mapping for client groups and methods.    
Visit official API [documentation](https://eodhistoricaldata.com/financial-apis/) for detailed description. 

### HTTP API group methods

In addition to original API parameters each method have:
- args: override or add http client `get` args.
- output: output format and optionally file location, format is `<type>[:path]`
  - types: response type
    - "response": raw binary response body
    - "content": decoded as response content type
    - "pandas": pandas dataframe
  - path: additionally save response to file
    - for "response" and "content" will save as is
    - for "pandas" will save in format specified by extension: 
      parquet, pickle, csv, hdf, xlsx, json, html, feather, tex, dta, md  
- writer: pandas writer parameters, see [original](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html) `to_<format>` methods for more details.  
  note that some formats may require 3rd-party libraries.  
  additionally writer can be provided with:
  - change:columns - dict to rename DataFrame columns. 
  - change:reorder - bool to use columns dict for DataFrame columns order.
  - change:reindex - str or list to set DataFrame columns as index.

### API support status

API support status and mapping for client groups and methods.   

- [x] HTTP
  - [x] Stock Market Prices, Splits and Dividends Data API
    - [x] End-Of-Day Historical Stock Market Data API
      - market.historical 
    - [x] Live (Delayed) Stock Prices API
      - market.delayed
    - [x] Historical Splits and Dividends API
      - market.dividends
      - market.splits
    - [x] Technical Indicator API
      - market.indicators
    - [x] Intraday Historical Data API
      - market.intraday
    - [x] Options Data API
      - market.options
  - [x] Fundamental and Economic Financial Data API
    - [x] Fundamental Data for Cryptocurrencies
      - fundamental.crypto
    - [x] Historical Market Capitalization API
      - fundamental.capitalization
    - [x] Insider Transactions API
      - fundamental.insider
    - [x] Fundamental Data: Stocks, ETFs, Mutual Funds, Indices
      - fundamental.fundamentals
      - fundamental.bulk
    - [x] Calendar. Upcoming Earnings, Trends, IPOs and Splits
      - fundamental.calendar
    - [x] Bonds Fundamentals and Historical API
      - fundamental.bonds
  - [x] Exchanges (Stock Market) Financial APIs
    - [x] Bulk API for EOD, Splits and Dividends
      - exchange.bulk
    - [x] Exchanges API. Get List of Tickers
      - exchange.exchanges
      - exchange.tickers
    - [x] Exchanges API. Trading Hours, Stock Market Holidays, Symbols Change History
      - exchange.details
      - exchange.history
    - [x] Stock Market Screener API
      - exchange.screener
    - [x] Search API for Stocks, ETFs, Mutual Funds and Indices
      - exchange.search
  - [x] Alternative Data Financial API
    - [x] Sentiment Data Financial API for News and Tweets
      - alternative.sentiment
    - [x] Economic Events Data API
      - alternative.events
    - [x] Stock Market and Financial News API
      - alternative.news
    - [x] Macro Indicators API
      - alternative.macroindicators
    - [x] Macroeconomic Data API
      - alternative.macroeconomic
- [x] WebSockets
  - [x] Stock Market Prices, Splits and Dividends Data API
    - [x] Real-Time Data API

### Exceptions

Exceptions hierarchy:

- **ClientException**: Base HTTP client exception.
  - **ClientConnectionTimeout**: Client connection timeout exception. 
  - **ClientConnectionError**: Client connection error exception. 
  - **ClientHTTPError**: Client HTTP error exception.
- **ModuleException**: Base module exception. 
  - **FileIOError**: File IO exception. 
  - **UnsupportedContentType**: Unsupported response content exception. 
  - **UnsupportedExtension**: Unsupported pandas extension exception. 
  - **JSONDecodeError**: JSON decoding exception. 
  - **BytesDecodeError**: Bytes decoding exception. 
  - **PandasRuntimeError**: Pandas runtime exception. 
  - **UnknownClient**: Unknown client exception. 
  - **ImproperClient**: Improper client exception.
- **WebsocketException**: Base websocket exception. 
  - **WebsocketUnknownEndpoint**: Websocket unknown endpoint exception. 
  - **WebsocketAuthError**: Websocket authentication exception. 
  - **WebsocketResponseError**: Websocket response error exception.

## Custom HTTP clients

Additionally, you can provide your own HTTP client by passing its module instead of name string.  
Module should implement `get` method and `create` and `destroy` can be provided for asynchronous session management.  
Check modules under `eodhd.clients` for details about required parameters, return data type and exceptions handling.

## Disclaimer

The information in this document is for informational and educational purposes only. Nothing in this document 
can be construed as financial, legal, or tax advice. The content of this document is solely the opinion of the 
author, who is not a licensed financial advisor or registered investment advisor. The author is not affiliated 
as a promoter of EOD Historical Data services. 

This document is not an offer to buy or sell financial instruments. Never invest more than you can afford to 
lose. You should consult a registered professional advisor before making any investment.
