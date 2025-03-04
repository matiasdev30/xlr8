from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from transformers import pipeline
import torch
from langdetect import detect

class XLR8translation():
    
    def __init__(self):
        self.MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"
        self.device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
    
    def lang_detect(self, text: str) -> str:

        lang = detect(text)
            
        print(f"Lang detect >>{lang}<<")
        return lang


    

    def translation_pt_to_en(self,text: str) -> str:

        if self.lang_detect(text) != "en": 
        # The code snippet `model =
        # MBartForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)` is loading a
        # pre-trained MBart model for conditional generation from the Hugging Face model hub. It loads
        # the model specified by the `MODEL_NAME` variable, which is set to
        # "facebook/mbart-large-50-many-to-many-mmt". The `.to(device)` part moves the model to the
        # specified device (either "mps" if available or "cpu").
            model = MBartForConditionalGeneration.from_pretrained(self.MODEL_NAME).to(self.device)
            tokenizer = MBart50TokenizerFast.from_pretrained(self.MODEL_NAME, src_lang="pt_XX", tgt_lang="en_XX")
            

        # The line `model_inputs = tokenizer(text, return_tensors="pt", max_length=1024,
        # truncation=True).to(device)` is performing the following actions:
            model_inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True).to(self.device)

        
            # The code snippet you provided with `with torch.no_grad():` is a context manager in PyTorch
            # that temporarily sets all the `requires_grad` flags to `False`. This means that any
            # operations inside this context block will not be tracked for gradient computation.
            with torch.no_grad():  # Evita o cálculo de gradientes desnecessários
                translated_tokens = model.generate(
                    **model_inputs,
                    max_length=50,
                    num_beams=5,
                    early_stopping=True,
                    repetition_penalty=3.0,
                    length_penalty=1.2
                )

            
            # The code snippet `translated_text = tokenizer.batch_decode(translated_tokens,
            # skip_special_tokens=True)[0]` is responsible for decoding the translated tokens back into
            # text after the translation process has been performed using the pre-trained model.
            translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
            return translated_text
        else:
            return text


    def translation_en_to_pt(self, text: str) -> str:
        
        if self.lang_detect(text) != "pt":
            # Usar pipeline com GPU (MPS)
            # The code snippet `pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-pt",
            # device=0 if device.type == "mps" else -1)` is creating a translation pipeline using the
            # Helsinki-NLP model for translating English text to Portuguese. Here's a breakdown of what
            # each part of this code does:
            pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-big-en-pt", device=0 if self.device.type == "mps" else -1)
            p = pipe(text)
            return p[0]["translation_text"]
        else:
            return text
        

