import shutil


def print_horizontal_line():
    # Get the terminal width
    terminal_width, _ = shutil.get_terminal_size()

    # Create a horizontal line
    line = "-" * terminal_width

    # Print the horizontal line
    print(line)
