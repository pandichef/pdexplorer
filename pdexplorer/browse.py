from ._dataset import current

# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Pandas.py
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Browser_Paned.py
# import PySimpleGUI as sg
import threading
from time import time, sleep
import webbrowser
import numpy as np
import pandas as pd


def make_html(df, num_rows=200, title=""):
    # s = df.head(num_rows).style
    # return (
    #     '<html><head><meta http-equiv="refresh" content="1"></head><body>'
    #     + s._repr_html_()
    #     + "</body></html>"
    # )
    # return (
    #     '<meta http-equiv="refresh" content="1" >'
    #     + df.head(num_rows).to_html(justify="center")
    #     + f"<br>Displaying {min(num_rows,len(df))}  of {len(df)}"
    # )
    result = """
<html>
<head><meta http-equiv="refresh" content="1">
<style>

    h2 {
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
    }
    table { 
        margin-left: auto;
        margin-right: auto;
    }
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 5px;
        text-align: center;
        font-family: Helvetica, Arial, sans-serif;
        font-size: 90%;
    }
    .wide {
        width: 90%; 
    }
</style>
</head>
<body>
    """
    result += f"<h2>{' '.join(title.split()[:10])}</h2>"
    result += df.head(num_rows).to_html(classes="wide", escape=False, index=False)
    result += """
</body>
</html>
"""
    return result


def display_dataframe(notify_event, num_rows=200):
    """Function to display the DataFrame when changes occur"""
    previous_df = current.df.copy()
    first_run = True
    while not notify_event.is_set():  # Check the event flag
        current_df = current.df.copy()
        if not current_df.equals(previous_df) or first_run:
            # print("DataFrame has changed:")
            # print(current_df)
            # assert turned_on, "oh no"

            t0 = time()
            with open("updated_df.html", "w") as f:
                f.write(make_html(current_df, num_rows, current.metadata["data_label"]))
            print(f"Saved to file ({time()-t0} ms)")
            # print("df changed")
            # print(f"first run is {first_run}")
            previous_df = current_df.copy()
            first_run = False
        sleep(1)


turned_on = False


def browse(num_rows=200):
    global turned_on
    global browse_notify_event
    global browse_thread
    if not turned_on:
        # global browse_thread
        # global browse_notify_event
        # # Create an Event to notify the display thread of changes #
        browse_notify_event = threading.Event()

        # Create a separate thread to display the DataFrame when changes occur #
        # browse_thread = threading.Thread(target=display_dataframe, args=(browse_notify_event,))
        browse_thread = threading.Thread(
            target=display_dataframe, args=(browse_notify_event, num_rows,)
        )
        browse_thread.daemon = True  # prevent console from blocking
        turned_on = True
        browse_thread.start()
    else:
        print("Already turned on.")
    webbrowser.open("updated_df.html")


def browse_off():
    global turned_on
    browse_notify_event.set()
    browse_thread.join()
    turned_on = False
    import os

    os.remove("updated_df.html")


# atexit.register doesn't work to clean up the thread... but this does: #
# https://stackoverflow.com/questions/58910372/script-stuck-on-exit-when-using-atexit-to-terminate-threads #
# def monitor_thread():
#     main_thread = threading.main_thread()
#     main_thread.join()
#     browse_notify_event.set()
#     browse_thread.join()


# monitor = threading.Thread(target=monitor_thread)
# monitor.daemon = True
# monitor.start()
