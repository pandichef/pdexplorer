# Inspiration: https://xlsxwriter.readthedocs.io/working_with_pandas.html
# Note the complexity in handling the header in pandas
import pandas as pd
import subprocess
import os
from .dataset import current
from typing import Optional


def browse():
    import dtale  # very slow import

    # df = current.df
    if current.dtale_browser:
        current.dtale_browser.kill()
    new_dtale_browser = dtale.show(current.df_labeled, name="currentdf")
    if current.dtale_browser is None:
        new_dtale_browser.open_browser()
    current.dtale_browser = new_dtale_browser
    # current.dtale_browser = dtale.show(current.df_labeled, name="currentdf")
    # current.dtale_browser.open_browser()


def browse_in_excel(
    path: Optional[str] = None,
    limit: Optional[int] = None,
    run: bool = True,
    percentage_columns: Optional[list] = None,
    autofit_columns: Optional[list] = None,
) -> None:
    df = current.df

    if not path:
        # set default file i.e., tmp/easy_xlsxwriter.xlsx
        import tempfile

        path = os.path.join(tempfile.gettempdir(), "easy_xlsxwriter.xlsx")

    writer = pd.ExcelWriter(path=path, engine="xlsxwriter")  # type: ignore
    if limit:
        df.head(limit).to_excel(writer, sheet_name="Sheet1", startrow=1, header=False)
    else:
        df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    default_format = workbook.add_format(  # type: ignore
        {
            "num_format": "#,##0.00",
            "align": "center",
            # 'shrink': True,
        }
    )
    for column in df.columns:
        this_column_position = list(df.columns).index(column) + 1
        worksheet.set_column(
            this_column_position, this_column_position, cell_format=default_format
        )

    percentage_format = workbook.add_format({"num_format": "0%", "align": "center"})  # type: ignore
    if percentage_columns:
        for column in percentage_columns:
            this_column_position = list(df.columns).index(column) + 1
            worksheet.set_column(
                this_column_position,
                this_column_position,
                cell_format=percentage_format,
            )

    # format header
    header_format = workbook.add_format(  # type: ignore
        {
            "bold": True,
            "text_wrap": True,
            "align": "center",
            "valign": "top",
            "fg_color": "#D7E4BC",
            "border": 1,
        }
    )
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num + 1, value, header_format)
    worksheet.write(0, 0, "Ticker", header_format)
    worksheet.freeze_panes(1, 1)

    # autofit
    if autofit_columns:
        for column in autofit_columns:
            column_width = df[column].str.len().max()
            this_column_position = list(df.columns).index(column) + 1
            worksheet.set_column(
                this_column_position, this_column_position, width=column_width
            )

    # save excel file
    worksheet.set_zoom(75)
    writer.close()  # type: ignore
    if run:
        subprocess.run(f"start excel {path}", shell=True)
