"""gr.Checkbox() component."""

from __future__ import annotations

from typing import Any, Callable

from gradio_client.documentation import document

from gradio.components.base import FormComponent
from gradio.events import Events

class Toggle(FormComponent):
    """
    Creates a toggle button that can be set to `True` or `False`. Ideal for intuitive user controls and dynamic input handling in machine learning models and data presentations.
    

    Demos: sentence_builder, titanic_survival
    """

    EVENTS = [Events.change, Events.input, Events.select]

    def __init__(
        self,
        value: bool | Callable = False,
        *,
        label: str | None = None,
        info: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 75,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
    ):
        """
        Parameters:
            value: Initial state of the toggle. If a callable is provided, it sets the initial state dynamically.
            label: Text label displayed adjacent to the toggle. Useful for providing context.
            info: Additional information or instructions displayed below the toggle.
            every: If value is a callable, this defines how often (in seconds) to refresh the toggle's state.
            show_label: Controls the visibility of the label.
            scale: Adjusts the size of the toggle relative to adjacent components.
            min_width: Minimum width of the toggle in pixels. Ensures readability and usability.
            interactive: Enables or disables user interaction with the toggle.
            visible: Controls the visibility of the toggle on the interface.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: Determines if the toggle is rendered immediately in the Blocks context.
        """
        super().__init__(
            label=label,
            info=info,
            every=every,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            value=value,
        )

    def api_info(self) -> dict[str, Any]:
        return {"type": "boolean"}

    def example_inputs(self) -> bool:
        return True

    def preprocess(self, payload: bool | None) -> bool | None:
        """
        Parameters:
            payload: the status of the toggle
        Returns:
            Passes the status of the checkbox as a `bool`.
        """
        return payload

    def postprocess(self, value: bool | None) -> bool | None:
        """
        Parameters:
            value: Expects a `bool` value that is set as the status of the toggle
        Returns:
            The same `bool` value that is set as the status of the toggle
        """
        return value
