from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from transformers import BartForConditionalGeneration, BartTokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import torch

def get_vidid(url):
    if "youtu.be" in url:
        url=url.replace("https://youtu.be/","")
        
    else:
        url=url.replace("https://www.youtube.com/watch?v=", '')
        
        
    return url


def vid_transcript(video):
    
    transcript = YouTubeTranscriptApi.get_transcript(video)
    formatter = TextFormatter()
    text_formatted = formatter.format_transcript(transcript)
    with open('plaintext.txt', 'w', encoding='utf-8') as file:
        file.write(text_formatted)
        
    
    
def ext_summarizer(path):
    
    language = "english"
    word_limit = 1500
    
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()
        
    
    summarizer = TextRankSummarizer()
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    summary = summarizer(parser.document, word_limit)

    summary_text = " ".join(str(sentence) for sentence in summary)

    return summary_text


def abs_summarizer(t, max_length,min_length):
    
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu '# failing when device is gpu
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    
    text_input_ids = tokenizer.batch_encode_plus([t], return_tensors='pt', max_length=1024)['input_ids'].to(torch_device)
    summary_ids = model.generate(text_input_ids, num_beams=10, max_length=max_length, min_length=min_length)           
    summary_txt = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
    return summary_txt
    
    
    
    





    
    

    
    
    