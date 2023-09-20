import os
import requests
from bardapi import Bard, SESSION_HEADERS


def bard(prompt: str = "How is the weather today in seoul?"):
    # See https://github.com/dsdanielpark/Bard-API/issues/155
    # This is a really a big hack and barely works
    __Secure1PSID = os.environ["__Secure-1PSID"]
    __Secure1PSIDCC = os.environ["__Secure-1PSIDCC"]
    __Secure1PSIDTS = os.environ["__Secure-1PSIDTS"]

    session = requests.Session()
    token = __Secure1PSID
    # print(token)
    session.cookies.set("__Secure-1PSID", token)
    session.cookies.set("__Secure-1PSIDCC", __Secure1PSIDCC)
    session.cookies.set("__Secure-1PSIDTS", __Secure1PSIDTS)
    session.headers = SESSION_HEADERS

    bard = Bard(token=token, session=session)
    res = bard.get_answer(prompt)
    return res["content"]
