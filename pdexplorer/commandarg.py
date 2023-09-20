import re


def _clean(string_with_extra_spaces: str) -> str:
    cleaned = " ".join(string_with_extra_spaces.split())
    return cleaned


def parse_commandarg(_commandarg: str) -> dict:
    _commandarg = _commandarg.replace("==", "__eq__").replace("!=", "__neq__")
    split_identifiers = (
        " in ",
        "if ",
        "using",
        ",",
        " [",
        "]",
        "=",  # check for = before weights only
    )
    split_locations = {}
    end_of_anything = None
    for i, split_identifier in enumerate(split_identifiers):
        # this_location = commandarg.find(split_identifier)
        split_locations[split_identifier] = _commandarg.find(split_identifier)
        # print(split_identifier)
        # print(split_locations[split_identifier])
        if (  # exclude when "=" is after the open bracket
            split_identifier == "="
            and split_locations[" ["] > -1
            and split_locations[split_identifier] > split_locations[" ["]
        ):
            print(split_locations[split_identifier])
            print(split_locations[" ["])
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
    parsed = {}
    for index, (identifier, position) in enumerate(sorted_splits):
        if position == -1:
            parsed[identifier] = None
        else:
            if identifier == "[":
                startpos = position + len(identifier)
                endpos = split_locations["]"]
                parsed[identifier] = _clean(_commandarg[startpos:endpos])
            elif identifier != "]":
                startpos = position + len(identifier)  # + 1
                try:
                    endpos = sorted_splits[index + 1][1]
                    parsed[identifier] = _clean(_commandarg[startpos:endpos])
                except IndexError:
                    parsed[identifier] = _clean(_commandarg[startpos:])
        # if parsed[identifier] and :  # i.e., not None
        #     parsed[identifier] = " ".join(parsed[identifier].split())

    parsed["anything"] = _clean(_commandarg[:end_of_anything])
    if parsed["anything"] == "":
        parsed["anything"] = None
    if parsed["if "]:
        parsed["if "] = parsed["if "].replace("__eq__", "==").replace("__neq__", "!=")

    # rename
    parsed["weight"] = parsed[" ["]
    del parsed[" ["]
    if parsed["weight"] is None:
        del parsed["]"]  # hack
    parsed["options"] = parsed[","]
    del parsed[","]
    parsed["if"] = parsed["if "]
    del parsed["if "]
    parsed["in"] = parsed[" in "]
    del parsed[" in "]
    # parsed["exp"] = parsed["="]

    # print(parsed)
    return parsed


def parse_options(options_string: str, values_as_list=False) -> dict:
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
        result[word] = None

    if values_as_list:
        return {key: value.split(" ") for key, value in result.items()}
    else:
        return result


def parse_if_condition(if_condition_string: str) -> dict:
    return {}  # todo

