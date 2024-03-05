
import gradio as gr
from gradio_bettertextbox import betterTextBox

example = betterTextBox().example_inputs()


def workTest(test):
    print(test)

with gr.Blocks() as demo:
    temp = betterTextBox()
    
    temp.submit(workTest, temp)
    
if __name__ == "__main__":
    demo.launch()
