import re
from ._dataset import current


def _clean(string_with_extra_spaces: str) -> str:
    cleaned = " ".join(string_with_extra_spaces.split())
    return cleaned


def check_syntax(_: dict, syntax: str) -> dict:
    # _ is the parsed commandarg
    updates = {}
    if syntax is not None and syntax != "" and syntax.find("varlist") > -1:
        for name in _["anything"].split():
            assert (
                name in current.df.columns
            ), f"Syntax specifies a varlist, but {name} not found in current dataset."
        updates.update({"varlist": _["anything"]})
    else:
        pass
    return updates


def parse_options(options_string: str, split_values=False) -> dict:
    # split_values is used in _altair_mapper
    if options_string is None:
        return {}
    options_string = options_string.replace("( ", "(")
    options_string = options_string.replace(" )", ")")

    result = {}
    pattern = r"(\w+)\(([^)]*)\)"
    matches = re.findall(pattern, options_string)

    for key, value in matches:
        result[key] = value.strip()

    remaining_words = re.sub(pattern, "", options_string).split()
    for word in remaining_words:
        result[word] = True

    if split_values:
        return {key: value.split(" ") for key, value in result.items()}
    else:
        return result


def parse(commandarg: str, syntax: str = "") -> dict:
    commandarg = commandarg.replace("==", "__eq__").replace("!=", "__neq__")
    if (
        commandarg.startswith("if ")
        or commandarg.startswith("in ")
        or commandarg.startswith("using ")
    ):
        commandarg = " " + commandarg
    split_identifiers = (
        " in ",
        " if ",
        " using ",
        ",",
        " [",
        "]",
        "=",  # check for = before weights only
    )
    split_locations = {}
    end_of_anything = None
    for i, split_identifier in enumerate(split_identifiers):
        # this_location = commandarg.find(split_identifier)
        split_locations[split_identifier] = commandarg.find(split_identifier)
        # print(split_identifier)
        # print(split_locations[split_identifier])
        if (  # exclude when "=" is after the open bracket
            split_identifier == "="
            and split_locations[" ["] > -1
            and split_locations[split_identifier] > split_locations[" ["]
        ):
            # print(split_locations[split_identifier])
            # print(split_locations[" ["])
            split_locations[split_identifier] = -1
        if split_locations[split_identifier] > -1:
            if end_of_anything:
                end_of_anything = min(
                    split_locations[split_identifier], end_of_anything
                )
            else:
                end_of_anything = split_locations[split_identifier]
    # print(split_locations)
    sorted_splits = sorted(
        split_locations.items(), key=lambda x: x[1]
    )  # list of tuples
    _ = {}  # parsed commandarg is represented as _
    for index, (identifier, position) in enumerate(sorted_splits):
        if position == -1:
            _[identifier] = None
        else:
            if identifier == "[":
                startpos = position + len(identifier)
                endpos = split_locations["]"]
                _[identifier] = _clean(commandarg[startpos:endpos])
            elif identifier != "]":
                startpos = position + len(identifier)  # + 1
                try:
                    endpos = sorted_splits[index + 1][1]
                    _[identifier] = _clean(commandarg[startpos:endpos])
                except IndexError:
                    _[identifier] = _clean(commandarg[startpos:])
        # if parsed[identifier] and :  # i.e., not None
        #     parsed[identifier] = " ".join(parsed[identifier].split())

    _["anything"] = _clean(commandarg[:end_of_anything])
    if _["anything"] == "":
        _["anything"] = None
    if _[" if "]:
        _[" if "] = _[" if "].replace("__eq__", "==").replace("__neq__", "!=")

    # rename
    _["weight"] = _[" ["]
    del _[" ["]
    if _["weight"] is None:
        del _["]"]  # hack
    _["options"] = _[","]
    del _[","]
    _["if"] = _[" if "]
    del _[" if "]
    _["in"] = _[" in "]
    del _[" in "]
    _["using"] = _[" using "]
    del _[" using "]
    # parsed["exp"] = parsed["="]

    # See https://www.stata.com/manuals13/psyntax.pdf
    parsed_options = parse_options(_["options"])
    _.update(parsed_options)
    # _["options"] = parse_options(_["options"], split_values=True)
    updates = check_syntax(_, syntax)  # raise error is syntax is invalid
    _.update(updates)  # e.g., varlist added if passes validation
    return _


def parse_if_condition(if_condition_string: str) -> dict:
    return {}  # todo

