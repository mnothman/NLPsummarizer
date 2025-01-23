import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    doc = nlp(text)
    return " ".join(token.text for token in doc if not token.is_stop)
