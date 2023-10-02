from ._dataset import current

# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Pandas.py
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib_Browser_Paned.py
# import PySimpleGUI as sg
import threading
import time


def display_dataframe(notify_event):
    """Function to display the DataFrame when changes occur"""
    previous_df = current.df.copy()

    while not notify_event.is_set():  # Check the event flag
        current_df = current.df.copy()
        if not current_df.equals(previous_df):
            print("DataFrame has changed:")
            print(current_df)
            previous_df = current_df.copy()
        time.sleep(1)


turned_on = False


def browse():
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
            target=display_dataframe, args=(browse_notify_event,)
        )
        browse_thread.daemon = True  # prevent console from blocking
        browse_thread.start()
        turned_on = True
    else:
        print("Already turned on.")


def browse_off():
    global turned_on
    browse_notify_event.set()
    browse_thread.join()
    turned_on = False


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
