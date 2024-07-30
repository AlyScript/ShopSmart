from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Function to classify titles
def classify_title(title):
    # Tokenize input text
    inputs = tokenizer(title, return_tensors="pt", padding=True, truncation=True)

    # Forward pass through the model
    outputs = model(**inputs)

    # Get predicted label
    predicted_label = torch.argmax(outputs.logits).item()

    return predicted_label

# Example usage
title = "Organic Avocado"
predicted_label = classify_title(title)
print("Predicted label:", predicted_label)
