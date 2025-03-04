
from mlx_lm import load, generate

model, tokenizer = load("/Users/mvninull/.cache/lm-studio/models/mlx-community/DeepSeek-Coder-V2-Lite-Instruct-4bit-mlx")

def chat(prompt: str) -> str:

    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template is not None:
        messages = [{"role": "user", "content": prompt}]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

    response = generate(
        model, 
        tokenizer, 
        prompt=prompt, 
        verbose=True,
        max_tokens=800  
    )
    
    return response

