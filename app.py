import gradio as gr
from support import *
import os

os.system("pip install -r requirements.txt")

def initialize(link, max_length,min_length):
    
    path = "plaintext.txt"
    url = link

    video = get_vidid(url)
    vid_transcript(video)
    
    temp_summ = ext_summarizer(path)
    summ = abs_summarizer(temp_summ, max_length, min_length)
    
    return summ

    
        


interface = gr.Interface(
    inputs=[
        gr.inputs.Textbox(lines=2,label="YouTube Link"),
        gr.Slider(minimum=30,maximum=500,default=500,label="Max Length"),
        gr.Slider(minimum=30,maximum=50,default=50,label="Min Length")
    ],
    outputs=[
        gr.outputs.Textbox(label="Summarised YouTube Video "),
        
    ],
    fn=initialize
)
interface.launch()