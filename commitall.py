import os


def upgrade_pypi(package_name):
    """Upgrades pypi version
    e.g., version 0.0.3 automatically becomes 0.0.4
    """

    os.chdir(package_name)
    with open("setup.py", "r") as setup_file:
        setup_file_text = setup_file.read()
    setup_file_lines = setup_file_text.split("\n")
    last_version_line = [
        item for item in setup_file_lines if item.startswith("    version=")
    ][0]
    last_version_number = last_version_line.split('"')[1]
    last_version_split = last_version_number.split(".")
    new_version_number = (
        last_version_split[0]
        + "."
        + last_version_split[1]
        + "."
        + str(int(last_version_split[2]) + 1)
    )

    new_version_line = last_version_line.replace(
        last_version_number, new_version_number
    )
    new_setup_file_text = setup_file_text.replace(last_version_line, new_version_line)
    with open("setup.py", "w") as setup_file:
        setup_file.write(new_setup_file_text)
    os.system("rm -rf dist")
    os.system("python -m build")
    os.system(f"twine upload --repository {package_name} dist/*")  # uses .pypirc
    os.system("git add .")
    os.system(f'git commit -m "PyPI version {new_version_number}"')
    os.system("git push")
    # os.chdir("pdexplorer")  # optional
    # os.system("cloc . --vcs=git")  # optional


upgrade_pypi(package_name="pdexplorer")
