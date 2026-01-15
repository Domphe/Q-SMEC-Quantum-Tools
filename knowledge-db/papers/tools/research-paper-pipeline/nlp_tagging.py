
import spacy

# Load English NLP model (must be installed in requirements)
nlp = spacy.load("en_core_web_sm")

def extract_topics(textbook: dict) -> list:
    """Use NLP to extract potential topics from title + keywords."""
    text = textbook["title"] + " " + " ".join(textbook.get("keywords", []))
    doc = nlp(text.lower())
    return list({ent.text for ent in doc.ents if ent.label_ in {"ORG", "PRODUCT", "WORK_OF_ART", "EVENT"}})
