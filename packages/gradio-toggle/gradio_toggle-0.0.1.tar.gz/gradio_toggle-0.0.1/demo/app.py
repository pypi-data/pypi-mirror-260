
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
