import json
import requests
from typing import Optional
import datetime
import pandas as pd

# from datetime import datetime

# Documented here: #
# https://developers.binance.com/docs/binance-trading-api/futures#get-funding-rate-history #
# root_url = "https://fapi.binance.com/fapi/v1/fundingRate"
root_url = "https://fapi.binance.com/"


def fapi_v1_fundingRate_wrapper(
    symbol: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    limit: Optional[int] = None,
) -> list:
    url_path = "fapi/v1/fundingRate"
    if limit:
        assert limit <= 1000, f"Per {url_path}, limit must be <=1000"
    query = []
    query.append("symbol=" + symbol if symbol else "")
    query.append("startTime=" + str(start_time) if start_time else "")
    query.append("endTime=" + str(end_time) if end_time else "")
    query.append("limit=" + str(limit) if limit else "")
    query = list(filter(None, query))
    query = "&".join(query)
    url = root_url + url_path + "?" + query
    res = requests.get(url)
    return json.loads(res.text)


def to_dataframe(result: list) -> pd.DataFrame:
    df = pd.DataFrame(result)
    df["fundingTime"] = pd.to_datetime(df["fundingTime"], unit="ms")
    df["fundingRate"] = pd.to_numeric(df["fundingRate"], errors="coerce")
    return df


now = datetime.datetime.now()
end_time = int(now.timestamp() * 1000)
start_time = int((now - datetime.timedelta(days=3)).timestamp() * 1000)

result = fapi_v1_fundingRate_wrapper("ETHUSDT", start_time, end_time, 1000)
df = to_dataframe(result)

"""
# Original 
# Source:
# https://steemit.com/python/@marketstack/how-to-download-historical-price-data-from-binance-with-python
# https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data
import datetime as dt  # for dealing with times
import json  # for parsing what binance sends back to us
import hashlib
from json import JSONDecodeError
from types import SimpleNamespace  # for building urls
from typing import List, Union, Optional
import requests  # for making http requests to binance
from requests import Session, Request, Response
import pandas as pd
import numpy as np
from pandas import DataFrame

# from ...utils import pure

# root_url = "https://api.binance.com/api/v3/klines"
root_url = "https://fapi.binance.com/fapi/v1/fundingRate"
# from .urls import binance_funding_rate as root_url

# @pure
def _build_query(symbol: str | None = None, limit: int = 1000) -> Request:
    limit = int(limit)
    if symbol is None:
        url = root_url + "?limit=" + str(limit)
    else:
        url = root_url + "?symbol=" + symbol + "&limit=" + str(limit)
    return Request("GET", url)


def _make_request(request: Request) -> Response:
    s = Session()
    prepped_ = s.prepare_request(request)
    resp = s.send(prepped_)
    # print("#######################################################")
    # print("funding_rate.py: " + resp.text + "...")
    # print("#######################################################")
    return resp


# @pure
def _check_response(
    response: Response | SimpleNamespace, show_reponse: bool = False
) -> None:
    # nested function
    def _wrap(text: str, show_reponse: bool = show_reponse) -> str:
        if show_reponse:
            return __name__ + text + "\n" + response.text
        else:
            return __name__ + text

    try:
        obj = json.loads(response.text)
    except JSONDecodeError:
        raise AssertionError(_wrap(" could not be parsed (JSONDecodeError)"))
    assert type(obj) == list, _wrap(": response is not a list")
    assert type(obj[0]) == dict, _wrap(": response is not a list of objects")
    assert len(obj[0]) == 3, _wrap(": response is not a list of 3 numbers")
    return None


# @pure
def _make_dataframe(response: Response | SimpleNamespace) -> DataFrame:
    df = pd.DataFrame(json.loads(response.text))
    # df["fundingTime"] = pd.to_datetime(df["fundingTime"], unit="s")
    df["fundingTime"] = [dt.datetime.fromtimestamp(x / 1000) for x in df["fundingTime"]]
    df["fundingRate"] = df["fundingRate"].astype("float64")
    return df


def get_funding_rate(symbol: str | None = None, limit: int = 1000) -> DataFrame:
    request = _build_query(symbol=symbol, limit=limit)
    response = _make_request(request)
    _check_response(response, True)
    df = _make_dataframe(response)
    return df


def get_enhanced_funding_rate(
    symbol: str | None = None, limit: int = 1000
) -> DataFrame:
    # Do nothing for now
    df = get_funding_rate(symbol, limit)
    max_timestamp = df.fundingTime.max()
    df["is_latest"] = np.where(df["fundingTime"] == max_timestamp, True, False)
    return df


def extract_current_funding_rate(symbol: str | None = None) -> float:
    df = get_enhanced_funding_rate(symbol, 1)
    # print(df)
    return df["fundingRate"][0]


################################################################
# Applications


################################################################
if __name__ == "__main__":
    # df = get_enhanced_funding_rate()
    # df = get_klines("ETHUSDT", 20, "1d")
    # from ...utils import browse

    # browse(df=df)
    # vol = get_volatility("GRTUSDT", 30)
    # print(vol)
    # print(df)
    # res = extract_current_funding_rate("ETHUSDT")
    res = get_enhanced_funding_rate("ETHUSDT")
    print(res)
"""

