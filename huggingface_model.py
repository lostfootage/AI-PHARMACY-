%%writefile huggingface_model.py
from transformers import pipeline

ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_prescription_data_hf(text):
    entities = ner_pipeline(text)

    data = {
        "Patient Name": None,
        "Medication": [],
        "Dosage": [],
        "Frequency": [],
        "Instructions": None
    }

    for entity in entities:
        if entity['entity_group'] == "PER" and not data["Patient Name"]:
            data["Patient Name"] = entity['word']
        elif entity['entity_group'] in ["MISC", "ORG"]:
            data["Medication"].append(entity['word'])

    return data
