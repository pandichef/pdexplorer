import pytest
import altair as alt
from vega_datasets import data
from ..webuse import webuse
from .._altair_mapper import circlechart_  # type: ignore
from .._quietly import quietly


def test_altair():
    source = data.cars()
    dict_repr = (
        alt.Chart(source)
        .mark_circle(size=60)
        .encode(
            x="Horsepower",
            y="Miles_per_Gallon",
            color="Origin",
            tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
        )
    ).to_dict()
    assert dict_repr["encoding"]["x"] == {"field": "Horsepower", "type": "quantitative"}


def test_pdexplorer_version():
    with quietly():
        webuse("cars", "vega")
    dict_repr = (
        circlechart_(size=60)
        .encode(
            x="horsepower",
            y="miles_per_gallon",
            color="origin",
            tooltip=["name", "origin", "horsepower", "miles_per_gallon"],
        )
        .to_dict()
    )
    assert dict_repr["mark"] == {"type": "circle", "size": 60}
    assert dict_repr["encoding"]["x"] == {"field": "horsepower", "type": "quantitative"}
    assert dict_repr["encoding"]["y"] == {
        "field": "miles_per_gallon",
        "type": "quantitative",
    }


def test_commandarg():
    with quietly():
        webuse("cars", "vega")
    dict_repr = circlechart_(
        "miles_per_gallon horsepower, color(origin) \
        tooltip(name origin horsepower miles_per_gallon)",
        size=60,
    ).to_dict()
    assert dict_repr["mark"] == {"type": "circle", "size": 60}
    assert dict_repr["encoding"]["x"] == {
        "field": "horsepower",
        "title": "Horsepower",
        "type": "quantitative",
    }
    assert dict_repr["encoding"]["y"] == {
        "field": "miles_per_gallon",
        "title": "Miles_per_Gallon",
        "type": "quantitative",
    }


def test_simple_scatter_plot():
    with quietly():
        webuse("cars", "vega")
    dict_repr = circlechart_("miles_per_gallon horsepower").to_dict()
    assert dict_repr["mark"] == {"type": "circle"}
    # assert dict_repr["mark"] == "circle"
    assert dict_repr["encoding"]["x"] == {
        "field": "horsepower",
        "title": "Horsepower",
        "type": "quantitative",
    }
    assert dict_repr["encoding"]["y"] == {
        "field": "miles_per_gallon",
        "title": "Miles_per_Gallon",
        "type": "quantitative",
    }
    dict_repr = circlechart_("miles_per_gallon horsepower", use_labels=False).to_dict()
    assert dict_repr["encoding"]["x"] == {
        "field": "horsepower",
        "type": "quantitative",
    }
    assert dict_repr["encoding"]["y"] == {
        "field": "miles_per_gallon",
        "type": "quantitative",
    }


def test_stacked():
    with quietly():
        webuse("cars", "vega")
    chartA = circlechart_(
        "miles_per_gallon weight_in_lbs", calculate_variable_labels=False
    )
    chartB = circlechart_("horsepower weight_in_lbs", calculate_variable_labels=False)
    dict_repr = (chartA & chartB).to_dict()
    # "mark": {"type": "circle"},
    # "mark": {"type": "circle"},
    vconcat = [
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "weight_in_lbs",
                    "title": "Weight_in_lbs",
                    "type": "quantitative",
                },
                "y": {
                    "field": "miles_per_gallon",
                    "title": "Miles_per_Gallon",
                    "type": "quantitative",
                },
            },
        },
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "weight_in_lbs",
                    "title": "Weight_in_lbs",
                    "type": "quantitative",
                },
                "y": {
                    "field": "horsepower",
                    "title": "Horsepower",
                    "type": "quantitative",
                },
            },
        },
    ]
    assert dict_repr["vconcat"] == vconcat
    dict_repr = circlechart_(
        "miles_per_gallon horsepower weight_in_lbs",
        stacked=True,
        calculate_variable_labels=False,
    ).to_dict()
    assert dict_repr["vconcat"] == vconcat


