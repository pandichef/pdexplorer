import io
import sys

browser = None


def webbrowser_open(url, join_full_path=True, browser_name="Edge"):
    """
    browser_name: Chrome, Edge, ChromiumEdge, Firefox, Ie, Safari, WebKitGTK, WPEWebKit
    """
    # https://stackoverflow.com/questions/71680422/python-displaying-a-web-site-in-the-same-browser-tab-each-time-webbrowser-open
    global browser
    from selenium import webdriver
    import os

    if join_full_path:
        url = os.path.join(os.getcwd(), url)

    try:
        browser.get(url)
    except:
        # with suppress_stdout():
        try:
            browser = getattr(webdriver, browser_name)()
            browser.get(url)
        except:
            import webbrowser

            webbrowser.open(url)
