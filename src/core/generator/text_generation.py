from transformers import pipeline
from translation.translation import translation_en_to_pt, translation_pt_to_en

def text_generation(text: str) -> str:
   
    # The code snippet you provided is setting up a Question Answering (QA) pipeline using the Hugging
    # Face Transformers library. The `text_generation` variable is initialized with a pre-trained QA model
    # for answering questions. The `context` variable is then assigned the translated version of the
    # `text` parameter from Portuguese to English using the `translation_pt_to_en` function.
    text_generation = pipeline("text-generation", model="facebook/opt-1.3b", do_sample=True, device=0)
   
    # Gerar texto
    generation_kwargs = {
        'max_length': 400, 
        'num_return_sequences': 1,
        'temperature': 0.75,
        'top_k': 50,
        'top_p': 0.9,
        'repetition_penalty': 1.2,
        'truncation': True
    }
    
    results = text_generation(translation_pt_to_en(text), **generation_kwargs)
    return f"Resposta: {translation_en_to_pt(results[0]['generated_text'])}"
