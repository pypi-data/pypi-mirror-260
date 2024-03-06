from typing import Generator
from unittest.mock import Mock, patch

import pytest
from numerous import app, container, field, html, slider
from numerous.data_model import (
    ContainerDataModel,
    HTMLElementDataModel,
    NumberFieldDataModel,
    PlotlyElementDataModel,
    SliderElementDataModel,
    TextFieldDataModel,
    ToolDataModel,
    dump_data_model,
)


def test_dump_data_model_expected_tool_name() -> None:
    @app
    class ToolWithAName:
        param: str

    data_model = dump_data_model(ToolWithAName)

    assert data_model.name == "ToolWithAName"


def test_dump_data_model_number_field() -> None:
    default_param_value = 5

    @app
    class Tool:
        param: float = default_param_value

    data_model = dump_data_model(Tool)

    assert data_model == ToolDataModel(
        name="Tool",
        elements=[
            NumberFieldDataModel(
                name="param",
                label="param",
                default=default_param_value,
            ),
        ],
    )


def test_dump_data_model_text_field() -> None:
    default_param_value = "default string"

    @app
    class Tool:
        param: str = default_param_value

    data_model = dump_data_model(Tool)

    assert data_model == ToolDataModel(
        name="Tool",
        elements=[
            TextFieldDataModel(
                name="param",
                label="param",
                default=default_param_value,
            ),
        ],
    )


def test_dump_data_model_html_element_field() -> None:
    @app
    class HTMLTool:
        html: str = html(default="<div></div>")

    data_model = dump_data_model(HTMLTool)

    assert data_model == ToolDataModel(
        name="HTMLTool",
        elements=[
            HTMLElementDataModel(name="html", label="html", default="<div></div>"),
        ],
    )


def test_dump_data_model_slider_element_field() -> None:
    @app
    class SliderTool:
        slider: float = slider(
            default=10.0,
            label="Slider label",
            min_value=-20.0,
            max_value=30.0,
        )

    data_model = dump_data_model(SliderTool)

    assert data_model == ToolDataModel(
        name="SliderTool",
        elements=[
            SliderElementDataModel(
                name="slider",
                label="Slider label",
                default=10.0,
                slider_min_value=-20.0,
                slider_max_value=30.0,
            ),
        ],
    )


def test_dump_data_model_slider_element_field_with_defaults() -> None:
    @app
    class SliderTool:
        slider: float = slider()

    data_model = dump_data_model(SliderTool)

    assert data_model == ToolDataModel(
        name="SliderTool",
        elements=[
            SliderElementDataModel(
                name="slider",
                label="slider",
                default=0.0,
                slider_min_value=0.0,
                slider_max_value=100.0,
            ),
        ],
    )


def test_dump_data_model_field_element_string_with_label() -> None:
    @app
    class FieldTool:
        text_field: str = field(
            default="text field default",
            label="My text field label",
        )

    data_model = dump_data_model(FieldTool)

    assert data_model == ToolDataModel(
        name="FieldTool",
        elements=[
            TextFieldDataModel(
                name="text_field",
                label="My text field label",
                default="text field default",
            ),
        ],
    )


def test_dump_data_model_field_element_float_with_label() -> None:
    @app
    class FieldTool:
        number_field: float = field(
            default=42.0,
            label="My number field label",
        )

    data_model = dump_data_model(FieldTool)

    assert data_model == ToolDataModel(
        name="FieldTool",
        elements=[
            NumberFieldDataModel(
                name="number_field",
                label="My number field label",
                default=42.0,
            ),
        ],
    )


def test_dump_data_model_field_element_string_with_defaults() -> None:
    @app
    class FieldTool:
        text_field: str = field()

    data_model = dump_data_model(FieldTool)

    assert data_model == ToolDataModel(
        name="FieldTool",
        elements=[
            TextFieldDataModel(
                name="text_field",
                label="text_field",
                default="",
            ),
        ],
    )


def test_dump_data_model_field_element_float_with_defaults() -> None:
    @app
    class FieldTool:
        number_field: float = field()

    data_model = dump_data_model(FieldTool)

    assert data_model == ToolDataModel(
        name="FieldTool",
        elements=[
            NumberFieldDataModel(
                name="number_field",
                label="number_field",
                default=0.0,
            ),
        ],
    )


def test_dump_data_model_container_field() -> None:
    default_param_value = "default string"

    @container
    class Container:
        param: str = default_param_value

    @app
    class Tool:
        container: Container

    data_model = dump_data_model(Tool)

    assert data_model == ToolDataModel(
        name="Tool",
        elements=[
            ContainerDataModel(
                name="container",
                label="container",
                elements=[
                    TextFieldDataModel(
                        name="param",
                        label="param",
                        default=default_param_value,
                    ),
                ],
            ),
        ],
    )


def test_dump_data_model_plotly_field() -> None:
    import plotly.graph_objects as go  # type: ignore[import-untyped]

    @app
    class App:
        figure: go.Figure

    data_model = dump_data_model(App)

    assert data_model == ToolDataModel(
        name="App",
        elements=[
            PlotlyElementDataModel(
                name="figure",
                label="figure",
                default="",
            ),
        ],
    )


@pytest.fixture()
def patch_uuid4() -> Generator[Mock, None, None]:
    mock = Mock()
    with patch("plotly.io._html.uuid.uuid4", mock):
        yield mock


def test_dump_data_model_plotly_field_defalt_is_html(patch_uuid4: Mock) -> None:
    import plotly.graph_objects as go

    patch_uuid4.return_value = "abc123"  # mock uuid so div IDs are the same in HTML

    @app
    class App:
        figure: go.Figure = field(
            default_factory=lambda: go.Figure(
                go.Scatter(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5]),
            ),
        )

    data_model = dump_data_model(App)

    assert data_model == ToolDataModel(
        name="App",
        elements=[
            PlotlyElementDataModel(
                name="figure",
                label="figure",
                default=go.Figure(
                    go.Scatter(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5]),
                ).to_html(include_plotlyjs="cdn", full_html=False),
            ),
        ],
    )


def test_dump_data_model_plotly_field_with_label() -> None:
    import plotly.graph_objects as go

    @app
    class App:
        figure: go.Figure = field(label="My Figure")

    data_model = dump_data_model(App)

    assert data_model == ToolDataModel(
        name="App",
        elements=[
            PlotlyElementDataModel(
                name="figure",
                label="My Figure",
                default="",
            ),
        ],
    )
