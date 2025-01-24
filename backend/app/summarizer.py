import asyncio
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from aiocache import cached
from typing import Generator

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
    # Add num_beams to adjust speed/quality of summarization

    summary_ids = model.generate(**tokens, max_length=60, min_length=10, length_penalty=2.0)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Split text into chunks of max_length to summarize in parts
def split_text_into_chunks(text: str, max_length: int) -> Generator[str, None, None]:
    words = text.split()
    for i in range(0, len(words), max_length):
        yield " ".join(words[i:i + max_length])

# Process chunks of text and combine summaries
def summarize_large_text(text: str) -> str:
    chunks = split_text_into_chunks(text, max_length=tokenizer.model_max_length // 2)  # Divide model max length for safety
    summaries = [summarize_text(chunk) for chunk in chunks]
    return " ".join(summaries)

# Use asyncio to execute async for performance
# Use aiocache for 1 hr
@cached(ttl=3600)
async def summarize_text_async(text: str) -> str:
    return await asyncio.to_thread(summarize_large_text, text)
