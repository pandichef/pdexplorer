import json

# from json import JSONDecodeError
# from typing import Optional
import pandas as pd


def extract_api_requests(
    page="https://info.uniswap.org/#/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    api_prefix="https://api.thegraph.com/subgraphs/name/",
    wait_for: int = 20,
    filter_address="0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",
    output_file="pool_page.json",
):
    """
    This automates the process of extracting API requests from a page.
    The manual process is as follows: dev tools -> Network tab -> Fetch/XHR
    """
    from seleniumwire import webdriver  # Import from seleniumwire
    from selenium.webdriver.edge.options import Options

    # Create a new instance of the Chrome driver
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--headless")  # Optional: Run Edge in headless mode
    # driver = webdriver.Edge()
    try:
        driver = webdriver.Chrome(options=edge_options)
    except:
        driver = webdriver.Edge(options=edge_options)

    # Go to the Google home page
    driver.get(page)

    import time

    time.sleep(wait_for)

    list_of_requests0 = driver.requests.copy()
    list_of_requests1 = []

    for request in list_of_requests0:
        if request.url.startswith(api_prefix):
            list_of_requests1.append(request)

    print(
        f"Found {len(list_of_requests0)} requests; only {len(list_of_requests1)} are valid API requests."
    )
    # print(len(list_of_requests0))
    # print(len(list_of_requests1))

    list_of_dicts = []
    for i, obj in enumerate(list_of_requests1):
        # print(i)
        # print(repr(obj))
        new_dict = {}
        # try:
        body = json.loads(obj.body)
        new_dict["query"] = body["query"]
        if isinstance(body["variables"], str):
            new_dict["variables"] = json.loads(body["variables"])
        else:
            new_dict["variables"] = body["variables"]
        new_dict["endpoint"] = obj.url
        # new_dict["fnc"] = lambda x: x  # pd.DataFrame.from_records(x)
        list_of_dicts.append(new_dict)
        # except JSONDecodeError as e:
        #     print(obj)
        #     raise Exception("stop running")

    assert len(list_of_dicts) == len(list_of_requests1)

    # remove if its a different address #
    if filter_address:
        list_of_dicts2 = []
        for i, this_dict in enumerate(list_of_dicts):
            if this_dict["variables"].get("address") is None:
                list_of_dicts2.append(this_dict)
            elif (
                this_dict["variables"].get("address") is not None
                and this_dict["variables"]["address"] == filter_address
            ):
                list_of_dicts2.append(this_dict)
            else:
                pass
        print(
            f"Found {len(list_of_dicts)} valid API requests; only {len(list_of_dicts2)} are related to address {filter_address}."
        )
    else:
        list_of_dicts2 = list_of_dicts

    if output_file:
        with open(output_file, "w") as f:
            f.write(json.dumps(list_of_dicts2))

    return list_of_dicts2
    # return list_of_dicts


def _tothegraph(
    query: str,
    variables,
    endpoint: str = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
) -> dict:
    import json
    from gql import Client, gql
    from gql.transport.aiohttp import AIOHTTPTransport
    import pandas as pd

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url=endpoint)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    # gql apparently validates, but not thegraph server... #
    query = query.replace("Bytes!", "String!")

    # Execute the query on the transport
    if variables:
        # try:
        # result = client.execute(gql(query), variable_values=json.loads(variables))
        # except TypeError:
        result = client.execute(gql(query), variable_values=variables)
    else:
        result = client.execute(gql(query))
    # print(result)
    return result


def tothegraph(query_dict: dict, key_number=0) -> pd.DataFrame:
    """Send query to API server and return pd.DataFrame"""
    query = query_dict["query"]
    variables = query_dict["variables"]
    endpoint = query_dict["endpoint"]
    # fnc = query_dict["fnc"]
    response_dict = _tothegraph(query, variables, endpoint)
    if key_number is not None:
        key_name = list(response_dict.keys())[key_number]
        df = pd.DataFrame.from_records(response_dict[key_name])
    else:
        # key_name = list(response_dict.keys())[key_number]
        df = pd.DataFrame.from_records(response_dict)
    # if len(df) == 0:
    #     df = pd.DataFrame.from_records(response_dict)

    # df.to_clipboard()
    try:
        df["date"] = pd.to_datetime(df["date"], unit="s")
    except KeyError:
        pass

    for col in df.columns:
        if col != "date":
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass

    return df


def searchframes(list_of_dicts, column_name="volumeUSD"):
    """Send query to API server and search for column values"""
    from gql.transport.exceptions import TransportQueryError

    for i, this_dict in enumerate(list_of_dicts):
        try:
            df = tothegraph(this_dict)
            if "date" in df.columns:
                df = df.sort_values("date", ascending=False)
            if column_name in df.columns:
                print(
                    i,
                    ": ",
                    df[column_name][0],
                    f""" ({df['date'][0] if "date" in df.columns else '<NA>'})""",
                )
        except TransportQueryError as e:
            pass


def searchqueries(list_of_dicts, query_type="poolDayDatas"):
    """Search for column names in API request string"""
    query_type = query_type.lower()
    match_list = []
    for i, this_dict in enumerate(list_of_dicts):
        if query_type in this_dict["query"].lower():
            print(
                "[",
                i,
                "]\nQUERY:\n",
                this_dict["query"],
                "\nVARIABLES:\n",
                this_dict["variables"],
                "\n",
            )
            match_list.append(i)
    return match_list
