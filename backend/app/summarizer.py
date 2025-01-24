import asyncio
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Global loading model and tokenizer so only loaded once and reused for each request to /summarize
model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

def summarize_text(text: str) -> str:
    if not text:
        raise ValueError("Text for summarization cannot be empty.")

    max_input_length = tokenizer.model_max_length
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    if tokens.input_ids.shape[1] > max_input_length:
        raise ValueError("Input text is too long for the model.")
    
    summary_ids = model.generate(**tokens, max_length=60, min_length=10, length_penalty=2.0)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Use asyncio to execute async for performance
async def summarize_text_async(text: str) -> str:
    return await asyncio.to_thread(summarize_text, text)