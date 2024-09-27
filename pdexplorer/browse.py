# from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
# import io
# from contextlib import redirect_stdout
# import threading
# import sys
# from time import time, sleep

# import webbrowser
# import numpy as np
# import pandas as pd


# def make_html(df, num_rows=200, title=""):
#     # <meta http-equiv="refresh" content="1">
#     result = """
# <html>
# <head>
# <style>

#     h2 {
#         text-align: center;
#         font-family: Helvetica, Arial, sans-serif;
#     }
#     table {
#         margin-left: auto;
#         margin-right: auto;
#     }
#     table, th, td {
#         border: 1px solid black;
#         border-collapse: collapse;
#     }
#     th, td {
#         padding: 5px;
#         text-align: center;
#         font-family: Helvetica, Arial, sans-serif;
#         font-size: 90%;
#     }
#     .wide {
#         width: 90%;
#     }
# </style>
# </head>
# <body>
#     """
#     result += f"<h2>{' '.join(title.split()[:10])}</h2>"
#     result += df.head(num_rows).to_html(classes="wide", escape=False, index=False)
#     result += """<script>
#     let storedTableHTML = '';

#     function checkForChanges() {
#         fetch('http://localhost:8000/updated_df.html')
#             .then(response => response.text())
#             .then(newTableHTML => {
#                 const dataTable = document.getElementById('data-table');
#                 if (storedTableHTML !== '' && newTableHTML !== storedTableHTML) {
#                     // Content has changed, refresh the page
#                     location.reload();
#                 } else {
#                     // Update stored table HTML with the new data
#                     storedTableHTML = newTableHTML;
#                     // Replace the table content with the new HTML
#                     dataTable.innerHTML = newTableHTML;
#                 }
#             })
#             .catch(error => {
#                 console.error('Error fetching data:', error);
#             });
#     }

#     // Check for changes every 1 seconds (adjust the interval as needed)
#     setInterval(checkForChanges, 1000);
# </script></body></html>
# """
#     return result


# def save_html_file(notify_event, num_rows=200):
#     """Function to display the DataFrame when changes occur"""
#     previous_df = current.df.copy()
#     first_run = True
#     while not notify_event.is_set():  # Check the event flag
#         current_df = current.df.copy()
#         if not current_df.equals(previous_df) or first_run:
#             t0 = time()
#             with open("updated_df.html", "w") as f:
#                 f.write(make_html(current_df, num_rows, current.metadata["data_label"]))
#             print(f"Saved to file ({time()-t0} ms)")
#             previous_df = current_df.copy()
#             first_run = False
#         sleep(1)


# # stop_server = False


# def serve_html_file(notify_event):
#     # global stop_server
#     # stop_server = False

#     class SilentRequestHandler(SimpleHTTPRequestHandler):
#         def log_message(self, format, *args):
#             pass  # Suppress log messages

#     httpd = ThreadingHTTPServer(("localhost", 8000), SilentRequestHandler)

#     try:
#         while True:
#             if notify_event.is_set():
#                 break  # Exit the loop if the event is set
#             httpd.handle_request()
#     except KeyboardInterrupt:
#         pass

#     httpd.server_close()
#     print("Server stopped gracefully.")


# def browse(num_rows=200):
#     global notify_event
#     global save_thread
#     global serve_thread
#     if not current.browse_turned_on:
#         # # Create an Event to notify the display thread of changes #
#         notify_event = threading.Event()
#         # Create a save_thread to save the DataFrame when changes occur #
#         save_thread = threading.Thread(
#             target=save_html_file, args=(notify_event, num_rows,)
#         )
#         save_thread.daemon = True  # prevent console from blocking
#         current.browse_turned_on = True
#         save_thread.start()
#         # Create a serve_thread to create a light weight web server #
#         # serve_notify_event = threading.Event()
#         serve_thread = threading.Thread(target=serve_html_file, args=(notify_event,))
#         serve_thread.daemon = True  # prevent console from blocking
#         serve_thread.start()
#     else:
#         print("Already turned on.")
#     from ._webbrowser import webbrowser_open

#     webbrowser_open("http://localhost:8000/updated_df.html", join_full_path=False)


# def browse_off():
#     # global stop_server
#     notify_event.set()
#     save_thread.join()
#     serve_thread.join()
#     current.browse_turned_on = False
#     # stop_server = True
#     import os

#     sleep(1)
#     os.remove("updated_df.html")


# # atexit.register doesn't work to clean up the thread... but this does: #
# # https://stackoverflow.com/questions/58910372/script-stuck-on-exit-when-using-atexit-to-terminate-threads #
# # def monitor_thread():
# #     main_thread = threading.main_thread()
# #     main_thread.join()
# #     browse_notify_event.set()
# #     browse_thread.join()


# # monitor = threading.Thread(target=monitor_thread)
# # monitor.daemon = True
# # monitor.start()


# # def browse(num_rows=None):
# #     if num_rows:
# #         current.df.head(num_rows).to_clipboard()
# #     else:
# #         current.df.to_clipboard()

# import os
# import pandas as pd


# def browse(num_rows=None, file_name="output.csv"):
#     if num_rows:
#         current.df.head(num_rows).to_csv(file_name, index=True)
#     else:
#         current.df.to_csv(file_name, index=True)

#     os.startfile(os.path.abspath(file_name))
from ._dataset import current


import xlwings as xw
from pywintypes import com_error


def browse(file_name="pdexplorer.xlsx", sheet_name="Sheet1"):
    import xlwings as xw

    if not current.xlwings_workbook:
        current.xlwings_workbook = xw.Book(file_name)

    # pid = current.xlwings_workbook.app.pid
    # print(f"Excel process ID: {pid}")

    sheet = current.xlwings_workbook.sheets[sheet_name]
    sheet.clear()
    sheet.range("A1").value = current.df

    # current.xlwings_workbook.app.visible = True
    try:
        current.xlwings_workbook.app.activate(steal_focus=True)
    except:
        xw.apps.active.api.WindowState = -4137  # xlNormal
        current.xlwings_workbook.app.activate(steal_focus=True)

    current.xlwings_workbook.save()
