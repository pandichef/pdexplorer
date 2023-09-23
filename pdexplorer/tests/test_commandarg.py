from .._commandarg import parse, parse_options


def test_parse_options1():
    parsed = parse_options("by(hello world) verbose")
    assert parsed == {"by": "hello world", "verbose": True}


def test_parse_options2():
    parsed = parse_options("   by(hello   world)    verbose")
    assert parsed == {"by": "hello   world", "verbose": True}


def test_parse_options3():
    parsed = parse_options("by(species)")
    assert parsed == {"by": "species"}


def test_parse_options4():
    parsed = parse_options("by(species)", split_values=True)
    assert parsed == {"by": ["species"]}


def test_parse_commandarg1():
    parsed = parse("  brave      huxley   = exp in   new [  w=balance], world")
    assert parsed == {
        "if": None,
        "using": None,
        "=": "exp",
        "in": "new",
        "weight": "w=balance",
        "world": True,
        "options": "world",
        "anything": "brave huxley",
    }


def test_parse_commandarg2():
    parsed = parse('if species == "setosa"')
    assert parsed["if"] == 'species == "setosa"'


def test_parse_commandarg3():
    parsed = parse("(mean) sepallength sepalwidth [w=petalwidth], by(species)")
    assert parsed == {
        "if": None,
        "using": None,
        "=": None,
        "in": None,
        "weight": "w=petalwidth",
        "by": "species",
        "anything": "(mean) sepallength sepalwidth",
        "options": "by(species)",
    }


def test_parse_commandarg4_name_clash():
    parsed = parse(
        '  brave      huxley   = exp if index == 5 and serif == "sans" in   new [  w=balance], world'
    )
    # print(parsed)
    assert parsed == {
        "if": 'index == 5 and serif == "sans"',
        "using": None,
        "=": "exp",
        "in": "new",
        "weight": "w=balance",
        "world": True,
        "anything": "brave huxley",
        "options": "world",
    }


def test_parse_commandarg_exp_only():
    parsed = parse("a = 2")
    # print(parsed)
    assert parsed == {
        "if": None,
        "using": None,
        "=": "2",
        "in": None,
        "weight": None,
        "options": None,
        "anything": "a",
    }


def test_parse_commandarg_if_only():
    parsed = parse('if _merge!="both"')
    # print(parsed)
    assert parsed == {
        "if": '_merge!="both"',
        "using": None,
        "=": None,
        "in": None,
        "weight": None,
        "options": None,
        "anything": None,
    }