def test_stacked_calculate_variable_labels():
    with quietly():
        webuse("cars", "vega")
    chartA = circlechart_(
        "miles_per_gallon weight_in_lbs", calculate_variable_labels=True
    )
    chartB = circlechart_("horsepower weight_in_lbs", calculate_variable_labels=True)
    dict_repr = (chartA & chartB).to_dict()
    # "mark": {"type": "circle"},
    # "mark": {"type": "circle"},
    vconcat = [
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "weight_in_lbs",
                    "title": "Weight_in_lbs",
                    "type": "quantitative",
                },
                "y": {
                    "field": "miles_per_gallon",
                    "title": "Miles_per_Gallon",
                    "type": "quantitative",
                },
            },
            "transform": [
                {"calculate": "datum.name", "as": "Name"},
                {"calculate": "datum.miles_per_gallon", "as": "Miles_per_Gallon"},
                {"calculate": "datum.cylinders", "as": "Cylinders"},
                {"calculate": "datum.displacement", "as": "Displacement"},
                {"calculate": "datum.horsepower", "as": "Horsepower"},
                {"calculate": "datum.weight_in_lbs", "as": "Weight_in_lbs"},
                {"calculate": "datum.acceleration", "as": "Acceleration"},
                {"calculate": "datum.year", "as": "Year"},
                {"calculate": "datum.origin", "as": "Origin"},
            ],
        },
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "weight_in_lbs",
                    "title": "Weight_in_lbs",
                    "type": "quantitative",
                },
                "y": {
                    "field": "horsepower",
                    "title": "Horsepower",
                    "type": "quantitative",
                },
            },
            "transform": [
                {"calculate": "datum.name", "as": "Name"},
                {"calculate": "datum.miles_per_gallon", "as": "Miles_per_Gallon"},
                {"calculate": "datum.cylinders", "as": "Cylinders"},
                {"calculate": "datum.displacement", "as": "Displacement"},
                {"calculate": "datum.horsepower", "as": "Horsepower"},
                {"calculate": "datum.weight_in_lbs", "as": "Weight_in_lbs"},
                {"calculate": "datum.acceleration", "as": "Acceleration"},
                {"calculate": "datum.year", "as": "Year"},
                {"calculate": "datum.origin", "as": "Origin"},
            ],
        },
    ]
    assert dict_repr["vconcat"] == vconcat
    dict_repr = circlechart_(
        "miles_per_gallon horsepower weight_in_lbs",
        stacked=True,
        calculate_variable_labels=True,
    ).to_dict()
    assert dict_repr["vconcat"] == [
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "weight_in_lbs",
                    "title": "Weight_in_lbs",
                    "type": "quantitative",
                },
                "y": {
                    "field": "miles_per_gallon",
                    "title": "Miles_per_Gallon",
                    "type": "quantitative",
                },
            },
        },
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "weight_in_lbs",
                    "title": "Weight_in_lbs",
                    "type": "quantitative",
                },
                "y": {
                    "field": "horsepower",
                    "title": "Horsepower",
                    "type": "quantitative",
                },
            },
        },
    ]


def test_yX_format():
    with quietly():
        webuse("cars", "vega")
    dict_repr = circlechart_(
        "miles_per_gallon horsepower weight_in_lbs",
        yX=True,
        stacked=True,
        calculate_variable_labels=False,
    ).to_dict()
    assert dict_repr["vconcat"] == [
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "horsepower",
                    "title": "Horsepower",
                    "type": "quantitative",
                },
                "y": {
                    "field": "miles_per_gallon",
                    "title": "Miles_per_Gallon",
                    "type": "quantitative",
                },
            },
        },
        {
            "mark": {"type": "circle"},
            "encoding": {
                "x": {
                    "field": "weight_in_lbs",
                    "title": "Weight_in_lbs",
                    "type": "quantitative",
                },
                "y": {
                    "field": "miles_per_gallon",
                    "title": "Miles_per_Gallon",
                    "type": "quantitative",
                },
            },
        },
    ]


def test_not_stacked():
    with quietly():
        webuse("cars", "vega")
    dict_repr = circlechart_("miles_per_gallon horsepower weight_in_lbs").to_dict()
    assert dict_repr["encoding"] == {
        "color": {"field": "key", "type": "nominal"},
        "x": {
            "field": "weight_in_lbs",
            "title": "Weight_in_lbs",
            "type": "quantitative",
        },
        "y": {"field": "value", "type": "quantitative"},
    }


def test_transform_calculate_variable_labels():
    with quietly():
        webuse("cars", "vega")
    dict_repr = (
        circlechart_(calculate_variable_labels=False)
        .transform_calculate_variable_labels()
        .encode(
            y="value:Q", x=alt.X("weight_in_lbs", title="Weight_in_Lbs"), color="key:N"
        )
        .transform_fold(
            ["Miles_per_Gallon", "Horsepower"]  # The variable labels are accessible
        )
        .to_dict()
    )
    assert dict_repr["encoding"] == {
        "color": {"field": "key", "type": "nominal"},
        "x": {
            "field": "weight_in_lbs",
            "title": "Weight_in_Lbs",
            "type": "quantitative",
        },
        "y": {"field": "value", "type": "quantitative"},
    }
    assert dict_repr["transform"] == [
        {"calculate": "datum.name", "as": "Name"},
        {"calculate": "datum.miles_per_gallon", "as": "Miles_per_Gallon"},
        {"calculate": "datum.cylinders", "as": "Cylinders"},
        {"calculate": "datum.displacement", "as": "Displacement"},
        {"calculate": "datum.horsepower", "as": "Horsepower"},
        {"calculate": "datum.weight_in_lbs", "as": "Weight_in_lbs"},
        {"calculate": "datum.acceleration", "as": "Acceleration"},
        {"calculate": "datum.year", "as": "Year"},
        {"calculate": "datum.origin", "as": "Origin"},
        {"fold": ["Miles_per_Gallon", "Horsepower"]},
    ]
