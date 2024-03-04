
import gradio as gr
from app import demo as app
import os

_docs = {'Toggle': {'description': 'Creates a toggle button that can be set to `True` or `False`. Ideal for intuitive user controls and dynamic input handling in machine learning models and data presentations.\n\n', 'members': {'__init__': {'value': {'type': 'bool | Callable', 'default': 'False', 'description': 'Initial state of the toggle. If a callable is provided, it sets the initial state dynamically.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'Text label displayed adjacent to the toggle. Useful for providing context.'}, 'info': {'type': 'str | None', 'default': 'None', 'description': 'Additional information or instructions displayed below the toggle.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If value is a callable, this defines how often (in seconds) to refresh the toggle's state."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'Controls the visibility of the label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': None}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'Adjusts the size of the toggle relative to adjacent components.'}, 'min_width': {'type': 'int', 'default': '75', 'description': 'Minimum width of the toggle in pixels. Ensures readability and usability.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'Enables or disables user interaction with the toggle.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'Controls the visibility of the toggle on the interface.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'Determines if the toggle is rendered immediately in the Blocks context.'}}, 'postprocess': {'value': {'type': 'bool | None', 'description': 'Expects a `bool` value that is set as the status of the toggle'}}, 'preprocess': {'return': {'type': 'bool | None', 'description': 'Passes the status of the checkbox as a `bool`.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the Toggle changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the Toggle.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the Toggle. Uses event data gradio.SelectData to carry `value` referring to the label of the Toggle, and `selected` to refer to state of the Toggle. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'Toggle': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_toggle`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_toggle/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_toggle"></a>  
</div>

A custom component that toggles between on and off states. Ideal for intuitive user controls and dynamic input handling in machine learning models and data presentations.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_toggle
```

## Usage

```python

import gradio as gr
from gradio_toggle import Toggle

toggle_value = False
toggle_message = ""

def toggle_action(toggle_value):
    if toggle_value == False:
        toggle_message = "Toggle is False 👎"
    elif toggle_value == True:
        toggle_message = "Toggle is True 👍"
    else:
        toggle_message = "Error 😢"
    
    return toggle_message

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            input = Toggle(label="Input", value=toggle_value, show_label=True, info="This is a toggle button.")
        with gr.Column():
            output = gr.Label(label="Output")
    
    input.change(fn=toggle_action, inputs=input, outputs=output)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `Toggle`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["Toggle"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["Toggle"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the status of the checkbox as a `bool`.
- **As output:** Should return, expects a `bool` value that is set as the status of the toggle.

 ```python
def predict(
    value: bool | None
) -> bool | None:
    return value
```
""", elem_classes=["md-custom", "Toggle-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          Toggle: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
