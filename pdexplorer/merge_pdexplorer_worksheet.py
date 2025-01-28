import os
import click
import xlwings as xw
import pywintypes

file_dir = os.path.dirname(os.path.abspath(__file__))

@click.command()
@click.argument('dest_file', type=click.Path(exists=True))
def insert_pdexplorer(dest_file):
    """
    Insert the '_pdexplorer' sheet from '_pdexplorer.xlsm' into DEST_FILE as the first sheet.
    If a sheet named '_pdexplorer' already exists in the destination file, it is renamed and replaced.
    The renamed sheet is deleted after the new sheet is inserted.

    Args:
        dest_file: The destination workbook (can be .xlsm or .xlsx).
    """
    src_file = os.path.join(file_dir, "_pdexplorer.xlsm")
    src_sheet_name = "_pdexplorer"
    temp_sheet_name = "_temp_pdexplorer"

    # Ensure the source file exists
    if not os.path.exists(src_file):
        raise FileNotFoundError(f"The source file '{src_file}' does not exist.")

    # Open the source and destination workbooks
    src_wb = xw.Book(src_file)
    dest_wb = xw.Book(dest_file)

    # Ensure the source sheet exists
    if src_sheet_name not in [sheet.name for sheet in src_wb.sheets]:
        raise ValueError(f"The sheet '{src_sheet_name}' does not exist in the source file '{src_file}'.")

    # Get the source sheet
    src_sheet = src_wb.sheets[src_sheet_name]

    # If the destination workbook contains '_pdexplorer', rename it
    if src_sheet_name in [sheet.name for sheet in dest_wb.sheets]:
        dest_wb.sheets[src_sheet_name].name = temp_sheet_name

    # Copy the source sheet to the destination workbook
    try:
        src_sheet.api.Copy(Before=dest_wb.sheets[0].api)
    except pywintypes.com_error as e:
        src_wb.close()
        dest_wb.close()
        if str(e).__contains__("Excel cannot insert the sheets into the destination workbook, because it contains fewer rows and columns than the source workbook."):
            raise Exception("Insertion failed like due to using the older .xls file format. Please save the destination file as .xlsx and try again.")
        else:
            raise Exception("Insertion failed for an unknown reason.  Contact administrator.")

    # The copied sheet will have the same name as the source sheet
    new_sheet = dest_wb.sheets[0]
    new_sheet.name = src_sheet_name

    # Delete the renamed temporary sheet if it exists
    if temp_sheet_name in [sheet.name for sheet in dest_wb.sheets]:
        dest_wb.sheets[temp_sheet_name].delete()

    # Save and close the workbooks
    dest_wb.save()
    src_wb.close()
    dest_wb.close()

    click.echo(f"The sheet '{src_sheet_name}' has been inserted into '{dest_file}' as the first sheet.")

# Entry point for the script
if __name__ == "__main__":
    insert_pdexplorer()
